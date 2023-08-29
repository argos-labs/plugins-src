#!/usr/bin/env python
# coding=utf8


################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.demo.argtest import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0100_success(self):
        try:
            _ = main('4000', 'y', '50', '0.5', '1.2.3.4', 'tom', 'jerry', 'foo', 'foo')
            self.assertTrue(True)
        except ArgsError as e:
            # For Argument "ipaddr", "re_match" validatation error: user input
            # is "1.2.3.d" but rule is "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_failure(self):
        try:
            _ = main('4000', 'y', '50', '0.5', '1.2.3.d', 'tom', 'jerry', 'foo', 'foo')
            self.assertTrue(False)
        except ArgsError as e:
            # For Argument "ipaddr", "re_match" validatation error: user input
            # is "1.2.3.d" but rule is "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test9999_quit(self):
        if os.path.exists('_jb_unittest_runner.py.log'):
            os.unlink('_jb_unittest_runner.py.log')
        self.assertTrue(True)
