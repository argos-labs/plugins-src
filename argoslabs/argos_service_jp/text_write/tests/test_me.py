#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.text_write`
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
from argoslabs.argos_service_jp.text_write import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.argos_service_jp.text_write
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
    def test0100_add_e_e_success(self):
        try:
            r = main('C:/work/Text Write/argoslabs/argos_service_jp/text_write/tests/test_01.txt',
                     'test_line_xx',
                     'Add to End',
                     'Add to End')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_add_e_b_success(self):
        try:
            r = main('C:/work/Text Write/argoslabs/argos_service_jp/text_write/tests/test_02.txt',
                     'test_line_xx',
                     'Add to End',
                     'Add to Front')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_add_b_e_success(self):
        try:
            r = main('C:/work/Text Write/argoslabs/argos_service_jp/text_write/tests/test_03.txt',
                     'test_line_xx',
                     'Add to Front',
                     'Add to End')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_add_b_b_success(self):
        try:
            r = main('C:/work/Text Write/argoslabs/argos_service_jp/text_write/tests/test_04.txt',
                     'test_line_xx',
                     'Add to Front',
                     'Add to Front')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0300_new_create_success(self):
        try:
            r = main('C:/work/Text Write/argoslabs/argos_service_jp/text_write/tests/test_10.txt',
                     'test_line_xx',
                     'Add to End',
                     'Add to End',
                     '--file_exists',
                     'New Create')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0400_overwrite_success(self):
        try:
            r = main('C:/work/Text Write/argoslabs/argos_service_jp/text_write/tests/test_01.txt',
                     'test_line_xx',
                     'Add to End',
                     'Add to End',
                     '--overwrite')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
