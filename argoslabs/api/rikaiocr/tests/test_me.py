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
from argoslabs.api.rikaiocr import _main as main
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
            r = main('df0e1377caa04ec0b4',
                     '133e4c2327e849999736',
                     'imgs/01-Simple-Invoice.pdf',
                     'What is the invoice number?',
                     "What is the date of this invoice?",
                     '--json-file', 'imgs/01-Simple-Invoice.json',
                     '--yaml-file', 'imgs/01-Simple-Invoice.yaml',
                     )
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists('imgs/01-Simple-Invoice.json'))
            self.assertTrue(os.path.exists('imgs/01-Simple-Invoice.yaml'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
