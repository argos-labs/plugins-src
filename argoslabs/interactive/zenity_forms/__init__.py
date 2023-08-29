#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.interactive.zenity_forms`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Zenity Forms Plugin
"""
# Authors
# ===========
#
# * Irene Cho, Jerry Chae
#
# --------
#
# [2022/09/20]
#  - add req_gw_get()
#  * [2021/03/01]
#     - starting

################################################################################
import os
import re
import sys
import locale
import warnings
import subprocess

import io
import requests
import zipfile
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path

warnings.simplefilter("ignore", ResourceWarning)


################################################################################
class datefunc(object):
    OP_TYPE = ['YYYYMMDD', 'YYYY-MM-DD', 'YYYY/MM/DD', 'MMDDYYYY', 'MM-DD-YYYY',
               'MM/DD/YYYY' ]
               # 'M/D/YYYY', 'B D YYYY', 'B D, YYYY', 'D B YYYY',
               # 'D B YY', 'DBYY']

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.dformat = argspec.dformat

    # ==========================================================================
    def get_format(self):
        DATE_FORMAT = {
            'YYYYMMDD': "%Y%m%d",
            'YYYY-MM-DD': "%Y-%m-%d",
            'YYYY/MM/DD': "%Y/%m/%d",
            'MMDDYYYY': "%m%d%Y",
            'MM-DD-YYYY': "%m-%d-%Y",
            'MM/DD/YYYY': "%m/%d/%Y",
            #'M/D/YYYY': "%-m/%-d/%Y" if sys.platform != 'win32' else "%#m/%#d/%Y",
            # 'B D YYYY': "%b %-d %Y" if sys.platform != 'win32' else "%b %#d %Y",
            # 'B D, YYYY': "%b %-d, %Y" if sys.platform != 'win32' else "%b %#d, %Y",
            # 'D B YYYY': "%-d %b %Y" if sys.platform != 'win32' else "%#d %b %Y",
            # 'D B YY': "%-d %b %Y" if sys.platform != 'win32' else "%#d %b %Y",
            # 'DBYY': "%-d%b%Y" if sys.platform != 'win32' else "%#d%b%Y",
        }
        return DATE_FORMAT[self.dformat]


################################################################################
def req_gw_get():
    urls = [
        'https://pypi-official.argos-labs.com/gw-files/zenity.zip',
        'https://github.com/maravento/winzenity/raw/master/zenity.zip',
    ]
    for url in urls:
        try:
            r = requests.get(url)
            if r.status_code // 10 != 20:
                continue
            return r
        except:
            continue
    raise ReferenceError(f'Cannot download "zenity.zip" from urls={urls}')


################################################################################
@func_log
def zenity_f(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if sys.platform != 'win32':
            raise SystemError('Only Windows OS is supported!')
        out_d = os.path.join(os.path.expanduser('~'), '.argos-rpa.cache', 'Winzenity')
        if not os.path.exists(out_d):
            os.makedirs(out_d)
        t = os.path.join(out_d, 'zenity.exe')
        if not os.path.exists(t):
            # r = requests.get('https://github.com/maravento/winzenity/raw/master/zenity.zip')
            r = req_gw_get()
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(out_d)
        cmd = [t, '--forms']
        if argspec.title:
            cmd.append('--title=' + argspec.title)
        if argspec.add_entry:
            for ent in argspec.add_entry:
                cmd.append('--add-entry=' + ent)
        if argspec.add_password:
            for ent in argspec.add_password:
                cmd.append('--add-password=' + ent)
        if argspec.add_calendar:
            cmd.append('--add-calendar=' + argspec.add_calendar)
        if argspec.add_list:
            cmd.append('--add-list=' + argspec.add_list)
        if argspec.list_values:
            lst = '|'.join(ent for ent in argspec.list_values)
            cmd.append('--list-values=' + lst)
        if argspec.column_values:
            lst = '|'.join(ent for ent in argspec.column_values)
            cmd.append('--column-values=' + lst)
        if argspec.show_header:
            cmd.append('--show-header')
        if argspec.text:
            t = re.sub('&', ' ', argspec.text)
            cmd.append('--text=' + t)
        if argspec.separator:
            cmd.append('--separator=' + argspec.separator)
        if argspec.dformat:
            func = datefunc(argspec)
            cmd.append('--forms-date-format=' + func.get_format())
        if argspec.timeout:
            cmd.append('--timeout=' + argspec.timeout)
        if argspec.ok_label:
            cmd.append('--ok-label=' + argspec.ok_label)
        if argspec.cancel_label:
            cmd.append('--cancel-label=' + argspec.cancel_label)
        os_encoding = locale.getpreferredencoding()
        po = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None)
        t = po.communicate()[0].decode(os_encoding).rstrip('\r\n')
        if po.returncode==0:
            print(t, end='')
        return po.returncode
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 2
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS',
            group='7',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Dialog Forms',
            icon_path=get_icon_path(__file__),
            description='Create a dialog form',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('text', display_name='Text',
                          help='Set the dialog text')
        # ##################################### for app optional parameters
        mcxt.add_argument('--title', display_name='Title',
                          help='Set the dialog title')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--add_entry', display_name='Plain Text Field',
                          action='append',
                          help='Field name. Add a new Entry in forms dialog')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--add_password', display_name='Password Field',
                          action='append',
                          help='Field name. Add a new Password Entry in forms dialog')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--add_calendar', display_name='Add Calendar',
                          help='Calendar field name. Add a new Calendar in forms dialog')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--add_list', display_name='Add List',
                          help='List field and header name. Add a new List in forms dialog')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--list_values', display_name='List Values',
                          action='append',
                          help='List of values for List')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--column_values', display_name='Column Values',
                          action='append',
                          help='List of values for columns')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--show_header', display_name='Show Header',
                          default=False,
                          type=bool, help='Show the columns header')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--dformat', display_name='Date Format', choices=datefunc.OP_TYPE,
                          help='Set the format for the returned date')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--separator', display_name='Separator', default=',',
                          help='Set output separator character')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--timeout', display_name='Timeout',
                          show_default=True,
                          help='Set dialog timeout in seconds')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--ok_label', display_name='OK Label',
                          show_default=True,
                          help='Sets the label of the Ok button')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--cancel_label', display_name='Cancel Label',
                          show_default=True,
                          help='Sets the label of the Cancel button')
        argspec = mcxt.parse_args(args)
        return zenity_f(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
