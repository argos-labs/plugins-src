"""
====================================
 :mod:`argoslabs.system.system.tests.test_me`
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
#  * [2021/03/31]
#     - 그룹에 "1002-Verifications" 넣음
#  * [2021/03/03]
#     - class PSUtil
#  * [2021/03/02]
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
from argoslabs.system.psutil import _main as main
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
    def test0100_get_process_all(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('Get Process',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            with open(stdout) as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 10)
                    rows.append(row)
                self.assertTrue(len(rows) > 2)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0110_get_process_python(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('Get Process', '--pname', 'python',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            with open(stdout) as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 10)
                    rows.append(row)
                self.assertTrue(len(rows) > 2 and rows[-1][3].startswith('python'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0115_get_process_not_exists(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('Get Process', '--pname', 'unknown--process',
                     '--outfile', stdout)
            self.assertTrue(r == 1)
            with open(stdout) as ifp:
                rstr = ifp.read()
            self.assertTrue(not rstr)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0120_get_cpu_percent(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('CPU Percent',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            with open(stdout) as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) >= 2)
                    rows.append(row)
                self.assertTrue(len(rows) == 2 and float(rows[-1][-1]) > 0.0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0130_get_cpu_count(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('CPU Count',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            with open(stdout) as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 1)
                    rows.append(row)
                self.assertTrue(len(rows) == 2 and int(rows[-1][-1]) >= 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0140_get_load_avg(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('Load Avg',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            with open(stdout) as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 3)
                    rows.append(row)
                self.assertTrue(len(rows) == 2 and float(rows[-1][-1]) >= 0.0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0150_get_memory_info(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('Memory Info',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            with open(stdout) as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 5)
                    rows.append(row)
                self.assertTrue(len(rows) == 2 and float(rows[-1][2]) > 0.0 and float(rows[-1][2]) <= 100.0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0160_get_disk_info(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('Disk Info',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                print(ifp.read())
            with open(stdout) as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 10)
                    rows.append(row)
                self.assertTrue(len(rows) >= 2)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0170_get_network_stats(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('Network Stats',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                print(ifp.read())
            with open(stdout, encoding='utf-8') as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 9)
                    rows.append(row)
                self.assertTrue(len(rows) >= 2)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0180_get_network_conns(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('Network Conns',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                print(ifp.read())
            with open(stdout, encoding='utf-8') as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 8)
                    rows.append(row)
                self.assertTrue(len(rows) >= 2)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0190_get_nic_address(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('NIC Address',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                print(ifp.read())
            with open(stdout, encoding='utf-8') as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 6)
                    rows.append(row)
                self.assertTrue(len(rows) >= 2)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0200_get_nic_info(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('NIC Info',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                print(ifp.read())
            with open(stdout, encoding='utf-8') as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 5)
                    rows.append(row)
                self.assertTrue(len(rows) >= 2)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
