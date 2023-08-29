"""
====================================
 :mod:`argoslabs.screen.start_record`
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
#  * [2021/05/20]
#     - change python.exe => pythonw.exe
#  * [2021/05/18]
#     - icon-my.png must included at the module
#     - PAM waiting problem
#  * [2021/05/15]
#     - starting

################################################################################
import os
import sys
import time
import datetime
import warnings
import traceback
import subprocess
from tempfile import gettempdir
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from argoslabs.screen.start_record.argos_screen_record import ArgosScreenCapture
from pathlib import Path


################################################################################
warnings.filterwarnings('ignore', category=RuntimeWarning, module='runpy')
BREAK_FILE = os.path.join(gettempdir(), 'ARGOS_SCREEN_RECORDING.brk')
#STD_FILE = os.path.join(gettempdir(), 'ARGOS_SCREEN_RECORDING.std')
DETACHED_PROCESS = 0x00000008


################################################################################
def stop_recording(mcxt, timeout=1):
    if os.path.exists(BREAK_FILE):
        os.remove(BREAK_FILE)
    Path(BREAK_FILE).touch()
    time.sleep(timeout)
    if os.path.exists(BREAK_FILE):
        os.remove(BREAK_FILE)


################################################################################
@func_log
def start_recording(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        # 혹시 이전에 안 끝난 레코딩이 있었다면 종료시킴
        stop_recording(mcxt)
        _, ext = os.path.splitext(argspec.filename)
        if ext.lower() not in ArgosScreenCapture.SUPPORTED_CODECS:
            raise ValueError(f'File extension must be one of {ArgosScreenCapture.SUPPORTED_CODECS} but "{ext}"')

        if sys.platform == 'win32':
            import pathlib
            executable = str(pathlib.PureWindowsPath(sys.executable))
            # change python.exe => pythonw.exe
            executable = os.path.join(os.path.dirname(executable), 'pythonw.exe')
        else:
            executable = sys.executable
        cmd = [
            executable,
            '-m',
            'argoslabs.screen.start_record.argos_screen_record',
            argspec.filename,
            BREAK_FILE,
            '--size-percent', str(argspec.size_percent),
            '--fps', str(argspec.fps),
            '--timeout', str(argspec.timeout),
        ]
        # with open(STD_FILE, 'w') as stdf:
        #     _ = subprocess.Popen(cmd, stdout=stdf, stderr=stdf)
        #     # po.communicate()
        # Only for Windows?
        if sys.platform == 'win32':
            _ = subprocess.Popen(cmd, creationflags=DETACHED_PROCESS)
        else:
            _ = subprocess.Popen(cmd, stdout='/dev/null', stderr='/dev/null')

        print(os.path.abspath(argspec.filename), end='')
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
        display_name='Start Screen Recording',
        icon_path=get_icon_path(__file__),
        description='Start ARGOS LABS Screen Recording',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('filename',
                          input_method='filewrite',
                          help='Filename for saving screen recording. '
                               'Extension must one of {".mp4", "avi"}')
        # mcxt.add_argument('break_file',
        #                   help='If this file exists then stop this recording')
        # ##################################### for app dependent options
        mcxt.add_argument('--size-percent', type=int,
                          display_name='Resize Resolution',
                          default=80, min_value=10, max_value=100,
                          help='Percent of actual screen size, '
                               'value must between 10 and 100, default is [[80]]')
        mcxt.add_argument('--fps', type=int,
                          display_name='Fremes/Sec',
                          default=10, min_value=1, max_value=20,
                          help='Frames per second, value must between 1 and 20, default is [[10]]')
        mcxt.add_argument('--timeout', type=int,
                          display_name='Timeout',
                          default=600,
                          help='If this timeout seconds elapsed then stop the recording, '
                               'default is [[600]] seconds, 10 minutes')
        argspec = mcxt.parse_args(args)
        return start_recording(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
