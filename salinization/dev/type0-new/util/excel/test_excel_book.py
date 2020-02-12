import pytest

from .excel_workbook import ExcelWorkbook

from exception.excel_workbook_errors import InvalidExcelFormatOrCorrupted


def test_load_workbook_xlsx():
    workbook = ExcelWorkbook('../../dataset/bentre/So Lieu Man Ben Tre 2018.xlsx')

    sheetnames = workbook.sheet_names
    assert sheetnames is not None, 'Sheet name list can not be None'
    assert len(sheetnames) == 8, 'Invalid number of sheets'
    assert sheetnames[0] == 'Vàm Giồng', 'Invalid first sheet name'


def test_load_workbook_xls():
    workbook = ExcelWorkbook('../../dataset/bentre/solieuman Do bo sung_2018.xls')

    sheetnames = workbook.sheet_names
    assert sheetnames is not None, 'Sheet name list can not be None'
    assert len(sheetnames) == 1, 'Invalid number of sheets'
    assert sheetnames[0] == 'ben tre', 'Invalid first sheet name'


def test_load_workbook_jpg():
    with pytest.raises(InvalidExcelFormatOrCorrupted):
        ExcelWorkbook('../../dataset/VI TRIDO MAN 2019_DBSCL.jpg')


def test_load_workbook_not_exist():
    with pytest.raises(FileNotFoundError):
        ExcelWorkbook('../../dataset/file_does_not_exist')