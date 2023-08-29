"""
====================================
 :mod:`argoslabs.filesystem.stat`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module stat file system
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/07]
#     - 그룹에 "6-Files and Folders" 넣음
#  * [2020/11/15]
#     - starting

################################################################################
import os
import sys
import csv
from datetime import datetime
import argparse
from alabs.common.util.vvargs import ModuleContext, func_log,  \
    ArgsError, ArgsExit, get_icon_path


################################################################################
# noinspection PyShadowingBuiltins
@func_log
def file_stat(mcxt, args):
    try:
        header = ('pathname', 'basename', 'size', 'access_ts', 'modify_ts', 'create_ts')
        mcxt.logger.info('>>>starting...')
        c = csv.writer(sys.stdout, lineterminator='\n')
        c.writerow(header)
        for f in args.files:
            if not os.path.exists(f):
                continue
            st = os.stat(f)
            row = [
                os.path.abspath(f),
                os.path.basename(f),
                st.st_size,
                datetime.fromtimestamp(st.st_atime).strftime(
                    '%Y-%m-%d %H:%M:%S'),
                datetime.fromtimestamp(st.st_mtime).strftime(
                    '%Y-%m-%d %H:%M:%S'),
                datetime.fromtimestamp(st.st_ctime).strftime(
                    '%Y-%m-%d %H:%M:%S'),
            ]
            c.writerow(row)
        return 0
    except Exception as e:
        msg = 'argoslabs.filesystem.monitor Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='6',  # Files and Folders
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='File Status',
        icon_path=get_icon_path(__file__),
        description='''Getting file status''',
        formatter_class=argparse.RawTextHelpFormatter
    ) as mcxt:
        # ######################################## for app dependent options
        # mcxt.add_argument('--filter', '-f', action='append',
        #                   display_name='Search for', show_default=True,
        #                   help='Set file matching filter like *.txt '
        #                        '(multiple setting is possible, default is *.txt)')

        # ##################################### for app dependent parameters
        mcxt.add_argument('files', nargs='+',
                          display_name='Files',
                          input_method='fileread',
                          help='Files to get status')
        argspec = mcxt.parse_args(args)
        return file_stat(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
