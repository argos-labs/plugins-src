#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.filesystem.exists.tests.test_me`
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
#  * [2021/03/31]
#     - 그룹에 "1002-Verifications" 넣음
#  * [2021/03/08]
#     - starting

################################################################################
import os
import sys
import shutil
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.filesystem.exists import _main as main
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
# noinspection PyUnresolvedReferences
class TU(TestCase):
    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.abspath(os.path.dirname(__file__)))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0100_success_file_exists(self):
        try:
            with open('foo.txt', 'w') as ofp:
                ofp.write('this is foo.txt')
            with captured_output() as (out, err):
                r = main('foo.txt', '')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            # print(stdout)
            self.assertTrue(os.path.abspath('foo.txt') == stdout)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists('foo.txt'):
                os.remove('foo.txt')

    # ==========================================================================
    def test0110_success_folder_exists(self):
        try:
            os.makedirs('bar')
            with open('bar/foo.txt', 'w') as ofp:
                ofp.write('this is foo.txt')
            with captured_output() as (out, err):
                r = main('', 'bar')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            # print(stdout)
            self.assertTrue(os.path.abspath('bar') == stdout)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists('bar'):
                shutil.rmtree('bar')

    # ==========================================================================
    def test0120_success_file_exists_empty(self):
        try:
            with open('foo.txt', 'w'):
                pass
            with captured_output() as (out, err):
                r = main('foo.txt', '')
            self.assertTrue(r == 1)
            stdout = out.getvalue().strip()
            # print(stdout)
            self.assertTrue(os.path.abspath('foo.txt') == stdout and
                            os.path.getsize('foo.txt') == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists('foo.txt'):
                os.remove('foo.txt')

    # ==========================================================================
    def test0130_success_folder_exists_empty(self):
        try:
            os.makedirs('bar')
            with captured_output() as (out, err):
                r = main('', 'bar')
            self.assertTrue(r == 1)
            stdout = out.getvalue().strip()
            # print(stdout)
            self.assertTrue(os.path.abspath('bar') == stdout)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists('bar'):
                shutil.rmtree('bar')

    # ==========================================================================
    def test0140_success_file_not_exists(self):
        try:
            with captured_output() as (out, err):
                r = main('foo.txt', '')
            self.assertTrue(r == 2)
            stdout = out.getvalue().strip()
            # print(stdout)
            self.assertTrue(not stdout)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists('foo.txt'):
                os.remove('foo.txt')

    # ==========================================================================
    def test0150_success_folder_not_exists(self):
        try:
            with captured_output() as (out, err):
                r = main('', 'bar')
            self.assertTrue(r == 2)
            stdout = out.getvalue().strip()
            # print(stdout)
            self.assertTrue(not stdout)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists('bar'):
                shutil.rmtree('bar')

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
