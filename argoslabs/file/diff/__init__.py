"""
====================================
 :mod:`argoslabs.file.diff`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for converting encoding
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/03/17]
#     - starting

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
@func_log
def do_diff(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        if not os.path.exists(argspec.file):
            raise IOError(f'Cannot find file "{argspec.file}"')
        return 0
    except Exception as e:
        msg = 'argoslabs.data.chardet Error: %s' % str(e)
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
        group='file',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='File/Folder Diff',
        icon_path=get_icon_path(__file__),
        description='Check File or Folder diff',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('file',
                          display_name='File',
                          input_method='fileread',
                          help='File name to detect file characterset')
        argspec = mcxt.parse_args(args)
        return do_diff(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
