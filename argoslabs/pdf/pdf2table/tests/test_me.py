#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.pdf.pdf2table`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.pdf.pdf2table import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('invalid')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test0110_table(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice_table.txt')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0120_text(self):
    #     try:
    #         r = main('--text', 'June 2021 Invoice.pdf', '--output', 'June 2021 Invoice_text.txt')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0120_None_table(self):
    #     try:
    #         r = main('--table', 'Inv_11390_from_KOTRA_Silico_new.pdf',
    #                  '--output', 'inv.txt')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0130_PDF_not_table(self):
    #     try:
    #         r = main('--table', '18.PDF',
    #                  '--output', 'inv.txt')
    #         self.assertTrue(r == 1)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0140_PDF_Text_page(self):
    #     try:
    #         r = main('--text', 'April tech radar_0904-BV.pdf',
    #                  '--output', 'April tech radar_0904-BV.txt',
    #                  '--page', '4')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0200_table_csv(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice.csv')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0210_table_csv_page(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice.csv',
    #                  '--page', '1')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0220_none_table_csv_page_(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice.csv',
    #                  '--page', '2')
    #         self.assertTrue(r == 1)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0230_table_csv_page_table_index(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice.csv',
    #                  '--page', '1',
    #                  '--table-index', '1')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0230_None_table_csv_page_table_index(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice.csv',
    #                  '--page', '1',
    #                  '--table-index', '2')
    #         self.assertTrue(r == 9)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0300_table_text(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice.txt')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0310_table_txt_page(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice.txt',
    #                  '--page', '1')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0320_none_table_txt_page(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice.txt',
    #                  '--page', '2')
    #         self.assertTrue(r == 1)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0330_table_txt_page_table_index(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice.txt',
    #                  '--page', '1',
    #                  '--table-index', '1')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0340_None_table_txt_page_table_index(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice.txt',
    #                  '--page', '1',
    #                  '--table-index', '2')
    #         self.assertTrue(r == 9)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0350_table_txt_sep(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice.txt',
    #                  '--separator', '****')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0360_table_txt_page_sep(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice.txt',
    #                  '--page', '1',
    #                  '--separator', '$$$')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0370_table_txt_page_table_index_sep(self):
    #     try:
    #         r = main('--table', 'June 2021 Invoice.pdf',
    #                  '--output', 'June 2021 Invoice.txt',
    #                  '--page', '1',
    #                  '--table-index', '1',
    #                  '--separator', '%%')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
