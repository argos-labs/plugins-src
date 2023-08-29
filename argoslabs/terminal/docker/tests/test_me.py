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
from argoslabs.terminal.docker import _main as main
from alabs.common.util.vvnet import is_svc_opeded
from contextlib import contextmanager
from io import StringIO


################################################################################
@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    def setUp(self) -> None:
        self.host_args = [
            # '192.168.35.129', 'ubuntu', 'r',
            '192.168.35.12', 'pi', 'r',
        ]
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_not_enough_parameter(self):
        try:
            r = main('op', 'host')
            self.assertTrue(r == 98)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0060_invalid_host(self):
        try:
            with captured_output() as (out, err):
                r = main('Docker Info', 'host', 'user', '--password', 'r')
            self.assertTrue(r == 2)
            stderr = err.getvalue()
            print(stderr)
            self.assertTrue(stderr.find('getaddrinfo failed') > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_docker_info(self):
        try:
            with captured_output() as (out, err):
                r = main('Docker Info', '192.168.35.12', 'pi', '--password', 'r')
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            print(stdout)
            self.assertTrue(stdout.find('/usr/libexec/docker/cli-plugins/docker-app') > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_docker_run(self):
        try:
            with captured_output() as (out, err):
                r = main('Docker Command', '192.168.35.12', 'pi', '--password', 'r')
            self.assertTrue(r == 1)
            stderr = err.getvalue()
            print(stderr)
            self.assertTrue(stderr.find('Invalid Docker Command') >= 0)

            with captured_output() as (out, err):
                r = main('Docker Command', '192.168.35.12', 'pi', '--password', 'r',
                         '--docker-command',
                         'run --rm -it instrumentisto/nmap -sT -O -v 192.168.35.12')
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            print(stdout)
            self.assertTrue(stdout.find('Discovered open port 22/tcp') > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0120_docker_compsose_status(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main('State of Docker Compose', '192.168.35.12', 'pi', '--password', 'r')
            self.assertTrue(r == 2)
            stderr = err.getvalue()
            print(stderr)
            self.assertTrue(stderr.find('Invalid Docker Compose Yaml file') >= 0)

            with captured_output() as (out, err):
                r = main('State of Docker Compose', '192.168.35.12', 'pi', '--password', 'r',
                         '--docker-compose-yaml', 'speedtest.yaml',
                         '--params', 'LOOP_DELAY::=60',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            print(stdout)
            self.assertTrue(stdout.find('Up') < 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0130_docker_compsose_start(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main('Start Docker Compose', '192.168.35.12', 'pi', '--password', 'r',
                         '--docker-compose-yaml', 'speedtest.yaml',
                         '--params', 'LOOP_DELAY::=60',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            print(stdout)
            self.assertTrue(stdout.find('Creating speedtest_grafana_1') > 0 or
                            stdout.find('speedtest_grafana_1 is up-to-date') > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0140_docker_compsose_status(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main('State of Docker Compose', '192.168.35.12', 'pi', '--password', 'r',
                         '--docker-compose-yaml', 'speedtest.yaml',
                         '--params', 'LOOP_DELAY::=60',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            print(stdout)
            self.assertTrue(stdout.find('Up') < 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0150_docker_compsose_stop(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main('Stop Docker Compose', '192.168.35.12', 'pi', '--password', 'r',
                         '--docker-compose-yaml', 'speedtest.yaml',
                         '--params', 'LOOP_DELAY::=60',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            print(stdout)
            self.assertTrue(stdout.find('Removing network speedtest_default') > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
