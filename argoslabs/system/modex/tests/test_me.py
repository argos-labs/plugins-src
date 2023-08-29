#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:argoslabs.system.modex
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
from argoslabs.system.modex import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    key_id = None
    key = None

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.endpoint = 'https://bcdb.modex.tech/data-node01-api'
        cls.api_key = '..'
        cls.username = 'bcdb.admin@modex.tech'
        cls.password = '..'
        cls.clientid = '0x01'
        cls.clientsecret ='0x000001'

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('invalid')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_get_api_key(self):
        try:
            r = main('Get API Key', self.endpoint, '--username', self.username,
                     '--password', self.password, '--clientid', self.clientid,
                     '--clientsecret', self.clientsecret)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_create(self):
        try:
            r = main('Create Schema of Entity', self.endpoint, '--api_key', self.api_key,
                     '--entity_title', 'TestEntity1')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_retrieve_w_entity_title(self):
        try:
            r = main('Get Schema of Entity', self.endpoint, '--api_key',
                     'wKoRXyeHoqQMwsQSpAr0hFOp-HPmW61AEytb0FNu8fw',
                     '--entity_title', 'TestEntity3', '--outputfile', 'results.json')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_retrieve_wo_entity_title(self):
        try:
            r = main('Get Schema of Entity', self.endpoint, '--api_key', self.api_key)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_create_json(self):
        try:
            r = main('Create Schema of Entity', self.endpoint, '--api_key', self.api_key,
                     '--entity_title', 'TestEntity', '--entity_json', 'schema.json')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_retrieve_all_records(self):
        try:
            r = main('Get Record from Entity', self.endpoint, '--api_key', self.api_key,
                     '--entity_title', 'TestEntity3')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_retrieve_w_recordid(self):
        try:
            r = main('Get Record from Entity', self.endpoint, '--api_key', self.api_key,
                     '--entity_title', 'TestEntity', '--record_id', '386609d1ec11f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_insert_record(self):
        try:
            r = main('Insert Record into Entity', self.endpoint, '--api_key', self.api_key,
                     '--entity_title', 'TestEntity', '--record_json', 'records.json')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0180_upload_file(self):
        try:
            r = main('Upload File', self.endpoint, '--api_key', self.api_key,
                     '--entity_title', 'TestEntity', '--record_id',
                     '0505933d1cdbe00f1371c61ce2d07940bbacbab15b3a186cb7f700b4fa2a4dd2',
                     '--attachment', 'sample0.png')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
