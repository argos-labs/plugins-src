"""
====================================
 :mod:`argoslabs.data.excelcopy'
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Excel Copy Format
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
#  * [2020/09/14]
#     - build a plugin
#  * [2020/09/14]
#     - starting


################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.data.excelcopy import _main as main


################################################################################
# noinspection PyUnresolvedReferences,PyBroadException
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
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
            r = main(self.clf, '--range', 'A1:c1', '--pasterange', 'F1:h1')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test110_pastevalue(self):
        try:
            r = main(self.clf, '--range', 'A1', '--pasterange', 'F1:J1')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test120_pastevalue(self):
        try:
            r = main('(정산).xlsx', '--sheetname', '서식복사', '--pastesheet',
                     'Sheet1',
                     '--range', 'a4:xx4',
                     '--pasterange', 'a5:xx20', '--newfilename',
                     'newfile.xlsx', '--copyval')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test130_samecol_samecol(self):
        try:
            r = main('sample.xlsx', '--sheetname', 'Sheet1', '--pastesheet',
                     'Sheet2',
                     '--range', 'a:a', '--pasterange', 'b:b', '--newfilename',
                     'newfile.xlsx', )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test140_samecol_diffcol(self):
        try:
            r = main('sample.xlsx', '--sheetname', 'Sheet1', '--pastesheet',
                     'Sheet2',
                     '--range', 'a:a', '--pasterange', 'a:c', '--newfilename',
                     'newfile.xlsx', )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test150_cell_diffcol(self):
        try:
            r = main('sample.xlsx', '--sheetname', 'Sheet1', '--pastesheet',
                     'Sheet2',
                     '--range', 'a4', '--pasterange', 'b1:j10', '--newfilename',
                     'newfile.xlsx', )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test160_diffcol_cell(self):
        try:
            r = main('sample.xlsx', '--sheetname', 'Sheet1', '--pastesheet',
                     'Sheet2',
                     '--range', 'b4:b10', '--pasterange', 'c1', '--newfilename',
                     'newfile.xlsx', )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test170_samecol_cell(self):
        try:
            r = main('sample.xlsx', '--sheetname', 'Sheet1', '--pastesheet',
                     'Sheet2',
                     '--range', 'a:a', '--pasterange', 'c1', '--newfilename',
                     'newfile.xlsx', )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test180_diffcol_samecol(self):
        try:
            r = main('sample.xlsx', '--sheetname', 'Sheet1', '--pastesheet',
                     'Sheet2',
                     '--range', 'a:d', '--pasterange', 'a:a', '--newfilename',
                     'newfile.xlsx', '--copyval')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test190_diffcol_diffcol_smallpaste(self):
        try:
            r = main('sample.xlsx', '--sheetname', 'Sheet1', '--pastesheet',
                     'Sheet2',
                     '--range', 'a1:c7', '--pasterange', 'a1:b3',
                     '--newfilename',
                     'newfile.xlsx', '--copyval')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test200_diffcol_diffcol_largepaste(self):
        try:
            r = main('sample.xlsx', '--sheetname', 'Sheet1',
                     '--range', 'a1:b3', '--pasterange', 'a1:c7',
                     '--newfilename',
                     'newfile.csv', '--copyval', '--dataonly')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test210_diffcol_diffcol_largepaste0(self):
        try:
            r = main('sample.xlsx', '--sheetname', 'Sheet1', '--pastesheet',
                     'Sheet2', '--range', 'a4:xx4', '--newfilename',
                     'newfile.xlsx', '--pasterange', 'a5:xx20', '--copyval',
                     '--dataonly')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test220_diffcol_diffcol_largepaste0(self):
        try:
            r = main('sample.csv',
                     '--range', 'a4:xx4',
                     '--pasterange', 'a5:xx20', '--newfilename',
                     'newfile.xlsx', '--copyval', '--dataonly')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
