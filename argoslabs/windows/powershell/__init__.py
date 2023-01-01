#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.windows.powershell`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for binary op
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/08/28]
#     - starting

################################################################################
import os
import sys
import subprocess
from tempfile import gettempdir
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
@func_log
def do_powershell(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    # pscript_f = None
    try:
        pscript = argspec.script
        if argspec.script_file:
            if not os.path.exists(argspec.script_file):
                raise IOError(f'Cannot find script "{argspec.script_file}"')
            # with open(argspec.script_file, encoding=argspec.encoding) as ifp:
            #     pscript = ifp.read()
            script_file = os.path.abspath(argspec.script_file)
            cmd = [
                'powershell.exe',
                '-ExecutionPolicy', 'Bypass',
                '-File', script_file,
            ]
            if argspec.script_params:
                cmd.extend(argspec.script_params)
            po = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  )
        else:
            if not pscript:
                raise ValueError(f'Invalid Script or Script file')
            cmd = [
                'powershell.exe',
                pscript,
            ]
            po = subprocess.Popen(cmd, shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  )
        try:
            out, err = po.communicate(timeout=int(argspec.timeout))
        except subprocess.TimeoutExpired:
            po.kill()
            out, err = po.communicate(timeout=int(argspec.timeout))
        outs = out.decode(encoding=argspec.encoding)
        errs = err.decode(encoding=argspec.encoding)
        sys.stdout.write(outs.strip())
        sys.stderr.write(errs.strip())
        return 0
    except Exception as e:
        msg = 'argoslabs.windows.powershell Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s' % (msg, ))
        return 1
    finally:
        # if pscript_f and os.path.exists(pscript_f):
        #     os.remove(pscript_f)
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows'],
        output_type='text',
        display_name='PowerShell',
        icon_path=get_icon_path(__file__),
        description='Execute PowerShell script',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--script', '-s',
                          display_name='Script', show_default=True,
                          help='PowerShell Script to execute')
        mcxt.add_argument('--script-file', '-f',
                          display_name='Script File', show_default=True,
                          input_method='fileread',
                          help='PowerShell Script file to execute')
        mcxt.add_argument('--script-params',
                          display_name='Script Params', action='append',
                          help='Parameters for PowerShell Script file')
        mcxt.add_argument('--encoding',
                          display_name='Encoding', default='utf-8',
                          help='Encoding for the script file, default is "utf-8"')
        mcxt.add_argument('--timeout',
                          display_name='Timeout', default=60, type=int,
                          help='Timeout for executing powershell script, default is 60 sec')

        # ##################################### for app dependent parameters
        # mcxt.add_argument('left',
        #                   display_name='Left Val',
        #                   help='Left operand for binary operation')
        argspec = mcxt.parse_args(args)
        return do_powershell(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
