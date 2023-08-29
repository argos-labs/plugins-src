#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.filesystem.fo_stat`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Arun Kumar
#
# Change Log
# --------
#
#  * [2021/04/07]
#     - 그룹에 "6-Files and Folders" 넣음
#  * [2020/11/15]
#     - starting

################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.filesystem.fo_stat import _main as main
from contextlib import contextmanager
from io import StringIO


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
# noinspection PyUnresolvedReferences
class TU(TestCase):
    # ==========================================================================
    def setUp(self) -> None:
        pdir = os.path.join(os.path.dirname(__file__), '..')
        os.chdir(os.path.abspath(pdir))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_empty(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success(self):
        try:
            r = main(r'D:\Argos_git_repo\plugins-src\argoslabs\filesystem')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
