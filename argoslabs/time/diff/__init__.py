"""
====================================
 :mod:`argoslabs.time.diff`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for time diff
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
#  * [2021/04/28]
#     - lable change
#     - output format
#     - diff string chopping after seconds (n days, 00:00:00)
#  * [2021/04/26]
#     - starting

################################################################################
import os
import re
import sys
import datetime
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
OUTPUT_FORMATS = [
    'In seconds',
    'Timedelta string',
    'Values 1, 0, or -1'
]
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

GUESS_REC = [
    {
        'datetime': [
            {'YYYYMMDD-HHMMSS.mmm': re.compile(
                r'[12]\d{3}[01]\d[0-3]\d[\s-][0-2]\d[0-5]\d[0-5]\d\.\d+')},
            {'YYYY-MM-DD HH:MM:SS.mmm': re.compile(
                r'[12]\d{3}-\d{1,2}-\d{1,2}[\s][0-2]\d:[0-5]\d:[0-5]\d.\d+')},
            {'YYYY/MM/DD HH:MM:SS.mmm': re.compile(
                r'[12]\d{3}/\d{1,2}/\d{1,2}[\s][0-2]\d:[0-5]\d:[0-5]\d.\d+')},
            {'MMDDYYYY-HHMMSS.mmm': re.compile(
                r'[01]\d[0-3]\d[12]\d{3}[\s-][0-2]\d[0-5]\d[0-5]\d.\d+')},
            {'MM-DD-YYYY HH:MM:SS.mmm': re.compile(
                r'\d{1,2}-\d{1,2}-[12]\d{3}[\s][0-2]\d:[0-5]\d:[0-5]\d.\d+')},
            {'MM/DD/YYYY HH:MM:SS.mmm': re.compile(
                r'\d{1,2}/\d{1,2}/[12]\d{3}[\s][0-2]\d:[0-5]\d:[0-5]\d.\d+')},
            {'YYYYMMDD-HHMMSS': re.compile(
                r'[12]\d{3}[01]\d[0-3]\d[\s-][0-2]\d[0-5]\d[0-5]\d')},
            {'YYYY-MM-DD HH:MM:SS': re.compile(
                r'[12]\d{3}-\d{1,2}-\d{1,2}[\s][0-2]\d:[0-5]\d:[0-5]\d')},
            {'YYYY/MM/DD HH:MM:SS': re.compile(
                r'[12]\d{3}/\d{1,2}/\d{1,2}[\s][0-2]\d:[0-5]\d:[0-5]\d')},
            {'MMDDYYYY-HHMMSS': re.compile(
                r'[01]\d[0-3]\d[12]\d{3}[\s-][0-2]\d[0-5]\d[0-5]\d')},
            {'MM-DD-YYYY HH:MM:SS': re.compile(
                r'\d{1,2}-\d{1,2}-[12]\d{3}[\s][0-2]\d:[0-5]\d:[0-5]\d')},
            {'MM/DD/YYYY HH:MM:SS': re.compile(
                r'\d{1,2}/\d{1,2}/[12]\d{3}[\s][0-2]\d:[0-5]\d:[0-5]\d')},
        ]
    },
    {
        'date': [
            {'YYYYMMDD': re.compile(r'[12]\d{3}[01]\d[0-3]\d')},
            {'YYYY-MM-DD': re.compile(
                r'[12]\d{3}-\d{1,2}-\d{1,2}')},
            {'YYYY/MM/DD': re.compile(
                r'[12]\d{3}/\d{1,2}/\d{1,2}')},
            {'MMDDYYYY': re.compile(r'[01]\d[0-3]\d[12]\d{3}')},
            {'MM-DD-YYYY': re.compile(
                r'\d{1,2}-\d{1,2}-[12]\d{3}')},
            {'MM/DD/YYYY': re.compile(
                r'\d{1,2}/\d{1,2}/[12]\d{3}')},
            {'B D YYYY': re.compile(
                r'[A-Za-z]{3,9}\s\d{1,2}\s[12]\d{3}')},
            {'B D, YYYY': re.compile(
                r'[A-Za-z]{3,9}\s\d{1,2},\s[12]\d{3}')},
            {'D B YYYY': re.compile(
                r'\d{1,2}\s[A-Za-z]{3,9}\s[12]\d{3}')},
            {'D B YY': re.compile(
                r'\d{1,2}\s[A-Za-z]{3,9}\s\d{2}')},
            {'DBYY': re.compile(
                r'(\d{1,2})([A-Za-z]{3,9})(\d{2})')},
        ],
    },
]


################################################################################
def get_dt_from_format(vs, rectype, m=None):
    try:
        vt = None
        if rectype == 'YYYYMMDD-HHMMSS.mmm':
            vt = datetime.datetime.strptime(vs, "%Y%m%d-%H%M%S.%f")
        elif rectype == 'YYYY-MM-DD HH:MM:SS.mmm':
            vt = datetime.datetime.strptime(vs, "%Y-%m-%d %H:%M:%S.%f")
        elif rectype == 'YYYY/MM/DD HH:MM:SS.mmm':
            vt = datetime.datetime.strptime(vs, "%Y/%m/%d %H:%M:%S.%f")
        elif rectype == 'MMDDYYYY-HHMMSS.mmm':
            vt = datetime.datetime.strptime(vs, "%m%d%Y-%H%M%S.%f")
        elif rectype == 'MM-DD-YYYY HH:MM:SS.mmm':
            vt = datetime.datetime.strptime(vs, "%m-%d-%Y %H:%M:%S.%f")
        elif rectype == 'MM/DD/YYYY HH:MM:SS.mmm':
            vt = datetime.datetime.strptime(vs, "%m/%d/%Y %H:%M:%S.%f")

        elif rectype == 'DDMMYYYY-HHMMSS.mmm':
            vt = datetime.datetime.strptime(vs, "%d%m%Y-%H%M%S.%f")
        elif rectype == 'DD-MM-YYYY HH:MM:SS.mmm':
            vt = datetime.datetime.strptime(vs, "%d-%m-%Y %H:%M:%S.%f")
        elif rectype == 'DD/MM/YYYY HH:MM:SS.mmm':
            vt = datetime.datetime.strptime(vs, "%d/%m/%Y %H:%M:%S.%f")

        elif rectype == 'YYYYMMDD-HHMMSS':
            vt = datetime.datetime.strptime(vs, f"%Y%m%d{vs[8]}%H%M%S")
        elif rectype == 'YYYY-MM-DD HH:MM:SS':
            vt = datetime.datetime.strptime(vs, "%Y-%m-%d %H:%M:%S")
        elif rectype == 'YYYY/MM/DD HH:MM:SS':
            vt = datetime.datetime.strptime(vs, "%Y/%m/%d %H:%M:%S")
        elif rectype == 'MMDDYYYY-HHMMSS':
            vt = datetime.datetime.strptime(vs, "%m%d%Y-%H%M%S")
        elif rectype == 'MM-DD-YYYY HH:MM:SS':
            vt = datetime.datetime.strptime(vs, "%m-%d-%Y %H:%M:%S")
        elif rectype == 'MM/DD/YYYY HH:MM:SS':
            vt = datetime.datetime.strptime(vs, "%m/%d/%Y %H:%M:%S")

        elif rectype == 'DDMMYYYY-HHMMSS':
            vt = datetime.datetime.strptime(vs, "%d%m%Y-%H%M%S")
        elif rectype == 'DD-MM-YYYY HH:MM:SS':
            vt = datetime.datetime.strptime(vs, "%d-%m-%Y %H:%M:%S")
        elif rectype == 'DD/MM/YYYY HH:MM:SS':
            vt = datetime.datetime.strptime(vs, "%d/%m/%Y %H:%M:%S")

        elif rectype == 'YYYYMMDD':
            vt = datetime.datetime.strptime(vs, "%Y%m%d").date()
        elif rectype == 'YYYY-MM-DD':
            vt = datetime.datetime.strptime(vs, "%Y-%m-%d").date()
        elif rectype == 'YYYY/MM/DD':
            vt = datetime.datetime.strptime(vs, "%Y/%m/%d").date()
        elif rectype == 'MMDDYYYY':
            vt = datetime.datetime.strptime(vs, "%m%d%Y").date()
        elif rectype == 'MM-DD-YYYY':
            vt = datetime.datetime.strptime(vs, "%m-%d-%Y").date()
        elif rectype == 'MM/DD/YYYY':
            vt = datetime.datetime.strptime(vs, "%m/%d/%Y").date()

        elif rectype == 'DDMMYYYY':
            vt = datetime.datetime.strptime(vs, "%d%m%Y").date()
        elif rectype == 'DD-MM-YYYY':
            vt = datetime.datetime.strptime(vs, "%d-%m-%Y").date()
        elif rectype == 'DD/MM/YYYY':
            vt = datetime.datetime.strptime(vs, "%d/%m/%Y").date()

        elif rectype == 'B D YYYY':
            eles = vs.split()
            if len(eles[0]) > 3:
                eles[0] = eles[0][:3]
            vt = datetime.datetime.strptime(' '.join(eles), "%b %d %Y").date()
        elif rectype == 'B D, YYYY':
            eles = vs.split()
            if len(eles[0]) > 3:
                eles[0] = eles[0][:3]
            vt = datetime.datetime.strptime(' '.join(eles), "%b %d, %Y").date()
        elif rectype == 'D B YYYY':
            eles = vs.split()
            if len(eles[1]) > 3:
                eles[1] = eles[1][:3]
            vt = datetime.datetime.strptime(' '.join(eles), "%d %b %Y").date()
        elif rectype == 'D B YY':
            eles = vs.split()
            if len(eles[1]) > 3:
                eles[1] = eles[1][:3]
            eles[2] = '20' + eles[2]
            vt = datetime.datetime.strptime(' '.join(eles), "%d %b %Y").date()
        elif rectype == 'DBYY':
            eles = list(m.groups(1))
            if len(eles[1]) > 3:
                eles[1] = eles[1][:3]
            eles[2] = '20' + eles[2]
            vt = datetime.datetime.strptime(' '.join(eles), "%d %b %Y").date()
        return vt
    except Exception:
        raise ValueError(f'Failure to get proper Date/Time "{vs}" from format "{rectype}"')


################################################################################
def get_dt_format(vs, input_dt_format='Auto'):
    if input_dt_format != 'Auto':
        return get_dt_from_format(vs, input_dt_format)
    b_resolve = False
    for vt_recl in GUESS_REC:
        for vtype, reclist in vt_recl.items():
            if b_resolve:
                break
            for recd in reclist:
                if b_resolve:
                    break
                for rectype, rec in recd.items():
                    m = rec.match(vs)
                    if m is None:
                        continue
                    # if vtype.startswith('date'):
                    vt = get_dt_from_format(vs, rectype, m)
                    if vt is not None:
                        return vt
    return None


################################################################################
@func_log
def do_diff(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if not argspec.dt1:
            raise RuntimeError('Invalid "Left Date/Time"')
        if not argspec.dt2:
            raise RuntimeError('Invalid "Right Date/Time"')
        dt1 = get_dt_format(argspec.dt1, argspec.input_dt_format)
        if not dt1:
            raise RuntimeError(f'Invalid "Left Date/Time" format: {argspec.dt1}')
        dt2 = get_dt_format(argspec.dt2, argspec.input_dt_format)
        if not dt2:
            raise RuntimeError(f'Invalid "Left Date/Time" format: {argspec.dt2}')
        t_diff = dt1 - dt2
        if argspec.output_format == OUTPUT_FORMATS[1]:
            so = str(t_diff)
            print(so, end='')
            return 0
        td = int(t_diff.total_seconds())
        if argspec.output_format == OUTPUT_FORMATS[2]:
            if td > 0:
                td = 1
            elif td < 0:
                td = -1
        print(td, end='')
        return 0
    except Exception as e:
        msg = 'argoslabs.time.diff Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 9
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Time Diff',
        icon_path=get_icon_path(__file__),
        description='Get Time Diff',
    ) as mcxt:

        # ############################################ for app dependent options
        mcxt.add_argument('dt1',
                          display_name='Date/Time 1',
                          help='Left Date/Time')
        mcxt.add_argument('dt2',
                          display_name='Date/Time 2',
                          help='Right Date/Time 2')
        # ######################################### for app dependent parameters
        mcxt.add_argument('output_format',
                          display_name='Output Options',
                          choices=OUTPUT_FORMATS,
                          default=OUTPUT_FORMATS[0],
                          help='Set the format of TimeStamp')
        # ##################################### for app dependent options
        mcxt.add_argument('--input-dt-format',
                          display_name='Input Date/Time',
                          choices=INPUT_DT_FORMAT,
                          default=INPUT_DT_FORMAT[0],
                          help='Input Date/DateTime format')

        argspec = mcxt.parse_args(args)
        return do_diff(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
