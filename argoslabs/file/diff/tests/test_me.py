#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.chardet`
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
from unittest import TestCase
from argoslabs.file.chardet import _main as main


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
    def test0050_invalid_operation(self):
        try:
            _ = main('invalid')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_chardet(self):
        stdout = 'stdout.txt'
        try:
            r = main('jpn-01.csv', '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            rr = []
            with open(stdout, 'r') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(len(rr) == 2 and rr[1][1] == 'utf-8')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0110_chardet(self):
        stdout = 'stdout.txt'
        try:
            r = main('jpn-01.out.csv', '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            rr = []
            with open(stdout, 'r') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(len(rr) == 2 and rr[1][1] == 'SHIFT_JIS')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0120_chardet(self):
        stdout = 'stdout.txt'
        try:
            r = main('jpn-01.out2.csv', '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            rr = []
            with open(stdout, 'r') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(len(rr) == 2 and rr[1][1] == 'EUC-JP')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
