from pathlib import Path
from datetime import date, time
import logging
import csv

import luigi

from exception.excel_workbook_errors import UnhandledExcelParsing
from util.excel.excel_workbook import ExcelWorkbook
from util import time_series, str_list


class ReadDataPoint(luigi.Task):
	input_path = luigi.Parameter()
	output_path = luigi.Parameter()

	# sheet type 1 header
	type1_header_markers = [
		'KEÁT QUAÛ ÑO MAËN TRAÏM',
		'kÕt qu¶ ®o mÆn tr¹m',
		'KẾT QUẢ ĐO MẶN TRẠM',
		'SỐ LIỆU ĐO MẶN TRẠM',
	]

	# sheet type 1 footer
	type1_footer_markers = [
		'Max thaùng',
		'Max th¸ng',
		'Max tháng',
		'Min thaùng',
		'Min th¸ng',
		'Min tháng',
	]

	min_type1_footer_marker = str_list.min_len(type1_footer_markers)

	# station alias
	stations = {
		'BINHDAI': ['Binh Dai', 'BÌNH ÑAÏI', 'b×nh ®¹i', 'BÌNH ĐẠI', 'Bình Đại'],
		'LOCTHUAN': ['Loc Thuan', 'LOÄC THUAÄN', 'léc thuËn', 'LỘC THUẬN', 'Lộc Thuận'],
		'ANTHUAN': ['An Thuan', 'AN THUAÄN', 'an thuËn', 'AN THUẬN', 'An Thuận'],
		'SONDOC': ['Son Doc', 'SÔN ÑOÁC', 's¬n ®èc', 'SƠN ĐỐC', 'Sơn Đốc'],
		'BENTRAI': ['Ben Trai', 'BEÁÂN TRAÏI', 'bÕn tr¹i', 'BẾN TRẠI', 'Bến Trại'],
	}

	# month row markers
	month_markers = [
		'Tháng', 'Thaùng', 'Th¸ng',
	]

	# day row markers
	day_markers = [
		'Ngày', 'Ngaøy', 'Ngµy',
	]

	def extract_year_from_filename(self, filename: str) -> str:
		return filename[-4:]

	def extract_year_from_table_header(self, header: str) -> str:
		return header[-4:]

	def update_potential_year(self, year: str, date_stamp=None) -> date:
		if time_series.valid_year(year):
			return date.fromisoformat(f'{year}-12-31')

		return date_stamp

	def update_potential_station(self, name, station=None) -> str:
		if name is not None:
			for code in self.stations:
				if name in self.stations[code]:
					return code

		return station

	def extract_station_from_filename(self, filename: str):
		bracket_index = filename.find('(')
		if bracket_index < 7:
			return None

		dot_index = filename.find('.')
		if dot_index > bracket_index:
			return None

		return filename[dot_index + 1:bracket_index].strip()

	def extract_station_from_table_header(self, header: str):
		# TODO: Implement this logic later when having more clues
		return None

	def process_table_type1(self, output_path: str, workbook: ExcelWorkbook, row: int, date_stamp: date, station: str) -> int:
		sheet_name, rows, cols = workbook.sheet

		try:
			# locate month row
			while row < rows:
				row_cells = workbook.get_sheet_row(row)
				logging.debug(f'Row {row}: {row_cells}')
				row += 1

				if str_list.is_in(row_cells[0], self.month_markers):
					break
			else:  # the else block will be executed if the while finishes without break
				return row  # out of row to process

			# calculate number of available months
			row_cells = str_list.remove_empty(row_cells)
			months = len(row_cells) - 1

			# locate day row
			while row < rows:
				row_cells = workbook.get_sheet_row(row)
				logging.debug(f'Row {row}: {row_cells}')
				row += 1

				if str_list.is_in(row_cells[0], self.day_markers):
					break
			else:  # the else block will be executed if the while finishes without break
				return row  # out of row to process

			# calculate number of daily data points
			row_cells = str_list.remove_empty(row_cells)
			datapoints = len(row_cells) - 1

			# validate day columns to number of available months
			assert datapoints == 2 * months

			# read actual data points
			with open(Path(output_path) / Path(f'{date_stamp.year}-{station}.csv'), 'w') as csv_file:
				csv_writer = csv.writer(csv_file)
				csv_writer.writerow(['code', 'date', 'time', 'min', 'max',
				                     'h01', 'h02', 'h03', 'h04', 'h05', 'h06',
				                     'h07', 'h08', 'h09', 'h10', 'h11', 'h12',
				                     'h13', 'h14', 'h15', 'h16', 'h17', 'h18',
				                     'h19', 'h20', 'h21', 'h22', 'h23', 'h24',
				                    ])

				while row < rows:
					row_cells = workbook.get_sheet_row(row)
					logging.debug(f'Row {row}: {row_cells}')
					row += 1

					str_col0 = str(row_cells[0])
					if str_list.is_in(str_col0, self.type1_footer_markers):
						break

					day = str_list.to_int(str_col0)
					if day < 1:  # unavailable data point since there is no specific date
						continue

					for m in range(0, months):
						try:
							date_stamp = date_stamp.replace(month=m + 1, day=day)
							logging.debug(f'Month and day are set to date stamp {date_stamp}')
						except ValueError:  # handling months do not reach to 31
							continue

						max_value = str_list.to_float(str(row_cells[1 + 2 * m]))
						min_value = str_list.to_float(str(row_cells[2 + 2 * m]))
						logging.debug(f'Complete data point extracted for station {station} at {date_stamp}: max: {max_value}, min: {min_value}')

						# write to csv
						csv_writer.writerow([station, date_stamp, '', min_value, max_value] + ['' for i in range(0, 24)])
				else:  # the else block will be executed if the while finishes without break
					return row  # out of row to process or reach the end of the table
		except Exception as e:
			raise UnhandledExcelParsing(workbook.filename, sheet_name, e)

		return row

	def process_sheet(self, output_path: str, workbook: ExcelWorkbook, date_stamp: date, station: str):
		sheet_name, rows, cols = workbook.sheet
		logging.debug(f'Loaded sheet [{sheet_name}] as {rows} rows x {cols} columns')

		row = 0
		while row < rows:
			row_cells = workbook.get_sheet_row(row)
			logging.debug(f'Row {row}: {row_cells}')
			row += 1

			# skip empty rows
			row_cells = str_list.remove_empty(row_cells)
			if len(row_cells) < 1:
				continue

			# detect sheet type
			header = row_cells[0]
			if str_list.is_in(header, self.type1_header_markers):
				# type 1: # 2002 - 2011: Month,  Min - Max by Date, eg 003. Binh Dai(2002-2015.xls

				date_stamp = self.update_potential_year(self.extract_year_from_table_header(header), date_stamp)
				logging.debug(f'Potential year detected from table header {date_stamp}')

				station = self.update_potential_station(self.extract_station_from_table_header(header), station)
				logging.debug(f'Potential station detected from table header {station}')

				row = self.process_table_type1(output_path, workbook, row, date_stamp, station)

	def run(self):
		files = [file for file in Path(str(self.input_path)).iterdir() if file.is_file() and (file.name.endswith('.xlsx') or file.name.endswith('.xls'))]
		logging.debug(f'Newly received files {files}')

		for file in files:
			logging.debug(f'Processing file [{file}')

			workbook = ExcelWorkbook(str(file))
			logging.debug(f'Loaded workbook [{workbook}]')

			# filename only
			filename = file.stem.strip()

			# extract potential year from filename
			date_stamp = self.update_potential_year(self.extract_year_from_filename(filename))
			logging.debug(f'Potential year detected from filename {date_stamp}')

			# extract potential station from filename
			station = self.update_potential_station(self.extract_station_from_filename(filename))
			logging.debug(f'Potential station detected from filename {station}')

			sheet_names = workbook.sheet_names
			logging.debug(f'Workbook [{workbook}] has {len(sheet_names)} sheets: {sheet_names}')

			for sheet_name in sheet_names:
				logging.debug(f'Processing sheet [{sheet_name}]')

				workbook.sheet = sheet_name  # load and set active sheet
				sheet_name = sheet_name.strip()

				# extract potential year from sheet name
				date_stamp = self.update_potential_year(sheet_name, date_stamp)
				logging.debug(f'Potential year detected from sheet name {date_stamp}')

				# extract potential station from filename
				station = self.update_potential_station(sheet_name, station)
				logging.debug(f'Potential station detected from sheet name {station}')

				self.process_sheet(str(self.output_path), workbook, date_stamp, station)


# Start Luigi Daemon:
#   luigid --port 8082 --logdir ./log
# Execute Task:
#   python ./task/ReadDataPoint.py ReadDataPoint --workers=1 --input_path='../../../dataset/test'
if __name__ == '__main__':
	#luigi.run()
	luigi.build([ReadDataPoint(input_path='../../../dataset/test', output_path='../../../dataset/csv')])
