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

        filename = 'excel2003_style03.xlsx'

        test_dir = 'xlsxwriter/test/comparison/'
        self.got_filename = test_dir + '_test_' + filename
        self.exp_filename = test_dir + 'xlsx_files/' + filename

        self.ignore_files = ['xl/printerSettings/printerSettings1.bin',
                             'xl/worksheets/_rels/sheet1.xml.rels']
        self.ignore_elements = {'[Content_Types].xml': ['<Default Extension="bin"'],
                                'xl/worksheets/sheet1.xml': ['<pageMargins', '<pageSetup']}

    def test_create_file(self):
        """Test the creation of a simple XlsxWriter file."""

        workbook = Workbook(self.got_filename, {'excel2003_style': True})

        worksheet = workbook.add_worksheet()

        worksheet.set_paper(9)

        worksheet.set_header('Page &P')
        worksheet.set_footer('&A')

        bold = workbook.add_format({'bold': 1})

        worksheet.write('A1', 'Foo')
        worksheet.write('A2', 'Bar', bold)

        workbook.close()

        self.assertExcelEqual()
