#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.parsehub_api`
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
from argoslabs.argos_service_jp.parsehub_api import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.argos_service_jp.parsehub_api
    """
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

    # ==========================================================================
    def test0100_run_ez_success(self):
        with open("C:/work/parsehub API/argoslabs/argos_service_jp/parsehub_api/tests/key_token_test.txt") as f:
            l = f.readlines()
            api_key = l[0].strip()
            token = l[1].strip()
        try:
            r = main('Run Project',
                     api_key,
                     token,
                     'ON')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_run_success(self):
        with open(
                "C:/work/parsehub API/argoslabs/argos_service_jp/parsehub_api/tests/key_token_test.txt") as f:
            l = f.readlines()
            api_key = l[0].strip()
            token = l[1].strip()
        try:
            r = main('Run Project',
                     api_key,
                     token,
                     'OFF')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0200_get_ez_success(self):
        with open(
                "C:/work/parsehub API/argoslabs/argos_service_jp/parsehub_api/tests/key_token_test.txt") as f:
            l = f.readlines()
            api_key = l[0].strip()
            token = l[1].strip()
            run_token = l[2].strip()
        try:
            r = main('Get Data',
                     api_key,
                     token,
                     'ON',
                     '--run_token',
                     run_token,
                     '--format',
                     'json')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0210_get_success(self):
        with open(
                "C:/work/parsehub API/argoslabs/argos_service_jp/parsehub_api/tests/key_token_test.txt") as f:
            l = f.readlines()
            api_key = l[0].strip()
            token = l[1].strip()
            run_token = l[2].strip()
        try:
            r = main('Get Data',
                     api_key,
                     token,
                     'OFF',
                     '--run_token',
                     run_token,
                     '--format',
                     'json')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0220_get_success(self):
        with open(
                "C:/work/parsehub API/argoslabs/argos_service_jp/parsehub_api/tests/key_token_test.txt") as f:
            l = f.readlines()
            api_key = l[0].strip()
            token = l[1].strip()
            run_token = l[2].strip()
        try:
            r = main('Get Data',
                     api_key,
                     token,
                     'ON',
                     '--run_token',
                     run_token)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    """
    # ==========================================================================
    def test0300_del_success(self):
        try:
            r = main('Delete Run Data',
                     't5QR6p-sQVRU',
                     'tidUTSCzTmak',
                     'ON',
                     '--run_token',
                     'tSSEVeEZB_Ty')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
    """

    # ==========================================================================
    def test0400_get_list_success(self):
        with open(
                "C:/work/parsehub API/argoslabs/argos_service_jp/parsehub_api/tests/key_token_test.txt") as f:
            l = f.readlines()
            api_key = l[0].strip()
            token = l[1].strip()
        try:
            r = main('Get Projects List',
                     api_key,
                     token,
                     'ON')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0500_get_last_success(self):
        with open(
                "C:/work/parsehub API/argoslabs/argos_service_jp/parsehub_api/tests/key_token_test.txt") as f:
            l = f.readlines()
            api_key = l[0].strip()
            token = l[1].strip()
        try:
            r = main('Get Last Run',
                     api_key,
                     token,
                     'ON')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
