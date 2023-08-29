#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.storage.ftp_server`
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
from unittest import TestCase
from argoslabs.storage.ftp_server import _main as main
import json
import warnings

################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.storage.oci
    """
    # ==========================================================================
    f = open(r'C:\Users\Administrator\Desktop\ftp_cre.json')
    data = json.load(f)
    user = data['user']
    passw = data['pass']
    host = '127.0.0.1'
    port = 21


    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)


    # # ==========================================================================
    # def test0051_upload_files(self):
    #     try:
    #         r = main('Upload Files',
    #                  self.host,
    #                  self.user,
    #                  self.passw,
    #                  '--file', r'C:\Users\Administrator\Desktop\s2.png'
    #                  )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)



    # ==========================================================================
    def test0120_download_file(self):
        try:
            r = main('Download Files',
                     self.host,
                     self.user,
                     self.passw,
                     # '--ftp_dir','/',
                     # '--filename', 'AADHAR.pdf',
                     '--filename', 'school-bus.png',
                     '--output', r'C:\Users\Administrator\Desktop'
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            # self.assertTrue(r == 99)
            self.assertTrue(False)


    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
