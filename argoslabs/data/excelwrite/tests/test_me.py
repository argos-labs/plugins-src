"""
====================================
 :mod:`argoslabs.data.excelwrite`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>, Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
#
# Authors
# ===========
#
# * Kyobong An, Irene Cho
#
# Change Log
# --------
#
#  * [2021/03/17]
#

################################################################################
import os
import sys
# import csv
# import shutil
import unittest
from tempfile import gettempdir
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.data.excelwrite import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    xlf = 'sample.xlsx'
    csv = 'foo.csv'
    wxl = os.path.join(gettempdir(), 'foo.xlsx')
    wcsv = os.path.join(gettempdir(), 'foo.csv')
    out = 'stdout.txt'
    err = 'stderr.txt'

    # ==========================================================================
    @staticmethod
    def _get_safe_next_filename(fn):
        fn, ext = os.path.splitext(fn)
        for n in range(1, 1000000):
            nfn = f'{fn} ({n})' + ext
            if not os.path.exists(nfn):
                return nfn

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.abspath(os.path.dirname(__file__)))

    # ==========================================================================
    def test0000_xlsx_xlsx(self):
        try:
            xls = "text_excel_data.xlsx"
            out = "test_excel.xlsx"
            r = main(xls,
                     'name',
                     'Name',
                     out,
                     '--write-cell', 'B1',
                     '--range', 'B1',
                     '--sheet', 'Sheet1')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0010_xlsx_xlsx_renge_None(self):
        # sg = sys.gettrace()
        # print(sg)
        # if sg is None:  # Not in debug mode
        #      print('Skip testing at test/build time')
        #      return
        try:
            xls = "text_excel_data.xlsx"
            out = "test_excel.xlsx"
            r = main(xls,
                     '',
                     'blank',
                     out,
                     '--sheet', 'Sheet1')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0020_xlsx_xlsx_write_sheet(self):
        try:
            xls = "text_excel_data.xlsx"
            out = "test_excel.xlsx"
            r = main(xls,
                     '',
                     '',
                     out,
                     '--write-sheet', 'Sheet2',
                     '--sheet', 'Sheet2')
            self.assertTrue(r == 0)

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0030_xlsx_xlsx_write_sheet_start_cell(self):
        try:
            xls = "text_excel_data.xlsx"
            out = "test_excel.xlsx"
            r = main(xls,
                     '',
                     'start',
                     out,
                     '--write-sheet', 'Sheet2',
                     '--write-cell', 'B2',
                     '--sheet', 'Sheet2',)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0040_xlsx_xlsx_write_sheet_start_cell_range_onerow(self):
        try:
            xls = "text_excel_data.xlsx"
            out = "test_excel.xlsx"
            r = main(xls,
                     '',
                     'start',
                     out,
                     '--write-sheet', 'Sheet2',
                     '--write-cell', 'B2',
                     '--range', 'D',
                     '--sheet', 'Sheet2',)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0050_xlsx_xlsx_write_sheet_start_cell_range_onerow(self):
        try:
            xls = "text_excel_data.xlsx"
            out = "test_excel.xlsx"
            r = main(xls,
                     '',
                     'start',
                     out,
                     '--write-sheet', 'Sheet2',
                     '--write-cell', 'B2',
                     '--range', '4',
                     '--sheet', 'Sheet2',)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0050_xlsx_xlsx_write_sheet_start_cell_range_onecol(self):
        try:
            xls = "temp.xlsx"
            out = "temp.xlsx"
            r = main(xls,
                     out,
                     '--write-sheet', 'Sheet2new',
                     # '--write-cell', 'A1',
                     # '--sheet', 'Sheet2',
                     '--data-only')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_xlsx_csv_range_None(self):
        try:
            xls = "text_excel_data.xlsx"
            out = "test_csv.csv"
            r = main(xls,
                     '',
                     '',
                     out,
                     '--range', 'C',)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_xlsx_csv_range_onerow(self):
        try:
            xls = "text_excel_data.xlsx"
            out = "test_csv.csv"
            r = main(xls,
                     '',
                     '',
                     out,
                     '--range', 'A',)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_xlsx_csv_range_row(self):
        try:
            xls = "text_excel_data.xlsx"
            out = "test_csv.csv"
            r = main(xls,
                     '',
                     '',
                     out,
                     '--range', 'B:C',)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_xlsx_csv_range_onecol_read_sheet(self):
        try:
            xls = "text_excel_data.xlsx"
            out = "test_csv.csv"
            r = main(xls,
                     '',
                     'blank',
                     out,
                     '--range', '15',
                     '--sheet', 'Sheet2',)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_csv_csv_range_None(self):
        try:
            xls = "text_excel.csv"
            out = "test_csv.csv"
            r = main(xls,
                     out,)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_csv_csv_range_col(self):
        try:
            xls = "text_excel.csv"
            out = "test_csv.csv"
            r = main(xls,
                     out,
                     '--range', '3:14',)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0300_csv_xlsx_write_sheet_start_cell_range_none(self):
        try:
            r = main("test111.csv",
                     '--filename', 'test(1).xlsx',
                     '--sheet', 'Sheet4',
                     '-r', 'A',
                     # '--write-sheet', 'Sheet4',
                     '--write-cell', 'A1',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0310_csv_xlsx_datatype_num(self):
        try:
            r = main("excel_value_test.xlsx",
                     '--excel-value', '100',
                     # '--sheet', 'Sheet1',
                     '-r', 'A1:A5',
                     # '--write-sheet', 'test',
                     '--write-cell', 'D2',
                     # '--data-only'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0400_xlsx2csv(self):
        try:
            r = main("xlsx2csv.csv",
                     '--filename', 'temp.xlsx',
                     '--sheet', 'Sheet1',
                     '-r', 'C',
                     # '--write-sheet', 'test',
                     '--write-cell', 'D1',
                     # '--data-only',
                     # '--encoding', 'UTF-8'
                     )

            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0410_csv2csv(self):
        try:
            r = main("csv2csv.csv",
                     '--filename', 'xlsx2csv.csv',
                     # '--sheet', 'Sheet1',
                     '-r', 'A',
                     # '--write-sheet', 'test',
                     '--write-cell', 'B1',
                     # '--data-only',
                     # '--encoding', 'UTF-8'
                     )

            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0420_csv2xlsx(self):
        try:
            r = main("csv2xlsx.xlsx",
                     '--filename', 'xlsx2csv.csv',
                     # '--sheet', 'Sheet1',
                     '-r', 'A',
                     '--write-sheet', 'test',
                     '--write-cell', 'B1',
                     # '--data-only',
                     # '--encoding', 'UTF-8'
                     )

            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0430_test_error(self):
        try:
            r = main("test(1)1.xlsx",
                     '--filename', 'test(1)1.xlsx',
                     '--sheet', 'test1',
                     '-r', '1',
                     '--write-sheet', 'test1',
                     '--write-cell', 'A1',
                     '--data-only',
                     # '--encoding', 'UTF-8'
                     )

            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0430_test_out_put_csv_error(self):
        try:
            r = main("tedsast.csv",
                     '--excel-value', 'test',
                     # '--sheet', 'test1',
                     # '-r', '',
                     # '--write-sheet', 'tedsast',
                     '--write-cell', 'A1',
                     # '--data-only',
                     # '--encoding', 'UTF-8'
                     )

            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        if os.path.exists(self.out):
            os.remove(self.out)
        if os.path.exists(self.err):
            os.remove(self.err)
        if os.path.exists(self.wxl):
            os.remove(self.wxl)
        if os.path.exists(self.wcsv):
            os.remove(self.wcsv)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
