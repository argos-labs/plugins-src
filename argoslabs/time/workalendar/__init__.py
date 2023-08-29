"""
====================================
 :mod:`argoslabs.time.workalendar`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/11/01]
#     - days may 0 for operation 0,1
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
import re
import sys
import datetime
# import pkg_resources
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
# noinspection PyPackageRequirements
from workalendar.registry import registry
# noinspection PyPackageRequirements
from dateutil.relativedelta import relativedelta

################################################################################
# __version__ = pkg_resources.get_distribution(__package__).version


################################################################################
class WorkCal(object):
    REGION = {}
    OPLIST = [
        'Confirm working day',                  # 0
        'Add working days',                     # 1
        'Substract working days',               # 2
        'Find following working day',           # 3
        'Get first working day in a month',     # 4
        'Get last working day in a month',      # 5
        'Get holidays in the year',             # 6
        # 'Get nth weekday in month',
    ]
    DATE_REC = [
        {'YYYYMMDD': re.compile(r'[12]\d{3}[01]\d[0-3]\d')},
        {'YYYY-MM-DD': re.compile(r'[12]\d{3}-\d{1,2}-\d{1,2}')},
        {'YYYY/MM/DD': re.compile(r'[12]\d{3}/\d{1,2}/\d{1,2}')},
        {'MMDDYYYY': re.compile(r'[01]\d[0-3]\d[12]\d{3}')},
        {'MM-DD-YYYY': re.compile(r'\d{1,2}-\d{1,2}-[12]\d{3}')},
        {'MM/DD/YYYY': re.compile(r'\d{1,2}/\d{1,2}/[12]\d{3}')},
        {'B D YYYY': re.compile(r'[A-Za-z]{3}\s\d{1,2}\s[12]\d{3}')},
        {'B D, YYYY': re.compile(r'[A-Za-z]{3}\s\d{1,2},\s[12]\d{3}')},
        {'D B YYYY': re.compile(r'\d{1,2}\s[A-Za-z]{3}\s[12]\d{3}')},
        {'today': re.compile(r'today', re.IGNORECASE)},
    ]
    DATE_FORMAT = {
        'YYYYMMDD': "%Y%m%d",
        'YYYY-MM-DD': "%Y-%m-%d",
        'YYYY/MM/DD': "%Y/%m/%d",
        'MMDDYYYY': "%m%d%Y",
        'MM-DD-YYYY': "%m-%d-%Y",
        'MM/DD/YYYY': "%m/%d/%Y",
        'M/D/YYYY': "%-m/%-d/%Y" if sys.platform != 'win32' else "%#m/%#d/%Y",
        'B D YYYY': "%b %-d %Y" if sys.platform != 'win32' else "%b %#d %Y",
        'B D, YYYY': "%b %-d, %Y" if sys.platform != 'win32' else "%b %#d, %Y",
        'D B YYYY': "%-d %b %Y" if sys.platform != 'win32' else "%#d %b %Y",
    }

    # ==========================================================================
    def _get_date_format(self, datestr):
        for recd in self.DATE_REC:
            for rectype, rec in recd.items():
                m = rec.match(datestr)
                if m is None:
                    continue
                vs = None
                if rectype == 'YYYYMMDD':
                    vs = datetime.datetime.strptime(datestr, "%Y%m%d").date()
                elif rectype == 'YYYY-MM-DD':
                    vs = datetime.datetime.strptime(datestr, "%Y-%m-%d").date()
                elif rectype == 'YYYY/MM/DD':
                    vs = datetime.datetime.strptime(datestr, "%Y/%m/%d").date()
                elif rectype == 'MMDDYYYY':
                    vs = datetime.datetime.strptime(datestr, "%m%d%Y").date()
                elif rectype == 'MM-DD-YYYY':
                    vs = datetime.datetime.strptime(datestr, "%m-%d-%Y").date()
                elif rectype == 'MM/DD/YYYY':
                    vs = datetime.datetime.strptime(datestr, "%m/%d/%Y").date()
                elif rectype == 'B D YYYY':
                    vs = datetime.datetime.strptime(datestr, "%b %d %Y").date()
                elif rectype == 'B D, YYYY':
                    vs = datetime.datetime.strptime(datestr, "%b %d, %Y").date()
                elif rectype == 'D B YYYY':
                    vs = datetime.datetime.strptime(datestr, "%d %b %Y").date()
                elif rectype == 'today':
                    vs = datetime.date.today()
                if not vs:
                    raise ValueError('Cannot parse date string "%s"' % datestr)
                return vs
        raise ValueError('Cannot parse date string "%s"' % datestr)

    # ==========================================================================
    def _get_op_index(self, opstr):
        op_index = self.OPLIST.index(opstr)
        return op_index

    # ==========================================================================
    def __init__(self, args):
        self.args = args
        # parameters
        reg_code, cal_class = self.REGION.get(args.region, (None, None))
        if cal_class is None:
            raise RuntimeError('Cannot get calendar class for the region "%s"'
                               % args.region)
        # noinspection PyCallingNonCallable
        self.workcal = cal_class()
        self.date = self._get_date_format(args.date)
        self.op_index = self._get_op_index(args.op)
        # sometimes args.days may 0
        # if self.op_index in (1, 2) and not args.days:
        #     raise RuntimeError('Operation "%s" takes days parameter' % args.op)
        self.days = 0
        if args.days:
            self.days = int(args.days)
        self.date_format = self.DATE_FORMAT[args.date_format]

    # ==========================================================================
    def do(self):
        if self.op_index == 0:  # Confirm working day
            r = self.workcal.is_working_day(self.date)
            print('yes' if r else 'no', end='')
        elif self.op_index == 1:  # Add working days
            r = self.workcal.add_working_days(self.date, self.days)
            print(r.strftime(self.date_format), end='')
        elif self.op_index == 2:  # Subtract working days
            r = self.workcal.add_working_days(self.date, -self.days)
            print(r.strftime(self.date_format), end='')
        elif self.op_index == 3:  # Find following working day
            # 만약 금요일이면 다음 월요일이 나와야 정상 같은데 당일 나옴
            # 강제적으로 하루를 더해서 체크
            # https://peopledoc.github.io/workalendar/advanced.html
            dt = self.date + datetime.timedelta(days=1)
            r = self.workcal.find_following_working_day(dt)
            print(r.strftime(self.date_format), end='')
        elif self.op_index == 4:  # Get first working day in a month
            dt = datetime.date(self.date.year, self.date.month, 1)
            dtd = datetime.timedelta(days=1)
            while True:
                if self.workcal.is_working_day(dt):
                    break
                dt += dtd
            print(dt.strftime(self.date_format), end='')
        elif self.op_index == 5:  # Get last working day in a month
            dt = datetime.date(self.date.year, self.date.month, 1)
            dt += relativedelta(months=1)
            dtd = datetime.timedelta(days=1)
            while True:
                dt -= dtd
                if self.workcal.is_working_day(dt):
                    break
            print(dt.strftime(self.date_format), end='')
        elif self.op_index == 6:  # Get holidays in the year
            r = self.workcal.holidays(self.date.year)
            if r:
                print('date,holiday')
                for hdt, hds in r:
                    print('%s,%s' % (hdt.strftime(self.date_format), hds))


################################################################################
@func_log
def workalendar(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        wc = WorkCal(argspec)
        wc.do()
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    shorted = {
        'United States of America': 'USA',
    }
    dpd = {}
    for code, calendar_class in registry.region_registry.items():
        dpd[code] = calendar_class.name
        eles = code.split('-')
        if len(eles) > 1:
            nat = shorted[dpd[eles[0]]] if dpd[eles[0]] in shorted else dpd[
                eles[0]]
            dp = '%s-%s' % (nat, dpd[code])
        else:
            dp = dpd[code] if dpd[code] not in shorted else shorted[dpd[code]]
        # print("`{}` is code for '{}'".format(code, dp))
        WorkCal.REGION[dp] = (code, calendar_class)
    # for code, calendar_class in registry.region_registry.items():
    #     # print("`{}` is code for '{}'".format(code, calendar_class.name))
    #     WorkCal.REGION[calendar_class.name] = (code, calendar_class)

    with ModuleContext(
        owner='ARGOS-LABS',
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Work Calendar',
        icon_path=get_icon_path(__file__),
        description='Date Calculation of work day dependent on region',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--date-format',
                          display_name='Date Format',
                          choices=list(WorkCal.DATE_FORMAT.keys()),
                          default='YYYYMMDD',
                          help='Set the format of Date')
        # ##################################### for app dependent parameters
        mcxt.add_argument('region',
                          display_name='Region',
                          choices=list(sorted(WorkCal.REGION.keys())),
                          help='Calendar for region')
        mcxt.add_argument('date',
                          display_name='Date',
                          help='Date to calulate or "today"')
        mcxt.add_argument('op',
                          display_name='Date Op',
                          choices=WorkCal.OPLIST,
                          help='Date Operations')
        mcxt.add_argument('days', nargs="?", type=int, default=0, const=0,
                          display_name='Days for Add/Sub',
                          help='Days to add or subtract date operation')
        argspec = mcxt.parse_args(args)
        return workalendar(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
