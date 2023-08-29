
"""
====================================
 :mod:`argoslabs.datanalysis.pandas2`
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
#  * [2020/09/11]
#     - "Header" => "Header Row", "Out Index" => "Show Index"
#  * [2020/09/09]
#     - add --stat-file
#  * [2020/08/09]
#     - starting

################################################################################
import os
import sys
import csv
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.datanalysis.pandas2 import _main as main


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
            r = main('SHDATA20200404.xlsx', 'SHDATA20200404.csv',
                     '--stats', r"df = df.assign(IDS1=lambda x: x['Item Desc 1'].str.extract('^([\w\d\.]+)\s'),IDS2=lambda x: x['Item Desc 1'].str.extract('^[\w\d\.]+\s(\d+[- ][\d\.]+)'),IDS3=lambda x: x['Item Desc 1'].str.extract('^[\w\d\.]+\s\d+[- ][\d\.]+\s(ZN|ZY|YZ|ZINC|P&O|PHO|Phos|PLAIN|Plain|PLN)'),IDS4=lambda x: x['Item Desc 1'].str.extract('^[\w\d\.]+\s\d+[- ][\d\.]+\s(.+)$'))",
                     '--stats', r"df = df.assign(ProductType=lambda x: x['IDS2'].str.extract('^([\d]+)[- ]'),Grade=lambda x: x['IDS2'].str.extract('[- ]([\d\.]+)$'),Finish=lambda x: x['IDS4'].str.extract('(ZN|ZY|YZ|ZINC|P&O|PHO|Olive|Drab|GEOMET 500A|GEOMET 500B|PLAIN|Plain|PLN)'),Diameter=lambda x: 'M' + x['IDS1'].str.extract('^M(\d+)X'),Pitch1=lambda x: x['IDS1'].str.len(),Pitch2=lambda x: x['IDS1'].str.extract('X([\d\.]+)X'),Length=lambda x: x['IDS1'].str.extract('X([\d\.]+)$'),Etc=lambda x: x['IDS4'])",
                     '--stats', r"df = df.drop(columns=['IDS1', 'IDS2', 'IDS3', 'IDS4'])",
                     '--stats', r"df['Finish'] = df['Finish'].fillna('PLAIN')",
                     '--stats', r"df.loc[df['Item Desc 1'].isnull(), 'Finish'] = np.nan",
                     '--stats', r"df['Etc'] = df['Etc'].str.replace('^(ZN\s*|ZY\s*|YZ\s*|ZINC\s*|P&O\s*|PHO\s*|Phos\s*|PLAIN\s*|Plain\s*|PLN\s*)','')",
                     '--stats', r"df['Etc'] = df['Etc'].str.replace('^(\.\d+)$',r'0\1')",
                     '--stats', r"df['Pitch1'] = df['Pitch1'].replace(np.nan, '')",
                     '--stats', r"df['Pitch1'] = df['Pitch1'].str.replace('^([1-9]+)',r'X')",
                     '--stats', r"df['Pitch1'] = df['Pitch1'].replace(np.nan, 'X')",
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            rows = list()
            with open('SHDATA20200404.csv', encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (18,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2562 and
                            rows[519][-1] == 'PRINT# X4378639')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0110_success_csv(self):
        outfile = 'stdout.txt'
        try:
            r = main('SHDATA20200404.xlsx', 'SHDATA20200404.csv',
                     '--stat-file', "pandas2-body.py",
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            rows = list()
            with open('SHDATA20200404.csv', encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (18,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2562 and
                            rows[519][-1] == 'PRINT# X4378639')
            with open(outfile, encoding='utf-8') as ifp:
                rstr = ifp.read()
                self.assertTrue(rstr == os.path.abspath('SHDATA20200404.csv'))
                # print(rstr)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0120_success_stat_file(self):
        outfile = 'stdout.txt'
        try:
            r = main('PAYNET Template.xlsx', 'PAYNET Template-out.xlsx',
                     '--stats', "df = df[df['Amount (INR)'].notna()]",
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            # rows = list()
            # with open('result.csv', encoding='utf-8') as ifp:
            #     cr = csv.reader(ifp)
            #     for ndx, row in enumerate(cr):
            #         self.assertTrue(len(row) in (37,))
            #         rows.append(row)
            # self.assertTrue(len(rows) == 178 and
            #                 rows[-1][-1] == '3다가구')
            # with open(outfile, encoding='utf-8') as ifp:
            #     rstr = ifp.read()
            #     self.assertTrue(rstr == os.path.abspath('result.csv'))
                # print(rstr)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
