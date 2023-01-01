#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:argoslabs.datanalysis.matplotlib
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
from argoslabs.datanalysis.matplotlib import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_col_error_no_header(self):
        try:
            r = main('Scatter', 'name.csv', '100', '--pd_ycol', '3',
                     '--output', 'sample.png', '--no_header')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_col_error(self):
        try:
            r = main('Scatter', 'name.csv', 'Age','--pd_ycol', 'Kilogram',
                     '--output', 'sample.png')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)


    # ==========================================================================
    def test0120_linear(self):
        try:
            r = main('Linear', 'name.xlsx',  'Age', '--pd_ycol', 'Centimeters',
                     '--ylabel', 'ylabel', '--title', 'Title',
                     '--sheet-name', 'Sheet1')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_bar(self):
        try:
            r = main('Bar', 'sample.csv',  '4', '--pd_ycol', '0',
                     '--no_header',
                     '--ylabel', 'ylabel', '--title', 'Title',
                     '--plot_label', 'data1')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_pie(self):
        try:
            r = main('Pie', 'sample.csv',  '0',
                     '--ylabel', 'ylabel', '--title', 'Title',
                     '--pie_label', 'data1', '--pie_label', 'data2',
                     '--pie_label', 'data3', '--pie_label', 'data4',
                     '--no_header',
                     '--output', 'sample.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_scatter_xlsx(self):
        try:
            r = main('Scatter', 'name.xlsx', 'Age', '--pd_ycol', 'Centimeters',
                     '--ylabel', 'ylabel', '--title', 'Title',
                     '--plot_label', 'data1',
                     '--sheet-name', 'Sheet1',
                     '--output', 'sample.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_scatter_xlsx_error(self):
        try:
            r = main('Scatter', 'name.xlsx', 'Age',
                     '--pd_ycol', 'Centimeters',
                     '--sheet-name', 'Sheet')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0170_output_error(self):
        try:
            r = main('Linear', 'name.csv',   'Age',
                     '--pd_ycol', 'Kilograms',
                     '--output', 'sample.pn')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0180_property_error(self):
        try:
            r = main('Linear', 'name.csv',   'Age',
                     '--pd_ycol', 'Kilograms', '--xticks', '100,1',
                     '--ylabel', 'ylabel', '--title', 'Title')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0190_pie_error(self):
        try:
            r = main('Pie', 'name.csv','Number[1:4]',
                     '--pie_label', 'data1', )
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0200_figure_size(self):
        try:
            r = main('Pie', 'name.csv','Number[1:3]',
                     '--ylabel', 'ylabel', '--title', 'Title',
                     '--pie_label', 'data1', '--pie_label', 'data2',
                     '--figsize', '5,9')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
