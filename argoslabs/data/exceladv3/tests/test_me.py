"""
====================================
 :mod:`argoslabs.data.json.exceladv3`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Excel Advance III : UnitTest
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
#  * [2020/07/02]pywin32
#     - unittest
#  * [2020/07/02]
#     - starting


################################################################################
import os
import sys
import base64
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.data.exceladv3 import _main as main


################################################################################
# noinspection PyUnresolvedReferences,PyBroadException
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.xlf = 'sample.xlsx'
        cls.clf = 'sample.csv'

    # ==========================================================================
    def test50_missing(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test100_pastevalue(self):
        try:
            r = main(self.xlf, 'Put value/formula', '--sheetname',
                     'Sheet', '--newvalue', '11', '--range', 'A1:b1')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_replace(self):
        try:
            r = main(self.xlf, 'Replace value/formula', '--sheetname', 'Sheet2',
                     '--oldvalue', '3', '--newvalue', "null", '--newfilename',
                     'newfile.xlsx')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    # def test0120_convert_range(self):
    #     try:
    #         r = main(self.xlf, 'Convert str2num',
    #                  '--sheetname', 'Sheet', '--range', 'A1:S38')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0130_convert_cell(self):
    #     try:
    #         r = main(self.xlf, 'Convert str2num',
    #                  '--sheetname', 'Sheet', '--range', 'A1')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0140_convert_string(self):
    #     try:
    #         r = main(self.xlf, 'Convert str2num',
    #                  '--sheetname', 'Sheet', '--range', 'c2')
    #         self.assertTrue(r != 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)
    #
    # # ==========================================================================
    # def test0150_convert_cell(self):
    #     try:
    #         r = main(self.xlf, 'Convert str2num',
    #                  '--sheetname', 'Sheet', '--range', 'A1,B1')
    #         self.assertTrue(r != 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)
    #
    # # ==========================================================================
    def test0160_vlookup(self):
        outfile = 'std.txt'
        try:
            r = main(self.xlf, 'VLOOKUP', '--sheetname', 'Sheet1',
                     '--newcell', 'F5', '--targetcell', 'F4', '--range',
                     'B3:C7',
                     '--index', 2, '--bool', True, '--outfile', 'std.txt')
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.find('C') >= 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # # ==========================================================================
    # def test0170_count(self):
    #     try:
    #         r = main(self.xlf, 'COUNT',
    #                  '--sheetname', 'Sheet', '--range', 'A1:B2', '--range',
    #                  'A3', '--newvalue', '1.3', '--newvalue', 'str',
    #                  '--newcell', 'A10')
    #         self.assertTrue(r == 0)
    #     except ArgsError as a
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0180_counta(self):
    #     try:
    #         r = main(self.xlf, 'COUNTA',
    #                  '--sheetname', 'Sheet', '--range', 'A1:B1', '--range',
    #                  'A3', '--newcell', 'A10')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0190_countif(self):
    #     try:
    #         r = main(self.xlf, 'COUNTIF', '--newcell', 'A5',
    #                  '--sheetname', 'Sheet', '--range', 'A1:B2', '--condition',
    #                  '">10"')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0200_countif_condition_error(self):
    #     try:
    #         r = main(self.xlf, 'COUNTIF', '--newcell', 'A5',
    #                  '--sheetname', 'Sheet', '--range', 'A1:B2', '--condition',
    #                  '100')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0210_sum(self):
    #     try:
    #         r = main(self.xlf, 'SUM',
    #                  '--sheetname', 'Sheet', '--range', 'A1:B2', '--newcell',
    #                  'A10')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0220_sum_newvalue(self):
    #     try:
    #         r = main(self.xlf, 'SUM', '--newcell', 'A10', '--newfilename',
    #                  'newfile.xlsx',
    #                  '--sheetname', 'Sheet', '--range', 'A1:C2', '--range',
    #                  'A3', '--newvalue', '2')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0230_csv_sum_newvalue(self):
    #     try:
    #         r = main(self.clf, 'SUM', '--newcell', 'A10',
    #                  '--range', 'A1:C2', '--range',
    #                  'A3', '--newvalue', '2')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)
    #
    # # ==========================================================================
    # def test0240_csv_paste(self):
    #     try:
    #         r = main(self.clf, 'Put value/formula',
    #                  '--range', 'A1:C2', '--newvalue', '=e2/f2')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)
    #
    # # ==========================================================================
    def test0250_csv_replace_newfilename(self):
        try:
            r = main(self.clf, 'Replace value/formula',
                     '--range', 'A1:S38', '--oldvalue', '100', '--newvalue',
                     'NuLl', '--newfilename', 'new.xlsx')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test0260_csv_convert(self):
    #     try:
    #         r = main(self.clf, 'Convert str2num', '--newfilename',
    #                  'newsample.csv',
    #                  '--range', 'A1:S38')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)
    #
    # # ==========================================================================
    # def test0270_countif(self):
    #     try:
    #         r = main(self.xlf, 'COUNTIF', '--newcell', 'A5',
    #                  '--range', 'A1:B2', '--condition', '66', '--sheetname',
    #                  'Sheet2')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # #
    # # ==========================================================================
    # def test0280_full(self):
    #     try:
    #         r = main(self.clf, 'Fill formula', '--sheetname', 'Sheet',
    #                  '--newvalue', '=C1+d2', '--range', 'A1:b1')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # ==========================================================================
    def test0300_sum(self):
        try:
            r = main('sample.xlsx', 'SUM', '--sheetname', 'Sheet',
                     '--newcell', "e4", '--range', 'a1:a2',
                     '--newvalue', "10",  '--newfilename',
                     'output.xlsx')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0310_encoding_error(self):
    #     try:
    #         r = main('ftr_result.csv', 'SUM', '--encoding', 'cp1252',
    #                  '--newcell', "e3", '--range', 'c:c', '--newfilename',
    #                  'new.xlsx')
    #         self.assertTrue(r != 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0320_unmerge(self):
    #     try:
    #         r = main(self.xlf, 'Unmerge Cells', '--sheetname', 'Sheet3',
    #                  '--range', 'b1:b5','--range', 'a1:a9',
    #                  '--newfilename', 'new.xlsx')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0330_unmerge(self):
    #     try:
    #         r = main(self.xlf, 'Unmerge Cells', '--sheetname', 'Sheet3','--newfilename', 'new.xlsx')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    # # ==========================================================================
    # def test0340_vlookup(self):
    #     try:
    #         r = main('customer_list.csv', 'VLOOKUP',
    #                  '--newcell', 'c1', '--targetcell', '"Foghorn Leghorn"', '--range',
    #                  'a:b', '--index', 2)
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    def test0350_replace(self):
        try:
            r = main('sample.xlsx', 'Replace value/formula',
                        '--oldvalue','=100+100', '--range', 'a1:j30',
                     '--newvalue', 'string',
                     '--newfilename','new.xlsx','--sheetname','Sheet4')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0400_full(self):
        try:
            fml = '=sum(1,2)'
            v = base64.b64encode(fml.encode('utf-8'))
            v = v.decode('ascii')
            r = main('sample.xlsx', 'Fill formula',
                     '--newvalue',v ,'--sheetname','Sheet4',
                     '--range', 'F10')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
