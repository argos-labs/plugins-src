"""
====================================
 :mod:`argoslabs.screen.start_record.tests.test_me`
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
#  * [2021/05/16]
#     - starting

################################################################################
import os
import sys
import time
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
from argoslabs.screen.start_record import _main as main, BREAK_FILE
from argoslabs.screen.stop_record import _main as stop_main

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
    def test0100_recording(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            srf = 'screen-rec.mp4'
            with captured_output() as (out, err):
                r = main(srf)
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == os.path.abspath(srf))

            time.sleep(15)

            with captured_output() as (out, err):
                r = stop_main()
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == 'Stopped')
            self.assertTrue(not os.path.exists(BREAK_FILE))

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
