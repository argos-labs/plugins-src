#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.datanalysis.regressor`
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
from argoslabs.datanalysis.regressor import _main as main
from alabs.common.util.vvargs import ArgsError



################################################################################
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

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
    def test0100_compare_models(self):
        try:
            r = main('processed_dt.csv','confirmed_cases','Compare Models',
                     '--drop','Country','--drop','date')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_fit_model(self):
        outfile = 'output1.txt'
        try:
            r = main('processed_dt.csv','confirmed_cases','Fit Model',
                     '--drop','Country','--drop','date','--modeltype',
                     'LinearRegression')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_fit_model_with_plot(self):
        outfile = 'output1.txt'
        try:
            r = main('processed_dt.csv','confirmed_cases','Fit Model',
                     '--drop','Country','--drop','date','--modeltype',
                     'LinearRegression','--plottype','Residuals')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_fit_model_with_plot(self):
        try:
            r = main('processed_dt.csv','confirmed_cases','Fit Model',
                     '--drop','Country','--drop','date','--modeltype',
                     'LinearRegression','--plottype','PredictionError')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_fit_model_with_plot(self):
        outfile = 'output1.txt'
        try:
            r = main('processed_dt.csv','confirmed_cases','Fit Model',
                     '--drop','Country','--drop','date','--modeltype',
                     'LinearRegression','--plottype','CooksDistance')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_fit_model_with_plot(self):
        try:
            r = main('processed_dt.csv','confirmed_cases','Fit Model',
                     '--drop','Country','--drop','date','--modeltype',
                     'Lasso','--plottype','Residuals')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
