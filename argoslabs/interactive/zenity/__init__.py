#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.interactive.zenity`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Zenity Plugin
"""
# Authors
# ===========
#
# * Irene Cho, Jerry Chae
#
# --------
# [2024/04/01]
#  taehoon ahn
# - all advanced Date format option fix
#
# [2024/03/21]
#  taehoon ahn
#  - advanced Date format option fix
#
# [2022/09/20]
#  - add req_gw_get()
# [2021/02/25]
#  - starting


################################################################################
import os
import re
import sys
import locale
import datetime
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
               'MM/DD/YYYY',
               'M/D/YYYY', 'B D YYYY', 'B D, YYYY', 'D B YYYY',
               'D B YY', 'DBYY']

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.dformat = argspec.date_format

    # ==========================================================================
    def get_format(self, rv):
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
            'D B YY': "%-d %b %Y" if sys.platform != 'win32' else "%#d %b %Y",
            'DBYY': "%-d%b%Y" if sys.platform != 'win32' else "%#d%b%Y",
        }
        r = self.dformat
        # rv = datetime.datetime.strptime(rv, '%m/%d/%Y')
        # print(rv.strftime(DATE_FORMAT[r]), end='')
        rv = datetime.datetime.strptime(rv, DATE_FORMAT['YYYY-MM-DD']).strftime(DATE_FORMAT[r])
        # if r == 'D B YYYY' or '' or '' or '' or '':
        #     pass
        # else:
        #     pass
        #
        # rv = datetime.datetime.strptime(rv, DATE_FORMAT[r])
        # print(rv.strftime(DATE_FORMAT[r]), end='')
        print(rv)
        return 0


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
def zenity_cal(mcxt, argspec):
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
        cmd = [t, '--calendar']

        if argspec.day:
            cmd.append('--day=' + argspec.day)
        if argspec.month:
            cmd.append('--month=' + argspec.month)
        if argspec.year:
            cmd.append('--year=' + argspec.year)
        if argspec.text:
            t = re.sub('&', ' ', argspec.text)
            cmd.append('--text=' + t)
        if argspec.icon:
            cmd.append(' --window-icon=' + argspec.icon)
        if argspec.width:
            cmd.append('--width=' + argspec.width)
        if argspec.height:
            cmd.append('--height=' + argspec.height)
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
            if argspec.date_format:
                func = datefunc(argspec)
                return func.get_format(t)
            else:
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
            platform=['windows'],  # , 'darwin', 'linux'],
            output_type='csv',
            display_name='Dialog Calendar',
            icon_path=get_icon_path(__file__),
            description='Create a zenity calendar',
    ) as mcxt:
        # ##################################### for app dependent parameters
        # ##################################### for app optional parameters
        mcxt.add_argument('--date_format', display_name='Date Format',
                          choices=datefunc.OP_TYPE,
                          help='Set the format for the returned date')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--day', display_name='Day',
                          help='Set the calendar day')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--month', display_name='Month',
                          help='Set the calendar month')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--year', display_name='Year',
                          help='Set the calendar year')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--text', display_name='Text',
                          help='Set the dialog text', show_default=True)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--icon', display_name='Icon Path', show_default=True,
                          help='Set the window icon', input_method='fileread')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--width', display_name='Width', show_default=True,
                          help='Set the width')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--height', display_name='Height', show_default=True,
                          help='Set the height')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--timeout', display_name='Timeout', show_default=True,
                          help='Set dialog timeout in seconds')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--ok_label', display_name='OK Label', show_default=True,
                          help='Sets the label of the Ok button')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--cancel_label', display_name='Cancel Label', show_default=True,
                          help='Sets the label of the Cancel button')
        argspec = mcxt.parse_args(args)
        return zenity_cal(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
