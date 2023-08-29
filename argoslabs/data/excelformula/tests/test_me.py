"""
====================================
 :mod:`argoslabs.data.excelformula`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Excel Advance III : UnitTest
"""
#
# Authorsalabs.
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2020/08/07]
#     - unittest
#  * [2020/08/07]
#     - starting


################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.data.excelformula import _main as main


################################################################################
# noinspection PyUnresolvedReferences,PyBroadException
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test50_missing(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test100_pastevalue(self):
    #     try:
    #         r = main('new.xlsx', '--newfilename', 'new0.xlsx', 'D2',
    #                  '=SUM(50,50)', '--show_formula', True)
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test110_pastevalue(self):
    #     try:
    #         r = main('new.csv', '--newfilename', 'new0.xlsx', 'D2',
    #                  '=SUM(50,50)')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test120_pastevalue(self):
    #     try:
    #         r = main('new.csv', '--newfilename', 'new0.csv', 'D2',
    #                  '=SUM(50,50)')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test130_pastevalue(self):
    #     try:
    #         r = main('new.xlsx', '--newfilename', 'new0.csv', 'D2',
    #                  '=SUM(50,50)')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test140_pastevalue(self):
    #     try:
    #         r = main('new.xlsx', 'E2', '=SUM(50,50)')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test150_pastevalue(self):
    #     try:
    #         r = main('new.csv', 'E2', '=SUM(50,50)')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test160_test(self):
    #     try:
    #         r = main('sample0.xlsx', 'E2', '=SUM(50,50)', '--show_formula', True)
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test170_test(self):
    #     try:
    #         r = main('arraytest1.xlsx', 'd1', '=a1+c1','--sheetname', 'Sheet2',
    #                  '--show_formula', True)
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
