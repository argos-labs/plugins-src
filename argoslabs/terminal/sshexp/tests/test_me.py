#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.terminal.ssh-expect`
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
#  * [2019/04/15]
#     - starting

################################################################################
import os
import sys
# from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.terminal.sshexp import _main as main
from alabs.common.util.vvnet import is_svc_opeded


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True
    HOST = {
        'linux': [
            {
                'host': '192.168.99.250',
                'port': 22,
            },
            {
                'host': '10.211.55.2',
                'port': 10022,
            },
        ],
        'sw3560': [
            {
                'host': '192.168.168.1',
                'port': 22,
            },
            {
                'host': '10.211.55.2',
                'port': 20022,
            },
        ],
    }

    # ==========================================================================
    def _get_host(self, svc):
        for hi in self.HOST[svc]:
            if is_svc_opeded(hi['host'], hi['port']):
                return hi['host'], hi['port']
        raise RuntimeError('Cannot get propper socket address')

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0100_not_enough_parameter(self):
        try:
            _ = main('host')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_not_enough_parameter(self):
        try:
            _ = main('host', 'user')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0120_not_enough_parameter(self):
        try:
            _ = main('host', 'user', 'prompt')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0130_invalid_host(self):
        out_f = 'out.txt'
        err_f = 'err.txt'
        try:
            r = main('host', 'user', 'prompt', 'date',
                     '--outfile', out_f, '--errfile', err_f)
            self.assertTrue(r != 0)
            with open(err_f) as ifp:
                err = ifp.read()
                print(err)
                self.assertTrue(err.find('getaddrinfo failed') > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(out_f):
                os.remove(out_f)
            if os.path.exists(err_f):
                os.remove(err_f)

    # # ==========================================================================
    # def test0200_valid_host(self):
    #     out_f = 'out.txt'
    #     err_f = 'err.txt'
    #     try:
    #         host, port = self._get_host('linux')
    #         r = main(host, 'root', 'root@testweb.*# $',
    #                  '--port', port,
    #                  '--password', 'r',
    #                  '--echo-display',
    #                  'ls', 'date',
    #                  '--outfile', out_f, '--errfile', err_f)
    #         self.assertTrue(r == 0)
    #         with open(out_f) as ifp:
    #             out = ifp.read()
    #             print(out)
    #             self.assertTrue(out.find('Last login') >= 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(out_f):
    #             os.remove(out_f)
    #         if os.path.exists(err_f):
    #             os.remove(err_f)
    #
    # # ==========================================================================
    # def test0210_display_index(self):
    #     out_f = 'out.txt'
    #     err_f = 'err.txt'
    #     try:
    #         host, port = self._get_host('linux')
    #         r = main(host, 'root', 'root@testweb.*# $',
    #                  '--port', port,
    #                  '--password', 'r',
    #                  'ls',
    #                  '--display-index', 1,
    #                  '--outfile', out_f, '--errfile', err_f)
    #         self.assertTrue(r == 0)
    #         with open(out_f) as ifp:
    #             out = ifp.read()
    #             print(out)
    #             self.assertTrue(out.find('naswork') >= 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(out_f):
    #             os.remove(out_f)
    #         if os.path.exists(err_f):
    #             os.remove(err_f)
    #
    # # ==========================================================================
    # def test0220_display_index_multiple_command(self):
    #     out_f = 'out.txt'
    #     err_f = 'err.txt'
    #     try:
    #         host, port = self._get_host('linux')
    #         r = main(host, 'root', 'root@testweb.*# $',
    #                  '--port', port,
    #                  '--password', 'r',
    #                  'ls', 'echo "Hello world?"', 'df -h',
    #                  '--display-index', 2,
    #                  '--outfile', out_f, '--errfile', err_f)
    #         self.assertTrue(r == 0)
    #         with open(out_f) as ifp:
    #             out = ifp.read()
    #             print(out)
    #             self.assertTrue(out.find('Hello world?') >= 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(out_f):
    #             os.remove(out_f)
    #         if os.path.exists(err_f):
    #             os.remove(err_f)
    #
    # # ==========================================================================
    # def test0230_display_multiple_index_multiple_command(self):
    #     out_f = 'out.txt'
    #     err_f = 'err.txt'
    #     try:
    #         host, port = self._get_host('linux')
    #         r = main(host, 'root', 'root@testweb.*# $',
    #                  '--port', port,
    #                  '--password', 'r',
    #                  'ls', 'echo "Hello world?"', 'df -h',
    #                  '--display-index', 2, 3,
    #                  '--outfile', out_f, '--errfile', err_f)
    #         self.assertTrue(r == 0)
    #         with open(out_f) as ifp:
    #             out = ifp.read()
    #             print(out)
    #             self.assertTrue(out.find('Hello world?') >= 0
    #                             and out.find('Filesystem') > 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(out_f):
    #             os.remove(out_f)
    #         if os.path.exists(err_f):
    #             os.remove(err_f)

    # # ==========================================================================
    # def test0250_cisco_switch(self):
    #     out_f = 'out.txt'
    #     err_f = 'err.txt'
    #     try:
    #         host, port = self._get_host('sw3560')
    #         r = main(host, 'admin', '(Switch[>#]|Password: )$',
    #                  '--port', port,
    #                  '--password', 'r',
    #                  'enable', 'r',
    #                  'show interfaces GigabitEthernet 0/1 | include packets.*bytes',
    #                  'exit',
    #                  '--display-index', 3,
    #                  '--outfile', out_f, '--errfile', err_f)
    #         self.assertTrue(r == 0)
    #         with open(out_f) as ifp:
    #             out = ifp.read()
    #             print(out)
    #             self.assertTrue(out.find('packets') >= 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(out_f):
    #             os.remove(out_f)
    #         if os.path.exists(err_f):
    #             os.remove(err_f)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
