#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.time.getts`
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
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/04/10]
#     - add date format
#  * [2019/07/22]
#     - starting

################################################################################
import os
import sys
import datetime
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path

################################################################################
OUTPUT_FORMATS = {
    # Data & Time
    'YYYYMMDD-HHMMSS.mmm': "%Y%m%d-%H%M%S.%f",
    'YYYY-MM-DD HH:MM:SS.mmm': "%Y-%m-%d %H:%M:%S.%f",
    'YYYY/MM/DD HH:MM:SS.mmm': "%Y/%m/%d %H:%M:%S.%f",
    'MMDDYYYY-HHMMSS.mmm': "%m%d%Y-%H%M%S.%f",
    'MM-DD-YYYY HH:MM:SS.mmm': "%m-%d-%Y %H:%M:%S.%f",
    'MM/DD/YYYY HH:MM:SS.mmm': "%m/%d/%Y %H:%M:%S.%f",
    'M/D/YYYY HH:MM:SS.mmm': "%-m/%-d/%Y %H:%M:%S.%f" if sys.platform != 'win32' else "%#m/%#d/%Y %H:%M:%S.%f",
    'YYYYMMDD-HHMMSS': "%Y%m%d-%H%M%S",
    'YYYY-MM-DD HH:MM:SS': "%Y-%m-%d %H:%M:%S",
    'YYYY/MM/DD HH:MM:SS': "%Y/%m/%d %H:%M:%S",
    'MMDDYYYY-HHMMSS': "%m%d%Y-%H%M%S",
    'MM-DD-YYYY HH:MM:SS': "%m-%d-%Y %H:%M:%S",
    'MM/DD/YYYY HH:MM:SS': "%m/%d/%Y %H:%M:%S",
    'M/D/YYYY HH:MM:SS': "%-m/%-d/%Y %H:%M:%S" if sys.platform != 'win32' else "%#m/%#d/%Y %H:%M:%S",
    # Date
    'YYYYMMDD': "%Y%m%d",
    'YYYY-MM-DD': "%Y-%m-%d",
    'YYYY/MM/DD': "%Y/%m/%d",
    'MMDDYYYY': "%m%d%Y",
    'MM-DD-YYYY': "%m-%d-%Y",
    'MM/DD/YYYY': "%m/%d/%Y",
    'M/D/YYYY': "%-m/%-d/%Y" if sys.platform != 'win32' else "%#m/%#d/%Y",
    'DD-MM-YYYY': "%d-%m-%Y",
    'DD.MM.YYYY': "%d.%m.%Y",
    'DD-MM-YY': "%d-%m-",
    'DD.MM.YY': "%d.%m.",
}

################################################################################
@func_log
def do_binop(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if argspec.output_format not in OUTPUT_FORMATS:
            raise RuntimeError('Cannot find the format for "%s"' % argspec.output_format)
        if argspec.use_utc:
            now = datetime.datetime.utcnow()
        else:
            now = datetime.datetime.now()
        tstr = now.strftime(OUTPUT_FORMATS[argspec.output_format])
        if argspec.output_format in ('DD-MM-YY', 'DD.MM.YY'):
            tstr += '%02d' % (now.year % 100)
        print(tstr, end='')
        return 0
    except Exception as e:
        msg = 'argoslabs.filesystem.op Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        raise
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
        display_name='TimeStamp',
        icon_path=get_icon_path(__file__),
        description='Get TimeStamp',
    ) as mcxt:

        # ############################################ for app dependent options
        mcxt.add_argument('--use-utc',
                          display_name='Use UTC', action='store_true',
                          help='If set, get UTC timestamp instead local timezone.')
        # ######################################### for app dependent parameters
        mcxt.add_argument('--output-format', '-o',
                          display_name='DateTime Format', show_default=True,
                          default='YYYYMMDD-HHMMSS.mmm',
                          choices=list(OUTPUT_FORMATS.keys()),
                          help='Set the format of TimeStamp')

        # ##################################### for app dependent parameters
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
