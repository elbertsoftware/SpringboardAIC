import logging
import confuse

import numpy as np
import pandas as pd

from sklearn.metrics import mean_absolute_error, mean_squared_error

from salinization.data import load_stations, load_model, load_evaluation


models = {}


def forecast(code: str, start_year: int, end_year: int):
    config = confuse.Configuration('salinization', __name__)
    
    value_field = config['train']['field'].get()
    train_end = pd.to_datetime(config['train']['end'].get())
    
    if start_year <= train_end.year:
        raise ValueError(f'Start year must be greater than or equal to {train_end.year + 1}')

    if start_year > end_year:
        raise ValueError(f'End year must be greater than or equal to start year {start_year}')

    # load model if it has not been loaded yet
    if models.get(code) is None:
        models[code] = load_model(code)

    model = models[code]

    # load and prepare evaluation data into monthly samples
    eval_df = load_evaluation(code, start_year, end_year)  # eval_df is a data frame

    eval_data = eval_df[value_field].resample('MS').max()  # eval_data is a time series
    eval_data.dropna(inplace=True)

    eval_std = eval_data.std()
    
    period_in_months = 12 - train_end.month
    period_in_months += (end_year - start_year + 1) * 12  # number of months in those evaluation years
    
    # forecast
    forecast = model.predict(n_periods=period_in_months)
    forecast = pd.Series(forecast, index=pd.date_range(start=f'{start_year - 1}-{train_end.month + 1}-01', end=f'{end_year}-12-31', freq='MS'))

    # metrics
    eval_forecast = forecast[eval_data.index]  # trim down forecast to exact match of evaluation set

    mae = mean_absolute_error(eval_data, eval_forecast)
    mse = mean_squared_error(eval_data, eval_forecast)
    rmse = np.sqrt(mse)

    return {
        'forecast': forecast,
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'chart': None
    }
