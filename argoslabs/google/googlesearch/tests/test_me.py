#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.google.googlesearch`
====================================
.. moduleauthor:: Myeongkook Park <myeongkook@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.google.googlesearch import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.google.googlesearch
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        """
        argoslabs.google.googlesearch
        :return: raise exception ArgsError
        """
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success(self):
        """
        argoslabs.google.googlesearch orange
        :return: True
        """
        try:
            r = main('AIzaSyC7PUDhgSLOmMdqHYO1I1qzdJFa2486Q-s', '5173d767a8e36d1a9', '사나', 'Web', 100)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success_with_opt(self):
        """
        argoslabs.google.googlesearch
        :return: True
        """
        try:
            r = main('AIzaSyC7PUDhgSLOmMdqHYO1I1qzdJFa2486Q-s', '5173d767a8e36d1a9',
                     'oragne', 'Web', 10)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
