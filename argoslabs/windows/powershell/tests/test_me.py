#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.windows.powershell.tests.test_me`
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
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/08/28]
#     - starting

################################################################################
import os
import sys
import calendar
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.windows.powershell import _main as main
from contextlib import contextmanager
from io import StringIO
from datetime import date


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
# noinspection PyUnusedLocal
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        for month_idx in range(1, 13):
            print(calendar.month_name[month_idx])
            print(calendar.month_abbr[month_idx])
            print("")
        self.assertTrue(True)

    # ==========================================================================
    def test0010_help(self):
        try:
            _ = main('-h')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test0020_invalid(self):
    #     try:
    #         with captured_output() as (out, err):
    #             r = main()
    #         self.assertTrue(r != 0)
    #         errs = err.getvalue()
    #         outs = out.getvalue()
    #         self.assertTrue(errs.endswith('Invalid Script or Script file') and
    #                         not outs)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0030_invalid(self):
        try:
            with captured_output() as (out, err):
                r = main('--script-file', 'Invalid-script.sccc')
            self.assertTrue(r != 0)
            errs = err.getvalue()
            outs = out.getvalue()
            self.assertTrue(errs.find('Cannot find script') > 0 and
                            not outs)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_success_script(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                # PAM에서는 ' 로 표현되어야 함
                r = main('--script', "Get-Date -UFormat '%Y/%m/%d %R %Z'")
            self.assertTrue(r == 0)
            errs = err.getvalue()
            outs = out.getvalue()
            today_s = date.today().strftime('%Y/%m/%d')
            self.assertTrue(outs.startswith(today_s) and
                            not errs)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success_script(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main('--script', 'Get-Process -Name exp*,power*')
            self.assertTrue(r == 0)
            errs = err.getvalue()
            outs = out.getvalue()
            self.assertTrue(outs.find('ProcessName') > 0 and not errs)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_success_script_file(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main('--script-file', 'asc.ps1')
            self.assertTrue(r == 0)
            errs = err.getvalue()
            outs = out.getvalue()
            self.assertTrue(outs.find('Usage:   ASC.PS1  char') > 0 and not errs)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_success_script_file_with_param(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main('--script-file', 'asc.ps1',
                         '--script-params', 'a')
            self.assertTrue(r == 0)
            errs = err.getvalue()
            outs = out.getvalue()
            self.assertTrue(outs == '97' and not errs)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_success_script_file_with_param(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main('--script-file', 'bios.ps1',
                         '--script-params', '.')
            self.assertTrue(r == 0)
            errs = err.getvalue()
            outs = out.getvalue()
            self.assertTrue(outs.find('SMBIOSBIOS') > 0 and not errs)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_success_script_file(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main('--script-file', 'bootstate.ps1')
            self.assertTrue(r == 0)
            errs = err.getvalue()
            outs = out.getvalue()
            self.assertTrue(outs == 'Normal' and not errs)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    # def test0160_success_script_file(self):
    #     try:
    #         with captured_output() as (out, err):
    #             r = main('--script-file', 'sendemail-01.ps1',
    #                      '--script-params', 'jerrychae@outlook.com',
    #                      '--script-params', 'mcchae@argos-labs.com',
    #                      '--script-params', 'Test from jerrychae@outlook to argos-labs.com',
    #                      '--encoding', 'ISO-8859-1')
    #         self.assertTrue(r == 0)
    #         errs = err.getvalue()
    #         outs = out.getvalue()
    #         self.assertTrue(not outs and not errs)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
