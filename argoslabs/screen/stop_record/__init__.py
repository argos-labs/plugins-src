"""
====================================
 :mod:`argoslabs.screen.stop_record`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for running python script with requirements.txt
"""
#
# Authors
# ===========
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/05/16]
#     - starting

################################################################################
import os
import sys
import time
import datetime
import traceback
from tempfile import gettempdir
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from pathlib import Path


################################################################################
BREAK_FILE = os.path.join(gettempdir(), 'ARGOS_SCREEN_RECORDING.brk')


################################################################################
@func_log
def stop_recording(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        is_timeout = False
        Path(BREAK_FILE).touch()
        s_ts = datetime.datetime.now()
        while os.path.exists(BREAK_FILE):
            time.sleep(1)
            c_ts = datetime.datetime.now()
            if (c_ts - s_ts).total_seconds() >= argspec.timeout:
                is_timeout = True
                break
        if is_timeout:
            os.remove(BREAK_FILE)
            print('Not starting or not stopped', end='')
        else:
            print('Stopped', end='')
        return 0
    except Exception as e:
        _exc_info = sys.exc_info()
        _out = traceback.format_exception(*_exc_info)
        del _exc_info
        msg = '%s\n' % ''.join(_out)
        mcxt.logger.error(msg)
        msg = 'Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write(msg)
        return 9
    finally:
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
        display_name='Stop Screen Recording',
        icon_path=get_icon_path(__file__),
        description='Stop ARGOS LABS Screen Recording',
    ) as mcxt:
        # ##################################### for app dependent parameters
        # ##################################### for app dependent options
        mcxt.add_argument('--timeout', type=int,
                          display_name='Timeout',
                          default=3,
                          help='If this timeout seconds elapsed then stop the stopping, '
                               'default is 3 seconds')
        argspec = mcxt.parse_args(args)
        return stop_recording(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
