#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.print2image`
====================================
.. moduleauthor:: Taiki Shimasaki <shimasaki@argos-service.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.argos_service_jp.print2image import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.argos_service_jp.print2image
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        """
        argoslabs.argos_service_jp.print2image
        :return: raise exception ArgsError
        """
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_pdf_2_png_success(self):

        try:
            r = main('C:/Users/Windows/Pictures/QR/Create Newfile20200907.pdf',
                     'C:/Users/Windows/Desktop',
                     'PNG',
                     '--aft_file_name',
                     'test',
                     '--dpi',
                     300)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_word_2_png_success(self):

        try:
            r = main('C:/Users/Windows/Documents/RPA-Plugin/QR-Generate_img.docx',
                     'C:/Users/Windows/Desktop',
                     'PNG')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0300_excel_2_png_success(self):

        try:
            r = main('C:/Users/Windows/Desktop/test.xlsx',
                     'C:/Users/Windows/Desktop',
                     'JPEG')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0400_powerpoint_2_png_success(self):

        try:
            r = main('C:/Users/Windows/Documents/Test.pptx',
                     'C:/Users/Windows/Desktop',
                     'PNG',
                     '--dpi',
                     300,
                     '--rm_nl',
                     'ON')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0500_excel_2_pdf_success(self):

        try:
            r = main('C:/Users/Windows/Desktop/test.xlsx',
                     'C:/Users/Windows/Desktop',
                     'PDF')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0600_word_2_pdf_success(self):

        try:
            r = main('C:/Users/Windows/Documents/RPA-Plugin/QR-Generate_img.docx',
                     'C:/Users/Windows/Desktop',
                     'PDF')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0700_powerpoint_2_pdf_success(self):

        try:
            r = main('C:/Users/Windows/Documents/Test.pptx',
                     'C:/Users/Windows/Desktop',
                     'PDF')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
