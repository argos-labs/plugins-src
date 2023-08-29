#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.chatwork_get_messages`
====================================
.. moduleauthor:: Taiki Shimasaki <shimasaki@argos-service.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.argos_service_jp.chatwork_get_messages import _main as main
import config


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.argos_service_jp.chatwork_get_messages
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # Do not include Japanese in Return Value, it will cause an error in Build!
    # ==========================================================================
    def test0100_get_success_with_opt(self):
        try:
            r = main(config.token,
                     config.room_id,
                     '--force',
                     'Latest 100',
                     '--out_num',
                     '10',
                     '--key_name',
                     'message_id')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
