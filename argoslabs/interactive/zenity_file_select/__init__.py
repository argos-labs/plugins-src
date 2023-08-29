#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.interactive.zenity_file_selection`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Zenity File Selction Plugin
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
#  * [2021/03/04]
#     - starting

################################################################################
import os
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
        cmd = [t, '--file-selection']
        if argspec.filename:
            cmd.append('--filename=' + argspec.filename)
        if argspec.multiple:
            cmd.append('--multiple')
        if argspec.directory:
            cmd.append('--directory')
        if argspec.save:
            cmd.append('--save')
        if argspec.confirm_overwrite:
            cmd.append('--confirm-overwrite')
        if argspec.file_filter:
            cmd.append('--file-filter=' + argspec.file_filter)
        if argspec.separator:
            cmd.append('--separator=' + argspec.separator)
        if argspec.timeout:
            cmd.append('--timeout=' + argspec.timeout)
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
            display_name='Dialog File Selection',
            icon_path=get_icon_path(__file__),
            description='Display file selection',
    ) as mcxt:
        # ##################################### for app dependent parameters
        # ##################################### for app optional parameters
        mcxt.add_argument('--filename', display_name='Filename',
                          help='Set the filename')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--multiple', display_name='Multiple', default=False,
                          type=bool,
                          help='Allow multiple files to be selected')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--directory', display_name='Folder', default=False, type=bool,
                          help='Activate directory-only selection')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--save', display_name='Save', default=False, type=bool,
                          help='Activate save mode')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--separator', display_name='Separator', default=',',
                          help='Set output separator character')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--confirm_overwrite', display_name='Confirm Overwrite',
                          default=False, type=bool,
                          help='Confirm file selection if filename already exists')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--file_filter', display_name='File Filter',
                          help='Sets a filename filter')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--timeout', display_name='Timeout', show_default=True,
                          help='Set dialog timeout in seconds')
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
