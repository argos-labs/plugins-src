#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.mygroup.mycalc`
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
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.mygroup.mycalc import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.mygroup.mycalc
    """
    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_failure(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure_invalid_exp(self):
        try:
            r = main('')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_success(self):
        try:
            r = main('(2 + 3) ** 3')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success(self):
        stdout = 'stdout.txt'
        try:
            r = main('(2 + 3) ** 3',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                rs = ifp.read()
                self.assertTrue(rs == '125')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
