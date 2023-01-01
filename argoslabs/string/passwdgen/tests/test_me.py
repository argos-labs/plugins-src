#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.string.passwdgen`
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
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/05/30]
#     - starting

################################################################################
import os
import sys
# from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.string.passwdgen import _main as main
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
    def setUp(self) -> None:
        ...

    # ==========================================================================
    def tearDown(self) -> None:
        ...

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_invalid_length(self):
        stderr = None
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
                r = main('20',
                         '--minsp', '7', '--minlower', '7',
                         '--minupper', '5', '--mindigit', '4',
                         )
            self.assertTrue(r != 0)
            stderr = err.getvalue().strip()
            if stderr:
                print(stderr)
            self.assertTrue(stderr == 'Sum of all minimum number of characters cannot be exceed the password length')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_success(self):
        try:
            with captured_output() as (out, err):
                r = main('10')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(len(stdout) == 10)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success(self):
        try:
            with captured_output() as (out, err):
                r = main('20')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(len(stdout) == 20)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_spchars(self):
        try:
            with captured_output() as (out, err):
                r = main('20', '--spchars', '!@#$:;')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(len(stdout) == 20)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_spchars_failure(self):
        try:
            with captured_output() as (out, err):
                r = main('20', '--spchars', '!@#$:;', '--minsp', '11')
            self.assertTrue(r != 0)
            stderr = err.getvalue().strip()
            if stderr:
                print(stderr)
            self.assertTrue(stderr.startswith('Min # of any password element cannot exceed half of the total length of the password'))
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_spchars_success(self):
        try:
            with captured_output() as (out, err):
                r = main('20', '--spchars', '!@#$:;', '--minsp', '6')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(len(stdout) == 20)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_lower_failure(self):
        try:
            with captured_output() as (out, err):
                r = main('20', '--minlower', '11')
            self.assertTrue(r != 0)
            stderr = err.getvalue().strip()
            if stderr:
                print(stderr)
            self.assertTrue(stderr.startswith('Min # of any password element cannot exceed half of the total length of the password'))
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_lower_success(self):
        try:
            with captured_output() as (out, err):
                r = main('20', '--minlower', '10')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(len(stdout) == 20)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_upper_failure(self):
        try:
            with captured_output() as (out, err):
                r = main('20', '--minupper', '11')
            self.assertTrue(r != 0)
            stderr = err.getvalue().strip()
            if stderr:
                print(stderr)
            self.assertTrue(stderr.startswith('Min # of any password element cannot exceed half of the total length of the password'))
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0180_upper_success(self):
        try:
            with captured_output() as (out, err):
                r = main('20', '--minupper', '10')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(len(stdout) == 20)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0190_digit_failure(self):
        try:
            with captured_output() as (out, err):
                r = main('20', '--mindigit', '11')
            self.assertTrue(r != 0)
            stderr = err.getvalue().strip()
            if stderr:
                print(stderr)
            self.assertTrue(stderr.startswith('Min # of any password element cannot exceed half of the total length of the password'))
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_digit_success(self):
        try:
            with captured_output() as (out, err):
                r = main('20', '--mindigit', '10')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(len(stdout) == 20)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        ...
