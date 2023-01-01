#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.mygroup.regresson`
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
from argoslabs.datanalysis.regression import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # @classmethod
    # def setUpClass(cls) -> None:
    #     #os.chdir(os.path.dirname(__file__))
    #     os.chdir(r'W:\ARGOS-LABS\src\plugins\argoslabs\datanalysis\regression\tests')

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
            r = main('processed_dt.csv', 'confirmed_cases', 'Compare Models',
                     '--drop', 'Country', '--drop', 'date')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_diamond_csv(self):
        try:
            r = main('diamond.csv', 'Price', 'Compare Models',
                     '--onehotencoding', 'True')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_fit_model_onehotencoding(self):
        try:
            r = main('diamond.csv', 'Price', 'Fit Model',
                     '--normalize', 'False', '--plotoutput', 'output.png',
                     '--plottype', 'Residuals', '--onehotencoding', 'True',
                     '--modeltype',
                     'LinearRegression')
            self.assertTrue(r == 0)

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_fit_model_nonnormal(self):
        try:
            r = main('processed_dt.csv', 'confirmed_cases', 'Fit Model',
                     '--normalize', 'False',
                     '--drop', 'Country', '--drop', 'date', '--modeltype',
                     'LinearRegression')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_fit_model_with_Residulas_plot(self):
        try:
            r = main('processed_dt.csv', 'confirmed_cases', 'Fit Model',
                     '--drop', 'Country', '--drop', 'date',
                     '--plotoutput', 'output.png', '--modeltype',
                     'LinearRegression', '--plottype', 'Residuals')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_fit_model_with_PredictError_plot(self):
        try:
            r = main('processed_dt.csv', 'confirmed_cases', 'Fit Model',
                     '--drop', 'Country', '--drop', 'date',
                     '--plotoutput', 'output.png', '--modeltype',
                     'LinearRegression', '--plottype', 'PredictionError',
                     '--normalize', 'True')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_fit_model_with_Cookdist_plot(self):
        try:
            r = main('processed_dt.csv', 'confirmed_cases', 'Fit Model',
                     '--drop', 'Country', '--drop', 'date', '--modeltype',
                     'LinearRegression', '--plotoutput', 'CooksDistance.png',
                     '--plottype', 'CooksDistance')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_fit_model_with_Residual_plot(self):
        try:
            r = main('processed_dt.csv', 'confirmed_cases', 'Fit Model',
                     '--drop', 'Country', '--drop', 'date', '--modeltype',
                     'Lasso', '--plottype', 'Residuals')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_xlsx(self):
        try:
            r = main('processed_dt.xlsx', 'confirmed_cases', 'Fit Model',
                     '--drop', 'Country', '--drop', 'date', '--modeltype',
                     'Lasso', '--plotoutput', 'output.png', '--plottype',
                     'Residuals')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0180_diamond_csv_fit_model(self):
        try:
            r = main('diamond.csv', 'Price', 'Fit Model', '--modeltype',
                     'AdaBoost', '--onehotencoding', 'True')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0190_diamond_csv_fit_model_plot(self):
        try:
            r = main('diamond.csv', 'Price', 'Fit Model', '--modeltype',
                     'AdaBoost', '--onehotencoding', 'True', '--plotoutput',
                     'output.png',
                     '--plottype', 'Residuals')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_xlsx(self):
        try:
            r = main('processed_dt.xlsx', 'confirmed_cases', 'Fit Model',
                     '--drop', 'Country', '--drop', 'date', '--modeltype',
                     'Lasso', '--test_size', '0.1', '--seed', '12')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_diamond_csv_svm(self):
        try:
            r = main('processed_dt.xlsx', 'confirmed_cases', 'Fit Model',
                     '--drop', 'Country', '--drop', 'date', '--modeltype',
                     'SupportVectorMachine', '--test_size', '0.1', '--seed',
                     '12')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_diamond_csv_huber(self):
        try:
            r = main('processed_dt.xlsx', 'confirmed_cases', 'Fit Model',
                     '--drop', 'Country', '--drop', 'date', '--modeltype',
                     'Huber', '--test_size', '0.1', '--seed', '12')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
