#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:v
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
from argoslabs.data.splitpdf import _main as main
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

    # # ==========================================================================
    # def test0100_success(self):
    #     try:
    #         r = main('Splitting', '--filename', 'sample.pdf',
    #                  '--output_folder', 'sample')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0110_success(self):
    #     try:
    #         r = main('Merging', '--folder', 'sample',
    #                  '--output_file', 'merged_file.pdf')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0120_success(self):
    #     try:
    #         r = main('Merging', '--filename', 'sample/sample_1.pdf',
    #                  '--filename', 'sample/sample_2.pdf',
    #                  '--output_folder', 'sample0')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0130_success(self):
    #     try:
    #         r = main('Splitting', '--filename', 'sample.pdf',
    #                  '--output_folder', 'sample0')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0140_success(self):
    #     try:
    #         r = main('Merging', '--filename', 'sample/sample_1.pdf',
    #                  '--filename', 'sample/sample_2.pdf',
    #                  '--output_folder', 'sample0')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)