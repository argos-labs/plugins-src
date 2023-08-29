#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.google.tts.tests.test_me`
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
#  * [2021/04/07]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2020/04/29]
#     - add --file, --encoding options
#  * [2019/10/09]
#     - chagne --lang choices into real language name
#  * [2019/04/25]
#     - add arguments' display_name
#  * [2019/03/08]
#     - starting

################################################################################
import os
import sys
from uuid import uuid4
from unittest import TestCase
from argoslabs.google.tts import _main as main
from tempfile import gettempdir


################################################################################
class TU(TestCase):
    # ==========================================================================
    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

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
    def test0200_say_hello(self):
        try:
            r = main('Hello world?')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0210_say_hello_slow(self):
    #     try:
    #         r = main('Hello slow world?', '--slow')
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0250_say_hello_ko(self):
    #     try:
    #         r = main('안녕하세요? 저는 TTS입니다.', '--lang', 'Korean')
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0260_say_hello_ja(self):
    #     try:
    #         r = main('こんにちは世界？私はTTSです.', '--lang', 'Japanese')
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0270_say_hello_zh_cn(self):
    #     try:
    #         r = main('你好，世界？我是TTS.', '--lang', 'Chinese (Mandarin/China)')
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0300_say_hello_save_mp3(self):
    #     # write error happen so use temppdir
    #     mp3f = os.path.join(gettempdir(), '%s.mp3' % uuid4())
    #     try:
    #         r = main('Hello save world?', '--save-mp3', mp3f)
    #         self.assertTrue(r == 0 and os.path.exists(mp3f))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(mp3f):
    #             os.remove(mp3f)

    # # ==========================================================================
    # def test0310_say_hello_save_mp3(self):
    #     # write error happen so use temppdir
    #     mp3f = os.path.join(gettempdir(), '%s.mp3' % uuid4())
    #     try:
    #         r = main('Hello save world?', '--save-mp3', mp3f)
    #         self.assertTrue(r == 0 and os.path.exists(mp3f))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(mp3f):
    #             os.remove(mp3f)

    # # ==========================================================================
    # def test0320_say_hello_ko_file(self):
    #     try:
    #         msg_f = 'msg.txt'
    #         with open(msg_f, 'w', encoding='utf-8') as ofp:
    #             ofp.write('안녕하세요?\n 저는 TTS입니다\n')
    #         r = main('', '--file', msg_f, '--lang', 'Korean')
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
