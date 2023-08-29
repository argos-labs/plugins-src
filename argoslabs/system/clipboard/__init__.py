#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.system.clipboard`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module ai translate
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/08/09]
#     - 0.5초 20번 오류 등을 더 기다리도록 옵션 추가
#  * [2019/10/04]
#     - starting

################################################################################
import os
import sys
import time
import datetime
# noinspection PyPackageRequirements
import pyperclip
# import clipboard
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
OP_LIST = [
    'Copy',
    'Paste',
]


################################################################################
# noinspection PyBroadException
@func_log
def do_clipboard(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        if argspec.op not in OP_LIST:
            raise RuntimeError('Invalid clipboard operation "%s"' % argspec.op)
        last_exp = None
        s_ts = e_ts = datetime.datetime.now()
        while True:
            if (e_ts-s_ts).total_seconds() >= int(argspec.retry):
                break
            if argspec.op == 'Copy':
                if not argspec.copy_text:
                    msg = 'Clipboard error: Invalid text to copy'
                    sys.stderr.write('%s%s' % (msg, os.linesep))
                    mcxt.logger.error(msg)
                    return 2
                try:
                    pyperclip.copy(argspec.copy_text)
                    sys.stdout.write(argspec.copy_text)
                    sys.stdout.flush()
                    return 0
                except Exception as e:
                    # msg = 'Clipboard Copy error: %s' % str(e)
                    # sys.stderr.write('%s%s' % (msg, os.linesep))
                    # mcxt.logger.error(msg)
                    last_exp = e
                    time.sleep(0.5)
                    e_ts = datetime.datetime.now()
            elif argspec.op == 'Paste':
                # paste_text = None
                try:
                    paste_text = pyperclip.paste()
                    # if not paste_text:
                    #     msg = 'Clipboard error: Invalid text to paste'
                    #     sys.stderr.write('%s%s' % (msg, os.linesep))
                    #     mcxt.logger.error(msg)
                    #     return 3
                    sys.stdout.write(paste_text)
                    sys.stdout.flush()
                    return 0
                except Exception as e:
                    # msg = 'Clipboard Paste error: %s' % str(e)
                    # sys.stderr.write('%s%s' % (msg, os.linesep))
                    # mcxt.logger.error(msg)
                    last_exp = e
                    time.sleep(0.5)
                    e_ts = datetime.datetime.now()
        if last_exp is not None:
            raise last_exp
    except Exception as e:
        msg = 'Clipboard %s error: %s' % (argspec.op, str(e))
        sys.stderr.write('%s%s' % (msg, os.linesep))
        mcxt.logger.error(msg)
        return 1
    finally:
        mcxt.logger.info('>>>end...')


# ################################################################################
# # noinspection PyBroadException
# @func_log
# def do_clipboard_win32(mcxt, argspec):
#     import ctypes
#     # Get required functions, strcpy..
#     strcpy = ctypes.cdll.msvcrt.strcpy
#     ocb = ctypes.windll.user32.OpenClipboard  # Basic clipboard functions
#     ecb = ctypes.windll.user32.EmptyClipboard
#     gcd = ctypes.windll.user32.GetClipboardData
#     scd = ctypes.windll.user32.SetClipboardData
#     ccb = ctypes.windll.user32.CloseClipboard
#     ga = ctypes.windll.kernel32.GlobalAlloc  # Global memory allocation
#     gl = ctypes.windll.kernel32.GlobalLock  # Global memory Locking
#     gul = ctypes.windll.kernel32.GlobalUnlock
#     GMEM_DDESHARE = 0x2000
#
#     ############################################################################
#     def win32_paste_cb():
#         ocb(None)  # Open Clip, Default task
#         # 1 means CF_TEXT.. too lazy to get the token thingy...
#         pcontents = gcd(1)
#         data = ctypes.c_char_p(pcontents).value
#         # gul(pcontents) ?
#         ccb()
#         if isinstance(data, bytes):
#             return data.decode('utf-8')
#         if data is None:
#             return ""
#
#     ############################################################################
#     def win32_copy_cb(data):
#         ocb(None)  # Open Clip, Default task
#         ecb()
#         hCd = ga(GMEM_DDESHARE, len(bytes(data, "ascii")) + 1)
#         pchData = gl(hCd)
#         strcpy(ctypes.c_char_p(pchData), bytes(data, "ascii"))
#         gul(hCd)
#         scd(1, hCd)
#         ccb()
#
#     copy_funcs = (
#         win32_copy_cb,
#         # clipboard.copy,
#     )
#     paste_funcs = (
#         win32_paste_cb,
#         # clipboard.paste,
#     )
#     mcxt.logger.info('>>>starting...')
#     try:
#         if argspec.op not in OP_LIST:
#             raise RuntimeError('Invalid clipboard operation "%s"'
#             % argspec.op)
#         if argspec.op == 'Copy':
#             if not argspec.copy_text:
#                 msg = 'Clipboard error: Invalid text to copy'
#                 sys.stderr.write('%s%s' % (msg, os.linesep))
#                 mcxt.logger.error(msg)
#                 return 2
#             for func in copy_funcs:
#                 try:
#                     func(argspec.copy_text)
#                     break
#                 except Exception as e:
#                     msg = 'Clipboard Copy error: %s' % str(e)
#                     sys.stderr.write('%s%s' % (msg, os.linesep))
#                     mcxt.logger.error(msg)
#             sys.stdout.write(argspec.copy_text)
#             sys.stdout.flush()
#             return 0
#         elif argspec.op == 'Paste':
#             paste_text = None
#             for func in paste_funcs:
#                 try:
#                     paste_text = func()
#                     break
#                 except Exception as e:
#                     msg = 'Clipboard Paste error: %s' % str(e)
#                     sys.stderr.write('%s%s' % (msg, os.linesep))
#                     mcxt.logger.error(msg)
#             if not paste_text:
#                 msg = 'Clipboard error: Invalid text to paste'
#                 sys.stderr.write('%s%s' % (msg, os.linesep))
#                 mcxt.logger.error(msg)
#                 return 3
#             sys.stdout.write(paste_text)
#             sys.stdout.flush()
#             return 0
#     except Exception as e:
#         msg = 'Clipboard error: %s' % str(e)
#         sys.stderr.write('%s%s' % (msg, os.linesep))
#         mcxt.logger.error(msg)
#         return 1
#     finally:
#         mcxt.logger.info('>>>end...')


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
        display_name='Clipboard',
        icon_path=get_icon_path(__file__),
        description='Copy to or paste from system clipboard with text only.',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--copy-text',
                          display_name='Text to Clipboard', show_default=True,
                          help='Specify test text which is copied to clipboard')
        mcxt.add_argument('--retry',
                          display_name='Retry Duration', default=10, type=int,
                          help='Specify retry duration to paste from clipboard,'
                               ' default is 10 secs')
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          default=OP_LIST[-1],
                          choices=OP_LIST,
                          help='Choose operation of clipboard')
        argspec = mcxt.parse_args(args)
        # if sys.platform == 'win32':
        #     return do_clipboard_win32(mcxt, argspec)
        return do_clipboard(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
