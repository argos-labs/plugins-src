#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.terminal.scp`
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
#  * [2020/04/12]
#     - starting

################################################################################
import os
import sys
import shutil
# from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.terminal.scp import _main as main
from alabs.common.util.vvnet import is_svc_opeded


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        # cls.host = '10.211.55.57'
        # cls.port = 22
        cls.host = '..'
        cls.port = 22
        cls.user = '..'
        cls.passwd = '..'

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_not_enough_parameter(self):
        try:
            _ = main('host', 'user')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_get_file(self):
        stdout = 'stdout.txt'
        _local = 'hosts.txt'
        try:
            r = main(self.host, self.user, 'Get',
                     '/etc/hosts',
                     _local,
                     '--password', self.passwd,
                     '--outfile', stdout
                     )
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == _local)
            self.assertTrue(os.path.exists(_local))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)
            # if os.path.exists(_local):
            #     os.remove(_local)

    # ==========================================================================
    def test0110_get_file_recursive(self):
        stdout = 'stdout.txt'
        _local = 'work'
        try:
            r = main(self.host, self.user, 'Get',
                     '~/work',
                     _local,
                     '--password', self.passwd,
                     '--outfile', stdout
                     )
            self.assertTrue(r != 0)

            r = main(self.host, self.user, 'Get',
                     '~/work',
                     _local,
                     '--password', self.passwd,
                     '--recursive',
                     '--outfile', stdout
                     )
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == _local)
            self.assertTrue(os.path.exists(_local))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)
            # if os.path.exists(_local):
            #     shutil.rmtree(_local)

    # ==========================================================================
    def test0130_put_file(self):
        stdout = 'stdout.txt'
        _local = 'hosts.txt'
        try:
            r = main(self.host, self.user, 'Put',
                     '~/work/hosts.txt',
                     _local,
                     '--password', self.passwd,
                     '--outfile', stdout
                     )
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == _local)
            self.assertTrue(os.path.exists(_local))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)
            if os.path.exists(_local):
                os.remove(_local)

    # ==========================================================================
    def test0140_put_folder_recursive(self):
        stdout = 'stdout.txt'
        _local = 'work'
        try:
            r = main(self.host, self.user, 'Put',
                     '~/tmp',
                     _local,
                     '--password', self.passwd,
                     '--recursive',
                     '--outfile', stdout
                     )
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == _local)
            self.assertTrue(os.path.exists(_local))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)
            if os.path.exists(_local):
                shutil.rmtree(_local)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
