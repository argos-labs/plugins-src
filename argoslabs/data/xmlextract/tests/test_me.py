#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.xmlextract`
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
#  * [2021/07/31]
#     - Change group "9: Utility Tools" => "10: Web Scraping"
#  * [2021/04/01]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/05/07]
#     - bookstore multiple author
#  * [2020/05/07]
#     - change xpath with nargs=+
#  * [2020/05/06]
#     - starting for training of Cognizant

################################################################################
import os
import sys
import csv
# from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.data.xmlextract import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.xmlextract
    """
    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0030_failure(self):
        try:
            _ = main('foo.xml')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0040_failure(self):
        try:
            r = main('invalid.xml', '/')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_success_with_one_xpath(self):
        stdout = 'stdout.txt'
        try:
            r = main('foo.xml',
                     '/world/people/name',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read().rstrip()
            self.assertTrue(rs.split('\n')[-1] == 'Venus')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0110_success_with_two_xpath(self):
        stdout = 'stdout.txt'
        try:
            r = main('foo.xml',
                     '/world/people/name',
                     '/world/people/tall',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read().rstrip()
            self.assertTrue(rs.split('\n')[-1] == 'Venus,99cm')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0120_success_with_two_xpath_with_header(self):
        stdout = 'stdout.txt'
        try:
            r = main('foo.xml',
                     '/world/people/name',
                     '/world/people/tall',
                     '--header',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                rs = ifp.read().rstrip()
            self.assertTrue(rs.split('\n')[-1] == 'Venus,99cm' and
                            rs.split('\n')[0] == 'name,tall')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0120_success_with_xpath(self):
        stdout = 'stdout.txt'
        try:
            r = main('bookstore.xml',
                     '/bookstore/book/title',
                     '/bookstore/book/author',
                     '/bookstore/book/year',
                     '/bookstore/book/price',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            # with open(stdout, encoding='utf-8') as ifp:
            #     rs = ifp.read().rstrip()
            rows = list()
            with open(stdout, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (4,))
                    rows.append(row)
            # self.assertTrue(len(rows) == 39 and rows[-1][-2] == '14')
            self.assertTrue(len(rows) > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
