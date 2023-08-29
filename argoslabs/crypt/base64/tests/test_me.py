#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.crypt.base64`
====================================
.. moduleauthor:: Venkatesh Vanjre <vvanjre@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Venkatesh Vanjre, Jerry Chae
#
# Change Log
# --------
#  [2022/8/17]
#   - Debugging sample_japanese.pdf
#  [2021/5/21]
#   - starting

################################################################################
import os
import sys
import base64
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.crypt.base64 import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.crypt.base64
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        try:
            r = main('Encode')
            self.assertTrue(r==2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_success_string_encode(self):
        outfile = 'stdout.txt'
        try:
            r = main('Encode',
                     '--stringinput', 'test text',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == 'dGVzdCB0ZXh0')

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success_string_decode(self):
        outfile = 'stdout.txt'
        try:
            r = main('Decode',
                     '--stringinput', 'dGVzdCB0ZXh0',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == 'test text')

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_success_file_encode(self):
        outfile = 'stdout.txt'
        infile = 'infile.txt'
        with open(infile, 'w') as ofp:
            ofp.write('test text')
        try:
            r = main('Encode',
                     '--fileinput', infile,
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == 'dGVzdCB0ZXh0')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_success_file_decode(self):
        outfile = 'stdout.txt'
        infile = 'infile.txt'
        with open(infile, 'w') as ofp:
            ofp.write('dGVzdCB0ZXh0')
        try:
            r = main('Decode',
                     '--fileinput', infile,
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == 'test text')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_encoding_debug_japanese(self):
        outfile = 'sample_japanese.b64'
        infile = 'sample_japanese.pdf'
        try:
            r = main('Encode',
                     '--fileinput', infile,
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                # print(rs)
            self.assertTrue(rs)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_decoding_debug_japanese(self):
        orgfile = 'sample_japanese.pdf'
        outfile = 'sample_japanese.pdf2'
        infile = 'sample_japanese.b64'
        try:
            r = main('Decode',
                     '--fileinput', infile,
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, 'rb') as ifp:
                pdf2 = ifp.read()
            with open(orgfile, 'rb') as ifp:
                pdf = ifp.read()
            self.assertTrue(pdf == pdf2)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(infile):
                os.remove(infile)
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
