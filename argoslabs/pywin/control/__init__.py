"""
====================================
 :mod:`argoslabs.pywin.control`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Control Window UI
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
# import inspect


################################################################################
class PywinOp(object):
    # ==========================================================================
    OP_TYPE = ['Control By App',
               'Control Running App']
    BACKEND_TYPE = ['uia', 'win32']
    ACTION_TYPE = [
        '1 = Draw Outline',
        '2 = Click',
        '3 = Double Click Input',
        '4 = Right Click Input'
    ]

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
    @staticmethod
    def get_title_control_type(child_window):
        title = ''
        control_type = ''
        auto_id = ''
        class_name = ''
        child_window = child_window.split('"')
        for i, val in enumerate(child_window):
            if 'title' in val:
                title = child_window[i + 1]
            if 'control_type' in val:
                control_type = child_window[i + 1]
            if 'auto_id' in val:
                auto_id = child_window[i + 1]
            if 'class_name' in val:
                class_name = child_window[i + 1]
        return title, control_type, auto_id, class_name

    # ==========================================================================
    def control_running_process(self):
        try:
            if self.argspec.delay:
                time.sleep(self.argspec.delay)
            else:
                time.sleep(2)
            process_id = pywinauto.findwindows.find_element(
                title=self.argspec.title_re,
                found_index=0
            ).process_id
            c_app = pywinauto.Application(
                backend=self.argspec.op_btype).connect(
                process=process_id,
                found_index=0,
            )
            if not self.argspec.t_dialog_box:
                c_app.window(title=self.argspec.title_re,
                             visible_only=False).restore()
            c_app = c_app.top_window()
            if self.argspec.child_window:
                for i, child_window in enumerate(self.argspec.child_window):
                    title, control_type, auto_id,class_name = self.get_title_control_type(
                        child_window
                    )
                    if auto_id and title and control_type:
                        window = c_app.child_window(
                            title=title,
                            control_type=control_type,
                            auto_id=auto_id,
                            found_index=0
                        )
                    elif title and control_type:
                        window = c_app.child_window(
                            title=title,
                            control_type=control_type,
                            found_index=0
                        )
                    elif title and class_name:
                        window = c_app.child_window(
                            title=title,
                            class_name=class_name,
                            found_index=0
                        )
                    elif title:
                        window = c_app.child_window(
                            title=title,
                            found_index=0
                        )
                    elif class_name:
                        window = c_app.child_window(
                            title=title,
                            found_index=0
                        )
                    else:
                        raise Exception("Invalid child_window")
                    if self.argspec.action:
                        self.control_action(window, control_type, i)
            if self.argspec.store_controls:
                filename = self.argspec.store_controls
                c_app.print_control_identifiers(
                    filename=filename
                )
                print(filename, end='')
            else:
                print('success', end='')
        except Exception as e:
            raise Exception(f"{e}")

    # ==========================================================================
    def control_by_cmd_line(self):
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
                title=self.argspec.title_re,
                found_index=0,
            ).process_id
            c_app = pywinauto.Application(
                backend=self.argspec.op_btype).connect(
                process=process_id,
                found_index=0,
            )
            if not self.argspec.t_dialog_box:
                c_app.window(title=self.argspec.title_re,
                             visible_only=False).restore()
            c_app = c_app.top_window()
            if self.argspec.child_window:
                for i, child_window in enumerate(self.argspec.child_window):
                    title, control_type, auto_id,class_name = self.get_title_control_type(
                        child_window
                    )
                    if auto_id and title and control_type:
                        window = c_app.child_window(
                            title=title,
                            control_type=control_type,
                            auto_id=auto_id,
                            found_index=0
                        )
                    elif title and control_type:
                        window = c_app.child_window(
                            title=title,
                            control_type=control_type,
                            found_index=0
                        )
                    elif title and class_name:
                        window = c_app.child_window(
                            title=title,
                            class_name=class_name,
                            found_index=0
                        )
                    elif title:
                        window = c_app.child_window(
                            title=title,
                            found_index=0
                        )
                    elif class_name:
                        window = c_app.child_window(
                            title=title,
                            found_index=0
                        )
                    else:
                        raise Exception("Invalid child_window")
                    if self.argspec.action:
                        self.control_action(window,control_type,i)
            if self.argspec.store_controls:
                filename = self.argspec.store_controls
                c_app.print_control_identifiers(
                    filename=filename
                )
                print(filename, end='')
            else:
                print('success', end='')
            if self.argspec.cmd_line:
                app.kill()
            print(outst.getvalue(), end='')
        except Exception as e:
            raise Exception(f"{e}")

    # ==========================================================================
    def control_action(self,window,control_type,i):
        if control_type == 'ComboBox':
            found = False
            dup_find = '!@#$%'
            window.type_keys("%{DOWN}")
            while not found:
                window.type_keys('{VK_DOWN}')
                if window.selected_text() == self.argspec.action[i]:
                    window.type_keys('{ENTER}')
                    found = True
                    break
                if dup_find == window.selected_text():
                    break
                else:
                    dup_find = window.selected_text()
            while not found:
                window.type_keys('{VK_UP}')
                if window.selected_text() == self.argspec.action[i]:
                    window.type_keys('{ENTER}')
                    found = True
                    break
                if dup_find == window.selected_text():
                    break
                else:
                    dup_find = window.selected_text()
            if not found:
                raise Exception("Dropdoown not found")
        elif self.argspec.action[i] == '1':
            window.draw_outline()
        elif self.argspec.action[i] == '2':
            window.click_input()
        elif self.argspec.action[i] == '3':
            window.double_click_input()
        elif self.argspec.action[i] == '4':
            window.right_click_input()
        elif control_type == 'Edit':
            found = False
            dup_find = '!@#$%'
            window.type_keys("%{DOWN}")
            while not found:
                window.type_keys('{VK_DOWN}')
                if window.get_value() == self.argspec.action[i]:
                    window.type_keys('{ENTER}')
                    found = True
                    break
                if dup_find == window.get_value():
                    break
                else:
                    dup_find = window.get_value()
            while not found:
                window.type_keys('{VK_UP}')
                if window.get_value() == self.argspec.action[i]:
                    window.type_keys('{ENTER}')
                    found = True
                    break
                if dup_find == window.get_value():
                    break
                else:
                    dup_find = window.get_value()
            if not found:
                raise Exception("Dropdoown not found")
        else:
            raise Exception("No Action")


    # ==========================================================================
    def do(self, op):
        if op == 'Control By App':
            self.control_by_cmd_line()
        elif op == 'Control Running App':
            self.control_running_process()
        else:
            raise Exception("Select Function type")


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
            owner='ARGOS-LABS',
            group='9',
            version='1.0',
            platform=['windows'],
            output_type='text',
            display_name='Win UI Control',
            icon_path=get_icon_path(__file__),
            description='Control Window UI',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='Function type',
                          choices=PywinOp.OP_TYPE,
                          help='Type of operation')
        mcxt.add_argument('op_btype', display_name='Backend Type',
                          choices=PywinOp.BACKEND_TYPE,
                          default='uia',
                          help='win32 (Microsoft Windows API) & uia (Microsoft UI Automation)')
        mcxt.add_argument('title_re', display_name='Title',
                          help='Title of window')
        # ##################################### for app optional parameters
        mcxt.add_argument('--cmd_line', display_name='App',
                          help='App best result use .cpl & .mcs & .exe file')
        mcxt.add_argument('--t_dialog_box', display_name='Title Over App',
                          action='store_true',
                          help='App best result use .cpl & .mcs & .exe file')
        mcxt.add_argument('--child_window', display_name='Child Window String',
                          nargs='+',
                          help='title and control_type Child Window Name')
        mcxt.add_argument('--delay', display_name='Delay',
                          type=int,
                          default=2,
                          help='Delay for Load Window Interface')
        mcxt.add_argument('--action',
                          display_name='Action',
                          nargs='+',
                          help='1 = Draw Outline,2 = Click,3 = Double Click Input,4 = Right Click Input')
        mcxt.add_argument('--store_controls', display_name='Store Controls',
                          input_method='fileread',
                          help='File path to Store Controls')
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
