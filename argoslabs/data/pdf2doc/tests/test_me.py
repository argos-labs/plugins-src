#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.pdf2doc`
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
from argoslabs.data.pdf2doc import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    key_id = None
    key = None

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        cls.tdir = os.path.dirname(__file__)

    # ==========================================================================
    def tearDown(self) -> None:
        ...

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('invalid')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test0100_success(self):
    #     try:
    #         r = main(os.path.join(self.tdir, 'sample1.pdf'))
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0110_success(self):
    #     try:
    #         r = main( os.path.join(self.tdir, 'sample1.pdf'), '--output',
    #                  os.path.join(self.tdir,'results.docx'))
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0120_success(self):
    #     try:
    #         r = main( os.path.join(self.tdir, 'claimtech.pdf'), '--output',
    #                  os.path.join(self.tdir,'claimtech.docx'))
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
