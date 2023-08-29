#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.filesystem.op`
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
#  * [2021/04/08]
#     - 그룹에 "6-Files and Folders" 넣음
#  * [2021/02/17]
#     - create 때 이미 있으면 (1) 번호 붙이던가 overwirte 체크면 덮어쓰기
#     - already exists 문구 삭제
#  * [2020/12/17]
#     - copy 시 Target 파일 경로를 출력하도록 수정
#  * [2020/11/12]
#     - create 시 생성한 파일 경로를 출력하도록 수정
#  * [2020/08/26]
#     - 없는 파일/폴더를 삭제할 때 예외 말고 .. 리턴
#     - 있는 파일/폴더를 생성하려고 할 때 예외 말고 .. 리턴
#  * [2020/04/29]
#     - 기존 os.walk 대신 glob.glob로 변경
#     - --recursive 욥션 추가
#  * [2020/04/23]
#     - foo/*.txt 를 bar 폴더에 옮기는데 foo 자체가 지워지는 문제 밸생 문제
#  * [2020/04/21]
#     - 경우에 따라 결과에 계속해서 복사하는 문제 해결
#  * [2019/10/29]
#     - move 또는 remove 에서 와일드카드 작동하도록
#  * [2019/06/20]
#     - 와일드카드 추가
#     - 이동/복사 시 동일 이름의 target이 존재하면 (1), (2) ... 등을 붙임
#  * [2019/05/20]
#     - create 기능 추가
#  * [2019/04/26]
#     - target이 비어있지 않으면 지우는 로직 변경
#  * [2019/04/18]
#     - 이동하거나 복사할 목적지 폴더가 없으면 생성하려고 해 봄
#     - 이동하거나 복사할 대상 파일의 폴더가 없으면 생성하려고 해 봄
#     - src가 폴더이고 \로 끝나면 (윈도우에서) 오류 발생
#       - PAM에서
#         argoslabs.filesystem.op.exe -vvv copy "C:\tmp\1\" "C:\tmp\2"
#         라고 호출하면 src가 'C:\\tmp\\1" C:\\tmp\\2' 가 되는 문제점 발생
#       ==> PAM에서 수정하기로 함 (개별 args 목록에 넣는 것으로)
#  * [2019/03/08]
#     - add icon
#  * [2018/11/28]
#     - starting

################################################################################
import os
import sys
import time
import glob
import shutil
import tempfile
# from pathlib import Path
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.filesystem.op import _main as main
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
        for f in glob.glob(os.path.join(tempfile.gettempdir(), 'op_dir_*')):
            shutil.rmtree(f)
        self.assertTrue(True)

    # ==========================================================================
    def test0010_empty(self):
        try:
            _ = main()
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_mkdtemp(self):
        TU.td1 = tempfile.mkdtemp(prefix='op_dir_1_')
        self.assertTrue(os.path.exists(TU.td1))
        TU.td2 = tempfile.mkdtemp(prefix='op_dir_2_')
        self.assertTrue(os.path.exists(TU.td2))
        TU.td3 = tempfile.mkdtemp(prefix='op_dir_3_')
        self.assertTrue(os.path.exists(TU.td3))
        TU.td4 = tempfile.mkdtemp(prefix='op_dir_4_')
        self.assertTrue(os.path.exists(TU.td4))
        # for checking remove TU.td3
        shutil.rmtree(TU.td3)
        self.assertTrue(not os.path.exists(TU.td3))

    # ==========================================================================
    def test0030_mk_file(self):
        foo = os.path.join(TU.td1, 'foo.txt')
        with open(foo, 'w') as ofp:
            ofp.write('This is foo')
        self.assertTrue(os.path.exists(foo))
        bar = os.path.join(TU.td1, 'foo.txt')
        with open(bar, 'w') as ofp:
            ofp.write('This is foo')
        self.assertTrue(os.path.exists(bar))
        foo = os.path.join(TU.td2, 'foo.log')
        with open(foo, 'w') as ofp:
            ofp.write('Log for foo')
        self.assertTrue(os.path.exists(foo))
        bar = os.path.join(TU.td2, 'foo.log')
        with open(bar, 'w') as ofp:
            ofp.write('Log for foo')
        self.assertTrue(os.path.exists(bar))

    # ==========================================================================
    def test0040_mk_dir_file(self):
        foo = os.path.join(TU.td1, 'foo')
        os.makedirs(foo)
        self.assertTrue(os.path.isdir(foo))
        foo = os.path.join(foo, 'foo.txt')
        with open(foo, 'w') as ofp:
            ofp.write('This is foo2')
        self.assertTrue(os.path.exists(foo))
        bar = os.path.join(TU.td2, 'foo')
        os.makedirs(bar)
        self.assertTrue(os.path.isdir(bar))
        bar = os.path.join(bar, 'foo.txt')
        with open(bar, 'w') as ofp:
            ofp.write('This is bar2')
        self.assertTrue(os.path.exists(bar))

    # ==========================================================================
    def test0100_invalid_op(self):
        try:
            _ = main('invalid-op', 'src', 'target')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_invalid_src(self):
        try:
            r = main('copy', 'invalid-src', 'target')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # invalid-target 으로 복사를 하게 되어서 코멘트 아웃
    # # ==========================================================================
    # def test0120_invalid_target(self):
    #     try:
    #         if sys.platform == 'win32':
    #             invalid_target = 'C:\\foobar'
    #         _ = main('copy', os.path.join(TU.td1, 'foo.txt'), 'invalid-target')
    #         self.assertTrue(False)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)

    # ==========================================================================
    def test0130_copy_file(self):
        try:
            src = os.path.join(TU.td1, 'foo.txt')
            target = os.path.join(TU.td3, 'foo.txt')
            with captured_output() as (out, err):
                r = main('copy', src, target)
            self.assertTrue(r == 0)
            rs = out.getvalue()
            self.assertTrue(rs == target)
            s_mtime = os.path.getmtime(src)
            t_mtime = os.path.getmtime(target)
            self.assertTrue(s_mtime < t_mtime)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_copy_file_preserve(self):
        try:
            src = os.path.join(TU.td1, 'foo.txt')
            target = os.path.join(TU.td3, 'foo.txt')
            target_1 = os.path.join(TU.td3, 'foo (1).txt')
            r = main('copy', src, target, '--preserve')
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(target_1))
            s_mtime = os.path.getmtime(src)
            t_mtime = os.path.getmtime(target_1)
            self.assertTrue(s_mtime == t_mtime)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_copy_file_once_more(self):
        try:
            src = os.path.join(TU.td1, 'foo.txt')
            target = os.path.join(TU.td3, 'foo.txt')
            target_2 = os.path.join(TU.td3, 'foo (2).txt')
            r = main('copy', src, target)
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(target_2))
            s_mtime = os.path.getmtime(src)
            t_mtime = os.path.getmtime(target_2)
            self.assertTrue(s_mtime < t_mtime)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_copy_file_once_more_with_preserver_overwirte(self):
        try:
            time.sleep(1)
            src = os.path.join(TU.td1, 'foo.txt')
            if os.path.exists(src):
                os.remove(src)
            with open(src, 'w') as ofp:
                ofp.write('This is a new foo foo...\n')
            with open(src) as ifp:
                src_str = ifp.read()
            target = os.path.join(TU.td3, 'foo.txt')
            r = main('copy', src, target, '--preserve', '--overwrite')
            self.assertTrue(r == 0)
            s_mtime = os.path.getmtime(src)
            t_mtime = os.path.getmtime(target)
            self.assertTrue(s_mtime == t_mtime)
            with open(target) as ifp:
                target_str = ifp.read()
            self.assertTrue(src_str == target_str)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_copy_file_same_src_target(self):
        try:
            src = os.path.join(TU.td1, 'foo.txt')
            target = os.path.join(TU.td1, 'foo.txt')
            _ = main('copy', src, target)
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0175_copy_dir_same_src_target(self):
        try:
            src = os.path.join(TU.td1)
            target = os.path.join(TU.td1)
            _ = main('copy', src, target)
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0190_copy_folder(self):
        try:
            time.sleep(1)
            # target 폴더를 삭제하지 않고 복사하도록 함
            # shutil.rmtree(TU.td3)
            exf = os.path.join(TU.td3, 'foobar.txt')
            with open(exf, 'w') as ofp:
                ofp.write('This is foobar!')
            src = os.path.join(TU.td1+os.path.sep)
            target = os.path.join(TU.td3)
            with captured_output() as (out, err):
                r = main('copy', src, target, '--recursive')
            self.assertTrue(r == 0)
            rs = out.getvalue()
            self.assertTrue(len(rs.split('\n')) == 2)
            s_mtime = os.path.getmtime(os.path.join(src, 'foo', 'foo.txt'))
            t_mtime = os.path.getmtime(os.path.join(target, 'foo', 'foo.txt'))
            # Note! in Windows ctime is changed with --preserve option
            self.assertTrue(s_mtime < t_mtime)
            self.assertTrue(os.path.exists(exf))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_copy_folder_with_preserve_without_update(self):
        try:
            time.sleep(1)
            src = os.path.join(TU.td1)
            src_bar = os.path.join(TU.td1, 'foo.txt')
            target_bar = os.path.join(TU.td3, 'foo.txt')
            target_bar_4 = os.path.join(TU.td3, 'foo (4).txt')
            with open(src_bar) as ifp:
                src_str = ifp.read()
            with open(target_bar, 'w') as ofp:
                ofp.write('This is foo foo')
            target = os.path.join(TU.td3)
            # update 옵션이 없으면 무조건 덮어씀
            r = main('copy', src, target, '--preserve', '--recursive')
            self.assertTrue(r == 0)
            s_mtime = os.path.getmtime(os.path.join(src, 'foo', 'foo.txt'))
            t_mtime = os.path.getmtime(os.path.join(target, 'foo', 'foo (1).txt'))
            # Note! in Windows ctime is changed with --preserve option
            self.assertTrue(int(s_mtime) == int(t_mtime))
            with open(target_bar_4) as ifp:
                target_str = ifp.read()
            self.assertTrue(src_str == target_str)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_copy_folder_with_preserve_with_overwrite(self):
        try:
            time.sleep(1)
            src = os.path.join(TU.td1)
            src_bar = os.path.join(TU.td1, 'foo.txt')
            target_bar = os.path.join(TU.td3, 'foo.txt')
            with open(src_bar) as ifp:
                src_str = ifp.read()
            with open(target_bar, 'w') as ofp:
                ofp.write('This is foo foo')
            target = os.path.join(TU.td3)
            r = main('copy', src, target, '--preserve', '--overwrite', '--recursive')
            self.assertTrue(r == 0)
            s_mtime = os.path.getmtime(os.path.join(src, 'foo', 'foo.txt'))
            t_mtime = os.path.getmtime(os.path.join(target, 'foo', 'foo.txt'))
            # Note! in Windows ctime is changed with --preserve option
            self.assertTrue(int(s_mtime) == int(t_mtime))
            with open(target_bar) as ifp:
                target_str = ifp.read()
            self.assertTrue(src_str == target_str)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0230_move_file(self):
        try:
            src = os.path.join(TU.td2, 'foo.log')
            target = os.path.join(TU.td3, 'foo.log')
            r = main('move', src, target)
            self.assertTrue(r == 0)
            self.assertTrue(not os.path.exists(src))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0240_move_folder(self):
    #     try:
    #         src = os.path.join(TU.td2)
    #         target = os.path.join(TU.td4)
    #         src_foo = os.path.join(TU.td2, 'foo.txt')
    #         with open(src_foo, 'w') as ofp:
    #             ofp.write('This is foo foo text')
    #         r = main('move', src, target, '--recursive')
    #         self.assertTrue(r == 0)
    #         self.assertTrue(not os.path.exists(TU.td2))
    #         # NB) Previously move file foo.log is removed first
    #         self.assertTrue(os.path.exists(os.path.join(TU.td4, 'foo.txt')))
    #         # self.assertTrue(os.path.exists(os.path.join(TU.td4, 'foo.log')))
    #         self.assertTrue(os.path.exists(os.path.join(TU.td4, 'foo', 'foo.txt')))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0250_create_file(self):
        out = os.path.join(tempfile.gettempdir(), 'test0250_create_file_stdout.txt')
        try:
            src = os.path.join(TU.td1, 'foo', 'foo234.txt')
            with captured_output() as (out, err):
                r = main('create', src)
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(src) and os.path.getsize(src) == 0)
            rstr = out.getvalue()
            print(rstr)
            self.assertTrue(os.path.exists(rstr))

            with captured_output() as (out, err):
                r = main('create', src)
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(src) and os.path.getsize(src) == 0)
            rstr = out.getvalue()
            print(rstr)
            # (1) appended
            self.assertTrue(rstr != src and os.path.exists(rstr))

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0260_create_folder(self):
        try:
            src = os.path.join(TU.td1, 'foo', 'foobardir') + os.path.sep
            r = main('create', src)
            self.assertTrue(r == 0)
            self.assertTrue(os.path.isdir(src))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0300_copy_folder_wildcard(self):
    #     try:
    #         src = os.path.join(TU.td4)
    #         target = os.path.join(TU.td2)
    #         r = main('copy', src, target, '--wildcard', '*.txt')
    #         self.assertTrue(r == 0)
    #         self.assertTrue(os.path.exists(TU.td4))
    #         # NB) Previously move file foo.log is removed first
    #         self.assertTrue(not os.path.exists(os.path.join(TU.td2, 'foo.log')))
    #         self.assertTrue(os.path.exists(os.path.join(TU.td2, 'foo.txt')))
    #         self.assertTrue(not os.path.exists(os.path.join(TU.td2, 'foo', 'foo.txt')))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0310_move_folder_wildcard(self):
    #     try:
    #         src = os.path.join(TU.td4)
    #         target = os.path.join(TU.td2)
    #         r = main('move', src, target, '--wildcard', '*.txt')
    #         self.assertTrue(r == 0)
    #         # 이동을 하고 나서 비어 있지 않으면 해당 폴더를 그대로
    #         # self.assertTrue(not os.path.exists(TU.td4))
    #         # NB) Previously move file foo.log is removed first
    #         self.assertTrue(not os.path.exists(os.path.join(TU.td2, 'foo.log')))
    #         self.assertTrue(os.path.exists(os.path.join(TU.td2, 'foo (1).txt')))
    #         self.assertTrue(not os.path.exists(os.path.join(TU.td2, 'foo')))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0400_remove_file(self):
        try:
            src = os.path.join(TU.td1, 'foo', 'foo.txt')
            r = main('remove', src)
            self.assertTrue(r == 0)
            self.assertTrue(not os.path.exists(src))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0410_remove_folder_wildcard(self):
        try:
            s = os.path.join(TU.td1, 'foo.txt')
            t = os.path.join(TU.td1, 'foo.log')
            shutil.copy(s, t)
            s = os.path.join(TU.td1, 'foo', 'foo234.txt')
            t = os.path.join(TU.td1, 'foo', 'foo234.log')
            shutil.copy(s, t)
            r = main('remove', TU.td1, '--wildcard', '*.log', '--recursive')
            self.assertTrue(r == 0)
            self.assertTrue(not os.path.exists(t))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0420_remove_folder(self):
        try:
            src_l = (TU.td1, TU.td3)
            for src in src_l:
                r = main('remove', src)
                self.assertTrue(r == 0)
                self.assertTrue(not os.path.exists(src))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0430_copy_debug(self):
        src = os.path.join(os.path.dirname(__file__), 'foo')
        tgt = os.path.join(src, 'bar')
        try:
            r = main('copy', src, tgt, '--wildcard', '*.txt')
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(tgt))
            self.assertTrue(not os.path.exists(os.path.join(tgt, 'bar')))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(tgt):
                shutil.rmtree(tgt)

    # # ==========================================================================
    # def test0440_move_debug(self):
    #     src = os.path.join(os.path.dirname(__file__), 'foo')
    #     tgt = os.path.join(src, 'bar')
    #     try:
    #         r = main('move', src, tgt, '--wildcard', '*.txt')
    #         self.assertTrue(r == 0)
    #         self.assertTrue(os.path.exists(tgt))
    #         self.assertTrue(not os.path.exists(os.path.join(tgt, 'bar')))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(tgt):
    #             shutil.rmtree(tgt)

    # ==========================================================================
    def test0450_remove_invalid_folder(self):
        try:
            invalid_dir = os.path.join(tempfile.gettempdir(), 'invalidfoldertotest')
            r = main('remove', invalid_dir)
            self.assertTrue(r == 0)
            self.assertTrue(not os.path.exists(invalid_dir))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0500_wildcard__ASJ_556(self):
        try:
            invalid_dir = os.path.join(tempfile.gettempdir(), 'invalidfoldertotest')
            r = main('copy',
                     'C:\\Users\\argos\\Desktop\\bongsplugin\\plug-in-test\\File Folder OP\\test folder',
                     'C:\\Users\\argos\\Desktop\\bongsplugin\\plug-in-test\\File Folder OP\\target folder',
                     '--wildcard', 'test*')
            self.assertTrue(r == 0)
            self.assertTrue(not os.path.exists(invalid_dir))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0500_move_wildcard_ASJ582(self):
        try:
            invalid_dir = os.path.join(tempfile.gettempdir(), 'invalidfoldertotest')
            r = main('move',
                     r'C:\Users\argos\Desktop\ASJ\ASJ-dsa\input',
                     r'C:\Users\argos\Desktop\ASJ\ASJ-dsa\output',
                     '--wildcard', '*.csv')
            self.assertTrue(r == 0)
            self.assertTrue(not os.path.exists(invalid_dir))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0510_remove_wildcard_ASJ581(self):
        try:
            invalid_dir = os.path.join(tempfile.gettempdir(), 'invalidfoldertotest')
            r = main('remove',
                     r'C:\Users\argos\Desktop\ASJ\ASJ-581\TEST',
                     # r'C:\Users\argos\Desktop\ASJ\ASJ-dsa\output',
                     '--wildcard', '*.csv',
                     # '--recursive'
                     )
            self.assertTrue(r == 0)
            self.assertTrue(not os.path.exists(invalid_dir))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        for f in glob.glob(os.path.join(tempfile.gettempdir(), 'op_dir_*')):
            shutil.rmtree(f)
            self.assertTrue(not os.path.exists(f))
