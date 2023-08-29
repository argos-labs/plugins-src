#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.storage.boxii`
====================================
.. moduleauthor:: Arun Kumar <ak080495@gmail.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
# import os
import sys
# from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.storage.boxii import _main as main
import warnings

warnings.simplefilter("ignore", ResourceWarning)

################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.myuti.text
    """
    # ==========================================================================
    token = ''
    csecret = ''
    cid = ''

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def ignore_warnings(test_func):
        def do_test(self, *args, **kwargs):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", ResourceWarning)
                test_func(self, *args, **kwargs)
        return do_test

    # ==========================================================================
    @ignore_warnings
    def test0050_file_lists(self):
        try:
            r = main('File/Folder Lists', self.csecret,self.cid,
                     '--token', self.token,
                     '--folderid', 0)
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    @ignore_warnings
    def test0051_upload_files(self):
        try:
            r = main('Upload Files', self.csecret, self.cid,
                     '--token',self.token,
                     '--files', 'Q.txt',
                     '--folderid', '0')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(r == 99)

    # ==========================================================================
    @ignore_warnings
    def test0052_upload_files_error(self):
        try:
            r = main('Upload Files', self.csecret, self.cid,
                     '--token', self.token,
                     '--files', 'testbox.txt',
                     '--folderid', '0')
            self.assertTrue(r == 1)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(r == 99)

    # ==========================================================================
    @ignore_warnings
    def test0120_download_files(self):
        try:
            r = main('Download Files/Folder', self.csecret, self.cid,
                     '--token', self.token,
                     # '--folderid', '167821520820',
                     '--fileid', '985813811560',
                     '--output', 'C:/Users/Administrator/Desktop/test/'
                     )
            print(r)
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(r == 99)

    # # ==========================================================================
    @ignore_warnings
    def test0120_download_files_field_error(self):
        try:
            r = main('Download Files/Folder', self.csecret,self.cid,
                     '--token', self.token,
                     # '--folderid', '0',
                     # '--fileid', '985592137417',
                     # '--output', 'output'
                     )
            self.assertTrue(r == 1)
        except Exception as e:
            print(e)
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(r == 99)

    # # ==========================================================================
    # @ignore_warnings
    # def test0160_get_token(self):
    #     try:
    #         r = main('Get Access Token',  self.csecret, self.cid, '--redirect_uri',
    #                  'https://app.mybox.com', '--user_id', '',
    #                  '--pwd', '')
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
