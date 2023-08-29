#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.text_read`
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
from argoslabs.argos_service_jp.text_read import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.argos_service_jp.text_read
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        """
        argoslabs.argos_service_jp.text_read
        :return: raise exception ArgsError
        """
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_all_success(self):
        try:
            r = main('C:/work/Text Read/argoslabs/argos_service_jp/text_read/tests/test_text.txt',
                     'All Lines')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_all_nl_success(self):
        try:
            r = main('C:/work/Text Read/argoslabs/argos_service_jp/text_read/tests/test_text.txt',
                     'All Lines',
                     '--nl_code',
                     'display')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_first_success(self):
        try:
            r = main('C:/work/Text Read/argoslabs/argos_service_jp/text_read/tests/test_text.txt',
                     'First Line')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_last_success(self):
        try:
            r = main('C:/work/Text Read/argoslabs/argos_service_jp/text_read/tests/test_text.txt',
                     'Last Line')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0300_2_10_success(self):
        try:
            r = main('C:/work/Text Read/argoslabs/argos_service_jp/text_read/tests/test_text.txt',
                     'Select Lines',
                     '--start_line',
                     '2',
                     '--end_line',
                     '10')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0310_3_last_success(self):
        try:
            r = main('C:/work/Text Read/argoslabs/argos_service_jp/text_read/tests/test_text.txt',
                     'Select Lines',
                     '--start_line',
                     '3',
                     '--nl_code',
                     'display')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0320_first_13_success(self):
        try:
            r = main('C:/work/Text Read/argoslabs/argos_service_jp/text_read/tests/test_text.txt',
                     'Select Lines',
                     '--end_line',
                     '13')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0400_only_7_success(self):
        try:
            r = main('C:/work/Text Read/argoslabs/argos_service_jp/text_read/tests/test_text.txt',
                     'Select Lines',
                     '--start_line',
                     '7',
                     '--end_line',
                     '7')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0500_over_failure(self):
        try:
            r = main('C:/work/Text Read/argoslabs/argos_service_jp/text_read/tests/test_text.txt',
                     'Select Lines',
                     '--start_line',
                     '12',
                     '--end_line',
                     '20')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    """
    # ==========================================================================
    def test0600_failure(self):
        try:
            r = main('C:/work/Text Read/argoslabs/argos_service_jp/text_read/tests/text.txt',
                     'Select Lines',
                     '--start_line',
                     '3',
                     '--end_line',
                     '6')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
    """

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
