#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.check.netspeed.tests`
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
#  * [2020/07/12]
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
from argoslabs.check.netspeed import _main as main
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
    def test0100_success_yaml_network_speed(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
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
                    self.assertTrue(len(row) == 2)
                    rows.append(row)
                self.assertTrue(len(rows) == 2 and rows[0][0] == 'download_speed')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
