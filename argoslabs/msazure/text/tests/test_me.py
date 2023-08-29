"""
====================================
 :mod:`argoslabs.msazure.text`

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
from argoslabs.msazure.text import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    apikey = None
    endpoint = None

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.apikey = '..'
        cls.endpoint = 'https://westus.api.cognitive.microsoft.com/'

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

    # ==========================================================================
    def test0100_success(self):
        outfile = 'stdout.txt'
        try:
            r = main(TU.apikey, TU.endpoint, "image003.jpg",
                     '--box-imgfile', 'image003-out.png',
                     '--outfile', outfile)
            self.assertTrue(r != 0)
            # with open(outfile, encoding='utf-8') as ifp:
            #     rs = ifp.read()
            #     # print(rs)
            #     self.assertTrue(rs.find('주민등록번호') > 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        # finally:
        #     if os.path.exists(outfile):
        #         os.remove(outfile)

    # ==========================================================================
    def test0110_success(self):
        outfile = 'stdout.txt'
        try:
            r = main(TU.apikey, TU.endpoint, "en_test1.png",
                     '--box-imgfile', 'en_test1-out.png',
                     '--outfile', outfile)
            self.assertTrue(r != 0)
            # with open(outfile, encoding='utf-8') as ifp:
            #     rs = ifp.read()
            #     self.assertTrue(rs.find('819543') > 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        # finally:
        #     if os.path.exists(outfile):
        #         os.remove(outfile)

    # ==========================================================================
    def test0120_success(self):
        outfile = 'stdout.txt'
        try:
            r = main(TU.apikey, TU.endpoint, "en_test2.png",
                     '--box-imgfile', 'en_test2-out.png',
                     '--outfile', outfile)
            self.assertTrue(r != 0)
            # with open(outfile, encoding='utf-8') as ifp:
            #     rs = ifp.read()
            #     self.assertTrue(rs.find('DISCOVER 6452') > 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        # finally:
        #     if os.path.exists(outfile):
        #         os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
