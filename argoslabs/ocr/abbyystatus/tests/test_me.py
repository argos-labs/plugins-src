"""
====================================
 :mod:`argoslabs.ocr.abbyystatus`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for  ABBYY Status: UnitTest
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
#  * [2020/11/11]
#     - unittest
#  * [2020/11/11]
#     - starting


################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.ocr.abbyystatus import _main as main


################################################################################

class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.api_id = '..'
        cls.api_token = '..'

    # ==========================================================================
    def test50_missing(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test100_multidocs(self):
    #     try:
    #         r = main(self.api_id, self.api_token, '5fb42e77a67d394888602d60')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test110_singledoc(self):
    #     try:
    #         r = main(self.api_id, self.api_token, '5fb410a34d9ac50ac071717c')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test120_singledoc(self):
    #     try:
    #         r = main(self.api_id, self.api_token, '5fb5d3b7a6ea3d1544188e84',
    #                  '5fb410a34d9ac50ac071717c','5fb5d3b7a6ea3d1544188e84')
    #         self.assertTrue(r != 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
