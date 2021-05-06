#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This is main calling function for running th training process. Can be run with python train_model.py
Use -h handle to get help on additional arguments
"""

import argparse
import configparser
import sys
import logging
import logging.config
from sklearn.externals import joblib
from sklearn import linear_model
from sklearn import model_selection

sys.path.append('..')
from data import make_dataset

logging.config.fileConfig('../logging.ini')
LOGGER = logging.getLogger()

ALPHA = [
    0.001,
    0.01,
    0.1,
    1,
    10,
    100,
    1000,
    ]


def parse_args():
    '''
    Parse Arguments from terminal
    '''
    parser = argparse.ArgumentParser(description='Training Model', \
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--lag', nargs='?', default=20, help='Lag Days')
    parser.add_argument('--scalar_loc', nargs='?', default='scaler.save',
                        help='Location for pickling the scaler; Necessary for use in predict.py')
    parser.add_argument('--scalar__loc', nargs='?',
                        default='scaler_.save',
                        help='Location for pickling the scaler for output variable')
    parser.add_argument('--pca_loc', nargs='?', default='pca.save',
                        help='Location for pickling the pca; Necessary for use in predict.py')
    return parser.parse_args()

def run():
    '''
    Training Process
    '''
    args = parse_args()
    LOGGER.info(args)
    config = configparser.ConfigParser()
    config.read('../../../../config.cfg')
    (scaled_x_train_df, scaled_y_train_df, time_split) = \
        make_dataset.make_dataset(config, args.lag, args.scalar_loc,
                                  args.scalar__loc, args.pca_loc)
    clf = linear_model.Ridge()
    cv_scores = model_selection.cross_val_score(
        clf,
        scaled_x_train_df,
        scaled_y_train_df,
        cv=time_split,
        scoring='r2',
        n_jobs=-1,
        )
    LOGGER.warning(cv_scores)
    LOGGER.warning(cv_scores.mean())
    param_grid = dict(alpha=ALPHA)
    grid = model_selection.GridSearchCV(
        estimator=clf,
        param_grid=param_grid,
        scoring='r2',
        n_jobs=-1,
        cv=time_split,
        verbose=2,
        )
    grid_result = grid.fit(scaled_x_train_df, scaled_y_train_df)
    LOGGER.info('Training Complete')
    joblib.dump(grid, 'model_gridsearch_cv.pkl')
    grid = joblib.load('model_gridsearch_cv.pkl')
    LOGGER.info('Best Score: ')
    LOGGER.info(grid_result.best_score_)
    LOGGER.info('Best Params: ')
    LOGGER.info(grid_result.best_params_)
    LOGGER.info('best_estimator_:')
    LOGGER.info(grid.best_estimator_.coef_)
    LOGGER.info('intercept_:')
    LOGGER.info(grid.best_estimator_.intercept_)

if __name__ == '__main__':
    LOGGER.info('Starting Training Process')
    run()
    logging.warning('Training Complete')
