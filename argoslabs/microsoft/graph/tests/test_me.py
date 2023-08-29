
"""
====================================
 :mod:`argoslabs.ibm.visualrecog`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
import csv
import json
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.microsoft.graph import _main as main
from configparser import ConfigParser
from contextlib import contextmanager
from io import StringIO
from pprint import pprint


################################################################################
@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    def setUp(self) -> None:
        config = ConfigParser()
        config.read("../../../../../src-vault/msgraph-test.ini")
        client_id = config.get("graph_api", "client_id")
        client_secret = config.get("graph_api", "client_secret")
        redirect_uri = config.get("graph_api", "redirect_uri")
        cred_file = 'msg-state.jsonc'
        TU.cred = client_id, client_secret, redirect_uri, cred_file

    # ==========================================================================
    def test0000_init(self):
        os.chdir(os.path.dirname(__file__))
        self.assertTrue(True)

    # ==========================================================================
    def test0010_failure(self):
        try:
            r = main('-vvv')
            self.assertTrue(r == 98)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_list_users(self):
        try:
            with captured_output() as (out, err):
                r = main(*TU.cred, 'List Users',)
            self.assertTrue(r == 0)
            print(out.getvalue())
            out.seek(0)
            rj = json.load(out)
            pprint(rj)
            self.assertTrue(isinstance(rj['value'], list) and 'displayName' in rj['value'][0])
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_get_root_drive(self):
        try:
            with captured_output() as (out, err):
                r = main(*TU.cred, 'Get Root Drive',)
            self.assertTrue(r == 0)
            print(out.getvalue())
            out.seek(0)
            rj = json.load(out)
            pprint(rj)
            self.assertTrue('id' in rj)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0120_get_root_drive(self):
    #     try:
    #         with captured_output() as (out, err):
    #             r = main(*TU.cred, 'Get Children')  # , '--children-folder', 'Temp')
    #         self.assertTrue(r == 0)
    #         print(out.getvalue())
    #         out.seek(0)
    #         rj = json.load(out)
    #         pprint(rj)
    #         self.assertTrue('id' in rj)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
