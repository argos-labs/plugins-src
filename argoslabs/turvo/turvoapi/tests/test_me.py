#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:argoslabs.turvo.turvoapi
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
from argoslabs.turvo.turvoapi import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    key_id = None
    key = None

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
    def test0100_wrong_pwd(self):
        try:
            r = main('send', 'secret', 'ssato@argos-labs.com',
                     'sendtransrpa', 'http://my-sandbox.turvo.com/api/pub')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_get_token(self):
        try:
            r = main('send', 'secret', 'ssato@argos-labs.com',
                     '..','http://my-sandbox.turvo.com/api/pub')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

