"""
Utility for generating features
"""
import numpy as np
import pandas as pd
from pmdarima import auto_arima
def build_lagged_features(s, lag=20, dropna=True):
    """
    Create lag features
    """
    if type(s) is pd.DataFrame:
        new_dict = {}
        for col_name in s:
            new_dict[col_name] = s[col_name]
            # create lagged Series
            for l in range(1, lag+1):
                new_dict['%s_lag%d' %(col_name, l)] = s[col_name].shift(l)
        res = pd.DataFrame(new_dict, index=s.index)

    elif type(s) is pd.Series:
        the_range = range(lag+1)
        res = pd.concat([s.shift(i) for i in the_range], axis=1)
        res.columns = ['lag_%d' %i for i in the_range]
    else:
        return None
    if dropna:
        return res.dropna()
    else:
        return res
def encode_and_bind(original_dataframe, feature_to_encode):
    """
    Create one hot encoding
    """
    dummies = pd.get_dummies(original_dataframe[[feature_to_encode]])
    res = pd.concat([original_dataframe, dummies], axis=1)
    res = res.drop(columns=[feature_to_encode], axis=1)
    return res
def datafix(column, numerator, denominator, df_, df_OrdersPlaced):
    """
    Using Auto arima to populate the remaining input columns
    """
    _temp = df_OrdersPlaced[df_OrdersPlaced.order_placed_date >= '2019-01-01']
    train = _temp[_temp.order_placed_date < '2020-01-01']
    train[column] = 100*train[numerator]/(train[numerator]+train[denominator])
    train = train[['order_placed_date', column]]
    train.set_index('order_placed_date', inplace=True)
    model = auto_arima(train, trace=True, error_action='ignore', suppress_warnings=True)
    model.fit(train)
    forecast = model.predict(n_periods=len(df_))
    df_[numerator] = np.inf
    df_[denominator] = np.inf
    for i in range(len(df_)):
        df_[numerator].iloc[i] = int((forecast[i]/100)*df_['Total Orders'].iloc[i])
        df_[denominator].iloc[i] = int(((100-forecast[i])/100)*df_['Total Orders'].iloc[i])
    return df_
