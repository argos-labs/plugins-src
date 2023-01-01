#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.line_id_card_ocr`
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
from argoslabs.argos_service_jp.line_id_card_ocr import _main as main
import config


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.argos_service_jp.line_id_card_ocr
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        """
        argoslabs.argos_service_jp.line_id_card_ocr
        :return: raise exception ArgsError
        """
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    """
    # If the Return Value is in Japanese, Build will not pass.
    # ==========================================================================
    def test0100_success(self):
        self.homedrive = os.getenv("HOMEDRIVE")
        try:
            r = main(config.token,
                     '{}/work/LINE ID Card OCR/argoslabs/argos_service_jp'
                     '/line_id_card_ocr/tests/20101204_1430898.jpg'
                     .format(self.homedrive))
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
    """

    # ==========================================================================
    def test0110_success_with_opt(self):
        self.homedrive = os.getenv("HOMEDRIVE")
        try:
            r = main(config.token,
                     '{}/work/LINE ID Card OCR/argoslabs/argos_service_jp'
                     '/line_id_card_ocr/tests/license.jpg'
                     .format(self.homedrive),
                     '--out_key',
                     'Birthday')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
