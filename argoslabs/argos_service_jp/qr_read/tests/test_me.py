#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.qr_read`
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
from argoslabs.argos_service_jp.qr_read import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.argos_service_jp.qr_read
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):

        try:
            _ = main('')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0060_failure(self):

        try:
            r = main('C:/Users/Windows/Pictures/QR/test0.jpg')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))

    # ==========================================================================
    def test0070_ignore_failure(self):

        try:
            r = main('C:/Users/Windows/Pictures/QR/test0.jpg',
                     '--read_err_opt',
                     'Ignore Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))

    # ==========================================================================
    def test0100_png_success(self):

        try:
            r = main('C:/Users/Windows/Pictures/QR/test1.png')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_jpg_success(self):

        try:
            r = main('C:/Users/Windows/Pictures/QR/test1.jpg')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_png_text_success(self):

        try:
            r = main('C:/Users/Windows/Pictures/QR/test2.png')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_png_text_3_success(self):

        try:
            r = main('C:/Users/Windows/Pictures/QR/test6.png')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_png_dirty_failure(self):

        try:
            r = main('C:/Users/Windows/Pictures/QR/test4.png')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_png_dirty_success(self):

        try:
            r = main('C:/Users/Windows/Pictures/QR/test5.png')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    """
    # ==========================================================================
    # When Building, Cannot Use Japanese in QR Code
    def test0160_png_jp_success(self):

        try:
            r = main('C:/Users/Windows/Pictures/QR/test7.png')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
    """

    # ==========================================================================
    def test0170_png_color_success(self):

        try:
            r = main('C:/Users/Windows/Pictures/QR/test8.png')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_png_color_inv_success(self):

        try:
            r = main('C:/Users/Windows/Pictures/QR/test9.png')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_tiff_success(self):

        try:
            r = main('C:/Users/Windows/Pictures/QR/test10.tif',
                     '--read_err_opt',
                     'Ignore Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
