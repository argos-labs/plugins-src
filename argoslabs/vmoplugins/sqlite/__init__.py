#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.vmoplugins.sqlite`
====================================
.. moduleauthor:: Hiep Tran <Tranquanghiep2009@gmail.com>
.. note:: ARGOS-LABS License

Description
===========
SQLite Execution Plugin
"""
# Authors
# ===========
#
# * Hiep Tran
#
# Change Log
# --------

################################################################################
import os
import sys
import sqlite3
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
@func_log
def exec(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    with sqlite3.connect(argspec.db_file) as conn:
        try:
            c = conn.cursor()
            for command in argspec.statements:

                resp = c.execute(command)
                print("Result for command: " + command)
                print(resp.fetchall())
            conn.commit()
            return 0
        except Exception as err:
            conn.rollback()
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
        owner='HIEP-TRAN',
        group='demo',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Execute SQLite Statement',
        icon_path=get_icon_path(__file__),
        description='Execute SQLite Statement',
    ) as mcxt:
        try:
            mcxt.add_argument('db_file', display_name='Database file', input_method='fileread',
                              help='SQLite database file')
            mcxt.add_argument('--sql_file', display_name='Statements file', input_method='fileread',
                              help='sql statements file')
            mcxt.add_argument('--statements', nargs="+", display_name='SQLite statements',
                                  help='SQLite statements file')
            argspec = mcxt.parse_args(args)
            return exec(mcxt, argspec)
        except Exception as ex:
            print(ex)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
