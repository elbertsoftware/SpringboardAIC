import logging

from xlrd import open_workbook
from xlrd.sheet import Sheet

from exception.excel_workbook_errors import InvalidExcelFormatOrCorrupted


class ExcelWorkbook:
    def __init__(self, filename: str):
        self.__filename = None
        self.__workbook = None
        self.__dirty = False

        # active sheet to read data from
        self.__sheet = None

        self.filename = filename

    @property
    def filename(self) -> str:
        return self.__filename

    @filename.setter
    def filename(self, filename: str):
        try:
            self.__workbook = open_workbook(filename, on_demand=True)  # read excel but not load any sheets
            self.__dirty = False
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise InvalidExcelFormatOrCorrupted(filename, e)
        else:
            self.__filename = filename

    def __str__(self):
        return f'Excel workbook is linked to file: {self.filename}'

    @property
    def sheet_names(self) -> list:
        # try:
        #     if self.__workbook is not None:
        #         return self.__workbook.sheet_names()
        # except AttributeError:
        #     pass
        #
        if self.__workbook is not None:
            return self.__workbook.sheet_names()

        return None

    @property
    def sheet(self) -> list:
        if self.__sheet is None:
            return [None, 0, 0]

        return [self.__sheet.name, self.__sheet.nrows, self.__sheet.ncols]  # name, rows, cols

    @sheet.setter
    def sheet(self, sheet_name: str):
        if self.__workbook is not None:
            if self.__sheet is not None:
                self.__workbook.unload_sheet(self.__sheet.name)

            self.__sheet = self.__workbook.sheet_by_name(sheet_name)

    def get_sheet_row(self, index: int) -> list:
        if self.__sheet is None:
            return []

        if index < 0 or index >= self.__sheet.nrows:
            return []

        return self.__sheet.row_values(index)


if __name__ == '__main__':
    # read old format .xlsx
    workbook = ExcelWorkbook('../../../../dataset/bentre/So Lieu Man Ben Tre 2018.xlsx')
    print(workbook)

    sheetnames = workbook.sheetnames
    print(sheetnames)

    sheet = workbook.load_sheet(sheetnames[0])
    rows = sheet.nrows
    cols = sheet.ncols
    print(f'Sheet 1 has {cols} columns and {rows} rows')

    for row in range(0, rows):
        print(sheet.row_values(row))

    # read new format .xls
    workbook.filename = '../../../../dataset/bentre/solieuman Do bo sung_2018.xls'
    print(workbook)

    sheetnames = workbook.sheetnames
    print(sheetnames)

    sheet = workbook.load_sheet(sheetnames[0])
    rows = sheet.nrows
    cols = sheet.ncols
    print(f'Sheet 1 has {cols} columns and {rows} rows')

    for row in range(0, rows):
        print(sheet.row_values(row))
