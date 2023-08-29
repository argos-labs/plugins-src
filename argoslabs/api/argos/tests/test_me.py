"""
====================================
 :mod:`argoslabs.api.argos.tests.test_me`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Kyobong An
#
# Change Log
# --------
#
#  * [2021/09/03]
#     - endpoint test추가
#  * [2021/08/30]
#     - start

################################################################################
import os
import sys
import json
import requests
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.api.argos import _main as main
from alabs.common.util.vvencoding import get_file_encoding


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    # cwd = os.getcwd()

    # ==========================================================================
    def test0000_getPamList(self):
        try:
            r = main('getPamList', '2c4e34ba47674e5fd295')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0010_getPamList_error(self):
        try:
            r = main('getPamList', '2c4e34ba4767f4e5fd295')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_getBotList(self):
        try:
            r = main('getBotList', '2c4e34ba47674e5fd295')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_getBotList_error(self):
        try:
            r = main('getBotList', '2c4e34ba47674e5fd295',
                     '--apiurl', 'fasf')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0200_sendOndemand(self):
    #     try:
    #         r = main('sendOndemand', 'feb44d8a598733537a57',
    #                  '--userid', 'akb0930@vivans.net',
    #                  '--scenarioid', 'c045a5c8954e4d36fe4e',
    #                  '--pamid', 'da6cd254d85ab2164bc8',
    #                  '--endpoint', 'http://input_your_endpoint',
    #                  '--workid', 'input_work_id',
    #                  '--valuename', '{{my.a}}',
    #                  '--valuename', '{{my.b}}',
    #                  '--valuename', '{{AAAAA.aaab}}',
    #                  '--value', 'hello, world',
    #                  '--value', 'hello, world2',
    #                  '--value', '["1", "2", "3", "A", "B", "C"]',
    #                  '--apiurl', 'https://api-kem-rpa.argos-labs.com:59901'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # ==========================================================================
    # def test0210_sendOndemand_vaeiable_test(self):
    #     try:
    #         r = main('sendOndemand', 'd65c86fd23483dcf1e49',
    #                  '--userid', 'akb0930@vivans.net',
    #                  '--scenarioid', '004987801c6a4d0c8071',
    #                  '--pamid', 'da6cd254d85ab2164bc8',
    #                  '--endpoint', 'http://input_your_endpoint',
    #                  '--workid', 'input_work_id',
    #                  '--valuename', '{{my.a}}',
    #                  '--valuename', '{{my.b}}',
    #                  '--valuename', '{{AAAAA.aaab}}',
    #                  '--value', 'hello, world',
    #                  '--value', 'hello, world2',
    #                  '--value', '["1", "2", "3", "A", "B", "C"]',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0220_sendOndemand_vaeiable_testVM(self):
    #     try:
    #         r = main('sendOndemand', '2c4e34ba47674e5fd295',
    #                  '--userid', 'akb0930@vivans.net',
    #                  '--scenarioid', '004987801c6a4d0c8071',
    #                  '--pamid', 'c1e8a7d977f5d9ace632',
    #                  '--valuename', 'my.a',
    #                  '--valuename', 'my.b',
    #                  '--valuename', 'AAAAA.aaab',
    #                  '--valuename', 'param.searchText',
    #                  '--value', 'hello, world',
    #                  '--value', 'hello, world2',
    #                  '--value', '["1", "2", "3", "A", "B", "C"]',
    #                  '--value', 'hello world',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0230_sendOndemand_endpoint(self):   # endpoint https://webhook.site/
    #     try:
    #         r = main('sendOndemand', '2c4e34ba47674e5fd295',
    #                  '--userid', 'akb0930@vivans.net',
    #                  '--scenarioid', '004987801c6a4d0c8071',
    #                  '--pamid', 'c1e8a7d977f5d9ace632',
    #                  '--endpoint', 'https://webhook.site/74b6e49d-f1b5-4adc-9354-73c9b48b1a66',
    #                  '--workid', 'testhook',
    #                  '--valuename', 'my.a',
    #                  '--valuename', 'my.b',
    #                  '--valuename', 'AAAAA.aaab',
    #                  '--valuename', 'param.searchText',
    #                  '--value', 'hello, world',
    #                  '--value', 'hello, world2',
    #                  '--value', '["1", "2", "3", "A", "B", "C"]',
    #                  '--value', 'hello world',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0240_sendOndemand_find_None(self):
        try:
            r = main('sendOndemand', '2c4e34ba47674e5fd295',
                     '--userid', 'akb0930@vivans.net',
                     '--scenarioid', '004987801c6a4d0c8071',
                     '--pamid', 'c1e8a7d977f5d9ace632',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
