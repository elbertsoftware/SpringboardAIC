from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt

from salinization.data import resample, load_full_training

IMAGE_TEMP_LOC = 'temp/image'


def generate_forecast_chart(code, eval, forecast):
    full_train_df = load_full_training(code)
    full_train = resample(full_train_df)

    fig, ax = plt.subplots(figsize=(20,4))

    ax.plot(full_train.index, full_train, c='green', label='Final Training')
    ax.plot(forecast.index, forecast, c='lightcoral', label='Forecasting')
    ax.scatter(x=eval.index, y=eval, c='maroon', label='Evaluation')

    plt.title(f'Station {code}: History vs. Forecasting')
    ax.legend();

    file = f'{IMAGE_TEMP_LOC}/{datetime.utcnow().strftime("%Y%m%d%H%M%S")}-{code}.png'
    plt.savefig(file)

    return file


def clean_up_charts():
    image_temp_path = Path(IMAGE_TEMP_LOC)
    for file in image_temp_path.glob('*'):
        file.unlink()