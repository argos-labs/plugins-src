#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.git.html.tests`
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
from argoslabs.git.html import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))
        self.gitmdlink='https://github.com/Jerry-Chae/plugins/blob/main/argoslabs/office/wordeditor/README.md'
        self.username='Jerry-Chae'
        self.output=r'C:\Users\Administrator\Desktop\test_now'

    # ==========================================================================
    def test0100_download_html_pdf(self):
        try:
            r = main(
                self.gitmdlink,
                self.username,
                self.output,
                '--filename',
                'wordeditor',
                '--word'
                # '--chromepath',
                # 'start chrome'
                # r'C:\Program Files\Google\Chrome\Application\chrome.exe'
            )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
