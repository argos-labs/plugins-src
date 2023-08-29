"""
====================================
 :mod:`argoslabs.ocr.docdigitizer`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for docdigitizer : UnitTest
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
#  * [2023/03/03]
#     - unittest
#  * [2023/03/03]
#     - starting


################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.ocr.docdigitizer import _main as main


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
    # def test100_success(self):
    #     try:
    #         r = main(self.api_key,r'C:\Users\Administrator\Desktop\SingleTableSample[520].JPG',
    #                  # '--filename','invoice0.pdf',
    #                  # '--tag','ok',
    #                  # "--callback_method","POST",
    #                  # "--callback_url","https:/docdigitizer-callback.customer.com",
    #                  # "--callback_headers","Authorization:apikey",
    #                  # "--callback_headers", "Basic:basic_api_key",
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
