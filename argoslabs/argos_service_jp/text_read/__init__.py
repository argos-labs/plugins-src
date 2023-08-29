#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.text_read`
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
#  * [2021/03/18]
#     Create

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import re


################################################################################
class Read_Text(object):

    # ==========================================================================
    def __init__(self, path, position, nl_code, encoding):
        self.path = os.path.abspath(path)
        self.position = position
        self.lines = None
        self.nl_code = nl_code
        self.encoding = encoding

        self.text_list = None
        self.text = None
        self.row_count = None
        self.last_row = None
        self.list_num = None
        self.list_slice = None

        self.match_check = None

        self.split_lines = None
        self.row_start = None
        self.row_end = None

        self.string = None

    # ==========================================================================
    def check_file_exists(self):
        if not os.path.isfile(self.path):
            raise IOError('File {} not found'.format(self.path))

        else:
            pass

    """
    # ==========================================================================
    def read_all(self):
        with open(self.path, mode="r", encoding=self.encoding) as f:
            self.text = f.read()
            print(self.text)
    """

    # ==========================================================================
    def read_lines(self):
        with open(self.path, mode="r", encoding=self.encoding) as f:
            if self.nl_code == 'default':
                self.text_list = [s.strip() for s in f.readlines()]
            elif self.nl_code == 'display':
                self.text_list = f.readlines()
                self.text_list = [s.replace('\n', '\\n') for s in self.text_list]

            self.row_count = len(self.text_list)
            self.last_row = self.row_count - 1

    # ==========================================================================
    def line_check(self):
        if self.position == 'All Lines':
            self.list_slice = self.text_list[:]
        elif self.position == 'First Line':
            self.list_slice = self.text_list[0]
        elif self.position == 'Last Line':
            self.list_slice = self.text_list[self.last_row]
        elif self.position == 'Select Lines':
            return 'select'

    # ==========================================================================
    def select_lines(self, lines):
        self.lines = lines
        self.match_check = re.fullmatch(r"[0-9]+?", self.lines)
        if self.match_check == None:
            self.match_check = re.fullmatch(r"[0-9]*?~[0-9]*?", self.lines)
            if self.match_check == None:
                raise IOError('The number of lines is incorrect.')
            else:
                pass

            self.match_check = re.fullmatch(r"[0-9]+?~[0-9]+?", self.lines)
            if self.match_check == None:
                pass
            else:
                self.split_lines = self.lines.split("~")
                self.row_start = int(self.split_lines[0]) - 1
                self.row_end = int(self.split_lines[1])

                if self.row_start > self.last_row:
                    raise IOError('Cannot be larger than the number of lines in the file!')
                elif self.row_end > self.last_row:
                    raise IOError('Cannot be larger than the number of lines in the file!')
                else:
                    pass

                self.list_slice = self.text_list[self.row_start:self.row_end]

            self.match_check = re.fullmatch(r"[0-9]+?~", self.lines)
            if self.match_check == None:
                pass
            else:
                self.split_lines = self.lines.split("~")
                self.row_start = int(self.split_lines[0]) - 1

                if self.row_start > self.last_row:
                    raise IOError('Cannot be larger than the number of lines in the file!')
                else:
                    pass

                self.list_slice = self.text_list[self.row_start:]

            self.match_check = re.fullmatch(r"~[0-9]+?", self.lines)
            if self.match_check == None:
                pass
            else:
                self.split_lines = self.lines.split("~")
                self.row_end = int(self.split_lines[1])

                if self.row_end > self.last_row:
                    raise IOError('Cannot be larger than the number of lines in the file!')
                else:
                    pass

                self.list_slice = self.text_list[:self.row_end]

        else:
            self.row_start = int(self.lines) - 1

            if self.row_start > self.last_row:
                raise IOError('Cannot be larger than the number of lines in the file!')
            else:
                pass

            self.list_slice = self.text_list[self.row_start]

    # ==========================================================================
    def select_line(self, start_line, end_line):
        if start_line == None:
            self.row_start = 0
        elif int(start_line) <= self.last_row:
            self.row_start = int(start_line) - 1
        else:
            raise IOError('Cannot be larger than the number of lines in the file!')

        if end_line == None:
            self.row_end = self.last_row + 1
        elif int(end_line) <= self.last_row:
            self.row_end = int(end_line)
        else:
            raise IOError('Cannot be larger than the number of lines in the file!')

        if self.row_start > self.row_end:
            raise IOError('The Start Line cannot be greater than the End Line!')

        self.list_slice = self.text_list[self.row_start:self.row_end]

    # ==========================================================================
    def output(self):
        if isinstance(self.list_slice, str) == True:
            self.string = self.list_slice
        elif isinstance(self.list_slice, list) == True:
            if len(self.list_slice) == 0:
                raise IOError('The corresponding line does not exist.')
            else:
                self.string = "\n".join(self.list_slice)
        else:
            raise IOError('Unexpected Error Occurred')

        print(self.string, end="")

################################################################################
@func_log
def read_text(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        RT = Read_Text(argspec.path,
                       argspec.position,
                       argspec.nl_code,
                       argspec.encoding)

        RT.check_file_exists()
        RT.read_lines()
        RT.line_check()

        if RT.line_check() == 'select':
            if argspec.start_line or argspec.end_line:
                #  RT.select_lines(argspec.lines)
                RT.select_line(argspec.start_line, argspec.end_line)
            else:
                raise IOError('Select \"Start Line\", \"End Line\" and Input values')
        else:
            pass

        RT.output()

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
        owner='ARGOS-SERVICE-JAPAN',
        group='2',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Text Read',
        icon_path=get_icon_path(__file__),
        description='Read text from a file',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('path',
                          display_name='File Path',
                          input_method='fileread',
                          help='A file to read the text')
        mcxt.add_argument('position',
                          display_name='Reading Position',
                          default='All Lines',
                          choices=['All Lines', 'First Line', 'Last Line', 'Select Lines'],
                          help='Select the position where you want to read')
        """
        mcxt.add_argument('--lines',
                          display_name='Reading Lines',
                          show_default=True,
                          help='Input the lines where you want to read')
        """
        mcxt.add_argument('--start_line',
                          display_name='Start Line',
                          show_default=True,
                          help='Input the lines where you want to read')
        mcxt.add_argument('--end_line',
                          display_name='End Line',
                          show_default=True,
                          help='Input the lines where you want to read')
        mcxt.add_argument('--nl_code',
                          display_name='New Line character',
                          default='default',
                          choices=['default', 'display'],
                          help='Select whether or not to display line feed character')
        # ######################################## for app dependent options
        mcxt.add_argument('--encoding',
                          default='utf-8',
                          display_name='Encoding',
                          help='File Encoding')

        argspec = mcxt.parse_args(args)
        return read_text(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
