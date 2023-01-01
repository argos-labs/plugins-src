"""
====================================
 :mod:`argoslabs.time.workalendar`
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
#  * [2021/04/13]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/03/16]
#     - Find following working day 수정
#  * [2019/08/15]
#     - Changing the region display name choices, Grouping with nation
#  * [2019/08/06]
#     - starting

################################################################################
import os
import sys
import datetime
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.time.workalendar import _main as main
from workalendar.registry import registry


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        shorted = {
            'USA': 'USA',
        }
        dpd = {}
        for code, calendar_class in registry.region_registry.items():
            dpd[code] = calendar_class.name
            eles = code.split('-')
            if len(eles) > 1:
                nat = shorted[dpd[eles[0]]] if dpd[eles[0]] in shorted else dpd[eles[0]]
                dp = '%s-%s' % (nat, dpd[code])
            else:
                dp = dpd[code] if dpd[code] not in shorted else shorted[dpd[code]]
            # print("`{}` is code for '{}'".format(code, dp))
        self.assertTrue(dpd)

    # ==========================================================================
    def test0010_failure(self):
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        try:
            _ = main('invalid', '2019/8/7', 'foo')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0030_failure(self):
        try:
            r = main('USA-California', '20/8/7', 'Add working days')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0040_failure(self):
        try:
            _ = main('USA', '2019/8/7', 'invalid op')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_is_working_day(self):
        outfile = 'stdout.txt'
        try:
            r = main('USA', '2019/8/7', 'Confirm working day',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            self.assertTrue(r == 'yes')

            r = main('USA-California', '2019/12/25', 'Confirm working day',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            self.assertTrue(r == 'no')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0110_add_working_day(self):
        outfile = 'stdout.txt'
        try:
            r = main('USA-California', '2019/8/7', 'Add working days', '5',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            self.assertTrue(r == '20190814')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0115_add_working_day_today(self):
        outfile = 'stdout.txt'
        try:
            r = main('USA-California', 'today', 'Add working days', '5',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            dt = datetime.date.today()
            dt += datetime.timedelta(days=5)
            self.assertTrue(r >= dt.strftime('"%Y%m%d'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0117_add_working_day_today(self):
        outfile = 'stdout.txt'
        try:
            r = main('USA-California', 'today', 'Add working days', '0',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            dt = datetime.date.today()
            dt += datetime.timedelta(days=0)
            self.assertTrue(r >= dt.strftime('"%Y%m%d'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0120_sub_working_day(self):
        outfile = 'stdout.txt'
        try:
            r = main('USA-California', '2019/8/7', 'Substract working days', '5',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            self.assertTrue(r == '20190731')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0130_find_the_following_working_day(self):
        outfile = 'stdout.txt'
        try:
            r = main('USA-California', '2019/8/7', 'Find following working day',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            self.assertTrue(r == '20190808')
            r = main('USA-California', '2019/8/10', 'Find following working day',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            self.assertTrue(r == '20190812')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0140_get_first_working_day_in_month(self):
        outfile = 'stdout.txt'
        try:
            r = main('USA-California', '2019/8/7', 'Get first working day in a month',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            self.assertTrue(r == '20190801')
            r = main('USA-California', '2019/6/15', 'Get first working day in a month',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            self.assertTrue(r == '20190603')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0150_get_last_working_day_in_month(self):
        outfile = 'stdout.txt'
        try:
            r = main('USA-California', '2019/8/7', 'Get last working day in a month',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            self.assertTrue(r == '20190830')
            r = main('USA-California', '2019/6/15', 'Get last working day in a month',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            self.assertTrue(r == '20190628')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0160_get_holidays(self):
        outfile = 'stdout.txt'
        try:
            r = main('USA-California', '2019/8/7', 'Get holidays in the year',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            print(r)
            lines = len(r.split('\n'))
            self.assertTrue(lines == 14)
            r = main('South Korea', '2019/8/7', 'Get holidays in the year',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
            print(r)
            lines = len(r.split('\n'))
            self.assertTrue(lines == 17)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0170_get_following_debug(self):
        # 만약 금요일이면 다음 월요일이 나와야 정상 같은데 당일 나옴
        # 강제적으로 하루를 더해서 체크
        # https://peopledoc.github.io/workalendar/advanced.html
        outfile = 'stdout.txt'
        try:
            r = main('USA-California', '2020/3/13', 'Find following working day',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
                print(r)
                self.assertTrue(r == '20200316')

            r = main('USA-California', '2020/3/11', 'Find following working day',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
                print(r)
                self.assertTrue(r == '20200312')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0180_get_last_working_debug(self):
        outfile = 'stdout.txt'
        try:
            r = main('USA-California', '2020/3/31', 'Get holidays in the year',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
                print(r)
                self.assertTrue(r.find('20200331') > 0)

            r = main('USA-California', '2020/3/31', 'Confirm working day',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
                print(r)
                self.assertTrue(r == 'no')

            r = main('USA-California', '2020/3/13', 'Get last working day in a month',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                r = ifp.read()
                print(r)
                self.assertTrue(r == '20200330')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
