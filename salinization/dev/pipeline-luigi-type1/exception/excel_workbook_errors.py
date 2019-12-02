class InvalidExcelFormatOrCorrupted(Exception):
	def __init__(self, filename, *args, **kwargs):
		args = (f'Filename: {filename}', ) + args  # add filename into tuple args
		Exception.__init__(self, *args, **kwargs)


class UnhandledExcelParsing(Exception):
	def __init__(self, filename, sheet, *args, **kwargs):
		args = (f'Filename: {filename}, sheet: {sheet}', ) + args  # add filename and sheet into tuple args
		Exception.__init__(self, *args, **kwargs)
