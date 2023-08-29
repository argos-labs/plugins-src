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
from argoslabs.ocr.xtracta import _main as main


################################################################################

class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.api_key = '..'
        cls.workflow = '967163'

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
            r = main(self.api_key,self.workflow,'--filename','invoice0.pdf',
                     '--filename','invoice0.pdf')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test110_wrong_api(self):
        try:
            r = main('175fb7800ee7766556dd87ff3095a7603636daf', self.workflow,
                     '--filename','invoice2.pdf')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test120_wrong_workflow(self):
        try:
            r = main(self.api_key, '112', '--filename','invoice2.pdf')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test130_wrong_file(self):
        try:
            r = main(self.api_key, self.workflow, '--filename','invoice.pdf')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test140_success(self):
        try:
            r = main(self.api_key,self.workflow,'--csvfile','filemon.csv')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)