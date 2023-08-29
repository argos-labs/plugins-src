#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.string.re`
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
#  * [2021/11/22]
#     - --replace 문자열도 base64 인코딩 하도록 함, '-'로 시작하는 경우 패러미터 파싱오류 발생
#  * [2021/08/04]
#     - tolower, toupper from file
#  * [2021/07/05]
#     - "String to handle" 패러미터에 input_method='base64' 지정 및 디코딩
#  * [2021/06/15]
#     - 패턴 패러미터에 input_method='base64' 지정 및 디코딩
#  * [2021/04/09]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/11/15]
#     - Need to Check  "String Manipulation" RE is not the same to find folder
#       only from "C:\Users\satto3\Desktop\Temp\Plugin Test\foo.txt" with RE "^.+\\"
#  * [2020/11/04]
#     - --apply-first 옵션 추가
#  * [2019/10/25]
#     - --file-encoding 옵션 추가
#  * [2019/09/23]
#     - add 'substring' operations
#  * [2019/09/12]
#     - add 'tolower', 'toupper' operations
#  * [2019/09/11]
#     - one replace result padding '\n' remove
#  * [2019/05/22]
#     - modify display_name and help string for limit
#  * [2019/05/02]
#     - starting

################################################################################
import os
import sys
# import base64
# from alabs.common.util.vvargs import ArgsError
import alabs.common.util.vvargs
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.string.re import _main as main
from contextlib import contextmanager
from io import StringIO
from tempfile import gettempdir
from alabs.common.util.vvargs import vv_base64_encode, G_VV_DECODE_ERROR


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
    file = os.path.join(gettempdir(), 'argoslabs.string.re.file.txt')

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))
        if alabs.common.util.vvargs.G_VV_DECODE_ERROR:
            alabs.common.util.vvargs.G_VV_DECODE_ERROR = False

    # ==========================================================================
    def test0000_init(self):
        if os.path.exists(TU.file):
            os.remove(TU.file)
        with open(TU.file, 'w') as ofp:
            ofp.write('''hello tom and jerry
hello Tom tom and jerry Jerry
hello,|Tom , tom|and    jerry\tJerry
''')
        self.assertTrue(os.path.exists(TU.file))

    # ==========================================================================
    def test0100_invalid_operator(self):
        try:
            _ = main('unknown', 'tom', 'jerry')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_find(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('find',
                         vv_base64_encode(r'\w+'),
                         vv_base64_encode('hello tom and jerry'))
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(len(stdout.split('\n')) == 4)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0115_find_length(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('find',
                         vv_base64_encode(r'\w+'),
                         vv_base64_encode('hello tom and jerry'),
                         '--length')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout == '4')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0120_find_limit(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('find',
                         vv_base64_encode(r'\w+'),
                         vv_base64_encode('hello tom and jerry'),
                         '--limit', '3')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(len(stdout.split('\n')) == 3)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0130_find_with_or(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('find',
                         vv_base64_encode(r'(tom|jerry)'),
                         vv_base64_encode('hello Tom tom and jerry Jerry'))
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(len(stdout.split('\n')) == 2)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0140_find_with_or_ignorecase(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('find',
                         vv_base64_encode(r'(tom|jerry)'),
                         vv_base64_encode('hello Tom tom and jerry Jerry'),
                         '--ignore-case')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(len(stdout.split('\n')) == 4)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0150_split(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('split',
                         vv_base64_encode(r'[\s,|]+'),
                         vv_base64_encode('hello,|Tom , tom|and    jerry\tJerry'))
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(len(stdout.split('\n')) == 6)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0155_split_length(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('split',
                         vv_base64_encode(r'[\s,|]+'),
                         vv_base64_encode('hello,|Tom , tom|and    jerry\tJerry'),
                         '--length')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout == '6')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0160_split_with_limit(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('split',
                         vv_base64_encode(r'[\s,|]+'),
                         vv_base64_encode('hello,|Tom , tom|and    jerry\tJerry'),
                         '--limit', '3')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(len(stdout.split('\n')) == 3)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0170_replace(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('replace',
                         vv_base64_encode(r'[\s,|]+'),
                         vv_base64_encode('hello,|Tom , tom|and    jerry\tJerry'),
                         '--replace', vv_base64_encode(','))
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(stdout == 'hello,Tom,tom,and,jerry,Jerry')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0180_replace_limit(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('replace',
                         vv_base64_encode(r'[\s,|]+'),
                         vv_base64_encode('hello,|Tom , tom|and    jerry\tJerry'),
                         '--replace', vv_base64_encode(','), '--limit', '4')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(stdout == 'hello,Tom,tom,and,jerry\tJerry')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0190_replace_limit_without_replace(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('replace',
                         vv_base64_encode(r'[\s,|]+'),
                         vv_base64_encode('hello,|Tom , tom|and    jerry\tJerry'),
                         '--limit', '4')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(stdout == 'helloTomtomandjerry\tJerry')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0195_replace(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('replace',
                         vv_base64_encode(r','),
                         vv_base64_encode('a@b.c.d,b@c.d.e'),
                         '--replace', vv_base64_encode(', '))
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(stdout == 'a@b.c.d, b@c.d.e')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0200_find_from_file(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('find',
                         vv_base64_encode(r'\w+'),
                         '--file', TU.file)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(len(stdout.split('\n')) == 16)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0210_find_from_file_limit(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('find',
                         vv_base64_encode(r'\w+'),
                         '--file', TU.file,
                         '--limit', 10)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(len(stdout.split('\n')) == 10)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0220_replace_from_file(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('replace',
                         vv_base64_encode(r'tom'),
                         '--file', TU.file,
                         '--replace', vv_base64_encode('foo'),
                         '--ignore-case')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(stdout == 'hello foo and jerry\nhello foo foo and jerry Jerry\nhello,|foo , foo|and    jerry	Jerry')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0230_replace_from_file_limit(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('replace',
                         vv_base64_encode(r'tom'),
                         '--file', TU.file,
                         '--replace', vv_base64_encode('foo'),
                         '--ignore-case', '--limit', 4)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(stdout == 'hello foo and jerry\nhello foo foo and jerry Jerry\nhello,|foo , tom|and    jerry	Jerry')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0240_split_with_file(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('split',
                         vv_base64_encode(r'[\s,|]+'),
                         '--file', TU.file)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(len(stdout.split('\n')) == 16)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0250_split_with_file_limit(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('split',
                         vv_base64_encode(r'[\s,|]+'),
                         '--file', TU.file,
                         '--limit', 13)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(len(stdout.split('\n')) == 13)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0260_find_with_ignorecase(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('find',
                         vv_base64_encode('hel'),
                         vv_base64_encode('hello, Hello world hello Hello Hel'),)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print('%s' % '='*80)
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(len(stdout.split('\n')) == 2)

            with captured_output() as (out, err):
                r = main('find',
                         vv_base64_encode('hel'),
                         vv_base64_encode('hello, Hello world hello Hello Hel'),
                         '--ignore-case')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print('%s' % '='*80)
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(len(stdout.split('\n')) == 5)

        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0270_tolower_toupper(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('tolower',
                         vv_base64_encode(''),
                         vv_base64_encode('Hi Hello World?'),)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(stdout == 'hi hello world?')

            with captured_output() as (out, err):
                r = main('toupper',
                         vv_base64_encode(''),
                         vv_base64_encode('Hi Hello World?'),)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(stdout == 'HI HELLO WORLD?')

            with captured_output() as (out, err):
                r = main('toupper',
                         vv_base64_encode(''),
                         vv_base64_encode('jerry'),
                         '--apply-first')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(stdout == 'Jerry')

            with captured_output() as (out, err):
                r = main('tolower',
                         vv_base64_encode(''),
                         vv_base64_encode('JERRY'),
                         '--apply-first')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(stdout == 'jERRY')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0275_tolower_toupper_file(self):
        case_f = 'case_f.txt'
        stderr = None
        try:
            with open(case_f, 'w') as ofp:
                ofp.write('Hi Hello World?')
            with captured_output() as (out, err):
                r = main('tolower',
                         vv_base64_encode(''),
                         '--file', case_f)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(stdout == 'hi hello world?')

            with captured_output() as (out, err):
                r = main('toupper',
                         vv_base64_encode(''),
                         '--file', case_f)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(stdout == 'HI HELLO WORLD?')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0280_substring(self):
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('substring',
                         vv_base64_encode('Hello'),
                         vv_base64_encode('Hi Hello World?'),)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(stdout == '3')

            with captured_output() as (out, err):
                r = main('substring',
                         vv_base64_encode('hello'),
                         vv_base64_encode('Hi Hello World?'),)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(stdout == '-1')

            with captured_output() as (out, err):
                r = main('substring',
                         vv_base64_encode('hello'),
                         vv_base64_encode('Hi Hello World?'),
                         '--ignore-case')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            self.assertTrue(stdout == '3')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0290_replace_twobyte_character_01(self):
        stderr = None
        mbstr = 'おはようございます。本日は晴天なり。　ここにダブルバイトが入っています。「　」。'
        try:
            with captured_output() as (out, err):
                r = main('replace',
                         vv_base64_encode(r'[\s]'),
                         vv_base64_encode(mbstr),
                         '--replace', vv_base64_encode(' '))
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            print(len(mbstr.encode('utf-8')))
            print(len(stdout.encode('utf-8')))
            self.assertTrue(len(mbstr.encode('utf-8')) == len(stdout.encode('utf-8'))+4)
            sbstr = stdout

            with captured_output() as (out, err):
                r = main('replace',
                         vv_base64_encode(r'　'),
                         vv_base64_encode(mbstr),
                         '--replace', vv_base64_encode(' '))
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            print(len(mbstr.encode('utf-8')))
            print(len(stdout.encode('utf-8')))
            self.assertTrue(len(mbstr.encode('utf-8')) == len(stdout.encode('utf-8'))+4)

            with captured_output() as (out, err):
                r = main('replace',
                         vv_base64_encode(r'[ ]'),
                         vv_base64_encode(sbstr),
                         '--replace', vv_base64_encode('　'))
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            print(len(sbstr.encode('utf-8')))
            print(len(stdout.encode('utf-8')))
            self.assertTrue(len(sbstr.encode('utf-8'))+4 == len(stdout.encode('utf-8')))
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0300_replace_twobyte_character_01(self):
        stderr = None
        mbstr = 'おはようございます。本日は晴天なり。　ここにダブルバイトが入っています。「　」。'
        try:
            with captured_output() as (out, err):
                r = main('replace',
                         vv_base64_encode(r'。'),
                         vv_base64_encode(mbstr),
                         '--replace', vv_base64_encode('.'))
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            print(len(mbstr.encode('utf-8')))
            print(len(stdout.encode('utf-8')))
            self.assertTrue(len(mbstr.encode('utf-8')) == len(stdout.encode('utf-8'))+8)
            sbstr = stdout

            with captured_output() as (out, err):
                r = main('replace',
                         vv_base64_encode(r'[.]'),
                         vv_base64_encode(sbstr),
                         '--replace', vv_base64_encode('。'))
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            print(len(sbstr.encode('utf-8')))
            print(len(stdout.encode('utf-8')))
            self.assertTrue(len(sbstr.encode('utf-8'))+8 == len(stdout.encode('utf-8')))
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0310_replace_from_file(self):
        stderr = None
        stdout = 'stdout.txt'
        try:
            r = main('replace',
                     vv_base64_encode(r',__LINECHANGE__,'),
                     '--file', 'name.txt',
                     '--replace', vv_base64_encode('\n'),
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open('name.txt', encoding='utf-8') as ifp:
                in_s = ifp.read()
            with open(stdout, encoding='utf-8') as ifp:
                out_s = ifp.read()
            self.assertTrue(in_s.replace(r',__LINECHANGE__,', '\n') == out_s)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0320_replace_from_file(self):
        stderr = None
        stdout = 'stdout.txt'
        try:
            r = main('replace',
                     vv_base64_encode(r'[\n\r]+'),
                     '--file', 'stringsample.txt',
                     '--replace', vv_base64_encode(' '),
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                out_s = ifp.read()
                # print(out_s)
                self.assertTrue(out_s == '九 時 運転 開始 十 時 現場 到着 十 一 時 作業 開始 ')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0330_replace_shige(self):
        stderr = None
        stdout = 'stdout.txt'
        ss_txt = 'ss.txt'
        with open(ss_txt, 'w') as ofp:
            ofp.write('''May 18, 2020
March 14, 2018
August 18, 2014
January 14, 2009
August 5, 2020
July 20, 2020''')
        try:
            r = main('replace',
                     vv_base64_encode(r'^(.*)$'),
                     '--file', ss_txt,
                     '--replace', vv_base64_encode(r'"\1"'),
                     '--multiline',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                out_s = ifp.read()
                # print(out_s)
                self.assertTrue(out_s[0] == out_s[-1] == '"')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0340_replace_rooman(self):
        stderr = None
        stdout = 'stdout.txt'
        ss_txt = 'String.txt'
        try:
            r = main('replace',
                     vv_base64_encode(r'\"?\\r\\n\s+\"?'),
                     '--file', ss_txt,
                     '--replace', vv_base64_encode(r''),
                     '--multiline',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                out_s = ifp.read()
                # print(out_s)
                self.assertTrue(out_s == 'Consultation / Evaluation and Management')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0350_debug_path(self):
        stderr = None
        stdout = 'stdout.txt'
        ss_txt = 'String.txt'
        try:
            r = main('find',
                     vv_base64_encode('^.+\\\\'),
                     vv_base64_encode(r'C:\Users\satto3\Desktop\Temp\Plugin Test\foo.txt'),
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                out_s = ifp.read()
                # print(out_s)
                self.assertTrue(out_s == 'C:\\Users\\satto3\\Desktop\\Temp\\Plugin Test\\')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0360_debug_svg_alex(self):
        stderr = None
        stdout = 'TESTDashboard-EE-Inventory-Combined.txt'
        ss_txt = 'TESTDashboard-EE-Inventory-Combined.svg'
        try:
            r = main('replace',
                     vv_base64_encode('<(path)\s'),
                     '--file', ss_txt,
                     '--replace', vv_base64_encode(r'<my_\1 '),
                     '--multiline',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                out_s = ifp.read()
                # print(out_s)
                self.assertTrue(out_s.find('my_path') > 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0370_debug_shige(self):
        stderr = None
        stdout = 'regex101-StringManipAdapter4.out'
        ss_txt = 'regex101-StringManipAdapter4.txt'
        try:
            r = main('find',
                     #r'<table class=\".+\">',
                     #r'<table class=".+">',
                     #r'<table class=\"[^"]+\">',
                     vv_base64_encode(r'<table class="[^"]+">'),
                     '--file', ss_txt,
                     '--multiline',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                out_s = ifp.read()
                # print(out_s)
                self.assertTrue(out_s.startswith('<table class="'))
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0380_debug_venkatesh(self):
        stderr = None
        stdout = 'stdout.out'
        try:
            r = main('find',
                     vv_base64_encode(r'\"[A-Z][a-z][a-z][a-z][a-z][a-z]-[a-z][a-z][0-9][a-z][a-z]\"'),
                     vv_base64_encode('"90 min video tutorial "Rocket-st1rt""'),
                     # '--multiline',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                out_s = ifp.read()
                # print(out_s)
                self.assertTrue(out_s == '"Rocket-st1rt"')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0390_debug_shige(self):
        stderr = None
        stdout = 'stdout.out'
        try:
            r = main('find',
                     # r'users\\',
                     # r'C:\users\argos\\',
                     vv_base64_encode(r'c'),
                     vv_base64_encode(r'c\\'),
                     # '--multiline',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                out_s = ifp.read()
                # print(out_s)
                self.assertTrue(out_s == 'c')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0400_debug_shige_find_group(self):
        stderr = None
        stdout = 'stdout.out'
        try:
            r = main('find',
                     vv_base64_encode(r'https://www\.linkedin\.com/in/[-a-z0-9]+\?miniProfileUrn&#61'),
                     '--file', 'find-group-shige-20210716.txt',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                out_s = ifp.read()
                print(out_s)
                self.assertTrue(out_s.find('marioharik') >= 0)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0410_find_without_base64_encode_ok(self):
        # 알파벳,숫자,+,/,=(마지막) 로만 이루어지지 않으면 일반 문자열로 간주
        stderr = None
        try:
            with captured_output() as (out, err):
                r = main('find',
                         r'\w+',
                         'hello tom and jerry')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            if stdout:
                print(stdout)
            stderr = err.getvalue().strip()
            if stderr:
                sys.stderr.write('%s%s' % (stderr, os.linesep))
            self.assertTrue(len(stdout.split('\n')) == 4)

            with captured_output() as (out, err):
                r = main('split',
                         r'[\s,|]+',
                         'hello,|Tom , tom|and    jerry\tJerry',
                         '--length')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout == '6')

        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0420_debug_shige_replace_newline(self):
        stderr = None
        stdout = 'stdout.out'
        try:
            r = main('replace',
                     # vv_base64_encode(r'\n'),
                     # vv_base64_encode('\n'),
                     vv_base64_encode(r'\n'),
                     '--file', 'shige-test03.txt',
                     '--replace', vv_base64_encode(' '),
                     # '--multiline',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                out_s = ifp.read()
                print(out_s)
                self.assertTrue(out_s =='Summary of Services Date Attorney Services Matter Amount 06/28/21 Andy Han Prepare claims for divisional application SEUR-00304CN $1,200')
# 'Summary of ServicesIA==Date Attorney Services Matter AmountIA==06/28/21 Andy Han Prepare claims for divisional application SEUR-00304CN $1,200'
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test0430_debug_shige_replace_filepath(self):
        # "replace" "XC5jc3Y=" "QzpcVXNlcnNcc2F0bzNcRGVza3RvcFxjaW5uYWJhci5jc3Y=" "--replace"  "-2.csv"
        stderr = None
        stdout = 'stdout.out'
        try:
            r = main('replace',
                     "XC5jc3Y=",
                     "QzpcVXNlcnNcc2F0bzNcRGVza3RvcFxjaW5uYWJhci5jc3Y=",
                     "--replace", vv_base64_encode("-2.csv"),
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                out_s = ifp.read()
                print(out_s)
                self.assertTrue(out_s == r'C:\Users\sato3\Desktop\cinnabar-2.csv')
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            if stderr:
                sys.stderr.write(stderr)
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        if os.path.exists(TU.file):
            os.remove(TU.file)
        self.assertTrue(not os.path.exists(TU.file))
