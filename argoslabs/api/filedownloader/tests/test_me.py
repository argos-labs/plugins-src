#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.api.filedownloader.tests`
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
from argoslabs.api.filedownloader import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))
        self.directory_path = r'C:\Users\Administrator\Desktop'


    # ==========================================================================
    def test0100_url_2_file(self):
        try:
            r = main(
                # 'https://research.nhm.org/pdfs/33557/33557-008.pdf',
                # 'https://www.sample-videos.com/zip/10mb.zip',
                'https://www.sample-videos.com/zip/100mb.zip',
                self.directory_path,
                '--filename','result'
            )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)