#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:argoslabs.turvo.updoc
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
from argoslabs.turvo.updoc import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    key_id = None
    key = None

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('invalid')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success(self):
        try:
            r = main('Other', '..',
                     'http://my-sandbox.turvo.com/api/pub', 'sample.pdf',
                     '--shipment_id', '38674', )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success(self):
        try:
            r = main('Proof of Delivery',
                     '..',
                     'http://my-sandbox.turvo.com/api/pub',
                     'sample.pdf', 'sample0.png', '--shipment_id', '38674')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_success(self):
        try:
            r = main('Other', '..',
                     'http://my-sandbox.turvo.com/api/pub', 'sample.pdf',
                     '--shipment_id', '38674', '--name', 'Other0',
                     '--description',
                     'descriptions', '--account_name', "Customer-Waldbart")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_success(self):
        try:
            r = main('Proof of Delivery', '..',
                     'http://my-sandbox.turvo.com/api/pub', 'sample.pdf',
                     '--shipment_id', '38674', '--name', 'Proof1',
                     '--description',
                     'descriptions', '--account_name', "Customer-Waldbart")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
