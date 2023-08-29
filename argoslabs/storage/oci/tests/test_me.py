#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.storage.oci`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
# import os
import sys
from unittest import TestCase
from argoslabs.storage.oci import _main as main
import json
import warnings

################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.storage.oci
    """
    # ==========================================================================
    f = open(r'C:\Users\Administrator\Desktop\cre.json')
    data = json.load(f)
    user=data['user']
    fingerprint=data['fingerprint']
    key_file=data['key_file']
    tenancy=data['tenancy']
    region=data['region']
    warnings.simplefilter("ignore", UserWarning)


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
    #                  self.user,
    #                  self.fingerprint,
    #                  self.key_file,
    #                  self.tenancy,
    #                  self.region,
    #                  '--file', r'C:\Users\Administrator\Desktop\docdigi.bot',
    #                  '--bucket_name',"bucket-20230324-1605",
    #                  # '--folderid', '0'
    #                  '--upload_folder',"excel/"
    #                  )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    #
    #
    # # ==========================================================================
    # def test0120_download_file(self):
    #     try:
    #         r = main('Download Files',
    #                  self.user,
    #                  self.fingerprint,
    #                  self.key_file,
    #                  self.tenancy,
    #                  self.region,
    #                  '--bucket_name',"bucket-20230324-1605",
    #                  '--object_name', 'docdigi.bot',
    #                  '--output',r'C:\Users\Administrator\Desktop\oci_api_code'
    #                  )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         # self.assertTrue(r == 99)
    #         self.assertTrue(False)


    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
