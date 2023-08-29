#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:argoslabs.turvo.shipment
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
from argoslabs.turvo.shipment import _main as main
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
    def test0100_delete_shipments(self):
        try:
            r = main('Delete Shipment',
                     '..',
                     'http://my-sandbox.turvo.com/api/pub',
                     '--shipment_id', '38674', '--shipment_id', '38672',
                     '--shipment_id', '38671', '--shipment_id', '38560',
                     '--shipment_id', '38551')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_create(self):
        try:
            r = main('Create Shipment',
                     '..',
                     'http://my-sandbox.turvo.com/api/pub', )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_success(self):
        try:
            r = main('Create Shipment',
                     '..',
                     'http://my-sandbox.turvo.com/api/pub',
                     '--ltlshipment', True, '--startdate', '2021-02-01',
                     '--enddate', '2021-02-29', '--timezone',
                     'America/New_York',
                     '--statuskey', 1231, '--status_value', 'Tendered',
                     '--equipment_key', 1200, '--equipment_value', '$10',
                     '--start_lane', 'Seoul, KR', '--end_lane',
                     'Los Angeles, USA',
                     '--customer_id', '65475')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_create_using_json(self):
        try:
            r = main('Create Shipment',
                     '..',
                     'http://my-sandbox.turvo.com/api/pub',
                     '--shipment_json', 'data.json')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_retrieve(self):
        try:
            r = main('Retrieve Shipment',
                     '..',
                     'http://my-sandbox.turvo.com/api/pub',
                     '--shipment_id', '38664')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_create(self):
        try:
            r = main('Create Shipment',
                     '..',
                     'http://my-sandbox.turvo.com/api/pub', '--startdate',
                     '1/5/2021', '--enddate', '1/6/2021', '--start_lane',
                     'US COLD STORAGE - FRESN 2519 E. NORTH AVENUE FRESNO, CA,93725',
                     '--end_lane', 'Kroger-Compton, CA Ralphs Deli Compton '
                                   '2201 S Willmington Ave Compton, CA,90220',
                     '--customer_id', '65543')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)