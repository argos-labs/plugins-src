#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.file.encoding`
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
#     - ignore 옵션 요청 by ASJ
#  * [2021/04/06]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/03/25]
#     - starting

################################################################################
import os
import sys
import csv
import chardet
from unittest import TestCase
from argoslabs.file.encoding import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_invalid_operation(self):
        try:
            _ = main('invalid_env', '', '', '')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_conv_encoding(self):
        stdout = 'stdout.txt'
        try:
            s_enc = 'cp932:Japanese'
            s = 'jpn-01.csv'
            t_enc = 'utf_8:all languages'
            t = 'jpn-01.cp932.csv'
            r = main(s_enc, s, t_enc, t,
                     '--outfile', stdout)
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0100_conv_encoding(self):
        stdout = 'stdout.txt'
        try:
            s_enc = 'utf_8:all languages'
            s = 'jpn-01.csv'
            t_enc = 'cp932:Japanese'
            t = 'jpn-01.cp932.csv'
            r = main(s_enc, s, t_enc, t,
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.endswith(t))
            # rr = []
            # with open(stdout, 'r') as ifp:
            #     cr = csv.reader(ifp)
            #     for row in cr:
            #         self.assertTrue(len(row) in (4,))
            #         rr.append(row)
            # self.assertTrue(len(rr) == 2 and
            #                 rr[1][0] == 'utf_8' and rr[1][2] == 'cp932')
            with open(t, 'rb') as ifp:
                rd = chardet.detect(ifp.read())
            self.assertTrue(rd['encoding'] == 'SHIFT_JIS')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0110_conv_encoding(self):
        stdout = 'stdout.txt'
        try:
            s_enc = 'utf_8:all languages'
            s = 'jpn-01.csv'
            t_enc = 'euc_jp:Japanese'
            t = 'jpn-01.cp932.csv'
            r = main(s_enc, s, t_enc, t,
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.endswith(t))
            with open(t, 'rb') as ifp:
                rd = chardet.detect(ifp.read())
            self.assertTrue(rd['encoding'] == 'EUC-JP')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0120_test_encoding(self):
        stdout = 'stdout.txt'
        try:
            s_enc = 'utf_8:all languages'
            s = '쿠팡테스트.csv'
            # t_enc = 'cp949:Korean'
            t_enc = 'euc_kr:Korean'
            t = '쿠팡테스트.out.csv'
            r = main(s_enc, s, t_enc, t,
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.endswith(t))
            with open(t, 'rb') as ifp:
                rd = chardet.detect(ifp.read())
            self.assertTrue(rd['encoding'] == 'EUC-KR')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0130_test_ignore(self):
        stdout = 'stdout.txt'
        try:
            s_enc = 'utf_8:all languages'
            s = 'Test_document.txt'
            t_enc = 'cp932:Japanese'
            t = 'Test_document.out.txt'

            # without ignore
            r = main(s_enc, s, t_enc, t,
                     '--outfile', stdout)
            self.assertTrue(r == 9)

            # with ignore
            r = main(s_enc, s, t_enc, t, '--ignore',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.endswith(t))
            with open(t, 'rb') as ifp:
                rd = chardet.detect(ifp.read())
            self.assertTrue(rd['encoding'] == 'SHIFT_JIS')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
