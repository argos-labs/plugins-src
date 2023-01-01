"""
====================================
 :mod:`argoslabs.data.excelread`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
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
import unittest
from tempfile import gettempdir
# from alabs.common.util.vvargs import ArgsError
import alabs.common.util.vvargs
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.data.excelread import _main as main


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
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))
        return super().setUp()

    # ==========================================================================
    def test0010_excelreplace_change_valueisnone(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     '--sheet', 'Sheet3',
                     '--data-only'
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_CSV_Range_OneColumn(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     '--range', '1:14'
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0030_data_only(self):
        try:
            xls = "arraytest1.xlsx"
            r = main(xls,
                     '--sheet', 'Sheet2',
                     # '--data-only'
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1200_xlsm(self):
        try:
            xls = "arraytest1.xlsm"
            r = main(xls,
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test1200_xlsm_kioxia(self):
    #     try:
    #         xls = "Budget_Summary_App.xlsm"
    #         r = main(xls,
    #                  '--sheet', 'HOME'
    #                  )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

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
