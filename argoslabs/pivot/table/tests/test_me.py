#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.pivot.table.tests`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.pivot.table import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))
        self.file_path=r'C:\Users\Administrator\Desktop\master_data.xlsx'
        self.directory_path = r'C:\Users\Administrator\Desktop\Attachements'


    # ==========================================================================
    def test0100_cre_pivot_table(self):
        try:
            r = main(
                self.file_path,
                r'C:\Users\Administrator\Desktop\master_data2.xlsx',
                'Sheet1',
                'Bot Name',
                'Bot Execution Status',
                '--output_sheet_name','Sheet3'
                #'--directory_path', self.directory_path,
                # '--filename','now',
            )
            # print(r)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)