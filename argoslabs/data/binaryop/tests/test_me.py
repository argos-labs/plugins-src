#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.binaryop`
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
#  * [2022/02/02]
#     - -0.11 * 100 Error
#  * [2021/11/06]
#     - output 포맷에 영국식 DDMMYYYY 추가
#     - --input-dt-format 추가
#     - today, now 추가
#  * [2021/03/27]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2021/03/27]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2021/01/14]
#     - --output-int-func 옵션 추가
#  * [2019/10/14]
#     - --datetime-separator 옵션 추가
#  * [2019/08/14]
#     - Month 파싱 때, 3자만 가져오는 대신 전체 파싱 하도록 수정
#  * [2019/06/27]
#     - date, datetime 출력 오류 수정
#  * [2019/06/20]
#     - starting

################################################################################
import sys
import calendar
import datetime
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.data.binaryop import _main as main
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

    # ==========================================================================
    def test0000_init(self):
        for month_idx in range(1, 13):
            print(calendar.month_name[month_idx])
            print(calendar.month_abbr[month_idx])
            print("")
        self.assertTrue(True)

    # ==========================================================================
    def test0050_help(self):
        try:
            _ = main('-h')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_invalid(self):
        try:
            _ = main('tom')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_invalid(self):
        try:
            _ = main('tom', 'jerry')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0120_string_add(self):
        try:
            with captured_output() as (out, err):
                r = main('tom', '+', 'jerry')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == 'tomjerry')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_string_subtract(self):
        try:
            with captured_output() as (out, err):
                r = main('tomjerrytomjerryfoo', '-', 'jerry')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == 'tomtomfoo')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_string_multiply_fail(self):
        try:
            with captured_output() as (out, err):
                _ = main('tom', '/', 'jerry')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0150_string_multiply(self):
        try:
            with captured_output() as (out, err):
                r = main('tom', '*', '3')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == 'tomtomtom')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_string_devide(self):
        try:
            with captured_output() as (out, err):
                _ = main('tom', '/', 'jerry')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0170_string_modular_fail(self):
        try:
            with captured_output() as (out, err):
                _ = main('tom', '%', 'jerry')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0180_string_add_type_fail(self):
        try:
            with captured_output() as (out, err):
                r = main('tom', '+', 'jerry',
                         '--type', 'int')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0200_int_calc(self):
        try:
            # Add
            with captured_output() as (out, err):
                r = main('1', '+', '2')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '3')
            # Subtract
            with captured_output() as (out, err):
                r = main('1', '-', '2')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '-1')
            # Multiply
            with captured_output() as (out, err):
                r = main('2', '*', '3')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '6')
            # Devide
            with captured_output() as (out, err):
                r = main('1', '/', '2')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '0.5')
            # Modular
            with captured_output() as (out, err):
                r = main('3', '%', '2')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '1')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0205_int_calc_error(self):
        try:
            # Devide by zero
            with captured_output() as (out, err):
                r = main('1', '/', '0')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0210_int_calc_type_string(self):
        try:
            with captured_output() as (out, err):
                r = main('1', '+', '2',
                         '--type', 'string')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '12')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_int_calc_type_float(self):
        try:
            with captured_output() as (out, err):
                r = main('1', '+', '2',
                         '--type', 'float')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '3.0')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0230_int_calc_type_fail(self):
        try:
            with captured_output() as (out, err):
                r = main('tom', '+', 'jerry',
                         '--type', 'date')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0300_float_calc(self):
        try:
            # Add
            with captured_output() as (out, err):
                r = main('1.2', '+', '2.3')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '3.5')
            # Subtract
            with captured_output() as (out, err):
                r = main('3.1', '-', '2')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '1.1')
            # Multiply
            with captured_output() as (out, err):
                r = main('2.0', '*', '3.3')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '6.6')
            # Devide
            with captured_output() as (out, err):
                r = main('3', '/', '2.0')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '1.5')
            # Modular
            with captured_output() as (out, err):
                r = main('3.5', '%', '1.5')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '0.5')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0310_float_calc_type(self):
        try:
            # int
            with captured_output() as (out, err):
                r = main('1.2', '+', '2.3',
                         '--type', 'int')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout, '3')
            # string
            with captured_output() as (out, err):
                r = main('1.2', '+', '2.3',
                         '--type', 'string')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '1.22.3')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0320_float_calc_type_fail(self):
        try:
            with captured_output() as (out, err):
                r = main('1.2', '+', '2.3',
                         '--type', 'datetime')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0330_diff_calc_type(self):
        try:
            # int
            with captured_output() as (out, err):
                r = main('1.2', '+', 'jerry')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '1.2jerry')
            # string
            with captured_output() as (out, err):
                r = main('tom2.3jerry', '-', '2.3')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == 'tomjerry')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0400_date_calc_success(self):
        try:
            # Add
            with captured_output() as (out, err):
                r = main(' 20190621 ', '+', ' 2day ')  # strip
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190623')
            # Subtract
            with captured_output() as (out, err):
                r = main('2019-06-25', '-', '2week')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190611')
            # Subtract
            with captured_output() as (out, err):
                r = main('2019-6-25', '-', '2week')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190611')
            # Subtract
            with captured_output() as (out, err):
                r = main('20190331', '-', '1month')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190228')
            # Add
            with captured_output() as (out, err):
                r = main('20160229', '+', '1year')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20170228')
            # Add
            with captured_output() as (out, err):
                r = main('20190228', '+', '24hour', '--type', 'date')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190301')
            # Add
            with captured_output() as (out, err):
                r = main('20190228', '+', '12hour')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190228')
            # Add
            with captured_output() as (out, err):
                r = main('20190228', '+', '86400sec')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190301')
            # Add
            with captured_output() as (out, err):
                r = main('20190228', '+', '3600sec')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190228')
            # Add
            with captured_output() as (out, err):
                r = main('2016-02-29', '+', '1year')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20170228')
            # Add
            with captured_output() as (out, err):
                r = main('2016/02/29', '+', '1year')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20170228')
            # Add
            with captured_output() as (out, err):
                r = main('2016/2/1', '+', '1year')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20170201')
            # Add
            with captured_output() as (out, err):
                r = main('2016/2/29', '+', '1year')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20170228')
            # Add
            with captured_output() as (out, err):
                r = main('Feb 29 2016', '+', '1year')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20170228')
            # Add
            with captured_output() as (out, err):
                r = main('February 29, 2016', '+', '1year')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20170228')
            # Add
            with captured_output() as (out, err):
                r = main('29 Feb 2016', '+', '1year')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20170228')
            # Add
            with captured_output() as (out, err):
                r = main('29 august 2016', '+', '1year')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20170829')
            # Add
            with captured_output() as (out, err):
                r = main('02-29-2016', '+', '1year')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20170228')
            # Add
            with captured_output() as (out, err):
                r = main('02/29/2016', '+', '1year')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20170228')
            # Add
            with captured_output() as (out, err):
                r = main('2/9/2016', '+', '1year')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20170209')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0405_date_calc_success_format(self):
        try:
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '+', '2day', '--date-format', 'YYYY-MM-DD')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '2019-06-23')
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '+', '2day', '--date-format', 'YYYY/MM/DD')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '2019/06/23')
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '+', '2day', '--date-format', 'MMDDYYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '06232019')
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '+', '2day', '--date-format', 'MM-DD-YYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '06-23-2019')
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '+', '2day', '--date-format', 'MM/DD/YYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '06/23/2019')
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '-', '20day', '--date-format', 'M/D/YYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '6/1/2019')
            # Add
            with captured_output() as (out, err):
                r = main('2019.06.21', '-', '20day', '--date-format', 'M/D/YYYY',
                         '--datetime-separator', '.')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '6/1/2019')
            # Add
            with captured_output() as (out, err):
                r = main('2019.6.1', '+', '20day', '--date-format', 'M/D/YYYY',
                         '--datetime-separator', '.')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '6/21/2019')
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '-', '20day', '--date-format', 'B D YYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == 'Jun 1 2019')
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '-', '20day', '--date-format', 'B D, YYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == 'Jun 1, 2019')
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '-', '20day', '--date-format', 'D B YYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '1 Jun 2019')

            # Add: "B D YYYY"
            with captured_output() as (out, err):
                r = main('Jun 1 2019', '+', '1day')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190602')

            # Add: "B D, YYYY"
            with captured_output() as (out, err):
                r = main('Jun 1, 2019', '+', '1day')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190602')

            # Add: "D B YYYY"
            with captured_output() as (out, err):
                r = main('11 Jun 2019', '+', '1day')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190612')

            # Add: "D B YY"
            with captured_output() as (out, err):
                r = main('11 Jun 19', '+', '1day')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190612')

            # Add: "DBYY"
            with captured_output() as (out, err):
                r = main('11Jun19', '+', '1day')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190612')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0410_date_calc_failure(self):
        try:
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '+', '2dayinvalid')
            self.assertTrue(False)
        except Exception as err:
            sys.stderr.write('%s\n' % str(err))
            self.assertTrue(True)
        try:
            # Subtract
            with captured_output() as (out, err):
                r = main('20190625', '-', '2')
            self.assertTrue(False)
        except Exception as err:
            sys.stderr.write('%s\n' % str(err))
            self.assertTrue(True)
        try:
            # Multiply
            with captured_output() as (out, err):
                r = main('20190625', '*', '2hour')
            self.assertTrue(False)
        except Exception as err:
            sys.stderr.write('%s\n' % str(err))
            self.assertTrue(True)
        try:
            # Devide
            with captured_output() as (out, err):
                r = main('20190625', '/', '2sec')
            self.assertTrue(False)
        except Exception as err:
            sys.stderr.write('%s\n' % str(err))
            self.assertTrue(True)
        try:
            # Modular
            with captured_output() as (out, err):
                r = main('20190625', '%', '2month')
            self.assertTrue(False)
        except Exception as err:
            sys.stderr.write('%s\n' % str(err))
            self.assertTrue(True)
        try:
            # Add
            with captured_output() as (out, err):
                r = main('20160230', '+', '1year')
            self.assertTrue(False)
        except Exception as err:
            sys.stderr.write('%s\n' % str(err))
            self.assertTrue(True)
        try:
            # Add date + date
            with captured_output() as (out, err):
                r = main('20160330', '+', '20160210')
            self.assertTrue(False)
        except Exception as err:
            sys.stderr.write('%s\n' % str(err))
            self.assertTrue(True)

    # ==========================================================================
    def test0420_datetime_calc_success(self):
        try:
            # Add
            with captured_output() as (out, err):
                r = main('20190621-123456', '+', '2day')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190623-123456')
            # Subtract
            with captured_output() as (out, err):
                r = main('2019-06-25 11:22:33', '-', '2week')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190611-112233')
            # Subtract
            with captured_output() as (out, err):
                r = main('20190331-012345', '-', '1month')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190228-012345')
            # Add
            with captured_output() as (out, err):
                r = main('20190228-153724', '+', '1year')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20200228-153724')
            # Add
            with captured_output() as (out, err):
                r = main('20190228-112233', '+', '24hour')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190301-112233')
            # Add
            with captured_output() as (out, err):
                r = main('20190228-012345', '+', '12hour')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190228-132345')
            # Add
            with captured_output() as (out, err):
                r = main('20190228-112200', '+', '100sec')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190228-112340')
            # Add
            with captured_output() as (out, err):
                r = main('2019-06-21 12:34:56', '+', '2day')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190623-123456')
            # Add
            with captured_output() as (out, err):
                r = main('2019-6-21 12:34:56', '+', '2day')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190623-123456')
            # Add
            with captured_output() as (out, err):
                r = main('2019/06/21 12:34:56', '+', '2day')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190623-123456')
            # Add
            with captured_output() as (out, err):
                r = main('06-21-2019 12:34:56', '+', '2day')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190623-123456')
            # Add
            with captured_output() as (out, err):
                r = main('6-21-2019 12:34:56', '+', '2day')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190623-123456')
            # Add
            with captured_output() as (out, err):
                r = main('06/21/2019 12:34:56', '+', '2day')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190623-123456')
            # Add
            with captured_output() as (out, err):
                r = main('6/1/2019 12:34:56', '+', '2day')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190603-123456')
            # Add
            with captured_output() as (out, err):
                r = main('6.1.2019 12:34:56', '+', '2day', '--datetime-separator', '.')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190603-123456')
            # Add
            with captured_output() as (out, err):
                r = main('6|1|2019 12:34:56', '+', '2day', '--datetime-separator', '|')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '20190603-123456')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0422_datetime_calc_success_timedelta(self):
        try:
            # Subtract
            with captured_output() as (out, err):
                r = main('20190621-123456.123456', '-', '20190621-123345.012456')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '0:01:11.111000')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0425_datetime_calc_success_with_format(self):
        try:
            # Add
            with captured_output() as (out, err):
                r = main('20190621-123456', '+', '2day',
                         '--datetime-format', 'YYYY-MM-DD HH:MM:SS')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '2019-06-23 12:34:56')
            # Add
            with captured_output() as (out, err):
                r = main('20190621-123456', '+', '2day',
                         '--datetime-format', 'YYYY/MM/DD HH:MM:SS')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '2019/06/23 12:34:56')
            # Add
            with captured_output() as (out, err):
                r = main('20190621-123456', '+', '2day',
                         '--datetime-format', 'MMDDYYYY-HHMMSS')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '06232019-123456')
            # Add
            with captured_output() as (out, err):
                r = main('20190621-123456', '+', '2day',
                         '--datetime-format', 'MM-DD-YYYY HH:MM:SS')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '06-23-2019 12:34:56')
            # Add
            with captured_output() as (out, err):
                r = main('20190621-123456.234567', '+', '2day',
                         '--datetime-format', 'MM/DD/YYYY HH:MM:SS.mmm')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '06/23/2019 12:34:56.234567')
            # Add
            with captured_output() as (out, err):
                r = main('20190621-123456.234567', '+', '111msec',
                         '--datetime-format', 'MM/DD/YYYY HH:MM:SS.mmm')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '06/21/2019 12:34:56.345567')
            # Add
            with captured_output() as (out, err):
                r = main('20190621-123456.234567', '+', '111usec',
                         '--datetime-format', 'MM/DD/YYYY HH:MM:SS.mmm')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '06/21/2019 12:34:56.234678')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0430_datetime_calc_failure(self):
        try:
            # Add
            with captured_output() as (out, err):
                _ = main('20190621-012345', '+', '2dayinvalid')
            self.assertTrue(False)
        except Exception as err:
            sys.stderr.write('%s\n' % str(err))
            self.assertTrue(True)
        try:
            # Subtract
            with captured_output() as (out, err):
                _ = main('20190625-012345', '-', '2')
            self.assertTrue(False)
        except Exception as err:
            sys.stderr.write('%s\n' % str(err))
            self.assertTrue(True)
        try:
            # Multiply
            with captured_output() as (out, err):
                _ = main('20190625-012345', '*', '2hour')
            self.assertTrue(False)
        except Exception as err:
            sys.stderr.write('%s\n' % str(err))
            self.assertTrue(True)
        try:
            # Devide
            with captured_output() as (out, err):
                _ = main('20190625-012345', '/', '2sec')
            self.assertTrue(False)
        except Exception as err:
            sys.stderr.write('%s\n' % str(err))
            self.assertTrue(True)
        try:
            # Modular
            with captured_output() as (out, err):
                _ = main('20190625-012345', '%', '2month')
            self.assertTrue(False)
        except Exception as err:
            sys.stderr.write('%s\n' % str(err))
            self.assertTrue(True)

    # ==========================================================================
    def test0440_date_calc_success_with_output_format(self):
        try:
            # Add
            with captured_output() as (out, err):
                r = main('20190601', '+', '2day',
                         '--output-date-format', 'YYYY.MM.DD')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '2019.06.03')
            # Add
            with captured_output() as (out, err):
                r = main('20190601', '+', '2day',
                         '--output-date-format', 'YY.MM.DD')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '19.06.03')
            # Add
            with captured_output() as (out, err):
                r = main('20190601', '+', '2day',
                         '--output-date-format', 'MM|DD')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '06|03')
            # Add
            with captured_output() as (out, err):
                r = main('20190601', '+', '2day',
                         '--output-date-format', 'D|M')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '3|6')
            # Add
            with captured_output() as (out, err):
                r = main('20190601-010203', '+', '2day',
                         '--output-date-format', 'D|M hhmmss')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '3|6 010203')
            # Add
            with captured_output() as (out, err):
                r = main('20190601-010203', '+', '2day',
                         '--output-date-format', 'D|M h-m-s')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '3|6 1-2-3')
            # Add
            with captured_output() as (out, err):
                r = main('20190601-010203', '+', '2day',
                         '--output-date-format', 'YY/MM/D h:m')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '19/06/3 1:2')

            # Add new date format
            with captured_output() as (out, err):
                r = main('1 SEP 2020', '+', '0day',
                         '--output-date-format', 'YYYY/MM/DD')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '2020/09/01')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0450_date_calc_success_with_input_output_format(self):
        try:
            with captured_output() as (out, err):
                r = main('1 SEP 20', '+', '0day',
                         '--output-date-format', 'YYYY/MM/DD')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '2020/09/01')

            with captured_output() as (out, err):
                r = main('29SEP20', '+', '0day',
                         '--output-date-format', 'YYYY/MM/DD')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '2020/09/29')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0460_output_int_func(self):
        try:
            with captured_output() as (out, err):
                r = main('23', '/', '2')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '11.5')

            with captured_output() as (out, err):
                r = main('23', '/', '2',
                         '--output-int-func', 'round')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '12')

            with captured_output() as (out, err):
                r = main('23', '/', '2',
                         '--output-int-func', 'ceil')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '12')

            with captured_output() as (out, err):
                r = main('23', '/', '2',
                         '--output-int-func', 'floor')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '11')

            with captured_output() as (out, err):
                r = main('23', '/', '2',
                         '--output-int-func', 'trunc')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '11')

            with captured_output() as (out, err):
                r = main('-23', '/', '2',
                         '--output-int-func', 'floor')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '-12')

            with captured_output() as (out, err):
                r = main('-23', '/', '2',
                         '--output-int-func', 'trunc')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '-11')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0470_datetime_calc_success_with_uk_format(self):
        try:
            # Add
            with captured_output() as (out, err):
                r = main('20190621-123456', '+', '2day',
                         '--datetime-format', 'DDMMYYYY-HHMMSS')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '23062019-123456')
            # Add
            with captured_output() as (out, err):
                r = main('20190621-123456', '+', '2day',
                         '--datetime-format', 'DD-MM-YYYY HH:MM:SS')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '23-06-2019 12:34:56')
            # Add
            with captured_output() as (out, err):
                r = main('20190621-123456.234567', '+', '2day',
                         '--datetime-format', 'DD/MM/YYYY HH:MM:SS.mmm')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '23/06/2019 12:34:56.234567')
            # Add
            with captured_output() as (out, err):
                r = main('20190621-123456.234567', '+', '111msec',
                         '--datetime-format', 'DD/MM/YYYY HH:MM:SS.mmm')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '21/06/2019 12:34:56.345567')
            # Add
            with captured_output() as (out, err):
                r = main('20190621-123456.234567', '+', '111usec',
                         '--datetime-format', 'DD/MM/YYYY HH:MM:SS.mmm')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '21/06/2019 12:34:56.234678')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0480_date_calc_success_uk_format(self):
        try:
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '+', '2day', '--date-format', 'DDMMYYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '23062019')
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '+', '2day', '--date-format', 'DD-MM-YYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '23-06-2019')
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '+', '2day', '--date-format', 'DD/MM/YYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '23/06/2019')
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '-', '20day', '--date-format', 'D/M/YYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '1/6/2019')
            # Add
            with captured_output() as (out, err):
                r = main('2019.06.21', '-', '20day', '--date-format', 'D/M/YYYY',
                         '--datetime-separator', '.')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '1/6/2019')
            # Add
            with captured_output() as (out, err):
                r = main('2019.6.1', '+', '20day', '--date-format', 'D/M/YYYY',
                         '--datetime-separator', '.')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '21/6/2019')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0490_date_input_format(self):
        try:
            # Add
            with captured_output() as (out, err):
                r = main('20190621', '+', '2day',
                         '--input-dt-format', 'YYYYMMDD',
                         '--date-format', 'DDMMYYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '23062019')
            # Add
            with captured_output() as (out, err):
                r = main('21/06/2019', '+', '2day',
                         '--input-dt-format', 'DD/MM/YYYY',
                         '--date-format', 'DD/MM/YYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '23/06/2019')
            # Add
            with captured_output() as (out, err):
                r = main('21/06/2019', '+', '2day',
                         '--input-dt-format', 'DD/MM/YYYY HH:MM:SS',
                         '--date-format', 'DD/MM/YYYY')
            self.assertTrue(r == 99)
            stderr = err.getvalue().strip()
            print(stderr)
            self.assertTrue(stderr ==
                            'argoslabs.filesystem.op Error: time data \'21/06/2019\' does not match format \'%d/%m/%Y %H:%M:%S\'')

            # Add
            with captured_output() as (out, err):
                r = main('21/06/2019 12:34:56', '+', '2day',
                         '--input-dt-format', 'DD/MM/YYYY HH:MM:SS',
                         '--datetime-format', 'DD/MM/YYYY HH:MM:SS')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '23/06/2019 12:34:56')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0500_today_now(self):
        try:
            # Today
            with captured_output() as (out, err):
                r = main('today', '+', '0day',
                         '--date-format', 'DDMMYYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == datetime.datetime.now().strftime("%d%m%Y"))

            # Now
            with captured_output() as (out, err):
                r = main('now', '+', '0hour',
                         '--datetime-format', 'DDMMYYYY-HHMMSS')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout.startswith(datetime.datetime.now().strftime("%d%m%Y")))

            # Today error
            with captured_output() as (out, err):
                r = main('today', '+', '0day',
                         '--date-format', 'DDMMYYYY')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == datetime.datetime.now().strftime("%d%m%Y"))

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0510_debug_shige(self):
        try:
            # Today
            with captured_output() as (out, err):
                r = main('-0.11', '*', '100',
                         '--output-int-func', 'round')
            self.assertTrue(r == 0)
            stdout = out.getvalue().strip()
            print(stdout)
            self.assertTrue(stdout == '-11')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
