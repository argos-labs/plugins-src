#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.qr_generate`
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
from argoslabs.argos_service_jp.qr_generate import _main as main
from datetime import datetime


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.argos_service_jp.qr_generate
    """
    os.chdir(os.path.dirname(__file__))
    now = datetime.now()
    now = now.strftime('%f')

    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        """
        argoslabs.argos_service_jp.qr_generate
        :return: raise exception ArgsError
        """
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test01_' + self.now,
                     'PNG',
                     'This is test QR-Code')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_sanitize_success(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     't\e/s:t*0?2"><_|' + self.now,
                     'PNG',
                     'This is test QR-Code',
                     '--validate',
                     'Sanitize')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_color_success(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test03_' + self.now,
                     'PNG',
                     'This is test QR-Code',
                     '--cell_color',
                     '#008000',
                     '--back_color',
                     'navy')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_jpeg_success(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test04_' + self.now,
                     'JPEG',
                     'This is test QR-Code')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_bmp_success(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test05_{}.bmp'.format(self.now),
                     'JPEG',
                     'This is test QR-Code')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_png_L_success(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test06_{}.png'.format(self.now),
                     'PNG',
                     'This is test QR-Code',
                     '--err_cor_lev',
                     'L (7%)')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    """
    # ==========================================================================
    def test0160_png_over_fail(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test07_' + self.now,
                     'PNG',
                     '人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a_',
                     # 1276+ byte
                     '--fail_opt',
                     'Return Failure')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_png__not_over_success(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test08_' + self.now,
                     'PNG',
                     '人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a人1a',
                     # 1276 byte
                     '--fail_opt',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
    """

    # ==========================================================================
    def test0180_png_box_100_success(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test09_' + self.now,
                     'PNG',
                     'This is test QR-Code',
                     '--box_size',
                     '100')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0190_png_version_20_success(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test10_' + self.now,
                     'PNG',
                     'This is test QR-Code',
                     '--version',
                     '20')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_png_add_n_success(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test',
                     'PNG',
                     'This is test QR-Code',
                     '--file_exists',
                     'Add (n) at End')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_png_ignore_success(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test',
                     'PNG',
                     'This is test QR-Code',
                     '--file_exists',
                     'Ignore Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_png_string_from_file_success(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test11_' + self.now,
                     'PNG',
                     '',
                     '--from_file',
                     'C:/Users/Windows/Pictures/QR/QR_test_utf8.txt',
                     '--file_exists',
                     'Ignore Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)


    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
