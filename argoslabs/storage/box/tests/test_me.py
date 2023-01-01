#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.storage.box`
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
from argoslabs.storage.box import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.token = ''
        cls.csecret = ''
        cls.cid = ''

    # # ==========================================================================
    # def test0050_failure(self):
    #     try:
    #         _ = main()
    #         self.assertTrue(False)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)

    # ==========================================================================
    # def test0100_file_lists(self):
    #     try:
    #         r = main('File/Folder Lists',  self.csecret, self.cid, '--token', self.token,
    #                  '--folderid', 0)
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0110_upload_files_error(self):
    #     try:
    #         r = main('Upload Files', self.csecret, self.cid,
    #                  '--token', self.token,
    #                  '--files', 'sample.txt',
    #                  '--folderid', '0')
    #         self.assertTrue(r == 9)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0120_download_files(self):
    #     try:
    #         r = main('Download Files/Folder', self.csecret, self.cid,
    #                  '--token', self.token,
    #                   '--folderid', '138899098099', '--fileid', '820305444040',
    #                  '--output', 'output')
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0130_wrong_api(self):
    #     try:
    #         r = main('File/Folder Lists', self.csecret, self.cid, '--token', 'token')
    #         self.assertTrue(r == 1)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0140_upload_errors(self):
    #     try:
    #         r = main('Upload Files', self.csecret, self.cid, '--token', self.token,
    #                  '--files', 'sample24.txt',
    #                  '--folderid', '0414'
    #                  )
    #         self.assertTrue(r == 9)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0150_download_error(self):
    #     try:
    #         r = main('Download Files/Folder', self.csecret, self.cid,
    #                  '--token', self.token,
    #                  '--folderid', 'sdfsdf', '--fileid', '820305444040',
    #                  '--output', 'output')
    #         self.assertTrue(r == 9)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0160_get_token(self):
    #     try:
    #         r = main('Get Access Token',  self.csecret, self.cid, '--redirect_uri',
    #                  'https://google.com', '--user_id', '',
    #                  '--pwd', '')
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0170_get_token(self):
        try:
            r = main('Get Access Token',  
                        'g4kzT9tqhzJ4N7Pq6FnhTLNtM3sGNOtH', 
                        'qfi66e2q61af69gl96bnxx0utf04xhzs', 
                        '--redirect_uri', 'https://app.box.com', 
                        '--user_id', '',
                        '--pwd', '')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
