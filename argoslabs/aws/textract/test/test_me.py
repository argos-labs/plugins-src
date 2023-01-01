#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.aws.textract`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2021/03/26]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2020/04/02]
#     - add icon
#  * [2020/04/02]
#     - starting

################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.aws.textract import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    key_id = None
    key = None

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.key_id = '..'
        cls.key = '..'

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
    #         r = main(TU.key_id, TU.key, "en_test1.png", 'OCR',
    #                  '--box-imgfile', 'en_test1-out.png',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile, encoding='utf-8') as ifp:
    #             rs = ifp.read()
    #             self.assertTrue(rs.find('Main') >= 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(outfile):
    #             os.remove(outfile)
    #
    # # ==========================================================================
    # def test0110_success(self):
    #     outfile = 'output1.txt'
    #     try:
    #         r = main(TU.key_id, TU.key, "en_test2.png", 'OCR',
    #                  '--box-imgfile', 'en_test2-out.png',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile, encoding='utf-8') as ifp:
    #             rs = ifp.read()
    #             self.assertTrue(rs.find('Total') > 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(outfile):
    #             os.remove(outfile)
    #
    # # ==========================================================================
    # def test0120_success(self):
    #     outfile = 'stdout.txt'
    #     try:
    #         r = main(TU.key_id, TU.key, "en_rotate1.png", 'Rekognition Text',
    #                  '--box-imgfile', 'en_rotate1_out.png',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile, encoding='utf-8') as ifp:
    #             rs = ifp.read()
    #             self.assertTrue(rs.find('Rotate') >= 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(outfile):
    #             os.remove(outfile)
    #
    # # ==========================================================================
    # def test0130_success(self):
    #     outfile = 'stdout.txt'
    #     try:
    #         r = main(TU.key_id, TU.key, "en_handwritten1.png",
    #                  'Rekognition Text',
    #                  '--box-imgfile', 'en_handwritten1_out.png',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile, encoding='utf-8') as ifp:
    #             rs = ifp.read()
    #             self.assertTrue(rs.find('Aa') >= 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(outfile):
    #             os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
