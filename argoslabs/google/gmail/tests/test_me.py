#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.google.gmail.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import sys
from unittest import TestCase
from argoslabs.google.translate import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0100_empty_parameter(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_unknown_engine(self):
        try:
            _ = main('unknown', 'hello world?')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0120_missing_msg(self):
        try:
            _ = main('google')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0200_hello_detect(self):
        out_f = 'out.txt'
        err_f = 'err.txt'
        try:
            r = main('こんにちは世界？私はTTSです?', '--detect',
                     '--outfile', out_f,
                     '--errfile', err_f)
            self.assertTrue(r == 0)
            with open(out_f) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'lang, confidence\nja, 1.0\n')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_hello_jp2en(self):
        out_f = 'out.txt'
        err_f = 'err.txt'
        try:
            r = main('こんにちは世界？私はTTSです?',
                     '--dest', 'English',
                     '--outfile', out_f,
                     '--errfile', err_f)
            self.assertTrue(r == 0)
            with open(out_f, encoding='utf8') as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out == 'Hello World? I am TTS?')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_hello_jp2ko(self):
        out_f = 'out.txt'
        err_f = 'err.txt'
        try:
            r = main('こんにちは世界？私はTTSです?',
                     '--dest', 'Korean',
                     '--outfile', out_f,
                     '--errfile', err_f)
            self.assertTrue(r == 0)
            with open(out_f, encoding='utf8') as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out == '안녕하세요 세계? 나는 TTS입니다?')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0230_hello_jp2cn(self):
        out_f = 'out.txt'
        err_f = 'err.txt'
        try:
            r = main('こんにちは世界？私はTTSです?',
                     '--dest', 'Chinese (Mandarin/China)',
                     '--outfile', out_f,
                     '--errfile', err_f)
            self.assertTrue(r == 0)
            with open(out_f, encoding='utf8') as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out == '你好世界？我TTS？')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
