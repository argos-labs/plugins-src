"""
====================================
 :mod:`argoslabs.vmoplugins.filediff.tests.test_me`
====================================
.. moduleauthor:: Phuong Nguyen <phuong.nguyen@vmodev.com>
.. note:: YOURLABS License

Description
===========
YOUR LABS plugin module : unittest
"""

################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.vmoplugins.filediff import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    pwd = None

    # ==========================================================================
    def setUp(self) -> None:
        self.pwd = os.path.abspath(os.path.dirname(__file__))
        os.chdir(self.pwd)

    # ==========================================================================
    def test0100_two_folder_diff(self):
        try:
            s = os.path.join(self.pwd, 'same-folder-1')
            t = os.path.join(self.pwd, 'diff-folder')
            r = main(s, t)
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    # def test0101_two_folder_same(self):
    #     try:
    #         r = main('C:/work/plugin-demo-master/argoslabs/execution/file_diff/tests/same-folder-2', 'C:/work/plugin-demo-master/argoslabs/execution/file_diff/tests/same-folder-2')
    #         self.assertTrue(r == 1)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0102_two_file_diff(self):
        try:
            s = os.path.join(self.pwd, 'same-folder-1')
            t = os.path.join(self.pwd, 'diff-folder')
            r = main(s, t)
            r = main('C:/work/bid21108-lowcode/argoslabs/vmoplugins/filediff/tests/same-folder-2/attention.csv',
                     'C:/work/bid21108-lowcode/argoslabs/vmoplugins/filediff/tests/same-folder-2/flights.csv')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    # def test0103_two_file_same(self):
    #         try:
    #             r = main('C:/work/plugin-demo-master/argoslabs/execution/file_diff/tests/same-folder-2/attention.csv', 'C:/work/plugin-demo-master/argoslabs/execution/file_diff/tests/same-folder-2/attention.csv')
    #             self.assertTrue(r == 1)
    #         except Exception as e:
    #             sys.stderr.write('\n%s\n' % str(e))
    #             self.assertTrue(False)

    # ==========================================================================
    def test0104_two_file_and_folder(self):
            try:
                r = main('C:/work/bid21108-lowcode/argoslabs/vmoplugins/filediff/tests/same-folder-2/attention.csv', 'C:/work/bid21108-lowcode/argoslabs/vmoplugins/filediff/tests/same-folder-2')
                self.assertTrue(r == 9)
            except Exception as e:
                sys.stderr.write('\n%s\n' % str(e))
                self.assertTrue(False)