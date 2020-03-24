import sys
import logging

import click

from salinization.models import forecast


logging.basicConfig(
    format='[%(asctime)s|%(module)s.py|%(levelname)s]  %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO,
    stream=sys.stdout
)


@click.command()
@click.option('--station', prompt='Station code', help='Enter station code in one word')
@click.option('--start', prompt='Start year', help='Enter the year the forecast will begin with')
@click.option('--end', prompt='End year', help='Enter the year the forecast will end by')
def salinization_analysis(station, start, end):
    result = forecast(station, start, end)
    print(result)


if __name__ == '__main__':
    salinization_analysis()