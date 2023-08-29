#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.git.uitext.tests`
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
from argoslabs.excel.image import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

        self.file_path=r'C:\Users\Administrator\Pictures\my work\my_plugin.xlsx'
        self.directory_path = r'C:\Users\Administrator\Desktop'


    # ==========================================================================
    def test0100_conv_2_image(self):
        try:
            r = main(
                self.file_path,
                self.directory_path,
                '--filename','now',
                '--sheetname','Sheet1',
                '--filetype','PNG'
            )
            # print(r)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)