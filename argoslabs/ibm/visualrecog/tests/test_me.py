
"""
====================================
 :mod:`argoslabs.ibm.visualrecog`
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
# TODO: warning: On 1 December 2021, Visual Recognition will no longer
#  be available. For more information,
#  see https://github.com/watson-developer-cloud/python-sdk/tree/master#visual-recognition-deprecation.
#
#  * [2021/04/08]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2020/03/05]
#     - change DisplayName starting with "IBM "
#  * [2020/01/23]
#     - change call parameters
#  * [2019/08/11]
#     - finish
#  * [2019/08/10]
#     - starting

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.ibm.visualrecog import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def setUp(self) -> None:
        return super().setUp()
    
    # ==========================================================================
    def test0000_init(self):
        os.chdir(os.path.dirname(__file__))
        self.assertTrue(True)

    # ==========================================================================
    def test0010_failure(self):
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        try:
            r = main('invalid', 'invalid_image')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0030_failure(self):
        try:
            r = main('..', 'invalid_image')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0040_failure(self):
        try:
            r = main('..',
                     'ROAD-SIGN-2-ALAMY_2699740b.jpg',
                     '--threshold', '1.1')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        try:
            r = main('..',
                     'ROAD-SIGN-2-ALAMY_2699740b.jpg',
                     '--threshold', '-0.1')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test0100_success(self):
    #     sg = sys.gettrace()
    #     if sg is None:  # Not in debug mode
    #         print('Skip testing at test/build time')
    #         return
    #     outfile = 'stdout.txt'
    #     try:
    #         r = main('..',
    #                  'ROAD-SIGN-2-ALAMY_2699740b.jpg',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile) as ifp:
    #             print(ifp.read())
    #         with open(outfile) as ifp:
    #             rows = list()
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (3,))
    #                 rows.append(row)
    #             self.assertTrue(len(rows) in (8, 9))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(outfile):
    #             os.remove(outfile)

    # # ==========================================================================
    # def test0110_success_with_threshold(self):
    #     sg = sys.gettrace()
    #     if sg is None:  # Not in debug mode
    #         print('Skip testing at test/build time')
    #         return
    #     outfile = 'stdout.txt'
    #     try:
    #         r = main('..',
    #                  'ROAD-SIGN-2-ALAMY_2699740b.jpg',
    #                  '--threshold', '0.6',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile) as ifp:
    #             print(ifp.read())
    #         with open(outfile) as ifp:
    #             rows = list()
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (3,))
    #                 rows.append(row)
    #             self.assertTrue(len(rows) in (3, 5))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(outfile):
    #             os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
