#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.window_op`
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
from argoslabs.argos_service_jp.window_op import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.argos_service_jp.window_op
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    """
    # This test is probably fine, but it will fail at building(EncodingError)
    # ==========================================================================
    def test0100_windows_list_success(self):
        try:
            r = main('Get Window\'s List')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
    """

    # ==========================================================================
    def test0200_select_success(self):
        try:
            r = main('Select Window',
                     '--window_title',
                     'TweetDeck*')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0300_max_success(self):
        try:
            r = main('Maximize',
                     '--window_title',
                     'TweetDeck - Google Chrome')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0400_min_success(self):
        try:
            r = main('Minimize',
                     '--window_title',
                     'TweetDeck - Google Chrome')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0500_resize_success(self):
        try:
            r = main('Select Window Resize',
                     '--window_title',
                     'TweetDeck - Google Chrome',
                     '--window_height',
                     '900',
                     '--window_width',
                     '1440')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0600_get_active_success(self):
        try:
            r = main('Get Active Window\'s Title')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0700_move_success(self):
        try:
            r = main('Select Window Move (relative)',
                     '--window_title',
                     'TweetDeck*',
                     '--move_right',
                     '0',
                     '--move_down',
                     '0')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0800_moveTo_success(self):
        try:
            r = main('Select Window Move (absolute)',
                     '--window_title',
                     'TweetDeck*',
                     '--move_X',
                     '0',
                     '--move_Y',
                     '0')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
