#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.string.basicstring`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Kyobong An
#
# Change Log
# --------
#
#  * [2021/10/12]
#     - starting

################################################################################
import os
import sys
# from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.string.basicstring import _main as main
from contextlib import contextmanager
from io import StringIO
from tempfile import gettempdir
from alabs.common.util.vvargs import vv_base64_encode


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
    file = os.path.join(gettempdir(), 'argoslabs.string.basicstring.tests.stdin.txt')

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0001_boolean_isalnum(self):
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test1234'),
                     '--boolean', 'isalnum',
                     # '--str1',vv_base64_encode('test'),
                     # '--str2',vv_base64_encode('test'),
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    # def test0002_boolean_isalpha(self):
    #     stderr = None
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main(vv_base64_encode('test'),
    #                  '--boolean', 'isalpha',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('%s\n' % str(e))
    #         self.assertTrue(False)
    def test0002_boolean_isalpha(self):
        stderr = None
        stdout = 'stdout.txt'
        r = main('--string', vv_base64_encode('test'),
                 '--boolean', 'isalpha',
                 # '--outfile', stdout
                 )
        self.assertTrue(r == 0)

    def test0002_boolean_isalpha_false(self):
        stderr = None
        stdout = 'stdout.txt'
        r = main('--string', vv_base64_encode(r'test1'),
                 '--boolean', 'isalpha',
                 '--outfile', stdout)
        self.assertTrue(r == 1)

    # ==========================================================================
    def test0003_boolean_isascii(self):
        stdin = 'stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test1234!@#$'),
                     '--boolean', 'isascii',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    # def test0004_boolean_isascii_file(self):
    #     stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main(
    #                  '--boolean', 'isascii',
    #                  '--file-path', stdin,
    #                  # '--outfile', stdout
    #                  )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0005_boolean_isdecemal(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('1234'),
                     '--boolean', 'isdecimal',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0006_boolean_isdigit(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('12343²'),
                     '--boolean', 'isdigit',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0007_boolean_islower(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test'),
                     '--boolean', 'islower',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0008_boolean_isnumeric(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('½3²'),
                     '--boolean', 'isnumeric',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0009_boolean_isspace(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('          '),
                     '--boolean', 'isspace',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0010_boolean_istitle(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('Test Is Good.'),
                     '--boolean', 'istitle',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0011_boolean_isupper(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('TEST IS GOOD.!'),
                     '--boolean', 'isupper',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0101_convert_capitalize(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test is good!'),
                     '--convert', 'capitalize'
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0102_convert_lower(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('TEST IS GOOD!'),
                     '--convert', 'lower'
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0103_convert_replace(self):
        stderr = None
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('tests is isisisis good!'),
                     '--convert', 'replace',
                     '--str1', vv_base64_encode('is'),
                     '--str2', vv_base64_encode('are'),
                     '--int1', '2',    # -1은 전부를 0은 바꾸지않음 1은 왼쪽-> 오른쪽
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0104_convert_swapcase(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('Test is Good!'),
                     '--convert', 'swapcase',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0105_convert_title(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test is good!'),
                     '--convert', 'capitalize',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0106_convert_upper(self):
        stderr = None
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test is good!'),
                     '--convert', 'upper',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0201_fill_center(self):
        stderr = None
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test is good!'),
                     '--fill', 'center',
                     '--int1', '20',
                     '--chr', ' ',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0202_fill_ljust(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test'),
                     '--fill', 'ljust',
                     '--int1', '10',
                     '--chr', '#',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0203_fill_rjust(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test'),
                     '--fill', 'rjust',
                     '--int1', '10',
                     '--chr', '-',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0204_fill_zfill(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test'),
                     '--fill', 'zfill',
                     '--int1', '10',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0301_find_count(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test is good!!!'),
                     '--find', 'count',
                     '--str1', vv_base64_encode('t'),
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0302_find_find(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test is good!!!'),
                     '--find', 'find',
                     '--str1', vv_base64_encode('g'),
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0303_find_index(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test is good!!!'),
                     '--find', 'index',
                     '--str1', vv_base64_encode('g'),
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0304_find_rfind(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test is good!!!'),
                     '--find', 'rfind',
                     '--str1', vv_base64_encode('t'),
                     '--int1', '0',
                     '--int2', '10',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0305_find_rindex(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test is good!!!'),
                     '--find', 'rindex',
                     '--str1', vv_base64_encode('g'),
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0401_join_join(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('sep'),
                     '--join', 'join',
                     '--list', 'test1',
                     '--list', 'test2',
                     '--list', 'test3',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0501_split_expandtabs(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        r = main('--string',
                 vv_base64_encode('a\tb\tc\t1\t2\t!\t@'),
                 '--split', 'expandtabs',
                 '--int1', '5',
                 # '--outfile', stdout
                 )
        self.assertTrue(r == 0)

    # ==========================================================================
    def test0502_split_partition(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test is good!!'),
                     '--split', 'partition',
                     '--str1', vv_base64_encode(' '),
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0503_split_rpartition(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test is good!!'),
                     '--split', 'rpartition',
                     '--str1', vv_base64_encode(' '),
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0504_split_rsplit(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test is good!!'),
                     '--split', 'rsplit',
                     '--str1', vv_base64_encode(' '),
                     '--int1', '-1',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0505_split_split(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('test is good!!'),
                     '--split', 'split',
                     '--str1', vv_base64_encode(' '),
                     '--int1', '2',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    # def test0506_split_splitlines(self):
    #     stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('--file-path', stdin,
    #                  # '--file-path', stdin,
    #                  '--split', 'splitlines',
    #                  # '--sub-boolean', 'True'
    #                  # '--sub-boolean', 'False'
    #                  # '--outfile', stdout
    #                  )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0601_strip_lstrip(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('   test   '),
                     # '--file-path', stdin,
                     '--strip', 'lstrip',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0602_strip_rstrip(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('   test   '),
                     # '--file-path', stdin,
                     '--strip', 'rstrip',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0603_strip_strip(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('   test   '),
                     # '--file-path', stdin,
                     '--strip', 'strip',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0701_swith_endswith(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('http://www.naver.com'),
                     # '--file-path', stdin,
                     '--swith', 'endswith',
                     '--str1', vv_base64_encode('.com'),
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0702_swith_endswith_tuple(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('http://www.naver.com'),
                     # '--file-path', stdin,
                     '--swith', 'endswith',
                     '--list', '.co.kr',
                     '--list', '.net',
                     '--list', '.com',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0703_swith_startswith(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('http://www.naver.com'),
                     # '--file-path', stdin,
                     '--swith', 'startswith',
                     '--str1', 'http',
                     # '--int1', '0',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0800_slice(self):
        stdin = r'C:\plugins\argoslabs\string\basicstring\tests\stdin.txt'
        stdout = 'stdout.txt'
        try:
            r = main('--string', vv_base64_encode('http://www.naver.com'),
                     # '--file-path', stdin,
                     # '--slice', '3',
                     '--slice', ':6',
                     # '--outfile', stdout
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        if os.path.exists(TU.file):
            os.remove(TU.file)
        self.assertTrue(not os.path.exists(TU.file))
