#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.pdf.miner.tests.test_me`
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
#  * [2020/06/03]
#     - starting
#

################################################################################
import os
import sys
import csv
# from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.pdf.miner import _main as main
from contextlib import contextmanager
from io import StringIO


################################################################################
@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def tearDown(self) -> None:
        ...

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_invalid_param(self):
        try:
            _ = main('unknown')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0090_totallength_failure(self):
        try:
            with captured_output() as (out, err):
                r = main('광진invoice/all5.pdf', '')
            self.assertTrue(r != 0)
            stderr = err.getvalue().strip()
            if stderr:
                print(stderr)
            self.assertTrue(stderr == 'invalid "Search Text"')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_success(self):
        try:
            with captured_output() as (out, err):
                r = main('광진invoice/all5.pdf', '1.000')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            # print(stdout)
            sout = StringIO(stdout)
            rows = list()
            cr = csv.reader(sout)
            for row in cr:
                self.assertTrue(len(row) in (8,))
                rows.append(row)
            self.assertTrue(len(rows) == 6 and rows[-1][-2] == '448.95')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success(self):
        try:
            with captured_output() as (out, err):
                r = main('광진invoice/all5.pdf', '1.0000')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            # print(stdout)
            sout = StringIO(stdout)
            rows = list()
            cr = csv.reader(sout)
            for row in cr:
                self.assertTrue(len(row) in (8,))
                rows.append(row)
            self.assertTrue(len(rows) == 8 and rows[1][-2] == '328.95')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_success_desc(self):
        try:
            with captured_output() as (out, err):
                r = main('광진invoice/all5.pdf', '1.0000',
                         '--desc')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            # print(stdout)
            sout = StringIO(stdout)
            rows = list()
            cr = csv.reader(sout)
            for row in cr:
                self.assertTrue(len(row) in (8,))
                rows.append(row)
            self.assertTrue(len(rows) == 8 and rows[-1][-2] == '328.95')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_success_startswith(self):
        try:
            with captured_output() as (out, err):
                r = main('광진invoice/all5.pdf', '1.0',
                         '--startswith')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            # print(stdout)
            sout = StringIO(stdout)
            rows = list()
            cr = csv.reader(sout)
            for row in cr:
                self.assertTrue(len(row) in (8,))
                rows.append(row)
            self.assertTrue(len(rows) == 13 and rows[1][-2] == '328.95')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_success_endswith(self):
        try:
            with captured_output() as (out, err):
                r = main('광진invoice/all5.pdf', '000',
                         '--endswith')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            # print(stdout)
            sout = StringIO(stdout)
            rows = list()
            cr = csv.reader(sout)
            for row in cr:
                self.assertTrue(len(row) in (8,))
                rows.append(row)
            self.assertTrue(len(rows) == 37 and
                            rows[1][0] == '2' and rows[1][-2] == '301.978')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_success_endswith_page(self):
        try:
            with captured_output() as (out, err):
                r = main('광진invoice/all5.pdf', '000',
                         '--endswith',
                         '--page', '2')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            # print(stdout)
            sout = StringIO(stdout)
            rows = list()
            cr = csv.reader(sout)
            for row in cr:
                self.assertTrue(len(row) in (8,))
                rows.append(row)
            self.assertTrue(len(rows) == 10 and
                            rows[1][0] == '2' and rows[1][-2] == '301.978')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_success_contains(self):
        try:
            with captured_output() as (out, err):
                r = main('광진invoice/all5.pdf', '.00',
                         '--contains')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            # print(stdout)
            sout = StringIO(stdout)
            rows = list()
            cr = csv.reader(sout)
            for row in cr:
                self.assertTrue(len(row) in (8,))
                rows.append(row)
            self.assertTrue(len(rows) == 36 and
                            rows[1][0] == '3' and rows[1][-2] == '271.88')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_success_contains_page(self):
        try:
            with captured_output() as (out, err):
                r = main('광진invoice/all5.pdf', '.00',
                         '--contains',
                         '--page', '3')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            # print(stdout)
            sout = StringIO(stdout)
            rows = list()
            cr = csv.reader(sout)
            for row in cr:
                self.assertTrue(len(row) in (8,))
                rows.append(row)
            self.assertTrue(len(rows) == 8 and
                            rows[1][0] == '3' and rows[1][-1] == '30.0000 CBM')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0180_success_startswith(self):
        try:
            with captured_output() as (out, err):
                r = main('광진invoice/all5.pdf', 'HASL',
                         '--startswith')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            # print(stdout)
            sout = StringIO(stdout)
            rows = list()
            cr = csv.reader(sout)
            for row in cr:
                self.assertTrue(len(row) in (8,))
                rows.append(row)
            self.assertTrue(len(rows) == 3 and
                            rows[1][0] == '2' and rows[1][-2] == '283.738')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        ...
