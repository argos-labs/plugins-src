#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.file.addimg`
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
from argoslabs.file.addimg import _main as main
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
    def test0100_excel(self):
        try:
            r = main('sample.xlsx', 'img.tif', '--cell', 'f10', '--dwidth',
                     '100',
                     '--dheight', '100', '--output', 'demo.xlsx')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_pdf(self):
        try:
            r = main('sample.pdf', 'img.tif', '--output', 'demo.pdf',
                     '--dheight', '100')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_docx(self):
        try:
            r = main('sample.docx', 'img.bmp', '--output', 'demo.docx',
                     '--dheight', '400', '--dwidth', '200')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # Bitmap Image File is a format developed by Microsoft for Window

    # ==========================================================================
    def test0130_pptx(self):
        try:
            r = main('sample.pptx', 'img.tif', '--output', 'demo.pptx', '--dx',
                     '10', '--dy', '10', '--dheight', '400', '--dwidth', '200')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_pdf(self):
        try:
            r = main('sample.pdf', 'colorimg.png', '--output', 'demo.pdf',
                     '--dx',
                     '100', '--dy', '100', '--dwidth', '250', '--dheight',
                     '250',
                     '--pagenum', 0)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
