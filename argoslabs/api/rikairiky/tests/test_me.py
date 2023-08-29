"""
====================================
 :mod:`argoslabs.api.easyocr.tests.test_me`
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
#  * [2021/03/25]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/12/25]
#     - 기존 httpie를 이용한 argoslabs.api.rest 에 제한이 있을 수 있어 requests를
#       바로 이용하도록 함

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.api.rikairiky import _main as main
# from alabs.common.util.vvencoding import get_file_encoding
from alabs.common.util.vvtest import captured_output
from io import StringIO


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    # cwd = os.getcwd()

    # ==========================================================================
    def setUp(self) -> None:
        cwd = os.path.dirname(os.path.abspath(__file__))
        os.chdir(cwd)

    # ==========================================================================
    def test0000_init(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        self.assertTrue(os.path.abspath(os.getcwd()) == cwd)

    # ==========================================================================
    def test0110_simple_folder(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('--0e1377caa04ec0--',
                     '--3e4c2327e8499997--',
                     '--tYbTdAfFqo8tAxHo--',
                     'imgs/ko-screenshot-01.png',
                     '이 문서의 제목은?',
                     "API 키는?",
                     '--json-file', 'imgs/ko-screenshot-01.json',
                     '--yaml-file', 'imgs/ko-screenshot-01.yaml',
                     )
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists('imgs/ko-screenshot-01.json'))
            self.assertTrue(os.path.exists('imgs/ko-screenshot-01.yaml'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_korean_questions(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('--0e1377caa04ec0--',
                     '--3e4c2327e8499997--',
                     '--tYbTdAfFqo8tAxHo--',
                     'imgs/약제비.pdf',
                     '이 문서는 무엇입니까?',
                     "주민등록번호는?",
                     '--json-file', 'imgs/약제비.json',
                     '--yaml-file', 'imgs/약제비.yaml',
                     )
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists('imgs/약제비.json'))
            self.assertTrue(os.path.exists('imgs/약제비.yaml'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_riky_file(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('--0e1377caa04ec0--',
                     '--3e4c2327e8499997--',
                     '--tYbTdAfFqo8tAxHo--',
                     'Marubeni_SKM_C65823040615130_3.pdf',
                     # [table]No 1の品名は？
                     # [table]No 1の数量は？
                     '--question-file', 'marubeni foods questions 01.txt',
                     '--json-file', 'imgs/약제비.json',
                     '--yaml-file', 'imgs/약제비.yaml',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_riky_without_file(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('--0e1377caa04ec0--',
                     '--3e4c2327e8499997--',
                     '--tYbTdAfFqo8tAxHo--',
                     'Marubeni_SKM_C65823040615130_3.pdf',
                     # "[table]No 1の品名は？",
                     # "[table]No 1の数量は？",
#                     '--question-file', 'marubeni foods questions 01.txt',
                     '--json-file', 'imgs/약제비.json',
                     '--yaml-file', 'imgs/약제비.yaml',
                     )
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_riky_return_ocr(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('--0e1377caa04ec0--',
                     '--3e4c2327e8499997--',
                     '--tYbTdAfFqo8tAxHo--',
                     'Marubeni_SKM_C65823040615130_3.pdf',
                     # "[table]No 1の品名は？",
                     # "[table]No 1の数量は？",
                     #                     '--question-file', 'marubeni foods questions 01.txt',
                     # '--return-ocr',  # 이 옵션 없이도 동작하도록 함
                     '--json-file', 'imgs/약제비.json',
                     '--yaml-file', 'imgs/약제비.yaml',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
