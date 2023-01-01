"""
====================================
 :mod:`argoslabs.file.snippingtool`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module: unittest
"""

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.file.snippingtool import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        os.chdir(os.path.dirname(__file__))
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        try:
            r = main('C:/work/hello.bmt')
            self.assertTrue(r == 0)
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    # def test0100_text_success(self):
    #     outfile = 'stdout.txt'
    #     try:
    #         r = main('--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         print(out)
    #         # self.assertTrue(out.endswith('C:\\Users\\Administrator\\Documents\\DragAndDrop\\image.png'))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(outfile):
    #             os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
