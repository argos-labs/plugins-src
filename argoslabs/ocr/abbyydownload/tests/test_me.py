"""
====================================
 :mod:`argoslabs.ocr.abbyydownload`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for  ABBYY: UnitTest
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
from argoslabs.ocr.abbyydownload import _main as main


################################################################################

class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.api_id = '..'
        cls.api_token = '..'
        cls.output = os.path.join(os.getcwd(), 'results')

    # ==========================================================================
    def test50_missing(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test100_success(self):
    #     try:
    #         r = main(self.api_id, self.api_token, '--result_name', 'temp.xlsx',
    #                  '--result_id', '5fb411084d9ac50ac071717f',
    #                  '--result_token',
    #                  '4F5614055E2A933F8D93A49DD149846446BBE253',
    #                  '--result_id', '5fb411084d9ac50ac071717f',
    #                  '--output', self.output)
    #         self.assertTrue(r != 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)

    # # ==========================================================================
    # def test110_success(self):
    #     try:
    #         r = main(self.api_id, self.api_token, '--result_name', 'temp.xlsx',
    #                  '--result_id', '5fb411084d9ac50ac071717f',
    #                  '--result_token',
    #                  '4F5614055E2A933F8D93A49DD149846446BBE253',
    #                  '--output', self.output)
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test120_success(self):
    #     try:
    #         r = main(self.api_id, self.api_token, '--statuscsv',
    #                  'abbyystatus.csv',
    #                  '--output', self.output)
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
