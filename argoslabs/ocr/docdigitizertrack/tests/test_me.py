"""
====================================
 :mod:`argoslabs.ocr.docdigitizertrack`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Docdigitizer : UnitTest
"""
#

# Authors
# ===========
#
# * Arun Kumar
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
from argoslabs.ocr.docdigitizertrack import _main as main


################################################################################

class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.api_key = ''

    # ==========================================================================
    def test50_missing(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test110_success_doc(self):
    #     try:
    #         r = main(self.api_key,'--docid','5139346f-62fd-4130-a976-c41ba4653b1c'
    #                  # '--docid','151525647'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)
