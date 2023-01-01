#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.convert_image_2`
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
from argoslabs.argos_service_jp.convert_image_2 import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.argos_service_jp.convert_image_2
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_png_success(self):
        try:
            r = main('C:/Users/Windows/Pictures/Argos/TS_icon.png',
                     'C:/Users/Windows/Desktop/',
                     'JPEG')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0200_multi_tif_success(self):
        try:
            r = main('C:/Users/Windows/Desktop/axq3e-9qj76.tiff',
                     'C:/Users/Windows/Desktop/',
                     'PNG',
                     # '--aft_file_name',
                     # 'NG_"file',
                     # '--validate',
                     # 'Return Failure',
                     # '--file_exists',
                     # 'Return Failure'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0210_single_tif_success(self):
        try:
            r = main('C:/Users/Windows/Desktop/スライド1.TIF',
                     'C:/Users/Windows/Desktop/',
                     'JPEG',
                     # '--aft_file_name',
                     # 'NG_"file',
                     # '--validate',
                     # 'Return Failure',
                     # '--file_exists',
                     # 'Return Failure'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0300_webp_success(self):
        try:
            r = main('C:/Users/Windows/Desktop/Print2Image.webp',
                     'C:/Users/Windows/Desktop/',
                     'JPEG',
                     # '--aft_file_name',
                     # 'NG_"file',
                     # '--validate',
                     # 'Return Failure',
                     # '--file_exists',
                     # 'Return Failure'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)