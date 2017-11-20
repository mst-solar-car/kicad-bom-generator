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

        filename = 'chart_combined09.xlsx'

        test_dir = 'xlsxwriter/test/comparison/'
        self.got_filename = test_dir + '_test_' + filename
        self.exp_filename = test_dir + 'xlsx_files/' + filename

        self.ignore_files = []
        self.ignore_elements = {'xl/charts/chart1.xml': ['<c:dispBlanksAs',
                                                         '<c:tickLblPos']}

    def test_create_file(self):
        """Test the creation of a simple XlsxWriter file."""

        workbook = Workbook(self.got_filename)

        worksheet = workbook.add_worksheet()
        chart1 = workbook.add_chart({'type': 'column'})
        chart2 = workbook.add_chart({'type': 'line'})

        chart1.axis_ids = [114984064, 114985600]
        chart2.axis2_ids = [114988928, 114987392]

        data = [
            [2, 7, 3, 6, 2],
            [20, 25, 10, 10, 20],

        ]

        worksheet.write_column('A1', data[0])
        worksheet.write_column('B1', data[1])

        chart1.add_series({'values': '=Sheet1!$A$1:$A$5'})

        chart2.add_series({'values': '=Sheet1!$B$1:$B$5', 'y2_axis': 1})

        chart1.set_y_axis({'num_font': {'bold': 1, 'baseline': -1}})
        chart2.set_y2_axis({'num_font': {'bold': 1, 'baseline': -1}})

        chart1.combine(chart2)

        worksheet.insert_chart('E9', chart1)

        workbook.close()

        self.assertExcelEqual()
