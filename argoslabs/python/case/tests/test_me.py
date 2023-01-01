"""
====================================
 :mod:`argoslabs.python.case.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
#
# Authors
# ===========
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/09/16]
#     - return '0' else case
#  * [2021/09/14]
#     - starting

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ArgsError, ArgsExit  # , vv_base64_encode
from unittest import TestCase
from argoslabs.python.case import _main as main

from contextlib import contextmanager
from io import StringIO


################################################################################
def vv_base64_encode(v):
    return v


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
        mdir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(mdir)

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0090_fail(self):
        try:
            with captured_output() as (out, err):
                r = main(vv_base64_encode('abc !! abc'))
            self.assertTrue(r == 99)
            _err = err.getvalue()
            self.assertTrue(_err == 'Error: Invalid Expression "abc !! abc"')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_success_1(self):
        try:
            with captured_output() as (out, err):
                r = main(vv_base64_encode('abc = abc'))
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == '1')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0105_success_else(self):
        try:
            with captured_output() as (out, err):
                r = main(vv_base64_encode('abc = def'))
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == '0')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success_4(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    vv_base64_encode('abc = abc'),
                    vv_base64_encode('abc==dev'),
                    vv_base64_encode('ef ==ef'),
                )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == '1,3')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_success_4(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    vv_base64_encode('1 = 1'),
                    vv_base64_encode('abc==3'),
                    vv_base64_encode('4.5 ==4.5'),
                    vv_base64_encode('3<def'),
                )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == '1,3,4')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_success_numeric(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    vv_base64_encode('-1 = 1'),
                    vv_base64_encode('1.0 >= -1.0'),
                    vv_base64_encode('-.5 < 4.5'),
                    vv_base64_encode('11.0 == 11'),
                )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == '2,3,4')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_success_empty(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    vv_base64_encode('= '),
                    vv_base64_encode(' =='),
                    vv_base64_encode('= 3'),
                    vv_base64_encode(' != abc'),
                    vv_base64_encode(' def <> '),
                    vv_base64_encode(' !='),
                )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == '1,2,4,5')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_wildcard_fail(self):
        try:
            with captured_output() as (out, err):
                r = main(vv_base64_encode('abc || abc'))
            self.assertTrue(r == 99)
            _err = err.getvalue()
            self.assertTrue(_err == 'Error: Right operand must have Wildcard')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_wildcard_1(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    vv_base64_encode('abc___def || abc*'),
                    vv_base64_encode('abc***def || *abc'),
                    vv_base64_encode('abc*zzz*def || *zzz*'),
                    vv_base64_encode('abc-zzz-def || abc*def'),
                )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == '1,3,4')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_space(self):
        try:
            with captured_output() as (out, err):
                r = main(
                    vv_base64_encode('== " "'),
                    vv_base64_encode(' = " "'),
                    vv_base64_encode(' = ""'),
                )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == '3')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
