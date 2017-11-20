###############################################################################
#
# Tests for XlsxWriter.
#
# Copyright (c), 2013-2017, John McNamara, jmcnamara@cpan.org
#

from ..excel_comparsion_test import ExcelComparisonTest
from ...workbook import Workbook


class TestCompareXLSXFiles(ExcelComparisonTest):
    """
    Test file created by XlsxWriter against a file created by Excel.

    """

    def setUp(self):
        self.maxDiff = None

        filename = 'format14.xlsx'

        test_dir = 'xlsxwriter/test/comparison/'
        self.got_filename = test_dir + '_test_' + filename
        self.exp_filename = test_dir + 'xlsx_files/' + filename

        self.ignore_files = []
        self.ignore_elements = {}

    def test_create_file(self):
        """Test the center across format."""

        workbook = Workbook(self.got_filename)

        worksheet = workbook.add_worksheet()
        center = workbook.add_format()

        center.set_center_across()

        worksheet.write('A1', 'foo', center)

        workbook.close()

        self.assertExcelEqual()

    def test_create_file_2(self):
        """Test the center across format."""

        workbook = Workbook(self.got_filename)

        worksheet = workbook.add_worksheet()
        center = workbook.add_format({"center_across": True})

        worksheet.write('A1', 'foo', center)

        workbook.close()

        self.assertExcelEqual()
