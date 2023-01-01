#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:argoslabs.web.bsoup_table
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
from argoslabs.web.bsoup_table import _main as main


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
    def test0100_all_tab(self):
        try:
            r = main('--filepath', 'sample1.html',)
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0110_idx_tab(self):
    #     try:
    #         r = main('--filepath', 'sample3.html',
    #                  # '--idx', '1',
    #                   '--idx','2',
    #                   # '--rng', '3:4'
    #                  )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0120_str_tab(self):
        try:
            r = main('--filepath', 'sample3.html', '--substr', 'US 30')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_str_tab(self):
        try:
            r = main('--filepath', 'input.html', '--idx', 1)
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_url(self):
        try:
            r = main('--url', 'https://www.investing.com/indices/indices-futures',
                     '--idx', '1')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

