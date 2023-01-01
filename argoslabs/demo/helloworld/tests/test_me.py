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
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.demo.helloworld import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

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
    def test0100_success(self):
        try:
            r = main('tom', 'jerry')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success_with_opt(self):
        outfile = 'stdout.txt'
        try:
            r = main('Tom', 'Jerry', '--opt', 'Brad',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs == 'Hello world Tom,Jerry with Brad')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0120_success_with_dumpspec(self):
        outfile = 'stdout.txt'
        try:
            r = main('--dumpspec')  # ,
                     #  '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs == 'Hello world Tom,Jerry with Brad')
        except ArgsExit as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
