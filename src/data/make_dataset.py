# -*- coding: utf-8 -*-

"""
Common Utilities for generating dataset
"""
import logging
import sys
import numpy as np
import pandas as pd
import psycopg2
from sklearn import decomposition
from sklearn import preprocessing
from sklearn.externals import joblib
from pmdarima import auto_arima
from sklearn.model_selection import TimeSeriesSplit
sys.path.append("..")
from features import sql_queries
from features import build_features
LOGGER = logging.getLogger(__name__)
DOW_COLUMNS = ['dayofweek_Friday', 'dayofweek_Monday', 'dayofweek_Saturday', \
               'dayofweek_Sunday', 'dayofweek_Thursday', 'dayofweek_Tuesday', \
               'dayofweek_Wednesday']
common_columns = ['order_placed_date', 'new_user', 'old_user', \
'courier_order', 'non_courier_order', \
'non_delayed', 'delayed', 'jit', 'non_jit']
def read_training_data(config):
    """
    Query from Database
    """
    LOGGER.info("Refreshing Base Tables")
    db_connection = psycopg2.connect("host={} dbname={} user={} password={} port={}".\
                                     format(*config['CLUSTER'].values()))
    query = sql_queries.Queries(lag=20, days_to_predict=30).sql_calls_received
    df_calls_received = pd.read_sql_query(query, db_connection, \
                                          parse_dates=['call_date'])
    query = sql_queries.Queries(lag=20, days_to_predict=30).sql_orders_placed
    df_orders_placed = pd.read_sql_query(query, db_connection,\
                                         parse_dates=['order_placed_date'])
    query = sql_queries.Queries(lag=20, days_to_predict=30).sql_weekly_shape
    df_weekly_shape = pd.read_sql_query(query, db_connection)
    LOGGER.info("Data Read")
    return df_calls_received, df_orders_placed, df_weekly_shape
def make_dataset(config, lag, scalar_loc, scalar__loc, pca_loc):
    """
    Make Training Dataset
    """
    df_calls_received, df_orders_placed, df_weekly_shape = read_training_data(config)
    df_orders_placed_lagged = build_features.build_lagged_features(\
                df_orders_placed[df_orders_placed.drop(columns=['order_placed_date', 'dayofweek']).\
                columns], \
                lag=lag, dropna=False)
    df_orders_placed_lagged.drop(columns=\
                                 ['non_delayed', 'delayed', \
                                  'courier_order', 'non_courier_order', \
                                  'non_jit', 'jit'],\
                                 inplace=True)
    train_grid = pd.concat([df_orders_placed[['order_placed_date', 'dayofweek']], \
                            df_orders_placed_lagged], axis=1)
    features_to_encode = ['dayofweek']
    for feature in features_to_encode:
        train_grid = build_features.encode_and_bind(train_grid, feature)
    train_grid = train_grid[lag:]
    df_ = pd.merge(train_grid, df_calls_received,\
                left_on='order_placed_date', right_on='call_date', how='inner').\
                sort_values('order_placed_date')
    df_ = df_.drop(columns=['order_placed_date', 'call_date'])
    scaler = preprocessing.RobustScaler()
    standardized_features = scaler.fit_transform(\
                                                 train_grid.drop(columns=['order_placed_date']\
                                                                 +DOW_COLUMNS))
    joblib.dump(scaler, scalar_loc)
    pca = decomposition.PCA(20)
    pca_features = pca.fit_transform(standardized_features)
    joblib.dump(pca, pca_loc)
    scaler_ = preprocessing.RobustScaler()
    scaled_y_train_df = pd.DataFrame(scaler_.fit_transform(df_[['calls_received']]))
    joblib.dump(scaler_, scalar__loc)
    scaled_x_train_df = pd.concat([\
                                 pd.DataFrame(\
                                 pca.transform(scaler.transform(\
df_.drop(columns=['calls_received']+DOW_COLUMNS)))),\
                                 df_[DOW_COLUMNS]], axis=1)
    time_split = TimeSeriesSplit(n_splits=8)
    return scaled_x_train_df, scaled_y_train_df, time_split

def hack(df_orders_placed_historical):
    rd = pd.read_excel('../../notebooks/Daily Order Prediction - Sample Data.xlsx')
    rd = rd[(rd['Date'] >= '2020-01-01')\
&(rd['Date'] <= '2020-02-20')]
    rd = build_features.datafix('%delayed', 'delayed', 'non_delayed', \
rd, df_orders_placed_historical)
    rd = build_features.datafix('%courier_order', 'courier_order', 'non_courier_order', \
rd, df_orders_placed_historical)
    rd = build_features.datafix('%jit', 'jit', 'non_jit', rd, df_orders_placed_historical)
    rd.rename(columns={'Date':'order_placed_date', \
'Old User Orders':'old_user', \
'New User Orders':'new_user'}, \
inplace=True)
    rd['dayofweek'] = rd['order_placed_date'].dt.day_name()
    features_to_encode = ['dayofweek']
    for feature in features_to_encode:
        rd = build_features.encode_and_bind(rd, feature)
    return rd
def read_prediction_data(config):
    LOGGER.info("Refreshing Base Tables")
    db_connection = psycopg2.connect("host={} dbname={} user={} password={} port={}".\
format(*config['CLUSTER'].values()))
    query = sql_queries.Queries(lag=20, days_to_predict=30).sql_prediction_input
    df_orders_placed_historical = pd.read_sql_query(query, db_connection, \
 parse_dates=['order_placed_date'])
#     query=Queries(lag = 20,days_to_predict = 30).sql_ForecastedOrders
#     df_orders_placed_fo = pd.read_sql_query(query, db_connection,
#                                         parse_dates=['order_placed_date'])
    df_orders_placed_fo = hack(df_orders_placed_historical)
#     features_to_encode = ['dayofweek']
#     for feature in features_to_encode:
#         rd = build_features.encode_and_bind(rd, feature)
#     import pdb
#     pdb.set_trace()
    df_orders_placed = df_orders_placed_historical\
    [df_orders_placed_historical.order_placed_date\
     < df_orders_placed_fo.order_placed_date.min()]\
    [common_columns].append(df_orders_placed_fo[common_columns])
    missing = pd.date_range(start=df_orders_placed.order_placed_date.min(),\
                          end=df_orders_placed.order_placed_date.max()).\
                          difference(df_orders_placed.order_placed_date)
    assert len(missing) == 0, "Missing Dates Encountered"
    query = sql_queries.Queries(lag=20, days_to_predict=30).sql_weekly_shape
    df_weekly_shape = pd.read_sql_query(query, db_connection)
    LOGGER.info("Data Read")
    return df_orders_placed, df_weekly_shape, df_orders_placed_fo
def predict_dataset(config, scalar_loc, \
pca_loc, lag):
    """
    Create Prediction Dataset
    """
    df_orders_placed, df_weekly_shape, df_orders_placed_fo = read_prediction_data(config)
    df_orders_placed_lagged = build_features.build_lagged_features(\
df_orders_placed.drop(columns='order_placed_date'), \
                                                            lag=lag, dropna=False)
    df_orders_placed_lagged.drop(columns=\
                                ['non_delayed', 'delayed', \
'courier_order', 'non_courier_order', 'non_jit', 'jit'],\
                                inplace=True)
#     import pdb
#     pdb.set_trace()
    predict_grid = df_orders_placed_lagged[-51::]
#     pdb.set_trace()
    scaler = joblib.load(scalar_loc)
    pca = joblib.load(pca_loc)
#     pdb.set_trace()
    scaled_predict_df = pca.transform(scaler.transform(predict_grid))
    x_pred = np.hstack([scaled_predict_df, df_orders_placed_fo[DOW_COLUMNS].values])
    db_connection = psycopg2.connect("host={} dbname={} user={} password={} port={}".\
                                     format(*config['CLUSTER'].values()))
    query = sql_queries.Queries(lag=20, days_to_predict=30).sql_weekly_shape
    df_weekly_data = pd.read_sql_query(query, db_connection)
    df_weekly_data['slot'] = df_weekly_data['slot'].astype(int)
    table = pd.pivot_table(df_weekly_data, index='dayofweek', \
columns='slot', \
values='totalcalls', \
aggfunc=np.sum, \
margins=True, \
fill_value=0)
    weekly_shape = table.div(table.iloc[:, -1], axis=0)
    weekly_shape = weekly_shape.drop(columns=['All']).reset_index()
    weekly_shape = weekly_shape[weekly_shape.dayofweek != 'All']
    return x_pred, weekly_shape, df_orders_placed_fo
