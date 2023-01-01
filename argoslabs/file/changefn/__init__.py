"""
====================================
 :mod:`argoslabs.file.changefn`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for changing filename
"""
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2021/04/28]
#    - build a plugin
#  * [2021/04/28]
#     - starting

################################################################################
import os
import sys
import shutil
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
@func_log
def do_screenshot(mcxt, argspec):
    try:
        if not os.path.exists(argspec.input):
            raise IOError(f'Cannot find the filename "{argspec.input}"')
        fn = os.path.join(os.path.dirname(argspec.input), argspec.output)
        if os.path.exists(fn):
            if argspec.choice == 'Return Failure':
                return 1
            elif argspec.choice == 'Add (n) at End':
                fn, ext = os.path.splitext(fn)
                for n in range(1, 1000000):
                    nfn = f'{fn} ({n})' + ext
                    if not os.path.exists(nfn):
                        shutil.copy(argspec.input, nfn)
                        break
                print(os.path.abspath(nfn), end='')
                return 0
        os.rename(argspec.input, fn)
        print(os.path.abspath(fn), end='')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS',
            group='6',
            version='1.0',
            platform=['windows'],  # , 'darwin', 'linux'],
            output_type='text',
            display_name='Rename File',
            icon_path=get_icon_path(__file__),
            description='Change a filename',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('input',
                          display_name='File',
                          input_method='fileread',
                          help='An absolute file path ')
        # ======================================================================
        mcxt.add_argument('output',
                          display_name='New Filename',
                          help='A new filename to update ')
        # ======================================================================
        mcxt.add_argument('--choice', choices=['Add (n) at End', 'Return Failure',
                                             'Overwrite'],
                          default='Add (n) at End',
                          show_default= True,
                          display_name='If File Exists',
                          help='Select the options if the file already exists')
        # ##################################### for app dependent parameters
        argspec = mcxt.parse_args(args)
        return do_screenshot(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
