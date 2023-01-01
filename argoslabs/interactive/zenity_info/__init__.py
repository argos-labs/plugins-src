#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.interactive.zenity_info`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Zenity Info Plugin
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
#  * [2021/03/08]
#     - starting

################################################################################
import os
import locale
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
        ok_value = 'OK'
        cmd = [t, '--info', '--text=' + argspec.text]
        if argspec.icon:
            cmd.append('--icon-name=' + argspec.icon)
        if argspec.no_wrap:
            cmd.append('--no-wrap')
        if argspec.no_markup:
            cmd.append('--no-markup')
        if argspec.width:
            cmd.append('--width=' + argspec.width)
        if argspec.height:
            cmd.append('--height=' + argspec.height)
        if argspec.timeout:
            cmd.append('--timeout=' + argspec.timeout)
        if argspec.ok_label:
            cmd.append('--ok-label=' + argspec.ok_label)
            ok_value = argspec.ok_label
        os_encoding = locale.getpreferredencoding()
        po = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None)
        _ = po.communicate()[0].decode(os_encoding).rstrip('\r\n')
        if po.returncode == 0:
            print(ok_value, end='')
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
            display_name='Dialog Info',
            icon_path=get_icon_path(__file__),
            description='Pop up an information using zenity',
    ) as mcxt:
        # ##################################### for app dependent parameters
        # ##################################### for app optional parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('--no_wrap', display_name='No Wrap', default=False,
                          type=bool, help='Do not enable text wrapping')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--no_markup', display_name='No Markup',
                          default=False,
                          type=bool, help='Do not enable pango markup')
        # ----------------------------------------------------------------------
        mcxt.add_argument('text', display_name='Text', show_default=True,
                          help='Set the dialog text')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--icon', display_name='Dialog Icon',
                          default='dialog-information',
                          help='Set the dialog icon. Refer https://developer.gnome.org/icon-naming-spec/#names'
                               ' for some defaults ')
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
