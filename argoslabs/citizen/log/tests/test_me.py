#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.citizen.log.tests`
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
from argoslabs.citizen.log import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0010_fail_empty(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_initialize(self):
        try:

            r = main(
                'Initialize',
                r'C:\Users\Administrator\Desktop',
                # 'TXT',
                # 'CSV',
                'LOG',
                # '--fIle_name_wt'
                # 'MM/DD/YYYY HH:MM:SS'
                # 'DD.MM.YY'
                # 'YYYYMMDD-HHMMSS.mmm'
                # 'YYYYMMDD-HHMMSS.mmm',
                # 'YYYY-MM-DD HH:MM:SS.mmm',
                #  'YYYY/MM/DD HH:MM:SS.mmm',
                #  'MMDDYYYY-HHMMSS.mmm',
                #  'MM-DD-YYYY HH:MM:SS.mmm',
                #  'MM/DD/YYYY HH:MM:SS.mmm',
                #  'M/D/YYYY HH:MM:SS.mmm',
                #  'YYYYMMDD-HHMMSS',
                #  'YYYY-MM-DD HH:MM:SS',
                #  'YYYY/MM/DD HH:MM:SS',
                #  'MMDDYYYY-HHMMSS',
                #  'MM-DD-YYYY HH:MM:SS',
                #  'MM/DD/YYYY HH:MM:SS',
                 'M/D/YYYY HH:MM:SS',
                #  'YYYYMMDD',
                #  'YYYY-MM-DD',
                #  'YYYY/MM/DD',
                #  'MMDDYYYY',
                #  'MM-DD-YYYY',
                #  'MM/DD/YYYY',
                #  'M/D/YYYY',
                #  'DD-MM-YYYY',
                #  'DD.MM.YYYY',
                #  'DD-MM-YY',
                # 'DD.MM.YY'

            )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_add_log(self):
        try:
            # with captured_output() as (out, err):
            r = main(
                'Add Log',
                r'C:\Users\Administrator\Desktop',
                # 'TXT',
                # 'CSV',
                'LOG',
                'YYYYMMDD-HHMMSS.mmm',
                '--log_file_path',
                r'C:\Users\Administrator\Desktop\Log_28102022_224057.log',
                '--event_message',
                'ok lets do it.'
            )
            self.assertTrue(r == 0)

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
