#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.check.svcopen`
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
#  * [2021/03/27]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/05/14]
#     - starting

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from alabs.common.util.vvnet import is_svc_opeded


################################################################################
@func_log
def check_open(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        if not (argspec.alive_val and argspec.dead_val):
            raise RuntimeError('Invalid Alive or Dead value')
        is_opened = is_svc_opeded(argspec.host, argspec.port)
        rs = argspec.alive_val if is_opened else argspec.dead_val
        if argspec.csv_out:
            cwr = csv.writer(sys.stdout, lineterminator='\n')
            cwr.writerow(('host', 'port', 'status'))
            cwr.writerow((argspec.host, argspec.port, rs))
        else:
            print(rs, end='')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        sys.stdout.flush()
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
        display_name='Svc Check',
        icon_path=get_icon_path(__file__),
        description='Check if service is open or not',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('host',
                          display_name='Host',
                          help='Host name of IP address to check')
        mcxt.add_argument('port',
                          type=int,
                          display_name='Port',
                          help='Port number to check')
        # ######################################## for app dependent options
        mcxt.add_argument('--csv-out', action='store_true',
                          display_name='Return CSV',
                          help='If this flag is set, then return CSV format')
        mcxt.add_argument('--alive-val',
                          display_name='Alive', default='1',
                          help='Return value for alive service, default is [[1]]')
        mcxt.add_argument('--dead-val',
                          display_name='Dead', default='0',
                          help='Return value for dead service, default is [[0]]')
        argspec = mcxt.parse_args(args)
        return check_open(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
