#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.pdf2txt`
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
from argoslabs.data.pdf2txt import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):

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
    # def test0100_success(self):
    #     try:
    #         r = main('test.pdf')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0100_success(self):
    #     try:
    #         r = main('pdffiles/April tech radar_0904-BV (1).pdf')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    # # ==========================================================================
    # def test0150_success(self):
    #     try:
    #         r = main('pdffiles/Inv_11390_from_KOTRA_Silico.pdf','--output',
    #                  'output/Inv_11390_from_KOTRA_Silico.txt','--coordinates')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0200_success(self):
    #     try:
    #         r = main('pdffiles/Stevens Law Group 23126.pdf')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

