#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:argoslabs.interactive.zenity_forms
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
from unittest import TestCase
from argoslabs.interactive.zenity_forms import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_text_success(self):
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 인터엑티브 필요없음
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            r = main(
                 'New Form &!@##$%^',
                '--add_entry', 'User ID',
                '--add_entry', 'User ID2',
                '--add_password', 'Password',
                '--add_password', 'Password2',
                '--add_list', 'lst1',
                '--list_values', 'value1', '--list_values', 'value2',
                '--column_values', 'value1', '--column_values', 'value2',
                '--show_header', True, '--dformat', 'MM/DD/YYYY',
                # '--add_calendar', 'Date of Birth',
                #'--add_list', 'List1', '--separator',
                # '--show_header', True, '--forms-_date_format', 'Y%m%d',
                '--title', 'Enter your information',
                 '--timeout', '50',
                '--ok_label', 'Se lect', '--cancel_label', 'Ex it'
            )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
