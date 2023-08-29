#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.json_csv`
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
from argoslabs.argos_service_jp.json_csv import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.argos_service_jp.json_csv
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
    def test0100_J2C_success(self):
        try:
            r = main('JSON2CSV',
                     'C:/work/JSON - CSV/argoslabs/argos_service_jp/json_csv/tests/test.json',
                     'C:/work/JSON - CSV/argoslabs/argos_service_jp/json_csv/tests')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_C2J_success(self):
        try:
            r = main('CSV2JSON',
                     'C:/work/JSON - CSV/argoslabs/argos_service_jp/json_csv/tests/indeed_2021_0216_092933.csv',
                     'C:/work/JSON - CSV/argoslabs/argos_service_jp/json_csv/tests')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0300_J2C_Nested_success(self):
        try:
            r = main('JSON2CSV',
                     'C:/work/JSON - CSV/argoslabs/argos_service_jp/json_csv/tests/Env.json',
                     'C:/work/JSON - CSV/argoslabs/argos_service_jp/json_csv/tests',
                     '--key',
                     'monitors')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
