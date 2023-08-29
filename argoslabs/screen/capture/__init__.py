"""
====================================
 :mod:`argoslabs.screen.capture`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for screen capture
"""
#
# Authors
# ===========
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/06/16]
#     - 우선 영준팀장의 요청에 따라 official에 OPEN을 위해 active 윈도우
#       옵션 막고 올림
#  * [2021/06/14]
#     - main
#  * [2021/06/07]
#     - starting

################################################################################
import os
import sys
import pyautogui
import traceback
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
if sys.platform == 'win32':
    import win32gui
    import win32process


################################################################################
G_RECT = None


################################################################################
def get_safe_next_filename(fn):
    fn, ext = os.path.splitext(fn)
    for n in range(1, 1000000):
        nfn = f'{fn} ({n})' + ext
        if not os.path.exists(nfn):
            return nfn


################################################################################
def win32_callback(hwnd, pid):
    b_found = False
    win_pids = win32process.GetWindowThreadProcessId(hwnd)
    if isinstance(pid, (list, tuple)):
        for _pid in pid:
            if _pid in win_pids:
                b_found = True
                break
    if not b_found:
        return
    title = win32gui.GetWindowText(hwnd)
    if not (win32gui.IsWindowEnabled(hwnd) and
        win32gui.IsWindowVisible(hwnd)):
        return
    # rect = win32gui.GetWindowRect(hwnd)
    # print(f'pid={pid}, hwnd-pids={win_pids}')
    # print("Window %s:" % title)
    # print("\tLocation: (%d, %d)" % (x, y))
    # print("\t    Size: (%d, %d)" % (w, h))
    global G_RECT
    #G_RECT = list(rect)

    _left, _top, _right, _bottom = win32gui.GetClientRect(hwnd)
    left, top = win32gui.ClientToScreen(hwnd, (_left, _top))
    # right, bottom = win32gui.ClientToScreen(hwnd, (_right, _bottom))
    right = left + _right
    bottom = top + _bottom
    G_RECT = (left, top, right, bottom)

    # if G_RECT[0] < 0:
    #     G_RECT[0] = 0
    # if G_RECT[1] < 0:
    #     G_RECT[1] = 0
    # G_RECT = tuple(G_RECT)


################################################################################
def win32_active_capture(mcxt, argspec):
    if sys.platform != 'win32':
        raise RuntimeError('Active window capturing is only supported on Windows')
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    # return(psutil.Process(pid[-1]).name())
    win32gui.EnumWindows(win32_callback, pid)
    if G_RECT:
        _ = pyautogui.screenshot(argspec.filename, region=G_RECT)
    else:
        raise RuntimeError('Cannot get region of Active window')


################################################################################
@func_log
def do_capture(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if os.path.exists(argspec.filename):
            argspec.filename = get_safe_next_filename(argspec.filename)
        # if argspec.active_window:
        #     win32_active_capture(mcxt, argspec)
        # else:
        _ = pyautogui.screenshot(argspec.filename)
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
        display_name='Screen Capture',
        icon_path=get_icon_path(__file__),
        description='Start ARGOS LABS Screen Capture',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('filename',
                          display_name='Filename',
                          input_method='filewrite',
                          help='Filename for saving screen capture')
        # ##################################### for app dependent options
        # mcxt.add_argument('--active-window', action='store_true',
        #                   display_name='Active Win',
        #                   help='If this flag is set capture foremost, active windows only')
        argspec = mcxt.parse_args(args)
        return do_capture(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
