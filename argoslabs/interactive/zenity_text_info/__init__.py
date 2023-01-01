#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.interactive.zenity_text_info`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Zenity Text Information Plugin
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
import _locale
import warnings
import subprocess
import locale
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
        cmd = [t, '--text-info']
        if argspec.filename:
            cmd.append('--filename=' + argspec.filename)
        if not argspec.neditable:
            cmd.append('--editable')
        if argspec.font:
            cmd.append('--font=' + argspec.font)
        if argspec.checkbox:
            cmd.append('--checkbox=' + argspec.checkbox)
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
        po = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        t = po.communicate()[0].decode(os_encoding).rstrip('\r\n')
        if po.returncode==0:
            print(t,end='')
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
            display_name='Dialog Text Info',
            icon_path=get_icon_path(__file__),
            description='Display text information dialog',
    ) as mcxt:
        # ##################################### for app dependent parameters
        # ##################################### for app optional parameters
        mcxt.add_argument('--filename', display_name='Filename', input_method='fileread',
                          help='Open text file. e.g. *.txt, *.csv, *.json, etc')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--neditable', display_name='Non Editable', default=False,
                          type=bool, help='Allow changes to text')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--font', display_name='Font', default='sans',
                          help='Set the text font. e.g. serif, monospace')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--checkbox', display_name='Checkbox',
                          help='Enable an I read and agree checkbox')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--width', display_name='Width', show_default=True,
                          help='Set the width')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--height', display_name='Height', show_default=True,
                          help='Set the height')
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
