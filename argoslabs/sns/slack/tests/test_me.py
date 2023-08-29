"""
====================================
 :mod:`argoslabs.sns.slack`
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
from argoslabs.sns.slack import _main as main


################################################################################
# noinspection PyUnresolvedReferences,PyBroadException
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))
        #cls.bottoken = 'xox-1248895843525-1255298442994-Avhkw0Mkae2JdIFwSKXyPVp7'
        cls.weburl = 'https://hooks.slack.com/services/T017ASBQTFF/B017HEUSRA7/G5IQNwa7mGc6jcZTtFxC5TA'
        cls.usertoken = '..'

    # ==========================================================================
    def test50_missing(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test100_botmsg(self):
        try:
            r = main('--webhookurl',self.weburl,'--text','hi')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_usermsg(self):
        try:
            r = main('--user_token',self.usertoken,'--channel', '#general',
                     '--text','hello from unittest','--successoutput','Success')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_userfile(self):
        try:
            r = main('--user_token',self.usertoken,'--channel', '#general',
                     '--file','sample.txt')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)