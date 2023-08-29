#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.system.envvar.tests`
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
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/07/12]
#     - starting

################################################################################
import os
import sys
import csv
import json
import yaml
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.system.envvar import _main as main
from pprint import pprint


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
    def test0100_success_empty(self):
        stdout = 'stdout.txt'
        try:
            r = main('--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            with open(stdout) as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) >= 20)
                    rows.append(row)
                self.assertTrue(len(rows) == 2 and 'HOMEPATH' in rows[0])
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0110_success_2(self):
        stdout = 'stdout.txt'
        try:
            r = main('homedrive', 'HOMEPATH',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            with open(stdout) as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 2)
                    rows.append(row)
                self.assertTrue(len(rows) == 2 and rows[1][0] == os.environ['homedrive'])
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0120_success_3(self):
        stdout = 'stdout.txt'
        try:
            r = main('homedrive', 'HOMEPATH', 'userprofile',
                     '--out-format', 'json',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            with open(stdout) as ifp:
                rd = json.load(ifp)
                hp = rd['homedrive'] + rd['HOMEPATH']
                self.assertTrue(hp == rd['userprofile'])
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # # ==========================================================================
    # def test0130_success_3(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('homedrive', 'HOMEPATH', 'userprofile',
    #                  '--out-format', 'yaml',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout) as ifp:
    #             print(ifp.read())
    #         with open(stdout) as ifp:
    #             rd = yaml.load(ifp)
    #             hp = rd['homedrive'] + rd['HOMEPATH']
    #             self.assertTrue(hp == rd['userprofile'])
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
