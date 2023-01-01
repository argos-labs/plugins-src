
"""
====================================
 :mod:`argoslabs.ibm.visualrecog`
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
import csv
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.filesystem.append import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True
    APP_TXT = 'append.txt'

    # ==========================================================================
    def test0000_init(self):
        os.chdir(os.path.dirname(__file__))
        self.assertTrue(True)

    # ==========================================================================
    def test0010_failure_param(self):
        try:
            r = main()
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure_param(self):
        try:
            r = main('invalid-op', 'KKK:/invalid/file.txt')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0030_failure_param(self):
        try:
            r = main('String', 'KKK:/invalid/file.txt')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0040_failure_param(self):
        try:
            r = main('String', 'append.txt')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0090_success_clear(self):
        if os.path.exists(TU.APP_TXT):
            os.remove(TU.APP_TXT)
        self.assertTrue(not os.path.exists(TU.APP_TXT))

    # ==========================================================================
    def test0100_success_string(self):
        try:
            r = main('String', TU.APP_TXT, 'ABC')
            self.assertTrue(r == 0)
            with open(TU.APP_TXT, encoding='utf-8') as ifp:
                app_txt = ifp.read()
            self.assertTrue(app_txt == 'ABC')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success_string(self):
        try:
            r = main('String', TU.APP_TXT, 'de', 'FGH',
                     '--end-with', ':')
            self.assertTrue(r == 0)
            with open(TU.APP_TXT, encoding='utf-8') as ifp:
                app_txt = ifp.read()
            self.assertTrue(app_txt == 'ABCdeFGH:')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_success_string(self):
        try:
            r = main('String', TU.APP_TXT, 'ij',
                     '--end-with-line')
            self.assertTrue(r == 0)
            with open(TU.APP_TXT, encoding='utf-8') as ifp:
                app_txt = ifp.read()
            self.assertTrue(app_txt == 'ABCdeFGH:ij\n')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_success_line(self):
        try:
            r = main('Line', TU.APP_TXT, 'KL', ' MN')
            self.assertTrue(r == 0)
            with open(TU.APP_TXT, encoding='utf-8') as ifp:
                app_txt = ifp.read()
            self.assertTrue(app_txt == 'ABCdeFGH:ij\nKL MN\n')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0190_success_clear(self):
        if os.path.exists(TU.APP_TXT):
            os.remove(TU.APP_TXT)
        self.assertTrue(not os.path.exists(TU.APP_TXT))

    # ==========================================================================
    def test0200_success_csv(self):
        try:
            r = main('CSV Row', TU.APP_TXT, 'a', 'b,c', 'd')
            self.assertTrue(r == 0)
            with open(TU.APP_TXT, encoding='utf-8') as ifp:
                app_txt = ifp.read()
            self.assertTrue(app_txt == 'a,"b,c",d\n')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_success_csv(self):
        try:
            r = main('CSV Row', TU.APP_TXT, '11', '23"abc",d', 'abcde')
            self.assertTrue(r == 0)
            with open(TU.APP_TXT, encoding='utf-8') as ifp:
                app_txt = ifp.read()
            self.assertTrue(app_txt == 'a,"b,c",d\n11,"23""abc"",d",abcde\n')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
