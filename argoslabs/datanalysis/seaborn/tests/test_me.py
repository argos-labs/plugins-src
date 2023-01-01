#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:argoslabs.datanalysis.seaborn
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.datanalysis.seaborn import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0001_failure(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test050_(self):
        try:
            r = main('name.csv',
                     'Kilograms', '--y', 'Centimeters',
                     '--relational-plots', 'relplot',
                     '--output', 'sample.png')
            self.assertFalse(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_relplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--relational-plots', 'relplot',
                     '--output', 'relplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_relplot_sheet(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--relational-plots', 'relplot',
                     '--sheet-name', 'Sheet2',
                     '--output', 'relplot1.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_relplot_sheet_hue(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--relational-plots', 'relplot',
                     '--sheet-name', 'Sheet2',
                     '--hue', 'dataset',
                     '--output', 'relplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_relplot_hue_all_Style(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--relational-plots', 'relplot',
                     '--sheet-name', 'Sheet2',
                     '--hue', 'dataset',
                     '--output', 'relplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test200_scatterplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--relational-plots', 'scatterplot',
                     '--output', 'scatterplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test300_lineplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--relational-plots', 'lineplot',
                     '--output', 'lineplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test400_displot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--distribution-plots', 'displot',
                     '--output', 'displot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test500_histplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--distribution-plots', 'histplot',
                     '--output', 'histplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test600_ecdfplot(self):     # x축 or y축 둘중하나만 사용해야함
        try:
            r = main('anscombe.csv',
                     'x',
                     '--distribution-plots', 'ecdfplot',
                     '--output', 'ecdfplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test700_rugplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--distribution-plots', 'rugplot',
                     '--output', 'rugplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test800_catplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--categorical-plots', 'catplot',
                     '--output', 'catplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test900_stripplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--categorical-plots', 'stripplot',
                     '--output', 'stripplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1000_swarmplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--categorical-plots', 'swarmplot',
                     '--output', 'swarmplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1100_boxplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--categorical-plots', 'boxplot',
                     '--output', 'boxplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1200_violinplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--categorical-plots', 'violinplot',
                     '--output', 'violinplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1300_boxenplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--categorical-plots', 'boxenplot',
                     '--output', 'boxenplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1400_pointplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--categorical-plots', 'pointplot',
                     '--output', 'pointplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1500_barplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--categorical-plots', 'barplot',
                     '--output', 'barplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1600_lmplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--regression-plots', 'lmplot',
                     '--output', 'lmplot.png',
                     '--title', 'title size',
                     '--title-fontsize', '30',
                     '--xlabel', 'x axis',
                     '--xfontsize', '20',)
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1700_regplot(self):
        try:
            r = main('anscombe.csv',
                     'x', '--y', 'y',
                     '--title', 'size None',
                     '--title-fontsize', 20,
                     '--regression-plots', 'regplot',
                     '--output', 'regplot.png')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1800_residplot(self):
        try:
            r = main('C:\\Users\\argos\\Desktop\\bongsplugin\\plug-in-test\\seaborn\\anscombe.csv',
                     'x', '--y', 'y',
                     '--regression-plots', 'residplot',)
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
