#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.check.svcopen.tests`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/03/27]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/05/14]
#     - starting

################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.check.svcopen import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_failure(self):
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        try:
            _ = main('host')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0030_failure(self):
        try:
            _ = main('host', 'invalid_port')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success_svc_open(self):
        stdout = 'stdout.txt'
        try:
            r = main('google.com', '80',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
            self.assertTrue(rs == '1')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    # def test0110_success_svc_open(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('redis.argos-labs.com', '6379',
    #                  '--alive-val', 'alive',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout, encoding='utf-8') as ifp:
    #             rs = ifp.read()
    #         self.assertTrue(rs == 'alive')
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0120_failure_svc_open(self):
        stdout = 'stdout.txt'
        try:
            r = main('redis.argos-labs.com', '16379',
                     '--dead-val', 'dead',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
            self.assertTrue(rs == 'dead')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    # def test0130_success_svc_open_csv_out(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('redis.argos-labs.com', '6379',
    #                  '--alive-val', 'alive', '--csv-out',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout, encoding='utf-8') as ifp:
    #             rs = ifp.read().rstrip()
    #         self.assertTrue(rs.split('\n')[-1] == 'redis.argos-labs.com,6379,alive')
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
