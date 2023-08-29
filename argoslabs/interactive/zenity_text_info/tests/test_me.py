#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:argoslabs.interactive.zenity_text_info
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
from argoslabs.interactive.zenity_text_info import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('invalid')
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
                    '--filename', 'sample.csv',
                    # '--neditable', True,
                    '--font', 'monospace',
                    #'--checkbox', 'I read and accept the terms.',
                    '--timeout', '3', '--width', '500', '--height', '500',
                    '--ok_label', 'Select', '--cancel_label', 'Exit'
                    )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)