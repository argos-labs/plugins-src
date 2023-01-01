#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.naver.ocr`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.naver.ocr import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    key = None
    url = None

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.key = '..'
        cls.url = 'https://8fc9ca186dcf41559f368bdd1e3d930c.apigw.ntruss.com/custom/v1/7145/03983b1af0bd12639da3e9fe0bc8ae205d754f2690cdff6a8e0c800ec0fd5ef8/general'

    # ==========================================================================
    def tearDown(self) -> None:
        ...

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('invalid')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test0100_success(self):
    #     outfile = 'stdout.txt'
    #     try:
    #         r = main(TU.key, TU.url, "image003.jpg",
    #                  '--box-imgfile', 'image003-out.png',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile, encoding='utf-8') as ifp:
    #             rs = ifp.read()
    #             self.assertTrue(rs.find('가족') >= 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(outfile):
    #             os.remove(outfile)

    # # ==========================================================================
    # def test0110_success(self):
    #     outfile = 'stdout.txt'
    #     try:
    #         r = main(TU.key, TU.url, "en_test1.png",
    #                  '--box-imgfile', 'en_test1-out.png',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile, encoding='utf-8') as ifp:
    #             rs = ifp.read()
    #             self.assertTrue(rs.find('819543') > 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(outfile):
    #             os.remove(outfile)

    # # ==========================================================================
    # def test0120_success(self):
    #     outfile = 'stdout.txt'
    #     try:
    #         r = main(TU.key, TU.url, "image011.png",
    #                  '--box-imgfile', 'image011-out.png',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile, encoding='utf-8') as ifp:
    #             rs = ifp.read()
    #             self.assertTrue(rs.find('가') >= 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(outfile):
    #             os.remove(outfile)

    # # ==========================================================================
    # def test0130_success(self):
    #     outfile = 'naver.txt'
    #     try:
    #         r = main(TU.key, TU.url, "kor001.jpg",
    #                  '--outfile', outfile, '--output_type', 'csv')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0140_success(self):
    #     try:
    #         r = main(TU.key, TU.url, "kor001.jpg", '--output_type', 'csv')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
