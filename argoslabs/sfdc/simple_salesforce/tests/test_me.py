#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.SFDC.simple_salesforce`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
#
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2020/05/05]
#     - change package name "SFDC" => "sfdc"  <Jerry Chae>

################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.sfdc.simple_salesforce import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
# noinspection PyBroadException
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
                r = main('Contact', 'Create',
                         TU.username, TU.password, TU.security_token,
                         '--data', 'Lastname=Jack4',
                         '--data', 'email=jac21@ex.com'
                         )
                self.assertTrue(r == 0)
            except Exception:
                ...
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_update(self):
        try:
            try:
                r = main('Contact', 'Update',
                         TU.username, TU.password, TU.security_token,
                         '--data', 'Firstnam=J', '--id',
                         '0035w00003O5nLbAAJ')
                self.assertTrue(r == 0)
            except Exception:
                ...
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_delete(self):
        try:
            try:
                r = main('Contact', 'Delete',
                         TU.username, TU.password, TU.security_token,
                         '--id', '0035w00003O5nLbAAJ')
                self.assertTrue(r == 0)
            except Exception:
                ...
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0140_select_query(self):
    #     of = 'stdout.txt'
    #     try:
    #         r = main('Contact', 'Select-Query',
    #                  TU.username, TU.password, TU.security_token,
    #                  '--fieldnames', 'name', '--fieldnames', 'email',
    #                  '--outfile', of)
    #         self.assertTrue(r == 0)
    #         with open(of) as ifp:
    #             out = ifp.read()
    #             self.assertTrue(out >= 'Contact')
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)

    # # ==========================================================================
    # def test0150_select_query(self):
    #     of = 'stdout.txt'
    #     try:
    #         r = main('Contact', 'Select-Query',
    #                  TU.username, TU.password, TU.security_token,
    #                  '--fieldnames', 'id', '--fieldnames', 'name', '--outfile', of)
    #         self.assertTrue(r == 0)
    #         with open(of) as ifp:
    #             out = ifp.read()
    #             self.assertTrue(out >= 'Items')
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)

    # # ==========================================================================
    # def test0160_search(self):
    #     of = 'stdout.txt'
    #     try:
    #         r = main('Contact', 'Search',
    #                  TU.username, TU.password, TU.security_token,
    #                  '--value', 'Smith', '--outfile', of)
    #         self.assertTrue(r == 0)
    #         with open(of, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #             self.assertTrue(out >= 'Items')
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)

    # # ==========================================================================
    # def test0170_create_json1(self):
    #     try:
    #         r = main('Contact', 'Create',
    #                  TU.username, TU.password, TU.security_token,
    #                  '--jsonfile', 'sample_short.json')
    #         self.assertTrue(r == 0)

    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0180_update_json(self):
    #     try:
    #         r = main('Contact', 'Update',
    #                  TU.username, TU.password, TU.security_token,
    #                  '--jsonfile', 'update.json')
    #         self.assertTrue(r == 0)

    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)


