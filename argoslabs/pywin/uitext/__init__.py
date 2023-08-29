"""
====================================
 :mod:`argoslabs.pywin.uitext`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Extract Text of Window UI
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
import time
from io import StringIO
import pywinauto
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from pywinauto import application
import warnings
import inspect


################################################################################
class PywinOp(object):
    # ==========================================================================
    OP_TYPE = ['Extract Text By App',
               'Extract Text From Running App']
    BACKEND_TYPE = ['uia', 'win32']

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.app = None

    # ==========================================================================
    def start(self):
        app = application.Application()
        if ".cpl" in self.argspec.cmd_line:
            s_app = app.start(cmd_line=f'control {self.argspec.cmd_line}',
                              timeout=20)
        elif ".msc" in self.argspec.cmd_line:
            s_app = app.start(cmd_line=f'mmc {self.argspec.cmd_line}',
                              timeout=20)
        else:
            s_app = app.start(cmd_line=f'{self.argspec.cmd_line}',
                              timeout=20)
        self.app = s_app
        return self.app

    # ==========================================================================
    def extract_text_from_running_process(self):
        outst = StringIO()
        try:
            if self.argspec.delay:
                time.sleep(self.argspec.delay)
            else:
                time.sleep(2)
            process_id = pywinauto.findwindows.find_element(
                title=self.argspec.title_re
            ).process_id
            c_app = pywinauto.Application(
                backend=self.argspec.op_btype).connect(
                process=process_id
            )
            if not self.argspec.t_dialog_box:
                c_app.window(title=self.argspec.title_re,
                             visible_only=False).restore()
            c_app = c_app.top_window()
            if not self.argspec.child_window:
                window = c_app
            else:
                window = c_app.child_window(title_re=self.argspec.child_window)
            # Wrap this control
            this_ctrl = window.wrapper_object()
            # Create a list of this control and all its descendants
            all_ctrls = [this_ctrl, ] + this_ctrl.descendants()
            for index, ctrl in enumerate(all_ctrls):
                if self.argspec.p_btype_controls:
                    outst.write(f'{index},{ctrl}')
                    outst.write('\n')
                elif self.argspec.filter_controls:
                    if self.argspec.filter_controls in str(ctrl):
                        text = ctrl.window_text()
                        outst.write(f'{text}')
                        outst.write('\n')
                elif self.argspec.filter_controls_w_index:
                    if self.argspec.filter_controls_w_index == index:
                        print(
                            # dir
                            inspect.signature
                                (
                                ctrl
                        # .double_click_input
                                # ()
                        # .draw_outline()
                        # .right_click_input()
                        # .click()
                            )
                        )
                        text = ctrl.window_text()
                    if self.argspec.filter_controls_w_index == index:
                        text = ctrl.window_text()
                        outst.write(f'{text}')
                        outst.write('\n')
                else:
                    ctrl_text = ctrl.window_text()
                    if ctrl_text:
                        # transform multi-line text to one liner
                        ctrl_text = ctrl_text.replace('\n', r'\n').replace('\r',
                                                                           r'\r')
                        outst.write(f"{ctrl_text}")
                        outst.write('\n')
            print(outst.getvalue(), end='')
        except Exception as e:
            raise Exception(f"{e}")

    # ==========================================================================
    def extract_text_by_cmd_line(self):
        outst = StringIO()
        self.start()
        try:
            if self.argspec.delay:
                time.sleep(self.argspec.delay)
            else:
                time.sleep(2)
            if ".msc" in self.argspec.cmd_line:
                app = pywinauto.Application(
                    backend=self.argspec.op_btype).connect(
                    path='mmc.exe',
                    timeout=30
                )
            else:
                app = pywinauto.Application(
                    backend=self.argspec.op_btype).connect(
                    found_index=0,
                    title=self.argspec.title_re,
                    timeout=30
                )
            process_id = pywinauto.findwindows.find_element(
                title=self.argspec.title_re
            ).process_id
            c_app = pywinauto.Application(
                backend=self.argspec.op_btype).connect(
                process=process_id
            )
            if not self.argspec.t_dialog_box:
                c_app.window(title=self.argspec.title_re,
                             visible_only=False).restore()
            c_app = c_app.top_window()
            if not self.argspec.child_window:
                window = c_app
            else:
                window = c_app.child_window(title_re=self.argspec.child_window)
            # Wrap this control
            this_ctrl = window.wrapper_object()
            # Create a list of this control and all its descendants
            all_ctrls = [this_ctrl, ] + this_ctrl.descendants()
            for index, ctrl in enumerate(all_ctrls):
                if self.argspec.p_btype_controls:
                    outst.write(f'{index},{ctrl}')
                    outst.write('\n')
                elif self.argspec.filter_controls:
                    if self.argspec.filter_controls in str(ctrl):
                        text = ctrl.window_text()
                        outst.write(f'{text}')
                        outst.write('\n')
                elif self.argspec.filter_controls_w_index:
                    if self.argspec.filter_controls_w_index == index:
                        text = ctrl.window_text()
                        outst.write(f'{text}')
                        outst.write('\n')
                else:
                    ctrl_text = ctrl.window_text()
                    if ctrl_text:
                        # transform multi-line text to one liner
                        ctrl_text = ctrl_text \
                            .replace('\n', r'\n') \
                            .replace('\r', r'\r')
                        outst.write(ctrl_text)
                        outst.write('\n')
            if self.argspec.cmd_line:
                app.kill()
            print(outst.getvalue(), end='')
        except Exception as e:
            raise Exception(f"{e}")

    # ==========================================================================
    def do(self, op):
        if op == 'Extract Text By App':
            self.extract_text_by_cmd_line()
        elif op == 'Extract Text From Running App':
            self.extract_text_from_running_process()
        else:
            Exception("Select Function type")


################################################################################
@func_log
def reg_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        warnings.simplefilter("ignore", UserWarning)
        f = PywinOp(argspec)
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
            owner='ARGOS-LABS-DEMO',
            group='9',
            version='1.0',
            platform=['windows'],
            output_type='text',
            display_name='Win UI Text',
            icon_path=get_icon_path(__file__),
            description='Extract Text of Window UI',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='Function type',
                          choices=PywinOp.OP_TYPE,
                          help='Type of operation')
        mcxt.add_argument('op_btype', display_name='Backend Type',
                          choices=PywinOp.BACKEND_TYPE,
                          default='win32',
                          help='win32 (Microsoft Windows API) & uia (Microsoft UI Automation)')
        mcxt.add_argument('title_re', display_name='Title',
                          help='Title of window')
        # ##################################### for app optional parameters
        mcxt.add_argument('--cmd_line', display_name='App',
                          help='App best result use .cpl & .mcs & .exe file')
        mcxt.add_argument('--t_dialog_box', display_name='Title Over App',
                          action='store_true',
                          help='App best result use .cpl & .mcs & .exe file')
        mcxt.add_argument('--child_window', display_name='Child Window Name',
                          help='Title App Child Window Name')
        mcxt.add_argument('--delay', display_name='Delay',
                          type=int,
                          help='Delay for Load Window Interface')
        mcxt.add_argument('--p_btype_controls',
                          display_name='Print Backend Type Controls',
                          action='store_true',
                          help='Delay for Load Window Interface')
        mcxt.add_argument('--filter_controls', display_name='Filter Controls',
                          help='Filter Controls')
        mcxt.add_argument('--filter_controls_w_index',
                          display_name='Filter Controls With Index',
                          type=int,
                          help='Filter Controls With Index')
        mcxt.add_argument('--index_action',
                          display_name='Filter Controls With Index',
                          type=int,
                          help='Filter Controls With Index')
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
