"""
====================================
 :mod:`argoslabs.filesystem.subfolder.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module monitor file system
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/07]
#     - 그룹에 "6-Files and Folders" 넣음
#  * [2020/12/10]
#     - 영준팀장의 요청으로 오류나는것 확인, 결과 없을 때 오류 문제
#  * [2020/10/06]
#     - 영준팀장의 요청으로 디폴트 출력에 target 폴더 이하만 출력하도록
#  * [2020/09/22]
#     - --depth-list, --basename, --exclude-empty
#  * [2020/09/08]
#     - change name 'Folder Structure'
#  * [2020/09/04]
#     - starting

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.filesystem.subfolder import _main as main
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
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

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
    def test0100_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('subf', '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                print(ifp.read())
            rr = []
            with open(stdout, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (7,))
                    rr.append(row)
            self.assertTrue(len(rr) == 8 and
                            rr[1][2].endswith('subbar')
                            and rr[-1][2].endswith('sub3foo'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0120_success_fullpath(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            subf = os.path.abspath('subf')
            r = main(subf, '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                print(ifp.read())
            rr = []
            with open(stdout, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (5, 7))
                    rr.append(row)
            self.assertTrue(len(rr) == 8 and
                            rr[1][2].endswith('subbar') and
                            rr[-1][2].endswith('sub3foo'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0130_success_basename(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            subf = os.path.abspath('subf')
            r = main(subf, '--basename',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                print(ifp.read())
            rr = []
            with open(stdout, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (5, 7))
                    rr.append(row)
            self.assertTrue(len(rr) == 8 and
                            rr[1][2] == 'subbar' and
                            rr[-1][2] == 'sub3foo')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0150_success_maxdepth(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('subf', '--max-depth', '1', '--basename',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                print(ifp.read())
            rr = []
            with open(stdout, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (5, 7))
                    rr.append(row)
            self.assertTrue(len(rr) == 3 and
                            rr[1][2] == 'subbar' and rr[-1][2] == 'subfoo')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0160_success_fullpath_exclude_empty(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            subf = os.path.abspath('subf')
            r = main(subf, '--exclude-empty',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                print(ifp.read())
            rr = []
            with open(stdout, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (5, 7))
                    rr.append(row)
            self.assertTrue(len(rr) == 8 and
                            rr[1][2].endswith('subbar') and
                            rr[-1][2].endswith('sub3foo'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0160_success_fullpath_depth_list(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            subf = os.path.abspath('subf')
            r = main(subf,
                     '--depth-list', '1',
                     '--depth-list', '3',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                print(ifp.read())
            rr = []
            with open(stdout, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (5, 7))
                    rr.append(row)
            self.assertTrue(len(rr) == 5 and
                            rr[1][2].endswith('subbar') and
                            rr[-1][2].endswith('sub3foo'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # # ==========================================================================
    # def test0170_success_fullpath_depth_list_all4one(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         subf = os.path.abspath(r'V:\tmp\2020.09.10 ARGOS')
    #         r = main(subf,
    #                  '--depth-list', '1',
    #                  '--depth-list', '4',
    #                  '--basename',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout, encoding='utf-8') as ifp:
    #             print(ifp.read())
    #         rr = []
    #         with open(stdout, encoding='utf-8') as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (5, 7))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) == 6 and
    #                         rr[1][2].endswith('subbar') and
    #                         rr[-1][2].endswith('sub3foo'))
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)

    # ==========================================================================
    def test0180_debug_ts(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            subf = r'W:\ARGOS-LABS\Bots\TS\2020.12.10\FolderStructure\2020.11.26 이채길2'
            r = main(subf,
                     '--depth-list', '4',
                     '--basename',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                print(ifp.read())
            rr = []
            with open(stdout, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (5, 7))
                    rr.append(row)
            self.assertTrue(len(rr) == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0190_success_sort(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        stdout = 'stdout.txt'
        try:
            r = main('subf', '--sort', '--ord-desc',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                print(ifp.read())
            rr = []
            with open(stdout, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (7,))
                    rr.append(row)
            self.assertTrue(len(rr) == 8 and
                            rr[-1][2].endswith('subbar')
                            and rr[1][2].endswith('sub3foo'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
