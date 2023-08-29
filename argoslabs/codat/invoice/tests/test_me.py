#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:argoslabs.codat.invoice
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Irene Cho
#
# --------
#
#  * [2021/03/27]
#     - 그룹에 "3-Cloud Solutions" 넣음
#  * [2021/01/25]
#     - starting

################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.codat.invoice import _main as main
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
        cls.endpoint = 'https://api-uat.codat.io'
        cls.api_key = '..'
        cls.company_id = '..'
        cls.connection_id = '..'

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('invalid')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_get_connection_id(self):
        try:
            r = main('Get Connection ID', self.endpoint, self.api_key,
                     self.company_id)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0110_create(self):
    #     try:
    #         r = main('Create Invoice', self.endpoint, self.api_key,
    #                  self.company_id, '--connection_id', self.connection_id,
    #                  '--customer_id', '06bf0258-4a11-4a44-b141-a991fcb1d7c7')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0120_retrieve_w_invoice_id(self):
    #     try:
    #         r = main('Retrieve Invoice', self.endpoint, self.api_key,
    #                  self.company_id, '--invoice_id', 'bba8a30b-0b5b-42c4-b62c-bbc3277f4b7f',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0130_retrieve_wo_invoice_id(self):
        try:
            r = main('Retrieve Invoice', self.endpoint, self.api_key,
                     self.company_id)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0140_retrieve_w_invoice_id(self):
    #     try:
    #         r = main('Retrieve Invoice', self.endpoint, self.api_key,
    #                  self.company_id, '--invoice_id', '93f34f2a-ab75-4266-96ee-ed1f6db83e62')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0150_create_using_json(self):
    #     try:
    #         r = main('Create Invoice', self.endpoint, self.api_key,
    #                  self.company_id, '--connection_id', self.connection_id,
    #                  '--invoice_json', 'strmanipulate-res.txt')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0160_wrong_endpoint(self):
        try:
            r = main('Create Invoice', 'ssd', self.api_key,
                     self.company_id, '--connection_id', self.connection_id)
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0170_wrong_apikey(self):
        try:
            r = main('Create Invoice', self.endpoint, '123',
                     self.company_id, '--connection_id', self.connection_id)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0180_wrong_company_id(self):
        try:
            r = main('Create Invoice', self.endpoint, self.api_key,
                     '123', '--connection_id', self.connection_id)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0190_get_customer_id(self):
        try:
            r = main('Get Customer ID', self.endpoint, self.api_key,
                     self.company_id)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0200_create_customer_account(self):
    #     try:
    #         r = main('Create Customer Account', self.endpoint, self.api_key,
    #                  self.company_id, '--connection_id', self.connection_id)
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
