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
ARGOS LABS plugin module for binary op
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
import os
import re
import sys
import math
import datetime
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from dateutil.relativedelta import relativedelta


################################################################################
class BinOp(object):
    # round, ceil, floor, trunc
    INT_FUNC = {
        'round': round,
        'ceil': math.ceil,
        'floor': math.floor,
        'trunc': math.trunc,
    }
    GUESS_REC = [
        {
            'datetime': [
                {'YYYYMMDD-HHMMSS.mmm': re.compile(r'[12]\d{3}[01]\d[0-3]\d[\s-][0-2]\d[0-5]\d[0-5]\d\.\d+')},
                {'YYYY-MM-DD HH:MM:SS.mmm': re.compile(r'[12]\d{3}-\d{1,2}-\d{1,2}[\s][0-2]\d:[0-5]\d:[0-5]\d.\d+')},
                {'YYYY/MM/DD HH:MM:SS.mmm': re.compile(r'[12]\d{3}/\d{1,2}/\d{1,2}[\s][0-2]\d:[0-5]\d:[0-5]\d.\d+')},
                {'MMDDYYYY-HHMMSS.mmm': re.compile(r'[01]\d[0-3]\d[12]\d{3}[\s-][0-2]\d[0-5]\d[0-5]\d.\d+')},
                {'MM-DD-YYYY HH:MM:SS.mmm': re.compile(r'\d{1,2}-\d{1,2}-[12]\d{3}[\s][0-2]\d:[0-5]\d:[0-5]\d.\d+')},
                {'MM/DD/YYYY HH:MM:SS.mmm': re.compile(r'\d{1,2}/\d{1,2}/[12]\d{3}[\s][0-2]\d:[0-5]\d:[0-5]\d.\d+')},
                {'YYYYMMDD-HHMMSS': re.compile(r'[12]\d{3}[01]\d[0-3]\d[\s-][0-2]\d[0-5]\d[0-5]\d')},
                {'YYYY-MM-DD HH:MM:SS': re.compile(r'[12]\d{3}-\d{1,2}-\d{1,2}[\s][0-2]\d:[0-5]\d:[0-5]\d')},
                {'YYYY/MM/DD HH:MM:SS': re.compile(r'[12]\d{3}/\d{1,2}/\d{1,2}[\s][0-2]\d:[0-5]\d:[0-5]\d')},
                {'MMDDYYYY-HHMMSS': re.compile(r'[01]\d[0-3]\d[12]\d{3}[\s-][0-2]\d[0-5]\d[0-5]\d')},
                {'MM-DD-YYYY HH:MM:SS': re.compile(r'\d{1,2}-\d{1,2}-[12]\d{3}[\s][0-2]\d:[0-5]\d:[0-5]\d')},
                {'MM/DD/YYYY HH:MM:SS': re.compile(r'\d{1,2}/\d{1,2}/[12]\d{3}[\s][0-2]\d:[0-5]\d:[0-5]\d')},
            ]
        },
        {
            'date': [
                {'YYYYMMDD': re.compile(r'[12]\d{3}[01]\d[0-3]\d')},
                {'YYYY-MM-DD': re.compile(r'[12]\d{3}-\d{1,2}-\d{1,2}')},
                {'YYYY/MM/DD': re.compile(r'[12]\d{3}/\d{1,2}/\d{1,2}')},
                {'MMDDYYYY': re.compile(r'[01]\d[0-3]\d[12]\d{3}')},
                {'MM-DD-YYYY': re.compile(r'\d{1,2}-\d{1,2}-[12]\d{3}')},
                {'MM/DD/YYYY': re.compile(r'\d{1,2}/\d{1,2}/[12]\d{3}')},
                {'B D YYYY': re.compile(r'[A-Za-z]{3,9}\s\d{1,2}\s[12]\d{3}')},
                {'B D, YYYY': re.compile(r'[A-Za-z]{3,9}\s\d{1,2},\s[12]\d{3}')},
                {'D B YYYY': re.compile(r'\d{1,2}\s[A-Za-z]{3,9}\s[12]\d{3}')},
                {'D B YY': re.compile(r'\d{1,2}\s[A-Za-z]{3,9}\s\d{2}')},
                {'DBYY': re.compile(r'(\d{1,2})([A-Za-z]{3,9})(\d{2})')},
            ],
        },
        {
            'timedelta': [
                {'nday': re.compile(r'(\d+)(day)')},
                {'nhour': re.compile(r'(\d+)(hour)')},
                {'nmin': re.compile(r'(\d+)(min)')},
                {'nsec': re.compile(r'(\d+)(sec)')},
                {'nmsec': re.compile(r'(\d+)(msec)')},
                {'nusec': re.compile(r'(\d+)(usec)')},
                {'nweek': re.compile(r'(\d+)week')},
                {'nmonth': re.compile(r'(\d+)month')},
                {'nyear': re.compile(r'(\d+)year')},
            ],
        },
        {
            'float': [
                {'n.n': re.compile(r'-?\d+\.\d+')},
                {'.n': re.compile(r'-?\.\d+')},
                {'n.': re.compile(r'-?\d+\.')},
            ],
        },
        {
            'int': [
                {'n': re.compile(r'-?\d+')},
            ],
        },
    ]
    DATETIME_FORMAT = {
        'YYYYMMDD-HHMMSS': "%Y%m%d-%H%M%S",
        'YYYY-MM-DD HH:MM:SS': "%Y-%m-%d %H:%M:%S",
        'YYYY/MM/DD HH:MM:SS': "%Y/%m/%d %H:%M:%S",
        'MMDDYYYY-HHMMSS': "%m%d%Y-%H%M%S",
        'MM-DD-YYYY HH:MM:SS': "%m-%d-%Y %H:%M:%S",
        'MM/DD/YYYY HH:MM:SS': "%m/%d/%Y %H:%M:%S",
        'M/D/YYYY HH:MM:SS': "%-m/%-d/%Y %H:%M:%S" if sys.platform != 'win32' else "%#m/%#d/%Y %H:%M:%S",
        'DDMMYYYY-HHMMSS': "%d%m%Y-%H%M%S",
        'DD-MM-YYYY HH:MM:SS': "%d-%m-%Y %H:%M:%S",
        'DD/MM/YYYY HH:MM:SS': "%d/%m/%Y %H:%M:%S",
        'D/M/YYYY HH:MM:SS': "%-d/%-m/%Y %H:%M:%S" if sys.platform != 'win32' else "%#d/%#m/%Y %H:%M:%S",
        'YYYYMMDD-HHMMSS.mmm': "%Y%m%d-%H%M%S.%f",
        'YYYY-MM-DD HH:MM:SS.mmm': "%Y-%m-%d %H:%M:%S.%f",
        'YYYY/MM/DD HH:MM:SS.mmm': "%Y/%m/%d %H:%M:%S.%f",
        'MMDDYYYY-HHMMSS.mmm': "%m%d%Y-%H%M%S.%f",
        'MM-DD-YYYY HH:MM:SS.mmm': "%m-%d-%Y %H:%M:%S.%f",
        'MM/DD/YYYY HH:MM:SS.mmm': "%m/%d/%Y %H:%M:%S.%f",
        'M/D/YYYY HH:MM:SS.mmm': "%-m/%-d/%Y %H:%M:%S.%f" if sys.platform != 'win32' else "%#m/%#d/%Y %H:%M:%S.%f",
        'DDMMYYYY-HHMMSS.mmm': "%d%m%Y-%H%M%S.%f",
        'DD-MM-YYYY HH:MM:SS.mmm': "%d-%m-%Y %H:%M:%S.%f",
        'DD/MM/YYYY HH:MM:SS.mmm': "%d/%m/%Y %H:%M:%S.%f",
        'D/M/YYYY HH:MM:SS.mmm': "%-d/%-m/%Y %H:%M:%S.%f" if sys.platform != 'win32' else "%#d/%#m/%Y %H:%M:%S.%f",
    }
    DATE_FORMAT = {
        'YYYYMMDD': "%Y%m%d",
        'YYYY-MM-DD': "%Y-%m-%d",
        'YYYY/MM/DD': "%Y/%m/%d",
        'MMDDYYYY': "%m%d%Y",
        'MM-DD-YYYY': "%m-%d-%Y",
        'MM/DD/YYYY': "%m/%d/%Y",
        'M/D/YYYY': "%-m/%-d/%Y" if sys.platform != 'win32' else "%#m/%#d/%Y",
        'DDMMYYYY': "%d%m%Y",
        'DD-MM-YYYY': "%d-%m-%Y",
        'DD/MM/YYYY': "%d/%m/%Y",
        'D/M/YYYY': "%-d/%-m/%Y" if sys.platform != 'win32' else "%#d/%#m/%Y",
        'B D YYYY': "%b %-d %Y" if sys.platform != 'win32' else "%b %#d %Y",
        'B D, YYYY': "%b %-d, %Y" if sys.platform != 'win32' else "%b %#d, %Y",
        'D B YYYY': "%-d %b %Y" if sys.platform != 'win32' else "%#d %b %Y",
        'D B YY': "%-d %b %Y" if sys.platform != 'win32' else "%#d %b %Y",
        'DBYY': "%-d%b%Y" if sys.platform != 'win32' else "%#d%b%Y",
    }
    INPUT_DT_FORMAT = [
        'Auto',
        'YYYYMMDD-HHMMSS.mmm',
        'YYYY-MM-DD HH:MM:SS.mmm',
        'YYYY/MM/DD HH:MM:SS.mmm',
        'MMDDYYYY-HHMMSS.mmm',
        'MM-DD-YYYY HH:MM:SS.mmm',
        'MM/DD/YYYY HH:MM:SS.mmm',
        'DDMMYYYY-HHMMSS.mmm',
        'DD-MM-YYYY HH:MM:SS.mmm',
        'DD/MM/YYYY HH:MM:SS.mmm',
        'YYYYMMDD-HHMMSS',
        'YYYY-MM-DD HH:MM:SS',
        'YYYY/MM/DD HH:MM:SS',
        'MMDDYYYY-HHMMSS',
        'MM-DD-YYYY HH:MM:SS',
        'MM/DD/YYYY HH:MM:SS',
        'DDMMYYYY-HHMMSS',
        'DD-MM-YYYY HH:MM:SS',
        'DD/MM/YYYY HH:MM:SS',
        'YYYYMMDD',
        'YYYY/MM/DD',
        'MMDDYYYY',
        'MM-DD-YYYY',
        'MM/DD/YYYY',
        'DDMMYYYY',
        'DD-MM-YYYY',
        'DD/MM/YYYY',
    ]

    # ==========================================================================
    def __init__(self, argspec, logger=None):
        self.left = argspec.left.strip()
        if argspec.datetime_separator:
            self.left = self.left.replace(argspec.datetime_separator, '/')
        self.output_date_format = argspec.output_date_format
        self.op = argspec.operation.strip()
        self.right = argspec.right.strip()
        vtype = argspec.type
        if vtype not in ("auto", "string", "int", "float", "date", "datetime"):
            raise RuntimeError('Invalid value type "%s"' % vtype)
        self.vtype = vtype
        self.input_dt_format = argspec.input_dt_format
        if self.input_dt_format not in self.INPUT_DT_FORMAT:
            raise ReferenceError(f'Invalid Input Date/Time format')
        if self.input_dt_format != self.INPUT_DT_FORMAT[0]:  # Not Auto
            if self.input_dt_format in (
                    'YYYYMMDD',
                    'YYYY/MM/DD',
                    'MMDDYYYY',
                    'MM-DD-YYYY',
                    'MM/DD/YYYY',
                    'DDMMYYYY',
                    'DD-MM-YYYY',
                    'DD/MM/YYYY',):
                self.vtype = 'date'
            else:
                self.vtype = 'datetime'
        if logger is None:
            raise RuntimeError('logger must not None!')
        self.date_format = argspec.date_format
        self.datetime_format = argspec.datetime_format
        self.output_int_func = argspec.output_int_func
        self.logger = logger

    # ==========================================================================
    def get_dt_from_format(self, vs, rectype, m=None):
        if rectype == 'YYYYMMDD-HHMMSS.mmm':
            vs = datetime.datetime.strptime(vs, "%Y%m%d-%H%M%S.%f")
        elif rectype == 'YYYY-MM-DD HH:MM:SS.mmm':
            vs = datetime.datetime.strptime(vs, "%Y-%m-%d %H:%M:%S.%f")
        elif rectype == 'YYYY/MM/DD HH:MM:SS.mmm':
            vs = datetime.datetime.strptime(vs, "%Y/%m/%d %H:%M:%S.%f")
        elif rectype == 'MMDDYYYY-HHMMSS.mmm':
            vs = datetime.datetime.strptime(vs, "%m%d%Y-%H%M%S.%f")
        elif rectype == 'MM-DD-YYYY HH:MM:SS.mmm':
            vs = datetime.datetime.strptime(vs, "%m-%d-%Y %H:%M:%S.%f")
        elif rectype == 'MM/DD/YYYY HH:MM:SS.mmm':
            vs = datetime.datetime.strptime(vs, "%m/%d/%Y %H:%M:%S.%f")

        elif rectype == 'DDMMYYYY-HHMMSS.mmm':
            vs = datetime.datetime.strptime(vs, "%d%m%Y-%H%M%S.%f")
        elif rectype == 'DD-MM-YYYY HH:MM:SS.mmm':
            vs = datetime.datetime.strptime(vs, "%d-%m-%Y %H:%M:%S.%f")
        elif rectype == 'DD/MM/YYYY HH:MM:SS.mmm':
            vs = datetime.datetime.strptime(vs, "%d/%m/%Y %H:%M:%S.%f")

        elif rectype == 'YYYYMMDD-HHMMSS':
            vs = datetime.datetime.strptime(vs, "%Y%m%d-%H%M%S")
        elif rectype == 'YYYY-MM-DD HH:MM:SS':
            vs = datetime.datetime.strptime(vs, "%Y-%m-%d %H:%M:%S")
        elif rectype == 'YYYY/MM/DD HH:MM:SS':
            vs = datetime.datetime.strptime(vs, "%Y/%m/%d %H:%M:%S")
        elif rectype == 'MMDDYYYY-HHMMSS':
            vs = datetime.datetime.strptime(vs, "%m%d%Y-%H%M%S")
        elif rectype == 'MM-DD-YYYY HH:MM:SS':
            vs = datetime.datetime.strptime(vs, "%m-%d-%Y %H:%M:%S")
        elif rectype == 'MM/DD/YYYY HH:MM:SS':
            vs = datetime.datetime.strptime(vs, "%m/%d/%Y %H:%M:%S")

        elif rectype == 'DDMMYYYY-HHMMSS':
            vs = datetime.datetime.strptime(vs, "%d%m%Y-%H%M%S")
        elif rectype == 'DD-MM-YYYY HH:MM:SS':
            vs = datetime.datetime.strptime(vs, "%d-%m-%Y %H:%M:%S")
        elif rectype == 'DD/MM/YYYY HH:MM:SS':
            vs = datetime.datetime.strptime(vs, "%d/%m/%Y %H:%M:%S")

        elif rectype == 'YYYYMMDD':
            vs = datetime.datetime.strptime(vs, "%Y%m%d").date()
        elif rectype == 'YYYY-MM-DD':
            vs = datetime.datetime.strptime(vs, "%Y-%m-%d").date()
        elif rectype == 'YYYY/MM/DD':
            vs = datetime.datetime.strptime(vs, "%Y/%m/%d").date()
        elif rectype == 'MMDDYYYY':
            vs = datetime.datetime.strptime(vs, "%m%d%Y").date()
        elif rectype == 'MM-DD-YYYY':
            vs = datetime.datetime.strptime(vs, "%m-%d-%Y").date()
        elif rectype == 'MM/DD/YYYY':
            vs = datetime.datetime.strptime(vs, "%m/%d/%Y").date()

        elif rectype == 'DDMMYYYY':
            vs = datetime.datetime.strptime(vs, "%d%m%Y").date()
        elif rectype == 'DD-MM-YYYY':
            vs = datetime.datetime.strptime(vs, "%d-%m-%Y").date()
        elif rectype == 'DD/MM/YYYY':
            vs = datetime.datetime.strptime(vs, "%d/%m/%Y").date()

        elif rectype == 'B D YYYY':
            eles = vs.split()
            if len(eles[0]) > 3:
                eles[0] = eles[0][:3]
            vs = datetime.datetime.strptime(' '.join(eles), "%b %d %Y").date()
        elif rectype == 'B D, YYYY':
            eles = vs.split()
            if len(eles[0]) > 3:
                eles[0] = eles[0][:3]
            vs = datetime.datetime.strptime(' '.join(eles), "%b %d, %Y").date()
        elif rectype == 'D B YYYY':
            eles = vs.split()
            if len(eles[1]) > 3:
                eles[1] = eles[1][:3]
            vs = datetime.datetime.strptime(' '.join(eles), "%d %b %Y").date()
        elif rectype == 'D B YY':
            eles = vs.split()
            if len(eles[1]) > 3:
                eles[1] = eles[1][:3]
            eles[2] = '20' + eles[2]
            vs = datetime.datetime.strptime(' '.join(eles),
                                            "%d %b %Y").date()
        elif rectype == 'DBYY':
            eles = list(m.groups(1))
            if len(eles[1]) > 3:
                eles[1] = eles[1][:3]
            eles[2] = '20' + eles[2]
            vs = datetime.datetime.strptime(' '.join(eles),
                                            "%d %b %Y").date()
        return vs

    # ==========================================================================
    def resolve_val_type(self, vs, vt, filter_=None):
        b_resolve = False
        if isinstance(filter_, str):
            filter_ = [filter_]
        for vt_recl in self.GUESS_REC:
            if b_resolve:
                break
            for vtype, reclist in vt_recl.items():
                if filter_ is not None and vtype not in filter_:
                    continue
                if b_resolve:
                    break
                for recd in reclist:
                    if b_resolve:
                        break
                    for rectype, rec in recd.items():
                        m = rec.match(vs)
                        if m is None:
                            continue
                        # g = m.group()
                        vt = vtype
                        if vtype.startswith('date'):
                            vs = self.get_dt_from_format(vs, rectype, m)
                        elif vtype == 'timedelta':
                            if vs.endswith('day'):
                                vs = datetime.timedelta(days=int(vs[:-3]))
                            elif vs.endswith('hour'):
                                vs = datetime.timedelta(hours=int(vs[:-4]))
                            elif vs.endswith('min'):
                                vs = datetime.timedelta(minutes=int(vs[:-3]))
                            elif vs.endswith('msec'):
                                vs = datetime.timedelta(milliseconds=int(vs[:-4]))
                            elif vs.endswith('usec'):
                                vs = datetime.timedelta(microseconds=int(vs[:-4]))
                            elif vs.endswith('sec'):
                                vs = datetime.timedelta(seconds=int(vs[:-3]))
                            elif vs.endswith('week'):
                                vs = datetime.timedelta(weeks=int(vs[:-4]))
                            elif vs.endswith('month'):
                                vs = relativedelta(months=int(vs[:-5]))
                            elif vs.endswith('year'):
                                vs = relativedelta(years=int(vs[:-4]))
                        else:
                            vs = eval('%s("%s")' % (vt, vs))
                        return vs, vt
        if vt == 'auto':
            if filter_ is not None:
                return None, None
            vt = "string"
            return vs, vt

    # ==========================================================================
    def get_val_type(self, vs, vt):
        if vs.lower() == 'today':
            return datetime.date.today(), 'date'
        elif vs.lower() == 'now':
            return datetime.datetime.now(), 'datetime'
        if vt == 'auto':
            return self.resolve_val_type(vs, vt)
        else:
            if vt == 'string':
                return str(vs), vt
            elif vt == 'int':
                tvs, tvt = self.resolve_val_type(vs, 'auto', filter_=['int', 'float'])
                return int(tvs), vt
            elif vt == 'float':
                return float(vs), vt
            elif vt == 'date':
                return self.resolve_val_type(vs, 'auto', filter_=['date', 'timedelta'])
            elif vt == 'datetime':
                return self.resolve_val_type(vs, 'auto', filter_=['datetime', 'timedelta'])
        if vt == 'auto':
            raise RuntimeError('Cannot guess type for the value "%s"' % vs)
        if vt == 'datetime':
            pass

    # ==========================================================================
    def get_dt_val_type(self, vs, vt):
        vs = self.get_dt_from_format(vs, self.input_dt_format)
        return vs, vt

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def get_custom_date_type(self, vs, vt):
        # parse with self.input_date_format
        vt = 'date'
        return vs, vt

    # ==========================================================================
    def get_custom_datetime(self, rv):
        r = None
        if self.output_date_format:
            r = self.output_date_format
            r = r.replace('YYYY', str(rv.year))
            r = r.replace('YY', str(rv.year % 100))
            r = r.replace('MM', '%02d' % rv.month)
            r = r.replace('M', '%d' % rv.month)
            r = r.replace('DD', '%02d' % rv.day)
            r = r.replace('D', '%d' % rv.day)
            if isinstance(rv, datetime.datetime):
                r = r.replace('hh', '%02d' % rv.hour)
                r = r.replace('h', '%d' % rv.hour)
                r = r.replace('mm', '%02d' % rv.minute)
                r = r.replace('m', '%d' % rv.minute)
                r = r.replace('ss', '%02d' % rv.second)
                r = r.replace('s', '%d' % rv.second)
        else:
            if isinstance(rv, datetime.datetime):
                r = rv.strftime(self.DATETIME_FORMAT[self.datetime_format])
            elif isinstance(rv, datetime.date):
                r = rv.strftime(self.DATE_FORMAT[self.date_format])
        return r

    # ==========================================================================
    def calc(self):
        # if self.input_date_format:
        #     left, l_vtype = self.get_custom_date_type(self.left, self.vtype)
        # else:
        #     left, l_vtype = self.get_val_type(self.left, self.vtype)
        if self.input_dt_format != self.INPUT_DT_FORMAT[0]:  # Not Auto
            left, l_vtype = self.get_dt_val_type(self.left, self.vtype)
        else:
            left, l_vtype = self.get_val_type(self.left, self.vtype)
        right, r_vtype = self.get_val_type(self.right, self.vtype)
        if l_vtype != r_vtype:
            nok = True
            if {'int', 'float'} == {l_vtype, r_vtype}:
                nok = False
            if nok and l_vtype in ('date', 'datetime'):
                if r_vtype == 'timedelta':
                    nok = False
                else:
                    raise RuntimeError('date or datetime type need right operand of timedelta type')
            if nok and l_vtype == 'string' and r_vtype == 'int' and self.op == '*':
                nok = False
            if nok and l_vtype == 'string':
                right = str(right)
                r_vtype = 'string'
                nok = False
            if nok and r_vtype == 'string':
                left = str(left)
                l_vtype = 'string'
                nok = False
            if nok:
                raise RuntimeError('Unsupported Calculation value type between "%s" and "%s"'
                                   % (l_vtype, r_vtype))
        else:
            if l_vtype == 'date':
                raise RuntimeError('"date op date" is not permitted, but "date op timedelta" is allowed.')
            if l_vtype == 'datetime' and self.op != '-':
                raise RuntimeError('Only "datetime - datetime" is allowed.')
        rv = None
        if self.op == '+':
            rv = left + right
        elif self.op == '-':
            if l_vtype == 'string':
                rv = left.replace(right, '')
            else:
                rv = left - right
        elif self.op == '*':
            rv = left * right
        elif self.op == '/':
            rv = left / right
        elif self.op == '%':
            rv = left % right
        # output format or function
        if isinstance(rv, float) and self.output_int_func:
            rv = int(self.INT_FUNC[self.output_int_func](rv))
        if isinstance(rv, (datetime.datetime, datetime.date)):
            sys.stdout.write(self.get_custom_datetime(rv))
        else:
            sys.stdout.write('%s' % rv)
        return 0


################################################################################
@func_log
def do_binop(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        bo = BinOp(argspec, logger=mcxt.logger)
        r = bo.calc()
        return r
    except Exception as e:
        msg = 'argoslabs.filesystem.op Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Arithmetic Op',
        icon_path=get_icon_path(__file__),
        description='Binary operation',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--type', '-t',
                          display_name='Value Type', show_default=True,
                          choices=["auto", "string", "int", "float", "date", "datetime"],
                          default='auto',
                          help='Set Value type, one of {"auto", "int", "float", "date", "datetime"}.'
                               ' Default is auto which means try to guess the best type of value')
        mcxt.add_argument('--input-dt-format',
                          display_name='Input Date/Time',
                          choices=BinOp.INPUT_DT_FORMAT,
                          default=BinOp.INPUT_DT_FORMAT[0],
                          help='Input Date/DateTime format')
        mcxt.add_argument('--date-format',
                          display_name='Out Date Format',
                          choices=list(BinOp.DATE_FORMAT.keys()),
                          default='YYYYMMDD',
                          help='Set output format of Date')
        mcxt.add_argument('--datetime-format',
                          display_name='Out DateTime Format',
                          choices=list(BinOp.DATETIME_FORMAT.keys()),
                          default='YYYYMMDD-HHMMSS',
                          help='Set output format of DateTime')
        mcxt.add_argument('--datetime-separator',
                          display_name='DateTime Separator',
                          help='Separator of Date or DateTime like "/" (Applied left operand only)')
        mcxt.add_argument('--output-date-format',
                          display_name='Custom Date Format',
                          help='Output format for Date or Datetime with combination of YYYY|YY MM|M DD|D hh|h mm|m ss|s and separator')
        mcxt.add_argument('--output-int-func',
                          display_name='Output Int Func',
                          choices=list(BinOp.INT_FUNC.keys()),
                          help='Output Integer Function for the integer output like round, ceil, floor, trunc')

        # ##################################### for app dependent parameters
        mcxt.add_argument('left',
                          display_name='Left Val',
                          help='Left operand for binary operation')
        mcxt.add_argument('operation',
                          display_name='Operator',
                          choices=['+', '-', '*', '/', '%'],
                          help='Binary operation, one of "+(add),-(subtract),*(multiply),/(divide),%%(modular)"')
        mcxt.add_argument('right',
                          display_name='Right Val',
                          help='Right operand for binary operation')
        argspec = mcxt.parse_args(args)
        return do_binop(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
