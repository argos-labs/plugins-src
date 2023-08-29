#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.office.docxextract`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/09]
#     - 그룹에 "2-Business Apps" 넣음
#  * [2020/05/08]
#     - starting

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.office.docxextract import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_failure(self):
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure_invalid_docx(self):
        try:
            r = main('infalid.docx')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0030_failure_not_docx(self):
        try:
            r = main('word-test-01.py')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_success(self):
        stdout = 'stdout.txt'
        try:
            r = main('basic.docx',
                     '--outfile',  stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
            self.assertTrue(rs.find('Jerry Chae') > 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if not os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0110_success(self):
        stdout = 'stdout.txt'
        try:
            r = main('basic.docx',
                     '--table-only',
                     '--outfile',  stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
            rr = []
            with open(stdout, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (4,))
                    rr.append(row)
            self.assertTrue(len(rr) == 4 and rr[-1][1] == 'John')

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if not os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0120_success(self):
        stdout = 'stdout.txt'
        try:
            r = main('basic.docx',
                     '--table-only', '--table-index', '1',
                     '--outfile',  stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
            rr = []
            with open(stdout, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (4,))
                    rr.append(row)
            self.assertTrue(len(rr) == 3 and
                            rr[-1][-1] == 'Desc line 1\nDesc line 2\nDesc line 3')

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if not os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0130_success(self):
        stdout = 'stdout.txt'
        try:
            r = main('basic.docx',
                     '--table-only', '--table-index', '-1',
                     '--outfile',  stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
            rr = []
            with open(stdout, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (4,))
                    rr.append(row)
            self.assertTrue(len(rr) == 7 and
                            rr[-1][-1] == 'Desc line 3')

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if not os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0140_success(self):
        stdout = 'stdout.txt'
        try:
            r = main('basic.docx',
                     '--table-only', '--table-index', '-1',
                     '--cell-merge',
                     '--outfile',  stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
            rr = []
            with open(stdout, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (4,))
                    rr.append(row)
            self.assertTrue(len(rr) == 3 and
                            rr[-1][-1] == 'Desc line 1\nDesc line 2\nDesc line 3')

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if not os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0150_success(self):
        stdout = 'stdout.txt'
        try:
            r = main('foo-01.docx',
                     '--table-only', '--table-index', '-1',
                     '--cell-merge',
                     '--outfile',  stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
                # print(rs)
            rr = []
            with open(stdout, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (5,))
                    rr.append(row)
            self.assertTrue(len(rr) == 4 and
                            rr[-1][0] == '13' and rr[-1][-1] == '이은석')

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if not os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
