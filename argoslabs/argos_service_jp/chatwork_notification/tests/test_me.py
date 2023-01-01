#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.myuti.text`
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
from datetime import datetime
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.argos_service_jp.chatwork_notification import _main as main
import config


################################################################################
class TU(TestCase):
    os.chdir(os.path.dirname(__file__))

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

    # ==========================================================================
    def test0100_message(self):
        try:
            r = main(config.token,
                     config.room_id,
                     'Unit Test Message: %s' % datetime.now())
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_message_failure(self):
        try:
            r = main('101010eee1010101010',
                     config.room_id,
                     'Unit Test Message: %s' % datetime.now())
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0120_message_unread(self):
        try:
            r = main(config.token,
                     config.room_id,
                     'Unit Test Message: %s' % datetime.now(),
                     '--unread',
                     'ON')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0130_message_to(self):
        try:
            r = main(config.token,
                     config.room_id,
                     'Unit Test Message: %s' % datetime.now(),
                     '--to',
                     'All')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0140_message_to(self):
        try:
            r = main(config.token,
                     config.room_id,
                     'Unit Test Message: %s' % datetime.now(),
                     '--to',
                     '3138632')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0200_img(self):
        try:
            r = main(config.token,
                     config.room_id,
                     'Unit Test Message: %s' % datetime.now(),
                     '--file',
                     'C:/Users/Windows/Pictures/Argos/TS_icon_circle.png')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0210_doc(self):
        try:
            r = main(config.token,
                     config.room_id,
                     'Unit Test Message: %s' % datetime.now(),
                     '--file',
                     'C:/Users/Windows/Documents/test.txt')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0220_video(self):
        try:
            r = main(config.token,
                     config.room_id,
                     'Unit Test Message: %s' % datetime.now(),
                     '--file',
                     'C:/Users/Windows/Videos/video-sample.mp4')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0300_unread_file(self):
        try:
            r = main(config.token,
                     config.room_id,
                     'Unit Test Message: %s' % datetime.now(),
                     '--unread',
                     'ON',
                     '--file',
                     'C:/Users/Windows/Documents/test.txt')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
