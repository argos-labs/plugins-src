"""
====================================
 :mod:`argoslabs.filesystem.exists`
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
#  * [2021/03/31]
#     - 그룹에 "1002-Verifications" 넣음
#  * [2021/03/08]
#     - starting

################################################################################
import os
import sys
import argparse
from alabs.common.util.vvargs import ModuleContext, func_log,  \
    ArgsError, ArgsExit, get_icon_path


################################################################################
# noinspection PyShadowingBuiltins
@func_log
def file_stat(mcxt, args):
    try:
        mcxt.logger.info('>>>starting...')
        ff = None
        if args.file:
            ff = args.file
        if args.folder:
            ff = args.folder
        if os.path.exists(ff):
            print(os.path.abspath(ff), end='')
            if os.path.isdir(ff):
                if not os.listdir(ff):
                    return 1
            else:
                if os.path.getsize(ff) == 0:
                    return 1
        else:
            return 2
        return 0
    except Exception as e:
        msg = 'argoslabs.filesystem.monitor Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='1002',   # Verifications
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='File/Folder Exists',
        icon_path=get_icon_path(__file__),
        description='''Getting file/folder existence''',
        formatter_class=argparse.RawTextHelpFormatter
    ) as mcxt:
        # ######################################## for app dependent options
        # mcxt.add_argument('--filter', '-f', action='append',
        #                   display_name='Search for', show_default=True,
        #                   help='Set file matching filter like *.txt '
        #                        '(multiple setting is possible, default is *.txt)')

        # ##################################### for app dependent parameters
        mcxt.add_argument('file',
                          display_name='File to check',
                          input_method='fileread',
                          input_group='radio=file_or_folder;default',
                          help='File to check existence')
        mcxt.add_argument('folder',
                          display_name='Folder to check',
                          input_method='folderread',
                          input_group='radio=file_or_folder',
                          help='File to check existence')
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
