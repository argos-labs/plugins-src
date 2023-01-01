#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.sfdc.newuser`
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
from argoslabs.sfdc.newuser import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    username = None
    password = None
    security_token = None

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.username = 'irene@argos-labs.com'
        cls.password = '..'
        cls.security_token = '..'

    # ==========================================================================

    def tearDown(self) -> None:
        ...

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('invalid')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_create(self):
        try:
            try:
                r = main('Create', TU.username, TU.password, TU.security_token,
                         '--newusername', 'bbb12451@sales.com', '--lastname',
                         '142',
                         '--email', '12345678@gmail.com', '--alias', 'integ',
                         '--timezone', 'America/Los_Angeles',
                         '--localkey', "en_US", '--encoding', 'UTF-8',
                         '--lngkey', 'en_US',
                         '--profileid', '00e5w000002BaFVAA0')
            except Exception:
                ...
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_create_json(self):
        try:
            try:
                r = main('Create',TU.username, TU.password, TU.security_token,
                         '--json', 'sample_json.json')
                self.assertTrue(r == 0)
            except Exception:
                ...
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_select_query(self):
        try:
            try:
                r = main('Search Profile Id',
                     TU.username, TU.password, TU.security_token)
                self.assertTrue(r == 0)
            except Exception:
                ...
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
