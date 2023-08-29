#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.pathname_manip`
======0==============================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for path
"""
#
# Authors
# ===========
#
# * Kyobong An
#
# Change Log
# --------
#  * [2021/06/17]
#   날짜출력  yyyy-mm-dd -> mm-dd-yyyy로 형식 변경
#  * [2021/06/15]
#   플러그인 이름 변경 "Pathname_manip" -> "Path Manipulation
#  * [2021/06/11]
#   잘못추가한 부분변경
#  * [2021/06/10]
#   getatime, getctime, getctime 시간출력되는 부분 수정
#  * [2021/06/09]
#   start


################################################################################
import os
import sys
from time import mktime, gmtime, localtime
from datetime import datetime
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class OpenError(Exception):
    pass


################################################################################
class Path(object):
    # ==========================================================================
    def __init__(self, argspec):
        if os.path.abspath(argspec.pathname):
            self.pathname = argspec.pathname
        else:
            raise OpenError(
                f'"{argspec.pathname}" not find'
            )
        self.path_m = argspec.path_method
        self.outpath = None

    # ==========================================================================
    def find_path(self):
        if self.path_m == 'abspath':
            self.outpath = os.path.abspath(self.pathname)
        elif self.path_m == 'basename':
            self.outpath = os.path.basename(self.pathname)
        elif self.path_m == 'dirname':
            self.outpath = os.path.dirname(self.pathname)
        elif self.path_m == 'exists':
            self.outpath = os.path.exists(self.pathname)
        elif self.path_m == 'expandvars':
            self.outpath = os.path.expandvars(self.pathname)
        elif self.path_m == 'getatime':
            t = localtime(os.path.getatime(self.pathname))
            self.outpath = datetime.fromtimestamp(mktime(t)).strftime("%m-%d-%Y %H:%M:%S")
        elif self.path_m == 'getmtime':
            t = localtime(os.path.getmtime(self.pathname))
            self.outpath = datetime.fromtimestamp(mktime(t)).strftime("%m-%d-%Y %H:%M:%S")
        elif self.path_m == 'getctime':
            t = localtime(os.path.getctime(self.pathname))
            self.outpath = datetime.fromtimestamp(mktime(t)).strftime("%m-%d-%Y %H:%M:%S")
        elif self.path_m == 'getsize':
            self.outpath = os.path.getsize(self.pathname)
        if self.outpath is None:
            raise OpenError
        return print(self.outpath, end='')


################################################################################
@func_log
def do_path(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        op = Path(argspec)
        op.find_path()
        sys.stdout.flush()
        return 0
    except OpenError as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 9
    finally:
        mcxt.logger.info('>>>end...')


######################
# ##########################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS',
            group='6',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Path Manipulation',
            icon_path=get_icon_path(__file__),
            description='path name',
    ) as mcxt:
        # ##################################### for app dependent options
        # ----------------------------------------------------------------------
        mcxt.add_argument('--path-method', default='abspath',
                          display_name='Path type',
                          show_default=True,
                          choices=['abspath', 'basename', 'dirname', 'exists', 'expandvars',
                                   'getatime', 'getmtime', 'getctime', 'getsize'],
                          help='choose method')
        # ##################################### for app dependent parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('pathname', nargs='?', default=None,
                          display_name='Path',
                          input_method='fileread',
                          help='pathname')
        argspec = mcxt.parse_args(args)
        return do_path(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
