import numpy as np
import pandas as pd

from pmdarima.arima.arima import ARIMA

from salinization.data import load_stations, load_samples, load_model, resample, load_full_training, load_evaluation


def test_load_stations():
    station_codes = load_stations()
    
    assert station_codes is not None
    assert type(station_codes) is np.ndarray
    assert station_codes.size == 5


def test_load_samples():
    df = load_samples(f'data/train/ANTHUAN.csv')

    assert df is not None
    assert type(df) is pd.DataFrame
    assert type(df.index) is pd.DatetimeIndex
    assert df.index.freq == 'D'  # train data have continuous time series


def test_load_model():
    model = load_model('SONDOC')

    assert model is not None
    assert type(model) is ARIMA


def test_resample():
    df = load_samples(f'data/train/ANTHUAN.csv')
    data = resample(df)

    assert data is not None
    assert type(data) is pd.Series
    assert type(data.index) is pd.DatetimeIndex


def test_load_full_training():
    df = load_full_training('BENTRAI')

    assert df is not None
    assert type(df) is pd.DataFrame
    assert type(df.index) is pd.DatetimeIndex
    assert df.index.freq == 'D'  # evaluation data might not have continuous time series
    assert min(df.index).year == 2002
    assert max(df.index).year == 2011


def test_load_evaluation():
    df = load_evaluation('BINHDAI', 2012, 2019)

    assert df is not None
    assert type(df) is pd.DataFrame
    assert type(df.index) is pd.DatetimeIndex
    assert df.index.freq != 'D'  # evaluation data might not have continuous time series
    assert min(df.index).year == 2012
    assert max(df.index).year == 2016