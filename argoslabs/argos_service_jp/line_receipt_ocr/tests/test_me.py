#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.line_receipt_ocr`
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
from argoslabs.argos_service_jp.line_receipt_ocr import _main as main
import config

################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.argos_service_jp.line_receipt_ocr
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        """
        argoslabs.argos_service_jp.line_receipt_ocr
        :return: raise exception ArgsError
        """
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)


    # If the Return Value is in Japanese, Build will not pass.
    # ==========================================================================
    def test0100_success(self):
        self.homedrive = os.getenv("HOMEDRIVE")
        try:
            r = main(config.token,
                     '{}/work/LINE receipt OCR/argoslabs/argos_service_jp'
                     '/line_receipt_ocr/tests/65.写真.15168980147429.jpg'
                     .format(self.homedrive))
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)


    # ==========================================================================
    def test0110_success_with_opt(self):
        self.homedrive = os.getenv("HOMEDRIVE")
        try:
            r = main(config.token,
                     '{}/work/LINE receipt OCR/argoslabs/argos_service_jp'
                     '/line_receipt_ocr/tests/receipt_01.jpg'
                     .format(self.homedrive),
                     '--out_key',
                     'Payment Time')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
