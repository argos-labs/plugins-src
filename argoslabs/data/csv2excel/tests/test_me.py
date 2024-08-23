"""
====================================
 :mod:`argoslabs.data.csv2xlsx'
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for converting csv to xlsx
"""
#
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2021/03/27] Jerry Chae
#     - 그룹에 "6-Files and Folders" 넣음
#  * [2020/09/23]
#     - build a plugin
#  * [2020/09/23]
#     - starting


################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.data.csv2excel import _main as main


################################################################################
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0050_missing(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0080_pastevalue(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            # only CSV is allowed for source
            r = main('randomalphabet.xlsx', '--newfilename', 'new.csv')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_list_format(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            stdout = 'stdout.txt'
            r = main('randomalphabet.csv', '--list-format',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs.find('yyyy-mm-dd') > 0)

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0110_success(self):
    #     try:
    #         stdout = 'stdout.txt'
    #         r = main('randomalphabet.csv', '--newfilename', 'new.xlsx', '--range',
    #                  'a:b',
    #                  '--format', 'yyyy-mm-dd', '--range', 'e:f', '--format',
    #                  '0%',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #         self.assertTrue(os.path.abspath(rs) == os.path.abspath('new.xlsx'))

    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0120_success(self):
    #     try:
    #         stdout = 'stdout.txt'
    #         r = main('ear_result.csv', '--newfilename', 'new2.xlsx',
    #                  '--range', 'a:a', '--format', 'yyyy-mm-dd',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #         self.assertTrue(os.path.abspath(rs) == os.path.abspath('new2.xlsx'))
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0130_success(self):
    #     try:
    #         stdout = 'stdout.txt'
    #         r = main('randomalphabet.csv',
    #                  '--range', 'e1', '--format', '0%',
    #                  '--range', 'c1', '--format', '"$"#,##0.00_-',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #         self.assertTrue(os.path.abspath(rs) == os.path.abspath('randomalphabet.xlsx'))
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0140_debug_shige(self):
    #     try:
    #         stdout = 'stdout.txt'
    #         r = main('ss_sample.csv',
    #                  '--range', 'g', '--format', 'mm-dd-yy',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #         self.assertTrue(os.path.abspath(rs) == os.path.abspath('ss_sample.xlsx'))
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
