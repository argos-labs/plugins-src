"""
====================================
 :mod:`argoslabs.filesystem.downloads_monitor.test.test_me`
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
#  * [2023/04/27]
#     - start

################################################################################
import os
import sys
# import json
# import requests
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.filesystem.downloads_monitor import _main as main
# from alabs.common.util.vvencoding import get_file_encoding


################################################################################
csv_path = 'downloads.csv'


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_get_Downloads_List(self):
        try:
            r = main('Before download', os.path.abspath(csv_path))
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0010_monitoring(self):
    #     try:
    #         r = main('Monitoring', os.path.abspath(csv_path))
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
