#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.interactive.zenity_list`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Zenity List Plugin
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
import subprocess
import sys
import warnings

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
        cmd = [t, '--list']
        if argspec.text:
            cmd.append('--text=' + argspec.text)
        if argspec.column:
            cmd.append('--column=' + argspec.column)
        if argspec.checklist:
            cmd.append('--checklist')
        if argspec.radiolist:
            cmd.append('--radiolist')
        if argspec.imagelist:
            cmd.append('--imagelist')
        if argspec.separator:
            cmd.append('--separator=' + argspec.separator)
        if argspec.multiple:
            cmd.append('--multiple')
        if argspec.editable:
            cmd.append('--editable')
        if argspec.print_column:
            cmd.append('--print-column=' + argspec.print_column)
        if argspec.hide_column:
            cmd.append('--hide-column=' + argspec.hide_column)
        if argspec.hide_header:
            cmd.append('--hide-header')
        if argspec.ok_label:
            cmd.append('--ok-label=' + argspec.ok_label)
        if argspec.cancel_label:
            cmd.append('--cancel-label=' + argspec.cancel_label)
        os.system(' '.join(cmd))
        # po = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None)
        # t = po.communicate()[0].decode("utf-8")
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
            display_name='Dialog List',
            icon_path=get_icon_path(__file__),
            description='Create zenity list',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('column', display_name='Column',
                          help='Use check boxes for first column')
        # ##################################### for app optional parameters
        mcxt.add_argument('--text', display_name='Text',
                          help='Set the dialog title')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--checklist', display_name='Checklist', default= False,
                          type=bool,
                          help='Field name. Add a new Password Entry in forms dialog')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--radiolist', display_name='Radiolist', default= False,
                          type=bool,
                          help='Use radio buttons for first column')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--imagelist', display_name='Imagelist',
                          help='Use an image for first column')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--separator', display_name='Separator',
                          help='Set output separator character')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--multiple', display_name='Multiple', default= False,
                          type=bool,
                          help='Allow multiple rows to be selected')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--editable', display_name='Editable', default= False,
                          type=bool,
                          help='Allow changes to text')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--print-column', display_name='Show Header',
                          default=False, type=bool,
                           help='Print a specific column (Default is 1. ALL can be used to print all columns)')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--hide-column', display_name='Hide Column',
                          default=False, type=bool,
                          help='Hide a specific column')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--hide-header', display_name='Hide Header',
                          default=False, type=bool,
                          help='Hides the column headers')
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
        return zenity_f(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
