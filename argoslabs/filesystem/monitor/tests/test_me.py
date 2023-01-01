#!/usr/bin/env python
# coding=utf8
"""
====================================
:mod:`argoslabs.filesystem.monitor`
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
#  * [2022/08/12]
#     - 윈도우에서 폴더이름에 [] 대괄호 있으면 안되는 문제 [허상민]
#  * [2021/04/07]
#     - 그룹에 "6-Files and Folders" 넣음
#  * [2020/11/19]
#     - default 필터를 *.txt 에서 *.* 으로
#  * [2020/11/18]
#     - Irene이 데모할 때 매 빈줄이 추가되는것 수정
#  * [2020/11/18]
#     - Irene이 데모할 때 매 빈줄이 추가되는것 수정
#  * [2020/11/15]
#     - File Monitor ==> Folder Monitor
#  * [2020/09/01]
#     - 매칭되는 csv 결과가 없을 때는 기존 멈춤 대신 헤더만 출력하도록
#     - csv_out이 False이고 basename이 True인 경우에는 이를 False로 수정
#  * [2020/08/24]
#     - --order-by, --desc 옵션 추가
#     - 모니터링에서 해당 폴더가 아예 없으면 오류가 나오는데 이를 0 으로 나오게
#  * [2020/04/13]
#     - Make sure the label os "--csv-out" : "Details in CSV" and show_default
#     - in case of "--basename": set "--csv-out"
#     - "--basename"의 레이블을 "File name only"로 변경
#  * [2019/04/25]
#     - default result is # of files, --
#  * [2019/04/08]
#     - add --basename option
#  * [2019/04/04]
#     - starting

################################################################################
import os
import sys
import csv
import shutil
import tempfile
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.filesystem.monitor import _main as main
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
# noinspection PyUnresolvedReferences
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_empty(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_mkdtemp(self):
        TU.td1 = tempfile.mkdtemp('mon_dir')
        self.assertTrue(os.path.exists(TU.td1))
        TU.td2 = tempfile.mkdtemp('mon_dir')
        self.assertTrue(os.path.exists(TU.td2))
        TU.td3 = tempfile.mkdtemp('mon_dir')
        self.assertTrue(os.path.exists(TU.td3))

    # ==========================================================================
    def test0030_mk_file(self):
        foo = os.path.join(TU.td1, 'foo.txt')
        with open(foo, 'w') as ofp:
            ofp.write('This is foo')
        self.assertTrue(os.path.exists(foo))
        bar = os.path.join(TU.td1, 'bar.txt')
        with open(bar, 'w') as ofp:
            ofp.write('This is bar bar')
        self.assertTrue(os.path.exists(bar))
        foo = os.path.join(TU.td2, 'foo.log')
        with open(foo, 'w') as ofp:
            ofp.write('Log for foo')
        self.assertTrue(os.path.exists(foo))
        bar = os.path.join(TU.td2, 'bar.log')
        with open(bar, 'w') as ofp:
            ofp.write('Log for bar bar')
        self.assertTrue(os.path.exists(bar))

    # ==========================================================================
    def test0040_mk_dir_file(self):
        foo = os.path.join(TU.td1, 'foo')
        os.makedirs(foo)
        self.assertTrue(os.path.isdir(foo))
        foo = os.path.join(foo, 'foo.txt')
        with open(foo, 'w') as ofp:
            ofp.write('This is foo')
        self.assertTrue(os.path.exists(foo))
        bar = os.path.join(TU.td2, 'bar')
        os.makedirs(bar)
        self.assertTrue(os.path.isdir(bar))
        bar = os.path.join(bar, 'bar.txt')
        with open(bar, 'w') as ofp:
            ofp.write('This is bar bar')
        self.assertTrue(os.path.exists(bar))

    # ==========================================================================
    def test0100_success(self):
        try:
            with captured_output() as (out, err):
                r = main(TU.td1)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout == '2')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0105_success_with_csv_out(self):
        try:
            with captured_output() as (out, err):
                r = main(TU.td1, '--csv-out')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout.find('foo.txt",11') > 0)

            with captured_output() as (out, err):
                r = main(TU.td1, '--csv-out', '--filter', '*.txt')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout.find('foo.txt",11') > 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success_with_multi(self):
        try:
            with captured_output() as (out, err):
                r = main(TU.td1, TU.td2)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout == '4')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_success_with_multi_filter(self):
        try:
            with captured_output() as (out, err):
                r = main(TU.td1, TU.td2, '--filter', '*.txt', '--filter', '*.log')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout == '4')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_success_with_multi_filter_recursive(self):
        try:
            with captured_output() as (out, err):
                r = main(TU.td1, TU.td2, '--filter', '*.txt', '--filter', '*.log', '-r')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout == '6')
        except TimeoutError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0135_success_with_multi_filter_recursive_basename(self):
        try:
            # --basename 만 지정하고 --csv-out을 지정안하면 무시하도록 수정
            with captured_output() as (out, err):
                r = main(TU.td1, TU.td2, '--filter', '*.txt', '--filter', '*.log',
                        '-r', '--basename')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            # self.assertTrue(len(stdout.split('\n')) == 7)
            self.assertTrue(stdout == '6')
        except TimeoutError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_failure_timeout(self):
        try:
            with captured_output() as (out, err):
                r = main(TU.td1, TU.td2, '--filter', '*.na', '--timeout', '3', '-r')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout == '0')
        except TimeoutError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0150_success_with_multi_filter_recursive_move(self):
        try:
            with captured_output() as (out, err):
                r = main(TU.td1, TU.td2, '--filter', '*.txt', '--filter', '*.log',
                        '-r', '--move', TU.td3)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout == '4')
        except TimeoutError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_folder_monitor(self):
        try:
            with captured_output() as (out, err):
                r = main(TU.td1, TU.td2, '--filter', '*.xyz')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout == '0')
        except TimeoutError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_success_with_alpha_ascending(self):
        try:
            with captured_output() as (out, err):
                r = main(
                        TU.td3, '--csv-out',
                        '--order-by', 'Filename',
                        )
            self.assertTrue(r == 0)
            rr = list()
            stdout = out.getvalue().strip()
            outsio = StringIO(stdout)
            cr = csv.reader(outsio)
            for row in cr:
                self.assertTrue(len(row) in (3,))
                rr.append(row)
            self.assertTrue(len(rr) in (5,) and rr[-1][1].endswith('foo.txt'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0180_success_with_alpha_descending(self):
        try:
            with captured_output() as (out, err):
                r = main(
                        TU.td3, '--csv-out',
                        '--order-by', 'Filename',
                        '--desc',
                        )
            self.assertTrue(r == 0)
            rr = list()
            stdout = out.getvalue().strip()
            outsio = StringIO(stdout)
            cr = csv.reader(outsio)
            for row in cr:
                self.assertTrue(len(row) in (3,))
                rr.append(row)
            self.assertTrue(len(rr) in (5,) and rr[-1][1].endswith('bar.log'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0190_success_with_size_ascending(self):
        try:
            with captured_output() as (out, err):
                r = main(
                        TU.td3, '--csv-out',
                        '--order-by', 'Size',
                        # '--desc',
                        )
            self.assertTrue(r == 0)
            rr = list()
            stdout = out.getvalue().strip()
            outsio = StringIO(stdout)
            cr = csv.reader(outsio)
            for row in cr:
                self.assertTrue(len(row) in (3,))
                rr.append(row)
            self.assertTrue(len(rr) in (5,) and int(rr[-1][-1]) == 15)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_success_with_size_ascending(self):
        try:
            with captured_output() as (out, err):
                r = main(
                        TU.td3, '--csv-out',
                        '--order-by', 'Size',
                        '--desc',
                        )
            self.assertTrue(r == 0)
            rr = list()
            stdout = out.getvalue().strip()
            outsio = StringIO(stdout)
            cr = csv.reader(outsio)
            for row in cr:
                self.assertTrue(len(row) in (3,))
                rr.append(row)
            self.assertTrue(len(rr) in (5,) and int(rr[-1][-1]) == 11)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_success_with_mtime_ascending(self):
        try:
            with captured_output() as (out, err):
                r = main(
                        TU.td3, '--csv-out',
                        '--order-by', 'Modify Time',
                        # '--desc',
                        )
            self.assertTrue(r == 0)
            rr = list()
            stdout = out.getvalue().strip()
            outsio = StringIO(stdout)
            cr = csv.reader(outsio)
            for row in cr:
                self.assertTrue(len(row) in (3,))
                rr.append(row)
            self.assertTrue(len(rr) in (5,) and int(rr[-1][-1]) in (11, 15))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_success_with_mtime_descending(self):
        try:
            with captured_output() as (out, err):
                r = main(
                        TU.td3, '--csv-out',
                        '--order-by', 'Modify Time',
                        '--desc',
                        )
            self.assertTrue(r == 0)
            rr = list()
            stdout = out.getvalue().strip()
            outsio = StringIO(stdout)
            cr = csv.reader(outsio)
            for row in cr:
                self.assertTrue(len(row) in (3,))
                rr.append(row)
            self.assertTrue(len(rr) in (5,) and int(rr[-1][-1]) == 11)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # 모니터링에서 해당 폴더가 아예 없으면 오류가 나오는데 이를 0 으로 나오게
    # ==========================================================================
    def test0230_invalid_folder_monitor(self):
        try:
            ivf = os.path.join(tempfile.gettempdir(), 'doesnotexistsfolder')
            with captured_output() as (out, err):
                r = main(ivf)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout == '0')
            # --csv-out 인 경우 여전히 오류 나오게 함
            # with captured_output() as (out, err):
            #     r = main(ivf, '--csv-out')
            # self.assertTrue(r == 0)
            # stdout = out.getvalue().strip()
            # self.assertTrue(stdout == '0')
        except TimeoutError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0240_debug_branket(self):
        try:
            TU.td1 = tempfile.mkdtemp('[mon_dir]')
            self.assertTrue(os.path.exists(TU.td1))
            self.assertTrue(True)
            foo = os.path.join(TU.td1, 'foo.txt')
            with open(foo, 'w') as ofp:
                ofp.write('This is foo')
            self.assertTrue(os.path.exists(foo))
            bar = os.path.join(TU.td1, 'bar.txt')
            with open(bar, 'w') as ofp:
                ofp.write('This is bar bar')
            self.assertTrue(os.path.exists(bar))
            with captured_output() as (out, err):
                r = main(TU.td1)
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            self.assertTrue(stdout == '2')
        except TimeoutError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(TU.td1):
                shutil.rmtree(TU.td1)

    # ==========================================================================
    def test9000_clear(self):
        if os.path.exists(TU.td1):
            shutil.rmtree(TU.td1)
        self.assertFalse(os.path.exists(TU.td1))
        if os.path.exists(TU.td2):
            shutil.rmtree(TU.td2)
        self.assertFalse(os.path.exists(TU.td2))
        if os.path.exists(TU.td3):
            shutil.rmtree(TU.td3)
        self.assertFalse(os.path.exists(TU.td3))

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
