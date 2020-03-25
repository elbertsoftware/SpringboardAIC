from pathlib import Path
import numpy as np

from salinization.models import forecast
from salinization.visualization import IMAGE_TEMP_LOC


def test_forecast():
    result = forecast('BENTRAI', 2012, 2018)

    assert result is not None
    assert type(result) is dict

    index = result.get('index')
    assert index is not None
    assert type(index) is list
    
    data = result.get('data')
    assert data is not None
    assert type(data) is list

    mae = result.get('mae')
    assert mae is not None
    assert type(mae) is np.float64

    mse = result.get('mse')
    assert mse is not None
    assert type(mse) is np.float64    

    rmse = result.get('rmse')
    assert rmse is not None
    assert type(rmse) is np.float64    

    metric = result.get('metric')
    assert metric is not None
    assert type(metric) is int
    
    file = result.get('chart')
    assert file is not None
    assert type(file) is str

    file_path = Path(f'{IMAGE_TEMP_LOC}/{file}')
    assert file_path.is_file()
    assert file_path.suffix == '.png'
    assert file_path.exists
    assert file_path.stat().st_size > 10


