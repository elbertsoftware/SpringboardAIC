from datetime import datetime as dt
import logging

date_format = '%Y-%m-%d'


def valid_year(year: str) -> bool:
	try:
		d = dt.strptime(f'{year}-12-31', date_format)
		logging.debug(f'valid_year: {d}')
	except ValueError:
		return False
	else:
		return True


