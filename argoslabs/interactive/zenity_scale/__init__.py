#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.interactive.zenity_scale`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Zenity Scale Plugin
"""
# Authors
# ===========
#
# * Irene Cho
#
# --------
#
#  * [2021/03/09]
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
@func_log
def zenity_q(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if sys.platform != 'win32':
            raise SystemError('Only Windows OS is supported!')
        out_d = os.path.join(os.path.expanduser('~'), 'Documents', 'Winzenity')
        if not os.path.exists(out_d):
            os.makedirs(out_d)
        t = os.path.join(out_d, 'zenity.exe')
        if not os.path.exists(t):
            r = requests.get(
                'https://github.com/maravento/winzenity/raw/master/zenity.zip')
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(out_d)
        cmd = [t, '--scale']
        if argspec.text:
            cmd.append('--text=' + argspec.text)
        if argspec.value:
            cmd.append('--value=' + argspec.value)
        if argspec.min_v:
            cmd.append('--min-value=' + argspec.min_v)
        if argspec.max_v:
            cmd.append('--max-value=' + argspec.max_v)
        if argspec.step:
            cmd.append('--step=' + argspec.step)
        if argspec.print_partial:
            cmd.append('--print-partial ')
        if argspec.hide_value:
            cmd.append('--hide-value')
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
        po = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None)
        t= po.communicate()[0].decode("utf-8")
        print(t)
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
            display_name='Dialog Scale',
            icon_path=get_icon_path(__file__),
            description='Display scale dialog',
    ) as mcxt:
        # ##################################### for app dependent parameters
        # ##################################### for app optional parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('--value', display_name='Value',
                          help='Set initial value')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--min_v', display_name='Min Value',
                          help='Set minimum value')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--max_v', display_name='Max Value',
                          help='Set maximum value')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--step', display_name='Step',
                          help='SSet step size')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--print_partial', display_name='Print Partial',
                          default=False, type=bool, help='Print partial values')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--hide_value', display_name='Hide Value',
                          default=False, type=bool, help='Hide value')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--text', display_name='Text', show_default=True,
                          help='Set the dialog text')
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
        mcxt.add_argument('--cancel_label', display_name='Cancel Label', show_default=True,
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
