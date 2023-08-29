"""
====================================
 :mod:`argoslabs.screen.capture.tests.test_me`
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
#  * [2021/06/14]
#     - main
#  * [2021/06/07]
#     - starting

################################################################################
import os
import sys
import time
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
from argoslabs.screen.capture import _main as main

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
        mdir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(mdir)

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0100_full_screen_capture(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            c_file = 'screen-capture.png'
            with captured_output() as (out, err):
                r = main(c_file)
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == os.path.abspath(c_file))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_active_screen_capture(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            time.sleep(5)
            c_file = 'screen-capture-aw.png'
            with captured_output() as (out, err):
                r = main(c_file, '--active-window')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == os.path.abspath(c_file))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
