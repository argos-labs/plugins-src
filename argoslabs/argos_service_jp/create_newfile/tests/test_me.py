#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.create_newfile`
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
from argoslabs.argos_service_jp.create_newfile import _main as main
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
    def test0100_txt(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test' + self.now,
                     'txt',
                     'None',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_txt_failure(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'te|st' + self.now,
                     'txt',
                     'None',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0120_ext_failure(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test' + self.now,
                     'INPUT [Other Extension(Adv)]',
                     'None',
                     'Return Failure',
                     'Return Failure',
                     '--other_ext',
                     'exte:nsi?on')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0200_docx(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test' + self.now,
                     'docx',
                     'None',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0210_pptx(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test' + self.now,
                     'pptx',
                     'None',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0220_csv(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test' + self.now,
                     'csv',
                     'None',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0230_log(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test' + self.now,
                     'log',
                     'None',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0240_xml(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test' + self.now,
                     'xml',
                     'None',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0250_html(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test' + self.now,
                     'html',
                     'None',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0300_timestamp_suf(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test' + self.now,
                     'txt',
                     'suffix',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0310_timestamp_pre(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test' + self.now,
                     'txt',
                     'prefix',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0400_xlsx(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test01' + self.now,
                     'xlsx',
                     'None',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0410_xlsx_sheetname(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test02' + self.now,
                     'xlsx',
                     'None',
                     'Return Failure',
                     'Return Failure',
                     '--sheetname',
                     'testsheet')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0420_xlsx_sheetname_valid_err(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test03' + self.now,
                     'xlsx',
                     'None',
                     'Return Failure',
                     'Return Failure',
                     '--sheetname',
                     'test\'sheet')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0430_xlsx_sheetname_len_err(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test04' + self.now,
                     'xlsx',
                     'None',
                     'Return Failure',
                     'Return Failure',
                     '--sheetname',
                     'testsheet_testsheet_testsheet_testsheet_testsheet_testsheet',
                     '--sheet_len_opt',
                     'Return Failure')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0440_xlsx_sheetname_len_cut(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test05' + self.now,
                     'xlsx',
                     'None',
                     'Return Failure',
                     'Return Failure',
                     '--sheetname',
                     'testsheet_testsheet_testsheet_testsheet_testsheet_testsheet',
                     '--sheet_len_opt',
                     'Cut to 31 char')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0500_input_extension(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test' + self.now,
                     'INPUT [Other Extension(Adv)]',
                     'None',
                     'Return Failure',
                     'Return Failure',
                     '--other_ext',
                     'png')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0510_input_extension_fail(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test' + self.now,
                     'INPUT [Other Extension(Adv)]',
                     'None',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0600_input_extension_error(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test' + self.now,
                     'xlsx',
                     'None',
                     'Return Failure',
                     'Return Failure',
                     '--other_ext',
                     'png')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0600_file_exists_error(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test',
                     'txt',
                     'None',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0700_no_ext(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test_01' + self.now,
                     'No Extension',
                     'None',
                     'Return Failure',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0710_no_other_ext(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test_02' + self.now,
                     'INPUT [Other Extension(Adv)]',
                     'None',
                     'Return Failure',
                     'Return Failure',
                     '--other_ext',
                     '')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0720_no_other_ext(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test_03' + self.now,
                     'No Extension',
                     'None',
                     'Return Failure',
                     'Return Failure',
                     '--other_ext',
                     '')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0800_file_exists_ow_txt(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test',
                     'txt',
                     'None',
                     'Overwrite',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0810_file_exists_ow_xl(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test',
                     'xlsx',
                     'None',
                     'Overwrite',
                     'Return Failure',
                     '--sheetname',
                     'test')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0820_file_exists_ig(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test',
                     'txt',
                     'None',
                     'Ignore Failure',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0830_file_exists_ig_xl(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test',
                     'xlsx',
                     'None',
                     'Ignore Failure',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0850_file_exists_addn(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'test',
                     'xlsx',
                     'None',
                     'Add (n) at End',
                     'Return Failure')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0900_filename_valid_err(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'COM3',
                     'No Extension',
                     'None',
                     'Add (n) at End',
                     'Return Failure')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0910_filename_valid_sani(self):
        try:
            r = main('C:/Users/Windows/Desktop',
                     'COM3',
                     'No Extension',
                     'None',
                     'Add (n) at End',
                     'Sanitize')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)