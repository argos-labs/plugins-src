"""
====================================
 :mod:`argoslabs.vmoplugins.graphview.tests.test_me`
====================================
.. moduleauthor:: Your Nmae <graph_view_plugin@modify.me>
.. note:: YOURLABS License

Description
===========
YOUR LABS plugin module : unittest
"""

################################################################################
import sys
from unittest import TestCase
from argoslabs.vmoplugins.graphview import _main as main



################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # =========================================================================

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    def test0100_line_chart(self):
        try:
            r = main('line', 'C:/work/bid21108-lowcode/argoslabs/vmoplugins/graphview/tests/input-file/flights.csv', 'C:/work/bid21108-lowcode/argoslabs/vmoplugins/graphview/tests/output-photo')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    def test0101_scatter_chart(self):
        try:
            r = main('scatter', 'C:/work/bid21108-lowcode/argoslabs/vmoplugins/graphview/tests/input-file/attention.csv', 'C:/work/bid21108-lowcode/argoslabs/vmoplugins/graphview/tests/output-photo')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    def test0102_bar_chart(self):
        try:
            r = main('bar', 'C:/work/bid21108-lowcode/argoslabs/vmoplugins/graphview/tests/input-file/flights.csv', 'C:/work/bid21108-lowcode/argoslabs/vmoplugins/graphview/tests/output-photo')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    def test0103_cat_plot(self):
        try:
            r = main('catplot', 'C:/work/bid21108-lowcode/argoslabs/vmoplugins/graphview/tests/input-file/flights.csv', 'C:/work/bid21108-lowcode/argoslabs/vmoplugins/graphview/tests/output-photo')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)