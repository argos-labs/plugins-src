"""
====================================
 :mod:`argoslabs.ibm.stt`
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
#  * [2021/01/23]
#     - mis-spell "Waston" => "Watson"
#  * [2020/03/05]
#     - change DisplayName starting with "IBM "
#  * [2019/08/11]
#     - starting

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.ibm.stt import _main as main


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
    def test0010_failure(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('invalid', 'invalid_image')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0030_failure(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('..', 'invalid_audio')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0040_failure(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('..',
                     'speech.wav', 'invalid_type')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('..',
                     'speech.wav', 'audio/wav', 'invalid_model')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0060_failure(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('..',
                     'speech.wav', 'audio/mp3', 'en-US_BroadbandModel')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0070_failure(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main('..',
                     'speech.wav', 'audio/wav', 'ko-KR_NarrowbandModel',
                     '--outfile', outfile)
            # self.assertTrue(r != 0)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out != 'thunderstorms could produce large hail isolated tornadoes and heavy rain')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0100_success(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main('..',
                     'speech.wav', 'audio/wav', 'en-US_BroadbandModel',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out == 'thunderstorms could produce large hail isolated tornadoes and heavy rain')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0110_success_with_threshold(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main('..',
                     'speech.wav', 'audio/wav', 'en-US_BroadbandModel',
                     '--word-confidence',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                print(ifp.read())
            with open(outfile) as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (2,))
                    rows.append(row)
                self.assertTrue(len(rows) == 11)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0120_success(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main('..',
                     'speech.wav', 'audio/wav', 'en-US_NarrowbandModel',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out == 'thunderstorms could produce large hail isolated tornadoes and heavy rain')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0130_success_with_threshold(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        os.chdir(os.path.dirname(__file__))
        outfile = 'stdout.txt'
        try:
            r = main('..',
                     'speech.wav', 'audio/wav', 'en-US_NarrowbandModel',
                     '--word-confidence',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                print(ifp.read())
            with open(outfile) as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (2,))
                    rows.append(row)
                self.assertTrue(len(rows) == 11)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0140_success(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        os.chdir(os.path.dirname(__file__))
        outfile = 'stdout.txt'
        try:
            r = main('..',
                     'Rec.mp3',
                     'audio/mpeg', 'en-US_BroadbandModel',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out == 'injunction with employee understands that it needs an employee violate any provision of this agreement are the')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0150_success(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        os.chdir(os.path.dirname(__file__))
        outfile = 'stdout.txt'
        try:
            r = main('..',
                     'Rec2.mp3',
                     'audio/mpeg', 'en-US_BroadbandModel',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out == 'recording is for single format %HESITATION Microsoft please record')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0160_success(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        os.chdir(os.path.dirname(__file__))
        outfile = 'stdout.txt'
        try:
            r = main('..',
                     'Rec.wav',
                     'audio/wav', 'en-US_BroadbandModel',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out == 'number five')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0170_success(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        os.chdir(os.path.dirname(__file__))
        outfile = 'stdout.txt'
        try:
            r = main('..',
                     'Rec2.wav',
                     'audio/wav', 'en-US_BroadbandModel',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out == 'recording is for testing the format of Microsoft please record')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0180_success(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        os.chdir(os.path.dirname(__file__))
        outfile = 'stdout.txt'
        try:
            r = main('..',
                     'Rec3.wav',
                     'audio/wav', 'en-US_BroadbandModel',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out == 'this is a test recording')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0190_success(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        os.chdir(os.path.dirname(__file__))
        outfile = 'stdout.txt'
        try:
            r = main('..',
                     'test0003.mp3',
                     'audio/mp3', 'en-US_BroadbandModel',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out == 'one of the most handy features of any android device is the ability to record yourself there are plenty of reasons for wanting to do so as well musicians may want to record a new idea journalists need to record interviews and some even set it up to see if they talk in their sleep')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
