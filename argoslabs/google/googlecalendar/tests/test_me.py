#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.mygroup.regression`
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
from argoslabs.google.googlecalendar import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def tearDown(self) -> None:
        ...

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('invalid')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_event_list(self):
        try:
            r = main('Event List', 'token.pickle','--timemin', '2020-08-03T00:00:00Z')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_create_event(self):
        try:
            r = main('Create Event', 'token.pickle', '--startime', '2020-08-07T00:00:00',
                     '--endtime', '2020-08-07T03:00:00')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    def test0130_delete_event(self):
        try:
            r = main('Delete Event', 'token.pickle','--event_id',
                         '9lr249fp6lfo2ico0o5bjb5iuc')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_update_event(self):
        try:
            r = main('Update Event', 'token.pickle','--event_id','ioctf3gjbgltgs2gur3hs9ig80',
            '--attendees', 'irene4@argos-labs.com', '--summary',
                     'Argos-event','--additional_value','location:Santa Clara'
            )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)


