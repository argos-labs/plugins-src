"""
====================================
 :mod:`argoslabs.sns.telegram`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Slack : UnitTest
"""
#
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2020/07/20]
#     - unittest
#  * [2020/07/20]
#     - starting


################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.sns.telegram import _main as main


################################################################################

class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        cls.token = '..'

    # ==========================================================================
    def test50_missing(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test100_chatid(self):
        try:
            r = main('Find a chatid','1226332337:AAEjK1negcfM-LiRs6FNqVQfcj0Tle8FccI')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test105_chatid(self):
        try:
            r = main('Find a chatid',self.token)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_usermsg(self):
        try:
            r = main('Send a file or message',self.token, '--chatid', '-455140957',
                     '--msg','hello from unittest','--successoutput','Success')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_userfile(self):
        try:
            r = main('Send a file or message',self.token, '--chatid', '-1001223467093',
                     '--file','sample')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)