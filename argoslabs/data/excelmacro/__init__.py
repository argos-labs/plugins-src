#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.excelmacro`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Excel Macro
"""
#
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/13]
#     - 그룹에 "2-Business Apps" 넣음
#  * [2020/04/28]
#     - only accept '.xlsm', 'xls'
#     - return abspath for filename
#  * [2019/07/17]
#     - starting
#

################################################################################
import os
import sys
import win32com.client as win32
# noinspection PyUnresolvedReferences
import pywintypes
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
def run_macro(filename, func, *args):
    if not os.path.exists(filename):
        raise IOError('Cannot read file "%s"' % filename)

    excel_macro = None
    # noinspection PyUnresolvedReferences
    try:
        excel_macro = win32.DispatchEx("Excel.Application")
        excel_path = os.path.abspath(filename)
        workbook = excel_macro.Workbooks.Open(Filename=excel_path)  # , ReadOnly=1)
        excel_macro.Application.Run(func, *args)
        workbook.Save()
        return 0
    except pywintypes.com_error as err:
        sys.stderr.write('Please make sure Excel Installed:%s\n' % (str(err)))
        return 1
    except Exception as err:
        sys.stderr.write('%s\n' % str(err))
        return 1
    finally:
        if excel_macro is not None:
            excel_macro.Application.Quit()
            del excel_macro


################################################################################
@func_log
def do_excel_macro(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: 0
    """
    mcxt.logger.info('>>>starting...')
    exl = None
    try:
        if argspec.params is None:
            argspec.params = []
        filename = argspec.filename
        _, ext = os.path.splitext(filename)
        if ext.lower() not in ('.xlsm', 'xls'):
            raise IOError(f'Cannot run macro for the extension {ext}')
        funcname = argspec.funcname
        params = argspec.params
        r = run_macro(filename, funcname, *params)
        if r == 0:
            mcxt.logger.info("Execute %s!%s(%s) OK!" %
                             (filename, funcname, ','.join(params)))
        else:
            mcxt.logger.info("Execute %s!%s(%s) Not OK!"
                             % (filename, funcname, ','.join(params)))
        sys.stdout.write('%s' % os.path.abspath(filename))
        sys.stdout.flush()
        return r
    except Exception as e:
        sys.stderr.write('%s%s' % (str(e), os.linesep))
        return 1
    finally:
        if exl is not None:
            exl.close()
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
        group='2',  # Business Apps
        version='1.0',
        platform=['windows'],  # , 'darwin', 'linux'],
        output_type='csv',
        display_name='Excel Macro',
        icon_path=get_icon_path(__file__),
        description='Execute Excel Macro function',
    ) as mcxt:
        # ##################################### for app dependent options
        # ----------------------------------------------------------------------
        mcxt.add_argument('--params', action='append',
                          display_name='Params', show_default=True,
                          help='Parameters for macro function')
        # ##################################### for app dependent parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('filename',
                          display_name='Excel File',
                          input_method='fileread',
                          help='Excel filename to execute macro. Supported extension is "*.xls" or "*.xlsm".')
        mcxt.add_argument('funcname',
                          display_name='Macro Name',
                          help='Macro function name to call.')
        argspec = mcxt.parse_args(args)
        return do_excel_macro(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
