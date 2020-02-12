import logging

import luigi

from util.excel.excel_workbook import ExcelWorkbook


class LoadWorkbook(luigi.Task):
	file = luigi.Parameter()
	workbook = luigi.Parameter(default=None)

	def run(self):
		logging.debug(self.file)

		self.workbook = ExcelWorkbook(self.file)
		logging.debug(f'Loaded [{self.workbook}] has the following sheets {self.workbook.sheetnames}')

	def output(self):
		return luigi.LocalTarget(self.file)


# Start Luigi Daemon:
#   luigid --background --port 8082 --logdir ./log
# Execute Task:
#   python ./task/LoadWorkbook.py LoadWorkbook --workers=2 --file='../../../dataset/bentre/So Lieu Man Ben Tre 2018.xlsx'
if __name__ == '__main__':
	luigi_run_result = luigi.build([LoadWorkbook(file='../../../dataset/bentre/So Lieu Man Ben Tre 2018.xlsx')], detailed_summary=True)
	print(luigi_run_result.summary_text)
	# luigi.run()
