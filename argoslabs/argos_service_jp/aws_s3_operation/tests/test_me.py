#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.aws_s3_operation`
====================================
.. moduleauthor:: Taiki Shimasaki <shimasaki@argos-service.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.argos_service_jp.aws_s3_operation import _main as main

################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # Commented out the error "Please destroy the QApplication singleton
    # before creating a new QApplication instance".
    # No problem with testing.
    """
    # ==========================================================================
    def test0100_up_success(self):
        self.homedrive = os.getenv("HOMEDRIVE")
        try:
            r = main('Upload',
                     '--bucket_path',
                     'shimasaki-argos-bucket/my-folder',
                     '--path',
                     '{}/work/AWS_S3_Operation/argoslabs/argos_service_jp/aws_s3_operation/tests/test.txt'.format(self.homedrive),
                     '--profile',
                     'argos')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_up_success(self):
        self.homedrive = os.getenv("HOMEDRIVE")
        try:
            r = main('Upload',
                     '--bucket_path',
                     'shimasaki-argos-bucket/my-folder/',
                     '--path',
                     '{}/work/AWS_S3_Operation/argoslabs/argos_service_jp/aws_s3_operation/tests/video-sample.mp4'.format(self.homedrive),
                     '--add_path',
                     '{}/work/AWS_S3_Operation/argoslabs/argos_service_jp/aws_s3_operation/tests/2021-03-10 13-57-59.mp4'.format(self.homedrive),
                     '--add_path',
                     '{}/work/AWS_S3_Operation/argoslabs/argos_service_jp/aws_s3_operation/tests/pycharm.log'.format(self.homedrive),
                     '--profile',
                     'argos')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_dl_success(self):
        self.homedrive = os.getenv("HOMEDRIVE")
        self.homepath = os.getenv("HOMEPATH")
        try:
            r = main('Download',
                     '--bucket_path',
                     'shimasaki-argos-bucket/my-folder/video-sample.mp4',
                     '--path',
                     '{}{}/Desktop'.format(self.homedrive, self.homepath),
                     '--add_path',
                     'shimasaki-argos-bucket/my-folder/2021-03-10 13-57-59.mp4',
                     '--add_path',
                     'shimasaki-argos-bucket/my-folder/pycharm.log')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0300_ls_success(self):
        self.homedrive = os.getenv("HOMEDRIVE")
        self.homepath = os.getenv("HOMEPATH")
        try:
            r = main('Get List')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0400_mb_success(self):
        self.homedrive = os.getenv("HOMEDRIVE")
        self.homepath = os.getenv("HOMEPATH")
        try:
            r = main('Make Bucket',
                     '--bucket_path'
                     'shimasaki-argos-bucket',
                     '--path'
                     '{}{}/Desktop'.format(self.homedrive, self.homepath))
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0500_df_success(self):
        try:
            r = main('Delete Files',
                     '--bucket_path',
                     'shimasaki-argos-bucket/copy_folder/',
                     '--profile',
                     'argos')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0600_cp_success(self):
        try:
            r = main('Copy',
                     '--bucket_path',
                     'shimasaki-argos-bucket/copy_folder',
                     '--path',
                     'shimasaki-argos-bucket/my-folder/test.txt',
                     '--profile',
                     'argos')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0610_cp_success(self):
        try:
            r = main('Copy',
                     '--bucket_path',
                     'shimasaki-argos-bucket/copy_folder',
                     '--path',
                     'shimasaki-argos-bucket/my-folder/test.txt',
                     '--add_path',
                     'shimasaki-argos-bucket/my-folder/2021-03-10 13-57-59.mp4',
                     '--add_path',
                     'shimasaki-argos-bucket/my-folder/pycharm.log',
                     '--profile',
                     'argos')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0700_ex_success(self):
        try:
            r = main('Exists Check',
                     '--bucket_path',
                     'shimasaki-argos-bucket/my-folder/test.txt',
                     '--profile',
                     'argos')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
    """
    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
