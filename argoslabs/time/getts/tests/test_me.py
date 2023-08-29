#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.binaryop`
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
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/04/10]
#     - add date format
#  * [2019/07/22]
#     - starting

################################################################################
import sys
import datetime
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.time.getts import _main as main
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
# noinspection PyUnusedLocal
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True
    outfile = 'stdout.txt'

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_help(self):
        try:
            _ = main('-h')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success_default(self):
        try:
            r = main('--outfile', TU.outfile)
            self.assertTrue(r == 0)
            with open(TU.outfile) as ifp:
                stdout = ifp.read()
                print("<%s>" % stdout)
                self.assertTrue(len(stdout) >= 17 and
                                stdout[8] == '-' and stdout[15] == '.')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_success_format_01(self):
        try:
            r = main('--output-format', 'M/D/YYYY HH:MM:SS.mmm',
                     '--outfile', TU.outfile)
            self.assertTrue(r == 0)
            with open(TU.outfile) as ifp:
                stdout = ifp.read()
                print("<%s>" % stdout)
                self.assertTrue(len(stdout) > 18)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0120_success_date_format(self):
        try:
            r = main('--output-format', 'YYYYMMDD',
                     '--outfile', TU.outfile)
            self.assertTrue(r == 0)
            with open(TU.outfile) as ifp:
                stdout = ifp.read()
                print("<%s>" % stdout)
                self.assertTrue(len(stdout) ==
                                datetime.datetime.now().strftime("%Y%m%d"))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0130_success_date_format(self):
        try:
            r = main('--output-format', 'DD-MM-YYYY',
                     '--outfile', TU.outfile)
            self.assertTrue(r == 0)
            with open(TU.outfile) as ifp:
                stdout = ifp.read()
                print("<%s>" % stdout)
                self.assertTrue(len(stdout) ==
                                datetime.datetime.now().strftime("%d-%m-%Y"))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0140_success_date_format(self):
        try:
            r = main('--output-format', 'DD.MM.YY',
                     '--outfile', TU.outfile)
            self.assertTrue(r == 0)
            now = datetime.datetime.now()
            with open(TU.outfile) as ifp:
                stdout = ifp.read()
                print("<%s>" % stdout)
                self.assertTrue(len(stdout) == now.strftime("%d.%m.")
                                + '%02d' % (now.year % 100))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
