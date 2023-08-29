#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.simple.counter.tests`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.simple.counter import _main as main
from alabs.common.util.vvargs import ArgsError
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
class TU(TestCase):

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))
        self.start_number = 4
        self.end_numbers = 5

    # ==========================================================================
    def test0010_fail_empty(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_initialize(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    'Initialize',
                    2,
                    1,
                    '--increment',
                    1
                )
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '2')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_count_up(self):
        try:

            with captured_output() as (out, err):
                r = main(
                    'Count Up',
                    1,
                    5,
                    '--increment',
                    1
                )
                self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '2')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_count_up2(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    'Count Up',
                    2,
                    5,
                    '--increment',
                    1
                )
                self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '3')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_count_up3(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    'Count Up',
                    3,
                    5,
                    '--increment',
                    1
                )
                self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '4')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_count_up4(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    'Count Up',
                    4,
                    5,
                    '--increment',
                    1
                )
                self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '5')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_count_up_no_event(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    'Count Up',
                    5,
                    5,
                    '--increment',
                    1
                )
                print(r)
                self.assertTrue(r == 1)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '1')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_count_down(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    'Count Down',
                    5,
                    1,
                    '--increment',
                    -1
                )
                self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '4')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_count_down2(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    'Count Down',
                    4,
                    1,
                    '--increment',
                    -1
                )
                self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '3')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_count_down3(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    'Count Down',
                    3,
                    1,
                    '--increment',
                    -1
                )
                self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '2')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_count_down4(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    'Count Down',
                    2,
                    1,
                    '--increment',
                    -1
                )
                self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '1')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_count_down_no_event(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    'Count Down',
                    1,
                    1,
                    '--increment',
                    -1
                )
                self.assertTrue(r == 1)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
