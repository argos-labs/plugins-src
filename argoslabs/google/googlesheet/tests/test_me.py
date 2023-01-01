"""
====================================
 :mod:`argoslabs.google.googlesheet`
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
import random
from unittest import TestCase
from argoslabs.google.googlesheet import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):
    isFirst = True
    spreadsheet_id = None
    new_spreadsheet_id = None

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.spreadsheet_id = ''
        cls.new_spreadsheet_id = ''

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
    def test0100_call_spreadsheet(self):
        outfile = 'stdout.txt'
        try:
            r = main('Read a Spreadsheet', 'token.pickle', '--spreadsheet_id',
                     TU.spreadsheet_id, '--range', 'diamond!A1:B3',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.find('Carat') >= 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0110_create_spreadsheet(self):
        try:
            r = main('Create a Spreadsheet', 'token.pickle',
                     '--title', 'New Test Sheet')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_write_spreadsheet(self):
        try:
            r = main('Write a Spreadsheet', 'token.pickle',
                     '--spreadsheet_id', '15F67unOvjSLGT25sQ0s1R_evVFYi33Gt2jY1nORJAro',
                     '--range', 'Sheet1', '--csvfile', 'names_and_emails.csv')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_addsheet(self):
        try:
            r = main('Add a Sheet', 'token.pickle',
                     '--spreadsheet_id', TU.new_spreadsheet_id,
                     '--sheetitle', random.randint(1,100000))
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_deletesheet(self):
        try:
            r = main('Delete a Sheet', 'token.pickle',
                     '--spreadsheet_id', TU.new_spreadsheet_id,
                     '--sheetid', '1966448009')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_renamesheet(self):
        try:
            r = main('Rename a Sheet', 'token.pickle',
                     '--spreadsheet_id', TU.new_spreadsheet_id,
                     '--sheetid', 31648, '--sheetitle', 'new_sheet10')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_chagetitle(self):
        try:
            r = main('Rename a Spreadsheet', 'token.pickle',
                     '--spreadsheet_id', TU.new_spreadsheet_id,
                     '--title', 'New Sheet')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_duplicate_sheet(self):
        try:
            r = main('Duplicate a Sheet', 'token.pickle',
                     '--spreadsheet_id', TU.new_spreadsheet_id,
                     '--sheetid',1668664510,'--sheetitle', random.randint(1,100000))
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0180_findreplace(self):
        try:
            r = main('Find and Replace', 'token.pickle',
                     '--spreadsheet_id', TU.new_spreadsheet_id,
                     '--find', 'otis', '--replace', 'jason', '--allSheets')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0190_findreplace(self):
        try:
            r = main('Find and Replace', 'token.pickle',
                     '--spreadsheet_id', TU.new_spreadsheet_id,
                     '--find', 'otis', '--replace', 'jason')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_addsheet(self):
        try:
            r = main('Add a Sheet', 'token.pickle',
                     '--spreadsheet_id', TU.new_spreadsheet_id,
                     '--sheetid', random.randint(1,100000),
                     '--sheetitle', random.randint(1,100000))
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_findreplace(self):
        try:
            r = main('Find and Replace', 'token.pickle',
                     '--spreadsheet_id', TU.new_spreadsheet_id,
                     '--find', 'otis', '--replace', 'jason','--sheetid',1668664510)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_duplicate_sheet(self):
        try:
            r = main('Duplicate a Sheet', 'token.pickle',
                     '--spreadsheet_id', TU.new_spreadsheet_id,'--index','3',
                     '--sheetid',1668664510,'--sheetitle', random.randint(1,100000))
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0230_write_spreadsheet(self):
        try:
            r = main('Write a Spreadsheet', 'token.pickle',
                     '--spreadsheet_id', '15F67unOvjSLGT25sQ0s1R_evVFYi33Gt2jY1nORJAro',
                     '--range', 'Sheet1', '--csvfile', '계정설정.xlsx','--xlsxsheetname',
                     'Sheet1')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

