#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.web.savehtml.tests.test_me`
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
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/08/13]
#     - starting

################################################################################
import os
import sys
import csv
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.web.savehtml import _main as main
from tempfile import gettempdir
from alabs.common.util.vvencoding import get_file_encoding


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def setup(self):
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        ...

    # ==========================================================================
    def test0050_fail_html(self):
        try:
            _ = main('invalid.url')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success_1(self):
        of = '%s/stdout.txt' % gettempdir()
        htmlfile = os.path.abspath('ecfr.html')
        try:
            r = main('https://www.ecfr.gov/cgi-bin/text-idx?SID=b4dfce00846d21edcda79062dad07dfc&mc=true&tpl=/updatesrecent.tpl',
                     'GET',
                     htmlfile,
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                self.assertTrue(htmlfile == ifp.read())
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
