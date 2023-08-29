"""
====================================
 :mod:`argoslabs.ocr.signiverfi`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Singature Verification UnitTest
"""
#
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
# * [2021/05/20]
# - build a plugin
# * [2021/05/20]
# - starting



################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.ocr.signverfi import _main as main


################################################################################

class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.api_token = '..'
        cls.api_key = '..'

    # ==========================================================================
    def test50_missing(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test100_success(self):
        try:
            r = main('Signature Checking', 1234, self.api_token,
                         'signature1.png')
            self.assertTrue(r == 9)

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test150_success(self):
        try:
            r = main('Signature Verfication', 12334, self.api_token,
                     'signature1.png', 'signature2.png','--testimgs',
                     'signature3.png')
            self.assertTrue(r == 9)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
