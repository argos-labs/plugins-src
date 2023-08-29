"""
====================================
 :mod:`argoslabs.ocr.xtracta`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Xtracta : UnitTest
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
#  * [2020/08/19]
#     - unittest
#  * [2020/08/19]
#     - starting


################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.ocr.xtractagetdoc import _main as main


################################################################################

class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.api_key = '..'
        cls.docid = '162731100'

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
            r = main(self.api_key, 'output','--docid', self.docid)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test110_wrong_api(self):
        try:
            r = main('175fb7800ee7766556dd87ff3095a7603636daf','output',
                     '--docid',self.docid)
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test120_wrong_doc(self):
        try:
            r = main(self.api_key, '--docid','112')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test130_success(self):
        try:
            r = main(self.api_key, 'output')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
