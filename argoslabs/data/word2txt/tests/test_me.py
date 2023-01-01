"""
====================================
 :mod:`argoslabs.data.word2txt`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for word2txt : unittest
"""
#
# Authors
# ===========
#
# * Kyobong An
#
# Change Log
# --------
#
#  * [2021/11/17]
#     - starting
#

################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.data.word2txt import _main as main


################################################################################
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # # ==========================================================================
    # def test50_missing(self):
    #     try:
    #         _ = main()
    #         self.assertTrue(False)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)
    #
    # # ==========================================================================
    # def test0100_docx(self):
    #     try:
    #         r = main('test.docx')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0110_docx_output(self):
    #     try:
    #         r = main('test.docx', '--output', 'docx.txt')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0200_doc(self):
    #     try:
    #         r = main('test.doc',
    #                  '--output', 'doc.txt',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
