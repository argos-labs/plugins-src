#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.sns.line`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
from datetime import datetime
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.sns.line import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.sns.line
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0100_failure(self):
        try:
            _ = main('invalid')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test0200_success(self):
    #     try:
    #         r = main('..',
    #                  'Hello Line now: %s' % datetime.now())
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)

    # ==========================================================================
    def test0300_wrong_api(self):
        try:
            r = main('..',
                     'Hello Line')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
