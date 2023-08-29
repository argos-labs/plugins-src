#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.pywin.uitext.tests`
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
from argoslabs.pywin.uitext import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))
        self.cmd_line = 'intl.cpl'
        self.title_re = 'Region'
        self.cmd_line2 = 'control panel'
        self.title_re2 = 'Control Panel'
        self.cmd_line3 = 'services.msc'  # 'work'
        self.title_re3 = 'Services'
        # self.cmd_line4 = 'Notepad'  # 'work'
        # self.title_re4 = 'Untitled - Notepad'
        self.cmd_line4 = 'Taskmgr.exe'  # 'work'
        self.title_re4 = 'Task Manager'

    # ==========================================================================
    def test0010_fail_empty(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_extract_text_by_cmd_line(self):
        try:
            r = main(
                'Extract Text By App',
                'uia',
                # 'win32',
                self.title_re,
                '--cmd_line',
                self.cmd_line
            )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_extract_text_by_cmd_line2(self):
        try:
            r = main(
                'Extract Text By App',
                'uia',
                # 'win32',
                self.title_re2,
                '--cmd_line',
                self.cmd_line2
            )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_extract_text_by_cmd_line3(self):
        try:
            r = main(
                'Extract Text By App',
                'uia',
                # 'win32',
                self.title_re3,
                '--cmd_line',
                self.cmd_line3,

            )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_extract_text_by_cmd_line4(self):
        try:
            r = main(
                'Extract Text By App',
                'uia',
                # 'win32',
                self.title_re4,
                '--cmd_line',
                self.cmd_line4,
                '--delay',
                2,
                # '--p_btype_controls',
                '--filter_controls',
                'ListItem',
                #     '--filter_controls_s_index',
                #     6,
                #     '--filter_controls_e_index',
                #     6
            )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_extract_text_from_running_process(self):
        try:
            r = main(
                'Extract Text From Running App',
                'uia',
                # 'win32',
                # 'Scenario Studio',
                # 'Region',
                # 'Task Manager',
                # 'result (3).txt - Notepad',
                # '--child_window',
                # 'Background processes'
                'Print',
                '--t_dialog_box',
                # '--p_btype_controls',
                # '--filter_controls',
                # 'Button',
                # 'TreeItem',
                # 'Static'
                '--filter_controls_w_index',
                '22',
                # '9',
            )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
