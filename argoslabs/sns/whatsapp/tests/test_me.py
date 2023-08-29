#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.myuti.text`
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
from argoslabs.sns.whatsapp import _main as main
    # _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.myuti.text
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_failure(self):
        try:
            _ = main('')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    # def test0020_failure_without_frend(self):
    #     try:
    #         _ = main('msg')
    #         self.assertTrue(False)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)
    #
    # # ==========================================================================
    # def test0030_failure_invalid_driver(self):
    #     try:
    #         r = main('msg', 'friend1',
    #                  # '--driver', 'invalid'
    #                  '-d', 'invalid'
    #                  )
    #         self.assertTrue(r != 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0100_success(self):
    #     outfile = 'stdout.txt'
    #     try:
    #         r = main('msg', 'friend1', 'friend2',
    #                  '--driver', 'Chrome',
    #                  '--driver-path', r'C:\....\chrome.exe',
    #                  '--file-path', r'C:\...',
    #                  '--file-path', r'D:\...',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #             self.assertTrue(rs == '20.897959183673468')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
