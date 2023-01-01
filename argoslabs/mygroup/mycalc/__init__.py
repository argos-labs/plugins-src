#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.mygroup.mycalc`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2020/06/01]
#     - starting

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from simpleeval import simple_eval


################################################################################
@func_log
def do_eval(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: 0 for success non-0 for failure
    """
    mcxt.logger.info('>>>starting...')
    try:
        if not argspec.expr:
            raise ValueError('Invalid Expression')
        if argspec.functions:
            fstr = '{' + ','.join(argspec.functions) + '}'
        else:
            fstr = '{}'
        r = simple_eval(argspec.expr, functions=eval(fstr))
        print(r, end='')
        mcxt.logger.info('>>>end...')
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
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS-DEMO',
        group='mygroup',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='My Calc',
        icon_path=get_icon_path(__file__),
        description='My Calculator',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('expr',
                          display_name='Expression',
                          help='Expression for calculation')
        # ######################################## for app dependent options
        mcxt.add_argument('--functions', action='append',
                          display_name='Function',
                          help='User defined function '
                               'like "\'square\': lambda x: x*x"')
        argspec = mcxt.parse_args(args)
        return do_eval(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
