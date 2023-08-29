"""
====================================
 :mod:`argoslabs.data.pathname_manip`
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
# * Kyobong An,
#
# Change Log
# --------
#
#  * [2021/06/09]
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
from argoslabs.data.pathname_manip import _main as main


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
    def test0000_abspath(self):
        try:
            r = main("test_excel.xlsx",
                     "--path-method", "abspath")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0010_basename(self):
        try:
            r = main("test_excel.xlsx",
                     "--path-method", "basename")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0020_dirname(self):
        try:
            r = main("test_excel.xlsx",
                     "--path-method", "dirname")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0030_exists(self):
        try:
            r = main("test_excel.xlsx",
                     "--path-method", "exists")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0040_expandvars(self):
        try:
            r = main("%appdata%",
                     "--path-method", "expandvars")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

# ==========================================================================
    def test0050_getatime(self):
        try:
            r = main("test.docx",
                     "--path-method", "getatime")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0060_getmtime(self):
        try:
            r = main("test.docx",
                     "--path-method", "getmtime")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0070_getctime(self):
        try:
            r = main("test.docx",
                     "--path-method", "getctime")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0080_getsize(self):
        try:
            r = main("test_excel.xlsx",
                     "--path-method", "getsize")
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
