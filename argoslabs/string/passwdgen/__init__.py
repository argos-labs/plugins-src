#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.string.passwdgen`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for string regular-expression operation
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/09]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/05/30]
#     - starting

################################################################################
import os
import sys
import random
import string
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
@func_log
def do_passwdgen(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: 0 for success
    """
    try:
        mcxt.logger.info('>>>starting...')
        # Min # of any password element cannot exceed half of the total length of the password
        is_exceed = False
        length = argspec.length
        halflen = length//2
        if not (0 <= argspec.minsp <= halflen):
            is_exceed = True
        if not (0 <= argspec.minlower <= halflen):
            is_exceed = True
        if not (0 <= argspec.minupper <= halflen):
            is_exceed = True
        if not (0 <= argspec.mindigit <= halflen):
            is_exceed = True
        if is_exceed:
            raise ValueError(f'Min # of any password element cannot exceed half of the total length of the password, {halflen}')
        if argspec.minsp + argspec.minlower + argspec.minupper + argspec.mindigit > length:
            raise ValueError(f'Sum of all minimum number of characters cannot be exceed the password length')
        random.seed = (os.urandom(1024))
        while True:
            chars = string.ascii_letters + string.digits + argspec.spchars
            pg = ''.join(random.choice(chars) for _ in range(length))
            num_sp = num_up = num_lo = num_di = 0
            for ch in pg:
                if ch in argspec.spchars:
                    num_sp += 1
                if ch.isupper():
                    num_up += 1
                elif ch.islower():
                    num_lo += 1
                elif ch.isdigit():
                    num_di += 1
            if argspec.minsp > num_sp:
                continue
            if argspec.minlower > num_lo:
                continue
            if argspec.minupper > num_up:
                continue
            if argspec.mindigit > num_di:
                continue
            break
        print(pg, end='')
        return 0
    except Exception as e:
        msg = str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Password Generator',
        icon_path=get_icon_path(__file__),
        description='This plugin is for password generation',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('length',
                          display_name='Length',
                          default=13, type=int,
                          help='Length of password. Default is [[13]]')
        # ##################################### for app dependent options
        mcxt.add_argument('--spchars',
                          display_name='Special Chs', show_default=True,
                          default='!@#$%^&*()',
                          help='Special Characters except alphabet and digits. Default is [[!@#$%^&*()]]')
        mcxt.add_argument('--minsp',
                          default=1, type=int, min_value=0,
                          display_name='Min Special Chs',
                          help='The password must has minimum number of lower case. Default is [[1]]')
        mcxt.add_argument('--minlower',
                          default=1, type=int, min_value=0,
                          display_name='Min Lower case',
                          help='The password must has minimum number of lower case. Default is [[1]]')
        mcxt.add_argument('--minupper',
                          default=1, type=int, min_value=0,
                          display_name='Min Upper case',
                          help='The password must has minimum number of upper case. Default is [[1]]')
        mcxt.add_argument('--mindigit',
                          default=1, type=int, min_value=0,
                          display_name='Min Digits',
                          help='The password must has minimum number of digits. Default is [[1]]')
        argspec = mcxt.parse_args(args)
        return do_passwdgen(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
