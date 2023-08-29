#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.string.similarstring`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Kyobong An
#
# Change Log
# --------
#
#  * [2021/11/11]
#     - starting

################################################################################
import os
import sys
# from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.string.similarstring import _main as main
from contextlib import contextmanager
from io import StringIO
from tempfile import gettempdir


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
    file = os.path.join(gettempdir(), 'argoslabs.string.similarstring.tests.test.csv')

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0001(self):
        try:
            r = main('test.csv',
                     'robert stevens jr',
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_threshold_sucess(self):
        try:
            r = main('test.csv',
                     'robert stevens jr',
                     '--threshold', '70',
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_threshold_error(self):
        try:
            r = main('test.csv',
                     'robert stevens jr',
                     '--threshold', '80',
                     )
            self.assertTrue(r == 1)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_case(self):
        try:
            r = main('test.csv',
                     'robert stevens jr',
                     # '--threshold', '80',
                     '--case'
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0300_threshold_test(self):
        try:
            r = main('main_test.csv',
                     'Techlaw',
                     '--threshold', '50',
                     # '--case',
                     '--csv-output',
                     '--header', '0'
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0400_column_test(self):
        try:
            r = main('test.csv',
                     'Techlaw',
                     '--threshold', '50',
                     '--header', '0',
                     '--csv-output',
                     '--column', 'C'
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)
