"""
====================================
 :mod:`argoslabs.data.excel`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>, Irene Cho <irene@argos-labs.com> 0
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
#
# Authors
# ===========
#
# * Kyobong An
#
# Change Log
# --------
#
#  * [2021/03/17]
#

################################################################################
import os
import sys
import shutil
import unittest
from tempfile import gettempdir
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.data.excelupdate import _main as main


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
    def test0000_init(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        tf = os.path.join(gettempdir(), self.xlf)
        if os.path.exists(tf):
            os.remove(tf)
        shutil.copy(self.xlf, tf)
        self.__class__.xlf = tf
        self.assertTrue(os.path.exists(self.xlf))

    # ==========================================================================
    def test0100_failure_empty(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_list_sheet(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.xlf, '--list-sheet')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_list_sheet(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.xlf, '--list-sheet',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                r = ifp.read().rstrip()
                self.assertTrue(r == 'hanbin,Sheet1')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_cannot_read(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            _ = main('not-existed.xlsx', '--list-sheet',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            with open(self.err) as ifp:
                r = ifp.read().rstrip()
                self.assertTrue(r == 'Cannot read excel file "not-existed.xlsx"')

        # ==========================================================================
    def test0800_excelreplace(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'A1:E4',
                     'apple',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0810_excelreplace_blank(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'B3:E4',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0820_excelreplace_value(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     '',
                     'bab',
                     '',
                     '--sheet', 'Sheet2'
                     )
            self.assertTrue(r == 0)

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0830_excelreplace_row(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'A1:B12',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0840_excelreplace_b2value(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'A1:B4',
                     ' abab',
                     ' bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0850_excelreplace_select_value(self):
        try:
            xls = "text_excel_data1.xlsx"
            r = main(xls,
                     'A',
                     'S1',
                     'Sol1',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0860_excelreplace_change_valueisnone(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     '',
                     'bab',
                     ''
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0870_excelreplace_row(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'A:B',
                     '',
                     'bab'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0880_excelreplace_sheet(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     '',
                     '',
                     'bab',
                     '--sheet', 'Sheet2'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0890_excelreplace_range_none(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'A1:E4',
                     'apple',
                     'bab',
                     '--sheet', 'Sheet2'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0900_write(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'E',
                     '',
                     'coding',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0910_range_one_cell(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'C1',
                     'banana',
                     'onecell',
                     '--sheet', 'Sheet2'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0920_range_one_cell(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'C:D',
                     'banana',
                     'Strawberry',
                     '--sheet', 'Sheet2'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0930_range(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'B2:E19',
                     'banana',
                     'Strawberry',
                     '--sheet', 'Sheet2'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1000_CSV(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     'B1',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1010_CSV_Range_OneRow(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     'B',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1020_CSV_Range_Row(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     'B:D',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1030_CSV_Range_OneColumn(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     '2',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1040_CSV_Range_Column(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     '2:6',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1050_CSV_Range_Select(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     'B2:E14',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1060_CSV_Range_OneColumn(self):
        try:
            r = main("text_excel.csv",
                     '280',
                     '1',
                     '-r', 'A4',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1100_replace_test_num2num(self):
        try:
            xls = "test(1).xlsx"
            r = main(xls,
                     'A',
                     '300',
                     '1',
                     '-s', 'Sheet4'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1110_replace_test_num2str(self):
        try:
            xls = "replace_test.xlsx"
            r = main(xls,
                     '',
                     '50',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1120_replace_test_str2num(self):
        try:
            xls = "replace_test.xlsx"
            r = main(xls,
                     '',
                     '170',
                     '50',
                     '--data-only'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

            # ==========================================================================
    def test1130_replace_test_str2num(self):
        try:
            xls = "formulas.xlsx"
            r = main(xls,
                     '',
                     '1',
                     '2',
                     '--sheet', 'Sheet2',
                     '--data-only'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test2100_replace_test_num2num(self):
        try:
            xls = "test(1).xlsx"
            r = main(xls,
                     'B',
                     '300',
                     '1',
                     '-s', 'Sheet4'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test2110_replace_test_str2num(self):
        try:
            xls = "test(1).xlsx"
            r = main(xls,
                     'A',
                     'test01',
                     '200',
                     '-s', 'Sheet4'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test2120_replace_test_currency2num(self):
        try:
            xls = "test(1).xlsx"
            r = main(xls,
                     'G',
                     '200',
                     '444',
                     '-s', 'Sheet4'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test2130_replace_test_date(self):
        try:
            xls = "test.xlsx"
            r = main(xls,
                     '',
                     '',
                     '',
                     '-s', 'Sheet4',
                     '--data-only'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test2140_replace_test_merge(self):
        try:
            r = main("test--merge.xlsx",
                     '=D2',
                     '=D2+D3-E2-E3',
                     '-r', 'F',
                     '-s', 'Sheet3',
                     # '--format', 'YYYY-MM-DD',
                     # '--newfile', 'XLtest.xlsx'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test2150_save_csv(self):
        try:
            r = main("test--merge.xlsx",
                     '222',
                     '200',
                     # '-r', '',
                     # '-s', 'Sheet4',
                     # '--newfile', 'test(1).csv'
                     # '--data-only'
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
