#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.system.clipboard.tests.test_me`
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
#  * [2020/08/09]
#     - 0.5초 20번 오류 등을 더 기다리도록 옵션 추가
#  * [2019/10/04]
#     - starting

################################################################################
import sys
from unittest import TestCase
from argoslabs.system.clipboard import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    CopyText = 'Hello World?\nI am fine.'

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_empty_parameter(self):
        try:
            r = main()
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_unknown_op(self):
        try:
            r = main('unknown-op')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0090_copy_invalid_text(self):
        out_f = 'out.txt'
        err_f = 'err.txt'
        try:
            r = main('Copy',
                     '--outfile', out_f,
                     '--errfile', err_f)
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_copy(self):
        out_f = 'out.txt'
        err_f = 'err.txt'
        try:
            r = main('Copy', '--copy-text', TU.CopyText,
                     '--outfile', out_f,
                     '--errfile', err_f)
            self.assertTrue(r == 0)
            with open(out_f) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == TU.CopyText)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_copy(self):
        out_f = 'out.txt'
        err_f = 'err.txt'
        try:
            r = main('Paste',
                     '--outfile', out_f,
                     '--errfile', err_f)
            self.assertTrue(r == 0)
            with open(out_f) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == TU.CopyText)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
