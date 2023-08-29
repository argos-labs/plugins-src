#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:argoslabs.dropbox.api
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.dropbox.api import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
	cls.token = ''
    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_file_lists(self):
        try:
            r = main('File/Folder Lists', self.token,  '--directory', '',)
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_upload_files(self):
        try:
            r = main('Upload Files', self.token, '--files', 'sample.txt',
                     '--files', 'sample2.txt',
                     '--directory', '/')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_download_files(self):
        try:
            r = main('Download Files/Folder', self.token,'--directory', '/test',
                     '--output', 'output')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_wrong_api(self):
        try:
            r = main('File/Folder Lists', 'api')
            self.assertTrue(r == 1)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_upload_errors(self):
        try:
            r = main('Upload Files', self.token, '--files', 'sample24.txt',
                     '--files', 'sample2.txt',
                     '--directory', '')
            self.assertTrue(r == 9)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_download_files_folders(self):
        try:
            r = main('Download Files/Folder', self.token, '--fdirectory', '/test/test.jpeg',
                     '--fdirectory', '/test/test2.jpeg', '--directory', '',
                     '--output', 'output')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_empty_folder(self):
        try:
            r = main('Download Files/Folder', self.token, '--directory', '/test/newfolder',
                     '--output', 'output')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)