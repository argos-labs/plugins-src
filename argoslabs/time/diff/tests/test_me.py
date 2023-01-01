"""
====================================
 :mod:`argoslabs.time.diff.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/11/12]
#     - add --input-dt-format
#  * [2021/04/26]
#     - starting

################################################################################
import sys
import datetime
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.time.diff import _main as main
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
# noinspection PyUnusedLocal
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True
    outfile = 'stdout.txt'

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_help(self):
        try:
            r = main('', '', 'In seconds')
            self.assertTrue(r == 9)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_success_one_day(self):
        try:
            with captured_output() as (out, err):
                r = main('20210102', '20210101', 'In seconds')
            self.assertTrue(r == 0)
            out = out.getvalue().strip()
            print(out)
            self.assertTrue(out == '86400')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_success_one_day_minus(self):
        try:
            with captured_output() as (out, err):
                r = main('20210101', '2021/01/02', 'In seconds')
            self.assertTrue(r == 0)
            out = out.getvalue().strip()
            print(out)
            self.assertTrue(out == '-86400')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_success_one_day(self):
        try:
            with captured_output() as (out, err):
                r = main('20210102', '20210101', 'Timedelta string')
            self.assertTrue(r == 0)
            out = out.getvalue().strip()
            print(out)
            self.assertTrue(out == '1 day, 0:00:00')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_success_one_day_minus(self):
        try:
            with captured_output() as (out, err):
                r = main('20210101', '2021/01/02', 'Timedelta string')
            self.assertTrue(r == 0)
            out = out.getvalue().strip()
            print(out)
            self.assertTrue(out == '-1 day, 0:00:00')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_success_time(self):
        try:
            dt1 = datetime.datetime(2021, 3, 4, 0, 0, 0)
            dt2 = dt1 + datetime.timedelta(seconds=-123)
            with captured_output() as (out, err):
                r = main(dt1.strftime('%Y%m%d %H%M%S'),
                         dt2.strftime('%Y%m%d %H%M%S'),
                         'In seconds')
            self.assertTrue(r == 0)
            out = out.getvalue().strip()
            print(out)
            self.assertTrue(out == '123')

            with captured_output() as (out, err):
                r = main(dt2.strftime('%Y%m%d %H%M%S'),
                         dt2.strftime('%Y%m%d %H%M%S'),
                         'In seconds')
            self.assertTrue(r == 0)
            out = out.getvalue().strip()
            print(out)
            self.assertTrue(out == '0')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_success_compare_only(self):
        try:
            dt1 = datetime.datetime(2021, 3, 4, 0, 0, 0)
            dt2 = dt1 + datetime.timedelta(seconds=-123)

            with captured_output() as (out, err):
                r = main(
                    dt1.strftime('%Y%m%d %H%M%S'),
                    dt2.strftime('%Y%m%d %H%M%S'),
                    'Values 1, 0, or -1',
                )
            self.assertTrue(r == 0)
            out = out.getvalue().strip()
            print(out)
            self.assertTrue(out == '1')

            with captured_output() as (out, err):
                r = main(
                    dt2.strftime('%Y%m%d %H%M%S'),
                    dt1.strftime('%Y%m%d %H%M%S'),
                    'Values 1, 0, or -1',
                )
            self.assertTrue(r == 0)
            out = out.getvalue().strip()
            print(out)
            self.assertTrue(out == '-1')

            with captured_output() as (out, err):
                r = main(
                    dt1.strftime('%Y%m%d %H%M%S'),
                    dt1.strftime('%Y%m%d %H%M%S'),
                    'Values 1, 0, or -1',
                )
            self.assertTrue(r == 0)
            out = out.getvalue().strip()
            print(out)
            self.assertTrue(out == '0')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_uk_datetime(self):
        try:
            dt1 = datetime.datetime(2021, 12, 11, 1, 2, 3)
            dt2 = dt1 + datetime.timedelta(seconds=-123)

            with captured_output() as (out, err):
                r = main(
                    dt1.strftime('%d%m%Y %H%M%S'),
                    dt2.strftime('%d%m%Y %H%M%S'),
                    'In seconds',
                    '--input-dt-format', 'YYYY/MM/DD HH:MM:SS.mmm',
                )
            self.assertTrue(r == 9)

            with captured_output() as (out, err):
                r = main(
                    dt1.strftime('%d%m%Y-%H%M%S'),
                    dt2.strftime('%d%m%Y-%H%M%S'),
                    'In seconds',
                    '--input-dt-format', 'DDMMYYYY-HHMMSS',
                )
            self.assertTrue(r == 0)
            out = out.getvalue().strip()
            print(out)
            self.assertTrue(out == '123')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0180_uk_date(self):
        try:
            dt1 = datetime.datetime(2021, 12, 11, 0, 0, 0)
            dt2 = dt1 + datetime.timedelta(days=-12)

            with captured_output() as (out, err):
                r = main(
                    dt1.strftime('%d/%m/%Y'),
                    dt2.strftime('%d/%m/%Y'),
                    'Timedelta string',
                    '--input-dt-format', 'DD/MM/YYYY',
                )
            self.assertTrue(r == 0)
            out = out.getvalue().strip()
            print(out)
            self.assertTrue(out == '12 days, 0:00:00')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
