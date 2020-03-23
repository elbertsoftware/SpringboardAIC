import numpy as np
import pandas as pd

from salinization import models


def test_forecast():
    result = models.forecast('BENTRAI', 2012, 2018)

    assert result is not None
    assert type(result) is dict

    forecast = result.get('forecast')
    assert forecast is not None
    assert type(forecast) is pd.Series
    
    mae = result.get('mae')
    assert mae is not None
    assert type(mae) is np.float64

    mse = result.get('mse')
    assert mse is not None
    assert type(mse) is np.float64    

    rmse = result.get('rmse')
    assert rmse is not None
    assert type(rmse) is np.float64    

