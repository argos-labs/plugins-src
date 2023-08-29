#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.excel_newfile`
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
from unittest import TestCase

from alabs.common.util.vvargs import ArgsError
# noinspection PyProtectedMember
from argoslabs.argos_service_jp.excel_newfile import _main as main
from datetime import datetime

################################################################################
class TU(TestCase):
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
        try:
            _ = main('')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_xlsx(self):
        try:
            r = main('Excel',
                     'C:/Users/Windows/Desktop',
                     'test01' + self.now,
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_xlsx_sheetname(self):
        try:
            r = main('Excel',
                     'C:/Users/Windows/Desktop',
                     'test02' + self.now,
                     'Return Failure',
                     'Return Failure',
                     '--sheetname',
                     'testsheet')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0120_xlsx_sheetname_valid_err(self):
        try:
            r = main('Excel',
                     'C:/Users/Windows/Desktop',
                     'test03' + self.now,
                     'Return Failure',
                     'Return Failure',
                     '--sheetname',
                     'test￥sheet')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0130_xlsx_sheetname_len_err(self):
        try:
            r = main('Excel',
                     'C:/Users/Windows/Desktop',
                     'test04' + self.now,
                     'Return Failure',
                     'Return Failure',
                     '--sheetname',
                     'testsheet_testsheet_testsheet_testsheet_testsheet',
                     '--sheet_len_opt',
                     'Return Failure')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0140_xlsx_sheetname_len_cut(self):
        try:
            r = main('Excel',
                     'C:/Users/Windows/Desktop',
                     'test05' + self.now,
                     'Return Failure',
                     'Return Failure',
                     '--sheetname',
                     'testsheet_testsheet_testsheet_testsheet_testsheet',
                     '--sheet_len_opt',
                     'Cut to 31 char')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0200_file_exists_error(self):
        try:
            r = main('Excel',
                     'C:/Users/Windows/Desktop',
                     'test',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0210_file_exists_addn(self):
        try:
            r = main('Excel',
                     'C:/Users/Windows/Desktop',
                     'test',
                     'Add (n) at End',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0300_filename_len_err(self):
        try:
            r = main('Excel',
                     'C:/Users/Windows/Desktop',
                     'test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_',
                     'Add (n) at End',
                     'Return Failure')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0400_csv(self):
        try:
            r = main('CSV',
                     'C:/Users/Windows/Desktop',
                     'test',
                     'Add (n) at End',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test500_filename_val(self):
        try:
            r = main('Excel',
                     'C:/Users/Windows/Desktop',
                     'te><st',
                     'Add (n) at End',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)