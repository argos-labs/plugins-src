#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:argoslabs.interactive.zenity_progress
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
from argoslabs.interactive.zenity_progress import _main as main


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
            r = main(
                 '--text', 'Update System Logs', '--percentage', '50',
                #'--pulsate',True,
                 # '--auto_close',True, '--auto_kill', True,
                 # '--no_cancel', True, '--timeout', 2,
                      '--width', '500', '--height', '500',
                      '--ok_label', 'Select', '--cancel_label', 'Exit'
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)