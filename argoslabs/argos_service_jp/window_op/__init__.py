#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.window_op`
====================================
.. moduleauthor:: Taiki Shimasaki <shimasaki@argos-service.com>
.. note:: ARGOS-LABS License

Description
===========
Input Plugin Description
"""
# Authors
# ===========
#
# * Taiki Shimasaki
#
# Change Log
# --------
#
#  * [2021/01/08]
#     Create

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import pygetwindow
import re
import ctypes


################################################################################
class Window_Op(object):

    # ==========================================================================
    def __init__(self, op, window_title):
        self.op = op

        self.titles = None

        self.window_title = window_title
        self.active_title = None
        self.selected = None
        self.window_title_list = None
        self.window_title_dupe = None

        self.window_height = None
        self.window_width = None

        self.move_right = None
        self.move_down = None

        self.move_X = None
        self.move_Y = None

    # ==========================================================================
    def select_op(self):
        if self.op == 'Get Window\'s List':
            return 'get list'

        elif self.op == 'Get Active Window\'s Title':
            return 'get active'

        elif self.op == 'Select Window':
            return 'select'

        elif self.op == 'Maximize':
            return 'max'

        elif self.op == 'Minimize':
            return 'min'

        elif self.op == 'Select Window Resize':
            return 'resize'

        elif self.op == 'Select Window Move (relative)':
            return 'move_re'

        elif self.op == 'Select Window Move (absolute)':
            return 'move_ab'

        else:
            pass

    """
    # This is available, but I'm not sure about the details
    # ==========================================================================
    def get_list(self):
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                             ctypes.POINTER(ctypes.c_int),
                                             ctypes.POINTER(ctypes.c_int))
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible

        titles = []

        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                titles.append(buff.value)
            return True

        EnumWindows(EnumWindowsProc(foreach_window), 0)

        print(titles)
    """

    # ==========================================================================
    def get_list(self):
        self.titles = pygetwindow.getAllTitles()
        for title in self.titles:
            if title == '':
                pass
            else:
                print(title)

    # ==========================================================================
    def get_active(self):
        self.active_title = pygetwindow.getActiveWindowTitle()
        if self.active_title == None:
            print('None')
        elif self.active_title == '':
            print('No Title')
        else:
            pass
        print(self.active_title, end="")

    # ==========================================================================
    def select_window(self):
        self.titles = pygetwindow.getAllTitles()
        self.window_title = self.window_title.replace('*', '.*')
        self.window_title_list = [s for s in self.titles if re.match(self.window_title, s)]
        self.window_title_dupe = len(self.window_title_list)
        if self.window_title_dupe != 1:
            raise IOError('There are {} windows that match your criteria!!!'.format(self.window_title_dupe))
        elif self.window_title_dupe == 0:
            raise IOError('There is No window that match your criteria!!!')
        else:
            pass
        self.selected = pygetwindow.getWindowsWithTitle(self.window_title_list[0])[0]

    # ==========================================================================
    def window_activate(self):
        if self.selected.isMaximized == True:
            self.selected.activate()

        elif self.selected.isMaximized == False:
            self.selected.restore()
            self.selected.activate()

    # ==========================================================================
    def maximize(self):
        if self.selected.isMaximized == True:
            self.selected.activate()

        elif self.selected.isMaximized == False:
            self.selected.restore()
            self.selected.maximize()
            self.selected.activate()

    # ==========================================================================
    def minimize(self):
        if self.selected.isMaximized == True:
            self.selected.activate()
            self.selected.restore()
            self.selected.minimize()

        elif self.selected.isMaximized == False:
            self.selected.restore()
            self.selected.activate()
            self.selected.minimize()

    # ==========================================================================
    def change_size(self, window_height, window_width):
        if window_height != None:
            self.window_height = int(window_height)
        else:
            self.window_height = self.selected.height

        if window_width != None:
            self.window_width = int(window_width)
        else:
            self.window_width = self.selected.width


        if self.selected.isMaximized == True:
            self.selected.activate()
            self.selected.resizeTo(self.window_width, self.window_height)
            self.selected.activate()

        elif self.selected.isMaximized == False:
            self.selected.restore()

            if self.selected.isMaximized == True:
                self.selected.restore()
            else:
                pass

        self.selected.activate()
        self.selected.resizeTo(self.window_width, self.window_height)
        self.selected.activate()

    # ==========================================================================
    def move_re(self, move_right, move_down):
        if move_right != None:
            self.move_right = int(move_right)
        else:
            self.move_right = 0

        if move_down != None:
            self.move_down = int(move_down)
        else:
            self.move_down = 0


        if self.selected.isMaximized == True:
            self.selected.activate()
            self.selected.move(self.move_right, self.move_down)
            self.selected.activate()

        elif self.selected.isMaximized == False:
            self.selected.restore()

            if self.selected.isMaximized == True:
                self.selected.restore()
            else:
                pass

        self.selected.activate()
        self.selected.move(self.move_right, self.move_down)
        self.selected.activate()

    # ==========================================================================
    def move_ab(self, move_X, move_Y):

        if self.selected.isMaximized == True:
            self.selected.activate()

            if move_X != None:
                self.move_X = int(move_X) - 8  # Fix later
            else:
                self.move_X = self.selected.left - 8  # Fix later

            if move_Y != None:
                self.move_Y = int(move_Y)
            else:
                self.move_Y = self.selected.top

            self.selected.moveTo(self.move_X, self.move_Y)
            self.selected.activate()

        elif self.selected.isMaximized == False:
            self.selected.restore()

            if self.selected.isMaximized == True:
                self.selected.restore()
            else:
                pass

            if move_X != None:
                self.move_X = int(move_X) - 8  # Fix later
            else:
                self.move_X = self.selected.left - 8  # Fix Later

            if move_Y != None:
                self.move_Y = int(move_Y)
            else:
                self.move_Y = self.selected.top

        self.selected.activate()
        self.selected.moveTo(self.move_X, self.move_Y)
        self.selected.activate()

################################################################################
@func_log
def window_op(mcxt, argspec):

    mcxt.logger.info('>>>starting...')
    try:
        wo = Window_Op(argspec.op, argspec.window_title)

        if wo.select_op() == 'get list':
            wo.get_list()

        elif wo.select_op() == 'get active':
            wo.get_active()

        elif wo.select_op() == 'select':
            wo.select_window()
            wo.window_activate()

        elif wo.select_op() == 'max':
            wo.select_window()
            wo.maximize()

        elif wo.select_op() == 'min':
            wo.select_window()
            wo.minimize()

        elif wo.select_op() == 'resize':
            wo.select_window()
            wo.change_size(argspec.window_height, argspec.window_width)

        elif wo.select_op() == 'move_re':
            wo.select_window()
            wo.move_re(argspec.move_right, argspec.move_down)

        elif wo.select_op() == 'move_ab':
            wo.select_window()
            wo.move_ab(argspec.move_X, argspec.move_Y)

        mcxt.logger.info('>>>end...')
        return 0
    except Exception as err:
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
        owner='ARGOS-SERVICE-JP',
        group='9',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Window Op',
        icon_path=get_icon_path(__file__),
        description='Some manipulation plugin for windows',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Operation',
                          choices=['Get Window\'s List',
                                   'Get Active Window\'s Title',
                                   'Select Window',
                                   'Select Window Resize',
                                   'Maximize',
                                   'Minimize',
                                   'Select Window Move (relative)',
                                   'Select Window Move (absolute)'],  # TBA 'Move'
                          default='Get Window\'s List',
                          help='Select the operation you want to perform')
        # ######################################## for app dependent options
        mcxt.add_argument('--window_title',
                          display_name='Window Title',
                          show_default=True,
                          help='Input purpose window\'s title')
        mcxt.add_argument('--window_height',
                          display_name='Window Height',
                          show_default=True,
                          help='Input purpose window\'s height')
        mcxt.add_argument('--window_width',
                          display_name='Window Width',
                          show_default=True,
                          help='Input purpose window\'s width')
        mcxt.add_argument('--move_right',
                          display_name='Move Right',
                          show_default=True,
                          help='Input the distance moving to right')
        mcxt.add_argument('--move_down',
                          display_name='Move Down',
                          show_default=True,
                          help='Input the distance moving to down')
        mcxt.add_argument('--move_X',
                          display_name='X-Coordinate',
                          show_default=True,
                          help='Input the X-Coordinate (Horizontally)')
        mcxt.add_argument('--move_Y',
                          display_name='Y-Coordinate',
                          show_default=True,
                          help='Input the Y-Coordinate (Vertically)')

        argspec = mcxt.parse_args(args)
        return window_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
