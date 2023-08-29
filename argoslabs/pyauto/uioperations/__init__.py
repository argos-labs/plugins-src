"""
====================================
 :mod:`argoslabs.pyauto.uitext`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Control GUI Mouse Action
"""
# Authors
# ===========
#
# * Arun Kumar
#
# Change Log
# --------
#


################################################################################
import os
import sys
import pyautogui
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class PyguiOp(object):
    # ==========================================================================
    OP_TYPE = ['Right Click',
               'Left Click',
               'Double Click',
               'Triple Click',
               'Middle Click',
               'Mouse Down',
               'Mouse Up',
               'Scroll']

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec

    # ==========================================================================
    def rightclick(self):
        if self.argspec.x and self.argspec.y:
            pyautogui.rightClick(x=self.argspec.x, y=self.argspec.y)
        else:
            pyautogui.rightClick()

    # ==========================================================================
    def leftclick(self):
        if self.argspec.x and self.argspec.y:
            pyautogui.leftClick(x=self.argspec.x, y=self.argspec.y)
        else:
            pyautogui.leftClick()

    # ==========================================================================
    def doubleclick(self):
        if self.argspec.x and self.argspec.y:
            pyautogui.doubleClick(x=self.argspec.x, y=self.argspec.y)
        else:
            pyautogui.doubleClick()

    # ==========================================================================
    def tripleclick(self):
        if self.argspec.x and self.argspec.y:
            pyautogui.tripleClick(x=self.argspec.x, y=self.argspec.y)
        else:
            pyautogui.tripleClick()

    # ==========================================================================
    def middleclick(self):
        if self.argspec.x and self.argspec.y:
            pyautogui.middleClick(x=self.argspec.x, y=self.argspec.y)
        else:
            pyautogui.middleClick()

    # ==========================================================================
    def mousedown(self):
        if self.argspec.x and self.argspec.y and self.argspec.duration:
            pyautogui.mouseDown(x=self.argspec.x,
                                y=self.argspec.y,
                                duration=self.argspec.duration)
        elif self.argspec.duration:
            pyautogui.mouseDown(x=self.argspec.x,
                                y=self.argspec.y,
                                duration=self.argspec.duration)
        elif self.argspec.x and self.argspec.y:
            pyautogui.mouseDown(x=self.argspec.x,
                                y=self.argspec.y,
                                duration=0.0, )
        else:
            pyautogui.mouseDown(duration=0.0)

    # ==========================================================================
    def mouseup(self):
        if self.argspec.x and self.argspec.y and self.argspec.duration:
            pyautogui.mouseUp(x=self.argspec.x,
                              y=self.argspec.y,
                              duration=self.argspec.duration)
        elif self.argspec.duration:
            pyautogui.mouseUp(x=self.argspec.x,
                              y=self.argspec.y,
                              duration=self.argspec.duration, )
        elif self.argspec.x and self.argspec.y:
            pyautogui.mouseUp(x=self.argspec.x,
                              y=self.argspec.y,
                              duration=0.0, )

        else:
            pyautogui.mouseUp(duration=0.0)

    # ==========================================================================
    def scroll(self):
        if self.argspec.x and self.argspec.y and self.argspec.s_click:
            pyautogui.scroll(x=self.argspec.x,
                             y=self.argspec.y,
                             clicks=self.argspec.s_click)
        elif self.argspec.x and self.argspec.y:
            pyautogui.scroll(x=self.argspec.x,
                             y=self.argspec.y,
                             clicks=1)
        elif self.argspec.s_click:
            pyautogui.scroll(clicks=self.argspec.s_click)
        else:
            pyautogui.scroll(clicks=1)

    # =========================================================================
    def do(self, op):
        if op == 'Right Click':
            self.rightclick()

        elif op == 'Left Click':
            self.leftclick()

        elif op == 'Double Click':
            self.doubleclick()

        elif op == 'Triple Click':
            self.tripleclick()

        elif op == 'Mouse Down':
            self.mousedown()

        elif op == 'Mouse Up':
            self.mouseup()

        elif op == 'Scroll':
            self.scroll()


################################################################################
@func_log
def reg_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        pyautogui.confirm('Shall I proceed?')
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 1.0
        f = PyguiOp(argspec)
        f.do(argspec.op)
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
    with ModuleContext(
            owner='ARGOS-LABS',
            group='7',
            version='1.0',
            platform=['windows'],
            output_type='text',
            display_name='Mouse Action',
            icon_path=get_icon_path(__file__),
            description='Mouse Action',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='Mouse Action',
                          choices=PyguiOp.OP_TYPE,
                          default='Right Click',
                          help='Type of Mouse Action')
        # ##################################### for app optional parameters
        mcxt.add_argument('--x', display_name='X',
                          type=int,
                          default=0,
                          help='X Position of mouse')
        mcxt.add_argument('--y', display_name='Y',
                          type=int,
                          default=0,
                          help='Y Position of mouse')
        mcxt.add_argument('--s_click', display_name='No of Scroll',
                          type=int,
                          default=0,
                          help='-ve Scroll Down +ve Scroll Up')
        mcxt.add_argument('--duration', display_name='Duration',
                          default=0.0,
                          help='time in 0.0 secs')
        argspec = mcxt.parse_args(args)
        return reg_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
