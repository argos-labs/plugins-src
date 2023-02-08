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
from argoslabs.api.easyocr import _main as main
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
    def test0100_one_file(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('ee1af14b249fbb5df0380cf967b8bf3d', 'testimgs/foobar.png')
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists('testimgs/foobar.txt'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_simple_folder(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('ee1af14b249fbb5df0380cf967b8bf3d', 'testimgs')
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists('testimgs/foo.yml'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_folder_35_imgs(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main('ee1af14b249fbb5df0380cf967b8bf3d', 'imgs')
            self.assertTrue(r == 0)
            rl = []
            # print(out.getvalue())
            stdout = StringIO(out.getvalue())
            cr = csv.reader(stdout)
            for row in cr:
                rl.append(row)
            self.assertTrue(rl[-1][0] == '35')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_one_file(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('ee1af14b249fbb5df0380cf967b8bf3d', 'testimgs/foobar.png',
                     '--url', 'https://router.vivans.net:23443/')
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists('testimgs/foobar.txt'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_simple_folder(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('ee1af14b249fbb5df0380cf967b8bf3d', 'testimgs',
                     '--url', 'https://router.vivans.net:23443/')
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists('testimgs/foo.yml'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_folder_35_imgs(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main('ee1af14b249fbb5df0380cf967b8bf3d', 'imgs',
                         '--url', 'https://router.vivans.net:23443/')
            self.assertTrue(r == 0)
            rl = []
            # print(out.getvalue())
            stdout = StringIO(out.getvalue())
            cr = csv.reader(stdout)
            for row in cr:
                rl.append(row)
            self.assertTrue(rl[-1][0] == '35')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
