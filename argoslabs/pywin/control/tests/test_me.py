#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.pywin.uitext.control`
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
from argoslabs.pywin.control import _main as main
from alabs.common.util.vvargs import ArgsError
import warnings

################################################################################
class TU(TestCase):

    # ==========================================================================
    def setUp(self) -> None:
        warnings.simplefilter("ignore", UserWarning)
        os.chdir(os.path.dirname(__file__))
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
    def test0100_filter_controls_action_start_app(self):
        try:
            r = main(
                'Control By App',
                # 'Print',
                'uia',
                # 'Untitled - Notepad',
                'PuTTY Configuration',
                '--cmd_line',
                # 'Notepad',
                'putty',
                # '--t_dialog_box',
                # '--child_window',
                # 'child_window(title="View", control_type="MenuItem"),',
                # '--action',
                # 2,
                # '--child_window',
                # 'child_window(title="Zoom", control_type="MenuItem")',
                # '--action',
                # 2,
                # '--child_window',
                # 'child_window(title="Portrait", class_name="ComboBox")',
                # '--action',
                # '2',
                # '--store_controls',
                # r'C:\Users\Administrator\Desktop\con_file.txt'
            )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)


    # ==========================================================================
    def test0100_filter_controls_action_running_process(self):
        try:
            r = main(
                'Control Running App',
                'uia',
                # 'win32',
                'PuTTY Configuration',
                # '--child_window',
                # 'child_window(title="Printer to send ANSI printer output to:", auto_id="1001", control_type="Edit")',

                # '--child_window',
                # 'child_window(title="{Ctrl,Shift} + Ins:", auto_id="1056", control_type="ComboBox")',
                # '--action',
                # # 'Microsoft XPS Document Writer',
                # 'No action',
                # # '--store_controls',
                # # r'C:\Users\Administrator\Desktop\con_file.txt'
            )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
