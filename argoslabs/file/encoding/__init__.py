#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.file.encoding`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for converting encoding
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/08]
#     - ignore 옵션 요청 by ASJ
#  * [2021/04/06]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/03/25]
#     - starting

################################################################################
import os
import re
import sys
import csv
# import chardet
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from alabs.common.util.vvencoding import get_file_encoding


################################################################################
CSTABLE = None


################################################################################
@func_log
def encoding_convert(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        src_enc = argspec.src_enc.split(':')[0]
        if not src_enc:
            raise RuntimeError('Invalid Srouce CharSet')
        if not os.path.exists(argspec.src):
            raise IOError(f'Cannot find Source File "{argspec.src}"')
        target_enc = argspec.target_enc.split(':')[0]
        if not target_enc:
            raise RuntimeError('Invalid Target CharSet')

        errors = 'ignore' if argspec.ignore else None
        with open(argspec.src, encoding=src_enc, errors=errors) as ifp:
            rs = ifp.read()
            with open(argspec.target, 'w', encoding=target_enc, errors=errors) as ofp:
                ofp.write(rs)

        # c = csv.writer(sys.stdout, lineterminator='\n')
        # h = ('Src Charset', 'Source', 'Target Charset', 'Target')
        # c.writerow(h)
        # c.writerow((src_enc, argspec.src, target_enc, argspec.target))
        print(os.path.abspath(argspec.target), end='')

        return 0
    except Exception as e:
        msg = 'argoslabs.file.encoding Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 9
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def read_encoding_table():
    rr = list()
    et_file = os.path.join(os.path.dirname(__file__), 'Python Encoding Table.csv')
    with open(et_file, 'r', encoding='utf8') as ifp:
        cr = csv.reader(ifp)
        for i, row in enumerate(cr):
            if i < 1:
                continue
            rr.append(f'{row[0]}:{row[2]}')
    return rr


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    global CSTABLE
    CSTABLE = read_encoding_table()
    if not CSTABLE:
        raise RuntimeError(f'Cannot get Character Set table')
    with ModuleContext(
        owner='ARGOS-LABS',
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Convert CharSet',
        icon_path=get_icon_path(__file__),
        description='Convert File Character Set',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('src_enc',
                          display_name='Src Charset',
                          choices=CSTABLE,
                          default='utf_8',
                          help='Source file character set. default is [[utf_8]]')
        mcxt.add_argument('src',
                          display_name='Source File',
                          input_method='fileread',
                          help='Source file name')
        mcxt.add_argument('target_enc',
                          display_name='Target Charset',
                          choices=CSTABLE,
                          default='utf_8',
                          help='Source file character set. default is [[utf_8]]')
        mcxt.add_argument('target',
                          display_name='Target File',
                          input_method='filewrite',
                          help='Target file name to write')
        # ##################################### for app dependent options
        mcxt.add_argument('--ignore',
                          display_name='Ignore Err',
                          action='store_true',
                          help='If this flag is set ignore errors')
        argspec = mcxt.parse_args(args)
        return encoding_convert(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
