#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.interactive.zenity_color`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Zenity Color Plugin
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
#  * [2021/03/09]
#     - starting

################################################################################
import os
import sys
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
def zenity_q(mcxt, argspec):
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
        cmd = [t, '--color-selection']
        if argspec.color:
            cmd.append('--color=' + argspec.color)
        if argspec.palette:
            cmd.append('--show-palette')
        if argspec.timeout:
            cmd.append('--timeout=' + argspec.timeout)
        if argspec.ok_label:
            cmd.append('--ok-label=' + argspec.ok_label)
        if argspec.cancel_label:
            cmd.append('--cancel-label=' + argspec.cancel_label)
        t = os.system(' '.join(cmd))
        print(t, end='')
        # po = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None)
        # t = po.communicate()[0]
        # print(t.rstrip('\r\n'), end='')
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
    with ModuleContext(
            owner='ARGOS-LABS',
            group='system',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Dialog Color Selction',
            icon_path=get_icon_path(__file__),
            description='Display color selection dialog',
    ) as mcxt:
        # ##################################### for app dependent parameters
        # ##################################### for app optional parameters
        mcxt.add_argument('--color', display_name='Color',
                          help='Set the color')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--palette', display_name='Show Palette', default=False,
                          type=bool, help='Show the palette')
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
        return zenity_q(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
