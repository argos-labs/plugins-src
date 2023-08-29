"""
====================================
 :mod:`argoslabs.filesystem.fo_stat`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module stat folder system
"""
# Authors
# ===========
#
# * Arun Kumar
#
# Change Log
# --------
#
#  * [2023/06/22]
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
def st_size(f):
    size = 0
    for path, dirs, files in os.walk(f):
        for fi in files:
            fp = os.path.join(path, fi)
            size += os.stat(fp).st_size
    return size

@func_log
def file_stat(mcxt, args):
    try:
        header = ('pathname', 'basename', 'size', 'access_ts', 'modify_ts', 'create_ts')
        mcxt.logger.info('>>>starting...')
        c = csv.writer(sys.stdout, lineterminator='\n')
        c.writerow(header)
        for f in args.folder:
            if not os.path.exists(f):
                continue
            st = os.stat(f)
            row = [
                os.path.abspath(f),
                os.path.basename(f),
                st_size(f),
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
        msg = 'argoslabs.filesystem.fo_stat Error: %s' % str(e)
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
        display_name='Folder Status',
        icon_path=get_icon_path(__file__),
        description='''Getting folder status''',
        formatter_class=argparse.RawTextHelpFormatter
    ) as mcxt:
        # ######################################## for app dependent options
        # ##################################### for app dependent parameters
        mcxt.add_argument('folder', nargs='+',
                          display_name='Folder Path',
                          input_method='folderread',
                          help='Folder to get status')
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
