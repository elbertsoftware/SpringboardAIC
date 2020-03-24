import logging

import pickle

import numpy as np
import pandas as pd

from salinization.config import get_config

def load_stations():
    station_top_count = get_config()['stations']['top_count'].get()

    df = pd.read_csv('data/station/stations.csv')
    return df.iloc[:station_top_count]['code'].to_numpy()


def load_samples(file):
    df = pd.read_csv(file, parse_dates=['date'])
    df.set_index('date', inplace=True)

    # set frequent to daily if possible
    try:
        df.index.freq = 'D'
        logging.debug(f'Read file {file} and set its index to daily (D) frequent')
    except:
        logging.debug(f'Read file {file} but could not set its frequent')
        pass

    return df


def load_model(code):
    with open(f'data/model/{code}.pkl', 'rb') as pkl:
        return pickle.load(pkl)


def resample(df):
    value_field = get_config()['train']['field'].get()

    data = df[value_field].resample('MS').max()  # resampled data is a time series
    data.dropna(inplace=True)

    return data


def load_full_training(code):
    train_end = pd.to_datetime(get_config()['train']['end'].get())

    train_df = load_samples(f'data/train/{code}.csv')
    test_df = load_samples(f'data/test/{code}-{train_end.year}.csv')

    return pd.concat([train_df, test_df])


def load_evaluation(code, start_year, end_year):
    eval_df = pd.DataFrame()

    for year in range(start_year, end_year + 1):
        try:
            df = load_samples(f'data/evaluation/{code}-{year}.csv')
            if eval_df.empty:
                eval_df = df
            else:
                eval_df = pd.concat([eval_df, df])
        except:
            continue

    return eval_df