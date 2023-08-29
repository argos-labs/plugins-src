
"""
====================================
 :mod:`argoslabs.datanalysis.pandasbasic`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS data analysis using PANDAS basic
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/02]
#     - 그룹에 "4-Data Science" 넣음
#  * [2020/08/09]
#     - 엑셀에서는 encoding 인자가 없음
#  * [2020/04/27]
#     - pandas_safe_eval 함수 추가
#  * [2020/04/26]
#     - --usecols 옵션 추가
#     - --dtype 옵션 추가
#  * [2020/04/09]
#     - add replace
#  * [2020/04/08]
#     - starting

################################################################################
import os
import sys
import csv
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.datanalysis.pandasbasic import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_failure(self):
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        try:
            r = main('invalid')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success_csv(self):
        outfile = 'stdout.txt'
        try:
            r = main('bar.csv', 'out.csv',
                     '--header', '0',
                     '--filter', "df['Units'].str.startswith('Dollars')",
                     '--filter', "df['Value'] > 1000000",
                     '--select-range', '1:,[2,5,8]',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                self.assertTrue(rs.endswith('out.csv'))
            rows = list()
            with open('out.csv') as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 3 and rows[2][2] == '1239800')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0110_success_csv(self):
        outfile = 'stdout.txt'
        errfile = 'stderr.txt'
        try:
            r = main('foo.xlsx', 'foo.csv',
                     # '--header', '0',
                     '--filter', "df['Item Desc 1'].notnull()",
                     '--filter', "~df['Item Desc 1'].str.contains('ISO')",
                     '--assign', r"IDS1=lambda x: x['Item Desc 1'].str.extract('^([\w\d\.]+)\s')",
                     '--assign', r"IDS2=lambda x: x['Item Desc 1'].str.extract('\s([\d\-.]+)')",
                     '--assign', r"IDS3=lambda x: x['Item Desc 1'].str.extract('^[\w\d\.]+\s[\d\-.]+\s(\w+)')",
                     '--assign', r"IDS4=lambda x: x['Item Desc 1'].str.extract('\s([\d\.]+)$')",
                     '--assign', r"ProductType=lambda x: x['IDS2'].str.extract('^([\d]+)-')",
                     '--assign', r"Grade=lambda x: x['IDS2'].str.extract('-([\d\.]+)$')",
                     '--assign', "Finish=lambda x: np.where(x['IDS3'].isna(), np.nan, np.where(x['IDS3'].str.contains('ZY'),'ZN', np.where(x['IDS3'].str.contains('YZ'),'ZN', np.where(x['IDS3'].str.contains('ZINC'),'ZN', np.where(x['IDS3'].str.contains('P&O'),'PHO', np.where(x['IDS3'].str.contains('Phos'),'PHO', np.where(x['IDS3'].str.contains('Plain'),'PLAIN', np.where(x['IDS3'].str.contains('PLN'),'PLAIN',x['IDS3']))))))))",
                     '--assign', r"Diameter=lambda x: x['IDS1'].str.extract('^M(\d+)X')",
                     '--assign', r"Pitch=lambda x: x['IDS1'].str.extract('X([\d\.]+)X')",
                     '--assign', r"Length=lambda x: x['IDS1'].str.extract('X([\d\.]+)$')",
                     '--assign', "Etc=lambda x: x['IDS4']",
                     '--drop-cols', 'IDS1',
                     '--drop-cols', 'IDS2',
                     '--drop-cols', 'IDS3',
                     '--drop-cols', 'IDS4',
                     '--outfile', outfile,
                     '--errfile', errfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                self.assertTrue(rs.endswith('foo.csv'))
            with open(errfile) as ifp:
                rs = ifp.read()
                self.assertTrue(not rs)
            rows = list()
            with open('foo.csv') as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (17,))
                    rows.append(row)
            self.assertTrue(len(rows) == 1895 and rows[1][2] == 'M6X30 931-10.9 ZN')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0120_success_csv(self):
        outfile = 'stdout.txt'
        try:
            r = main('foo.xlsx', 'foo2.csv',
                     '--header', '0',
                     '--filter', "df['Item Desc 1'].notnull()",
                     '--replace', r"Item Desc 1::='ISO\s',''",
                     '--assign', r"IDS1=lambda x: x['Item Desc 1'].str.extract('^([\w\d\.]+)\s')",
                     '--assign', r"IDS2=lambda x: x['Item Desc 1'].str.extract('\s([\d\-.]+)')",
                     '--assign', r"IDS3=lambda x: x['Item Desc 1'].str.extract('^[\w\d\.]+\s[\d\-.]+\s(\w+)')",
                     '--assign', r"IDS4=lambda x: x['Item Desc 1'].str.extract('\s([\d\.]+)$')",
                     '--assign', r"ProductType=lambda x: x['IDS2'].str.extract('^([\d]+)-')",
                     '--assign', r"Grade=lambda x: x['IDS2'].str.extract('-([\d\.]+)$')",
                     '--assign', "Finish=lambda x: np.where(x['IDS3'].isna(), np.nan, np.where(x['IDS3'].str.contains('ZY'),'ZN', np.where(x['IDS3'].str.contains('YZ'),'ZN', np.where(x['IDS3'].str.contains('ZINC'),'ZN', np.where(x['IDS3'].str.contains('P&O'),'PHO', np.where(x['IDS3'].str.contains('Phos'),'PHO', np.where(x['IDS3'].str.contains('Plain'),'PLAIN', np.where(x['IDS3'].str.contains('PLN'),'PLAIN',x['IDS3']))))))))",
                     '--assign', r"Diameter=lambda x: x['IDS1'].str.extract('^M(\d+)X')",
                     '--assign', r"Pitch=lambda x: x['IDS1'].str.extract('X([\d\.]+)X')",
                     '--assign', r"Length=lambda x: x['IDS1'].str.extract('X([\d\.]+)$')",
                     '--assign', r"Etc=lambda x: x['IDS4'].str.replace('^(\.\d+)',r'0\1')",
                     '--drop-cols', 'IDS1',
                     '--drop-cols', 'IDS2',
                     '--drop-cols', 'IDS3',
                     '--drop-cols', 'IDS4',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            rows = list()
            with open('foo2.csv') as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (17,))
                    rows.append(row)
            self.assertTrue(len(rows) == 1988 and rows[-1][2] == 'M20X1.5X200 961-8.8')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0130_success_xlsx(self):
        outfile = 'stdout.txt'
        try:
            r = main('foo.xlsx', 'foo3.csv',
                     '--sheet-name', '견적서 원본',
                     '--header', '0',
                     '--filter', "df['Item Desc 1'].notnull()",
                     '--replace', r'Item Desc 1::="ISO\s",""',
                     '--assign', r"IDS1=lambda x: x['Item Desc 1'].str.extract('^([\w\d\.]+)\s')",
                     '--assign', r"IDS2=lambda x: x['Item Desc 1'].str.extract('\s([\d\-.]+)')",
                     '--assign', r"IDS3=lambda x: x['Item Desc 1'].str.extract('^[\w\d\.]+\s[\d\-.]+\s(\w+)')",
                     '--assign', r"IDS4=lambda x: x['Item Desc 1'].str.extract('\s([\d\.]+)$')",
                     '--assign', r"ProductType=lambda x: x['IDS2'].str.extract('^([\d]+)-')",
                     '--assign', r"Grade=lambda x: x['IDS2'].str.extract('-([\d\.]+)$')",
                     '--assign', "Finish=lambda x: np.where(x['IDS3'].isna(), np.nan, np.where(x['IDS3'].str.contains('ZY'),'ZN', np.where(x['IDS3'].str.contains('YZ'),'ZN', np.where(x['IDS3'].str.contains('ZINC'),'ZN', np.where(x['IDS3'].str.contains('P&O'),'PHO', np.where(x['IDS3'].str.contains('Phos'),'PHO', np.where(x['IDS3'].str.contains('Plain'),'PLAIN', np.where(x['IDS3'].str.contains('PLN'),'PLAIN',x['IDS3']))))))))",
                     '--assign', r"Diameter=lambda x: x['IDS1'].str.extract('^M(\d+)X')",
                     '--assign', r"Pitch=lambda x: x['IDS1'].str.extract('X([\d\.]+)X')",
                     '--assign', r"Length=lambda x: x['IDS1'].str.extract('X([\d\.]+)$')",
                     '--assign', r'Etc=lambda x: x["IDS4"].str.replace("^(\.\d+)",r"0\1")',
                     '--drop-cols', 'IDS1',
                     '--drop-cols', 'IDS2',
                     '--drop-cols', 'IDS3',
                     '--drop-cols', 'IDS4',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            rows = list()
            with open('foo3.csv') as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (17,))
                    rows.append(row)
            self.assertTrue(len(rows) == 1988 and rows[-1][2] == 'M20X1.5X200 961-8.8')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0140_success_xlsm(self):
        outfile = 'stdout.txt'
        try:
            r = main('macro01.xlsm', 'macro01.csv',
                     '--sheet-name', 'Result',
                     '--header', '13',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            rows = list()
            with open('macro01.csv', encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (15, 16))
                    rows.append(row)
            self.assertTrue(len(rows) == 39 and rows[-1][-3] == '14')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
