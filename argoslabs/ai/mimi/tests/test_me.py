"""
====================================
 :mod:`argoslabs.ai.mimi`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
import csv
import unittest
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.ai.mimi import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    o_pwd = None
    app_id = None
    client_id = None
    secret = None

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        # Jerry's
        cls.app_id = '..'
        cls.client_id = '..'
        cls.secret = '..'

        cls.o_pwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    @classmethod
    def tearDown(cls) -> None:
        os.chdir(cls.o_pwd)

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        try:
            r = main('invalid-op', 'a', 'b', 'c')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        errfile = 'stderr.txt'
        try:
            r = main('Audio Recognition',
                     TU.app_id, TU.client_id+'foo', TU.secret,
                     '--errfile', errfile)
            self.assertTrue(r != 0)
            with open(errfile) as ifp:
                rs = ifp.read()
                # print(rs)
                self.assertTrue(rs.rstrip() == 'Cannot get token: Unauthorized')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(errfile):
                os.remove(errfile)

    # ==========================================================================
    def test0100_success_audio_recognition(self):
        outfile = 'stdout.txt'
        errfile = 'stderr.txt'
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('Audio Recognition',
                     TU.app_id, TU.client_id, TU.secret,
                     '--outfile', outfile,
                     '--errfile', errfile)
            self.assertTrue(r != 0)
            with open(errfile, encoding='utf-8') as ifp:
                rs = ifp.read().rstrip()
                self.assertTrue(rs ==
                                'Invalid Audio file for Audio Recognition')

            r = main('Audio Recognition',
                     TU.app_id, TU.client_id, TU.secret,
                     '--audio-file', 'mimi.example/audio.raw',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            # with open(outfile, encoding='utf-8') as ifp:
            #     print(ifp.read())
            with open(outfile, encoding='utf-8') as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (4,))
                    rows.append(row)
                self.assertTrue(len(rows) == 3)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)
            if os.path.exists(errfile):
                os.remove(errfile)

    # ==========================================================================
    def test0110_success_tts(self):
        outfile = 'stdout.txt'
        errfile = 'stderr.txt'
        out_wave = 'tts.out.wav'
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('Text to Speech',
                     TU.app_id, TU.client_id, TU.secret,
                     '--outfile', outfile,
                     '--errfile', errfile)
            self.assertTrue(r != 0)
            with open(errfile, encoding='utf-8') as ifp:
                rs = ifp.read().rstrip()
                self.assertTrue(rs == 'Empty Input Text for Text to Speech')

            r = main('Text to Speech',
                     TU.app_id, TU.client_id, TU.secret,
                     '--text', 'こんにちは世界',
                     '--outfile', outfile)
            self.assertTrue(r == 0)

            if os.path.exists(out_wave):
                os.remove(out_wave)
            r = main('Text to Speech',
                     TU.app_id, TU.client_id, TU.secret,
                     '--text', 'Hello world?',
                     '--in-lang', 'English',
                     '--out-wave', out_wave,
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(out_wave))

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)
            if os.path.exists(errfile):
                os.remove(errfile)
            if os.path.exists(out_wave):
                os.remove(out_wave)

    # ==========================================================================
    def test0120_success_translate(self):
        outfile = 'stdout.txt'
        errfile = 'stderr.txt'
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('Translation',
                     TU.app_id, TU.client_id, TU.secret,
                     '--outfile', outfile,
                     '--errfile', errfile)
            self.assertTrue(r != 0)
            with open(errfile, encoding='utf-8') as ifp:
                rs = ifp.read().rstrip()
                self.assertTrue(rs == 'Empty Input Text for Translation')

            r = main('Translation',
                     TU.app_id, TU.client_id, TU.secret,
                     '--text', 'こんにちは世界',
                     '--outfile', outfile,
                     '--errfile', errfile)
            self.assertTrue(r != 0)
            with open(errfile, encoding='utf-8') as ifp:
                rs = ifp.read().rstrip()
                self.assertTrue(rs == 'Input language and Out language must not same')

            r = main('Translation',
                     TU.app_id, TU.client_id, TU.secret,
                     '--text', 'こんにちは世界',
                     '--out-lang', 'Korean',
                     '--outfile', outfile,
                     '--errfile', errfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                rs = ifp.read()
                # print(rs)
                self.assertTrue(rs.rstrip() == '안녕하세요 세계.')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)
            if os.path.exists(errfile):
                os.remove(errfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)


################################################################################
if __name__ == '__main__':
    unittest.main()
