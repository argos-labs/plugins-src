#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.demo.helloworld`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
import csv
# from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.web.bsoup import _main as main
from tempfile import gettempdir
from alabs.common.util.vvencoding import get_file_encoding


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def setup(self):
        # os.chdir(os.path.join(os.path.dirname(__file__), 'EXAMPLE'))
        # self.assertTrue(os.path.exists('1.html'))
        pass

    # ==========================================================================
    def test0000_init(self):
        # os.chdir(os.path.join(os.path.dirname(__file__), 'EXAMPLE'))
        # self.assertTrue(os.path.exists('1.html'))
        pass

    # ==========================================================================
    def test0100_fail_html(self):
        try:
            _ = main('invalid.html')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_fail_spec(self):
        try:
            _ = main('1.html', '--spec-file', 'invalid.inv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success_exam_01(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('exam-01.html', '--spec-file', 'ext-exam-01.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            encoding = get_file_encoding(of)
            with open(of, encoding=encoding) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of, encoding=encoding) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 4)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0110_success_exam_02(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('exam.html', '--spec-file', 'ext-exam-01.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            encoding = get_file_encoding(of)
            with open(of, encoding=encoding) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of, encoding=encoding) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (2,))
                    rows.append(row)
            self.assertTrue(len(rows) == 4)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0400_success_(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('gnt-1.html', '--spec-file', 'ext_gnt_01.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            encoding = get_file_encoding(of)
            with open(of, encoding=encoding) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of, encoding=encoding) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (2,))
                    rows.append(row)
            self.assertTrue(len(rows) == 14)

            r = main('gnt-1.html', '--spec-file', 'ext_gnt_01.yaml',
                     '--limit', '5', '--outfile', of)
            self.assertTrue(r == 0)
            encoding = get_file_encoding(of)
            with open(of, encoding=encoding) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of, encoding=encoding) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (2,))
                    rows.append(row)
            self.assertTrue(len(rows) == 6)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0410_success_20_(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('gnt-2.html', '--spec-file', 'ext_gnt_01.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            encoding = get_file_encoding(of)
            with open(of, encoding=encoding) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of, encoding=encoding) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (2,))
                    rows.append(row)
            self.assertTrue(len(rows) == 6)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0420_success_20_(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('gnt-3.html', '--spec-file', 'ext_gnt_01.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            encoding = get_file_encoding(of)
            with open(of, encoding=encoding) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of, encoding=encoding) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (2,))
                    rows.append(row)
            self.assertTrue(len(rows) == 12)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
