#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.crypt.base64`
====================================
.. moduleauthor:: Venkatesh Vanjre <vvanjre@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Venkatesh Vanjre, Jerry Chae
#
# Change Log
# --------
#  [2022/8/17]
#   - Debugging sample_japanese.pdf
#  [2021/5/21]
#   - starting

################################################################################
import os
import sys
import base64
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
OP = ['Encode','Decode']


################################################################################
@func_log
def encodebase64(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        input_data = string_bytes = None
        if argspec.fileinput:
            if argspec.op == OP[0]:     # Encode
                with open(argspec.fileinput, 'rb') as ifp:
                    string_bytes = ifp.read()
            elif argspec.op == OP[1]:   # Decode
                with open(argspec.fileinput, encoding=argspec.encoding) as ifp:
                    input_data = ifp.read()
        elif argspec.stringinput:
            input_data = argspec.stringinput
            string_bytes = input_data.encode(argspec.encoding)
        if argspec.op == OP[0]:     # Encode
            if not string_bytes:
                raise ValueError('Invalid Input Value')
            base64_bytes = base64.b64encode(string_bytes)
            base64_string = base64_bytes.decode(argspec.encoding)
            # Jerry : Every printout needed no padding '\n' at the end
            print(base64_string, end='')
        elif argspec.op == OP[1]:   # Decode
            if not input_data:
                raise ValueError('Invalid Input Value')
            rb = base64.b64decode(input_data)
            # r = rb.decode(argspec.encoding)
            # print(r, end='')
            sys.stdout.buffer.write(rb)
        mcxt.logger.info('>>>end...')
        return 0
    except IOError as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    except ValueError as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 2
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        # Ususally unexpected exception return 9
        return 99
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
    try:
        with ModuleContext(
            owner='ARGOS-LABS',
            group='9',  # Utility Tools',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Base64',
            icon_path=get_icon_path(__file__),
            description='Base64 Encode/Decode',
        ) as mcxt:
            # ##################################### for app dependent parameters

            mcxt.add_argument('op',
                            choices=OP,
                            default='Encode',
                            display_name='Operation',
                            help='Operation for base64')
            mcxt.add_argument('--stringinput',
                            display_name='Input String',
                            input_group='radio=InputType;default',
                            show_default=True,
                            help='Input your string for crypto')
            mcxt.add_argument('--fileinput',
                            display_name='Input File',
                            input_group='radio=InputType',
                            input_method='fileread',
                            show_default=True,
                            help='select your file for crypto')
            # mcxt.add_argument('--encoding', display_name='Encoding',
            #                   default='utf-8',
            #                   help='Choose a proper encoding, default is "utf-8"')

            argspec = mcxt.parse_args(args)
            setattr(argspec, 'encoding', 'utf-8')
            return encodebase64(mcxt, argspec)
    except:
        return 98


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass