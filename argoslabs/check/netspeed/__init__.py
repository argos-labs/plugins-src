#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.check.netspeed`
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
#  * [2021/06/16]
#     - speedtest-cli>=2.1.3 이상 버전
#  * [2021/03/26]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/07/12]
#     - starting

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from speedtest import Speedtest


################################################################################
def get_hr_bytes(v):
    if v > 1024 * 1024 * 1024 * 1024:
        v /= 1024 * 1024 * 1024 * 1024
        return f'{round(v, 2)}T'
    if v > 1024 * 1024 * 1024:
        v /= 1024 * 1024 * 1024
        return f'{round(v, 2)}G'
    if v > 1024 * 1024:
        v /= 1024 * 1024
        return f'{round(v, 2)}M'
    if v > 1024:
        v /= 1024
        return f'{round(v, 2)}K'
    return f'{v}B'


################################################################################
@func_log
def get_netspeed(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        st = Speedtest()
        rd = {
            'download_speed': f'{get_hr_bytes(st.download())}Bit/s',
            'upload_speed': f'{get_hr_bytes(st.upload())}Bit/s',
        }
        header = ('download_speed', 'upload_speed')
        row = (rd['download_speed'], rd['upload_speed'])
        c = csv.writer(sys.stdout, lineterminator='\n')
        c.writerow(header)
        c.writerow(row)
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
        display_name='Speed Test',
        icon_path=get_icon_path(__file__),
        description='Test network download/upload speed',
    ) as mcxt:
        # ##################################### for app dependent parameters
        # mcxt.add_argument('host',
        #                   display_name='Host',
        #                   help='Host name of IP address to check')
        # ######################################## for app dependent options
        # mcxt.add_argument('--out-format', choices=EnvCheck.OUTPUT_FORMAT,
        #                   display_name='Output Format', default='csv',
        #                   show_default=True,
        #                   help='output format, one of "csv", "json" or "yaml"')
        argspec = mcxt.parse_args(args)
        return get_netspeed(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
