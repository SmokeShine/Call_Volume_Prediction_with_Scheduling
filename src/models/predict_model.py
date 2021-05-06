#!/usr/bin/env python -W ignore::DeprecationWarning
"""
Main Prediction Code
"""
import argparse
# import ast
import configparser
# import gc
import logging
import logging.config
# import os
import sys
# import psycopg2
# import numpy as np
from sklearn.externals import joblib
logging.config.fileConfig("../logging.ini")
LOGGER = logging.getLogger()
## Custom Imports
sys.path.append("..")
from data import make_dataset
import scheduler
DOW_COLUMNS = ['dayofweek_Friday', 'dayofweek_Monday', 'dayofweek_Saturday', \
               'dayofweek_Sunday', 'dayofweek_Thursday', 'dayofweek_Tuesday', \
               'dayofweek_Wednesday']
def parse_args():
    """
    Arguments passed from command prompt
    """
    parser = argparse.ArgumentParser(description="Training Model", \
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--lag', nargs='?', default=20, \
                        help='Lag Days')
    parser.add_argument('--scalar_loc', nargs='?', default='scaler.save', \
                        help='Location for reading the scaler pickle')
    parser.add_argument('--scalar__loc', nargs='?', default='scaler_.save', \
                        help='Location for reading the pickle for output variable')
    parser.add_argument('--pca_loc', nargs='?', default='pca.save', \
                        help='Location for reading the pca pickle')
    return parser.parse_args()
def run():
    """
    Prediction step
    """
    args = parse_args()
    LOGGER.info(args)
    config = configparser.ConfigParser()
    config.read('../../../../config.cfg')
    x_pred, weekly_shape, new_data = make_dataset.predict_dataset(config, \
                                        args.scalar_loc, args.pca_loc, args.lag)
    LOGGER.info("Restoring Model")
    grid = joblib.load('model_gridsearch_cv.pkl')
    LOGGER.info("Restoring Successful")
    raw_prediction = grid.predict(x_pred)
    scaler_ = joblib.load(args.scalar__loc)
    scaled_prediction = scaler_.inverse_transform(raw_prediction)
    LOGGER.info(scaled_prediction)
    LOGGER.info("Integer Programming Started")
    for i in range(len(scaled_prediction)):
        dow_ = new_data['order_placed_date'].dt.day_name().iloc[i]
        calls_ = []
        calc = 0
        for x, hour in enumerate(weekly_shape[weekly_shape.dayofweek == dow_].\
                                 drop(columns='dayofweek')):
            temp = weekly_shape[weekly_shape.dayofweek == dow_]\
            [hour].iloc[0]
            if (x+1)%2 == 0:

                calc = calc+(scaled_prediction[i]*temp)[0]
                calls_.append(int(calc))

                calc = 0
            else:
                calc = calc+(scaled_prediction[i]*temp)[0]
        scheduler.optimize(calls_)
    LOGGER.info("Exporting Output")
    new_data['prediction'] = scaled_prediction
    prediction_df = new_data[['order_placed_date', 'prediction']]
    prediction_df.to_csv('../../data/processed/output.csv', index=False)
if __name__ == '__main__':
    """
    Main function
    """
    LOGGER.info("Starting Prediction Process")
    run()
    LOGGER.warning("Prediction Complete")
    # Check file name in database before uncommenting the below line
    #push_file('../../data/processed/output.csv')
    LOGGER.warning("Exiting Code")
    