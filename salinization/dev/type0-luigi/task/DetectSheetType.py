import logging

import luigi

from task.LoadWorkbook import LoadWorkbook


class DetectSheetType(luigi.Task):
	file = luigi.Parameter()
	workbook = luigi.Parameter(default=None)
	sheet = luigi.Parameter(default=None)

	def requires(self):
		return [
			LoadWorkbook(
				file=self.file
			)
		]

	def run(self):
		self.sheet =
		rows = self.sheet.nrows
		cols = self.sheet.ncols
		logging.debug(f'Sheet [{self.sheet.name}] of [{self.workbook}] has [{cols}] columns and [{rows}] rows')


if __name__ == '__main__':
	luigi.run()
