"""
====================================
 :mod:`argoslabs.search.sphinx`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module to use Selenium
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/10/07]
#     - starting

################################################################################
import os
import sys
import csv
from unittest import TestCase
from argoslabs.search.sphinx import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        ...

    # ==========================================================================
    def test0010_fail_empty(self):
        try:
            _ = main('')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        of = 'stdout.txt'
        try:
            r = main('', '36307',
                     'apple',
                     'engdict_index',
                     'id', 'word', 'part',
                     '--outfile', of)
            self.assertTrue(r == 9)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0030_failure(self):
        of = 'stdout.txt'
        try:
            r = main('192.168.35.241', '3630',
                     'apple',
                     'engdict_index',
                     'id', 'word', 'part',
                     '--outfile', of)
            self.assertTrue(r == 99)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_success(self):
        of = 'stdout.txt'
        try:
            r = main('192.168.35.241', '36307',
                     'apple',
                     'engdict_index',
                     'id', 'word', 'part',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 11)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0110_success_limit(self):
        of = 'stdout.txt'
        try:
            r = main('192.168.35.241', '36307',
                     'apple',
                     'engdict_index',
                     'id', 'word', 'part',
                     '--limit', '20',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 21)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0120_success_and(self):
        of = 'stdout.txt'
        try:
            r = main('192.168.35.241', '36307',
                     'apple pear',      # apple and pear
                     'engdict_index',
                     'id', 'word', 'part',
                     '--limit', '20',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2 and rows[-1][0] == '43452')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0130_success_or(self):
        of = 'stdout.txt'
        try:
            r = main('192.168.35.241', '36307',
                     'apple | pear',      # apple and pear
                     'engdict_index',
                     'id', 'word', 'part',
                     '--limit', '20',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 21)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
