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
#  * [2021/03/26]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/07/10]
#     - starting

################################################################################
import os
import sys
import csv
import json
import yaml
import platform
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.check.env import _main as main
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

    # # ==========================================================================
    # def test0100_success_csv(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout) as ifp:
    #             print(ifp.read())
    #         with open(stdout) as ifp:
    #             rows = list()
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) > 20)
    #                 rows.append(row)
    #             self.assertTrue(len(rows) == 2 and rows[1][0] == platform.platform(()))
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)

    # ==========================================================================
    def test0110_success_json(self):
        stdout = 'stdout.txt'
        try:
            r = main('--out-format', 'json',
                        '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                rj = json.load(ifp)
            pprint(rj)
            self.assertTrue(rj['platform']['platform'] == platform.platform())
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0120_success_yaml(self):
        stdout = 'stdout.txt'
        try:
            r = main('--out-format', 'yaml',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            with open(stdout) as ifp:
                if yaml.__version__ >= '5.1':
                    # noinspection PyUnresolvedReferences
                    rj = yaml.load(ifp, Loader=yaml.FullLoader)
                else:
                    rj = yaml.load(ifp)
            # pprint(rj)
            self.assertTrue(rj['platform']['platform'] == platform.platform())
            self.assertTrue(rj['env_vars'])
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # # ==========================================================================
    # def test0130_success_yaml_network_speed(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('--out-format', 'yaml', '--is-check-network-speed',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout) as ifp:
    #             print(ifp.read())
    #         with open(stdout) as ifp:
    #             rj = yaml.load(ifp)
    #         # pprint(rj)
    #         self.assertTrue(rj['platform']['platform'] == platform.platform())
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
