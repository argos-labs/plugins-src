#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.text_write`
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
#  * [2021/03/16]
#     Create

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class Write_Text(object):

    # ==========================================================================
    def __init__(self, path, string, position, newline, nl_code, encoding,
                 file_exists, overwrite):
        self.path = os.path.abspath(path)
        self.string = string
        self.position = position
        self.mode = None

        self.newline = newline
        if nl_code == 'CR(\\r)':
            self.nl_code = '\r'
        elif nl_code == 'LF(\\n)':
            self.nl_code = '\n'
        elif nl_code == 'CRLF(\\r\\n)':
            self.nl_code = '\r\n'

        self.encoding = encoding
        self.file_exists = file_exists
        self.file_strings = None

        self.overwrite = overwrite

    # ==========================================================================
    def check_file_exists(self):
        if not os.path.isfile(self.path):
            if self.file_exists == 'New Create':
                with open(self.path, mode="w"):
                    pass
            elif self.file_exists == 'Return Failure':
                raise IOError('File {} not found'.format(self.path))

        else:
            pass

    # ==========================================================================
    def check_writing_position(self):
        if self.overwrite:
            self.mode = 'w'
            return 'overwrite'

        else:
            if self.position == 'Add to End':
                self.mode = 'a'
                return 'end'
            elif self.position == 'Add to Front':
                self.mode = 'w+'
                return 'begin'
            else:
                pass

    # ==========================================================================
    def add_end_write(self):
        with open(self.path, mode=self.mode, encoding=self.encoding) as f:
            if self.newline == 'Add to End':
                f.write('{}{}'.format(self.string, self.nl_code))
            elif self.newline == 'Add to Front':
                f.write('{}{}'.format(self.nl_code, self.string))
            elif self.newline == 'None':
                f.write(self.string)
            else:
                raise IOError('Unexpected Error Occurred')

            print(self.path, end="")

    # ==========================================================================
    def add_beg_write(self):
        with open(self.path, mode="r", encoding=self.encoding) as f:
            self.file_strings = f.readlines()

        if self.newline == 'Add to End':
            self.file_strings.insert(0, '{}{}'.format(self.string, self.nl_code))
        elif self.newline == 'Add to Front':
            self.file_strings.insert(0, '{}{}'.format(self.nl_code, self.string))
        elif self.newline == 'None':
            self.file_strings.insert(0, self.string)
        else:
            raise IOError('Unexpected Error Occurred')

        with open(self.path, mode=self.mode, encoding=self.encoding) as f:
            f.writelines(self.file_strings)

            print(self.path, end="")

    # ==========================================================================
    def over_write(self):
        with open(self.path, mode=self.mode, encoding=self.encoding) as f:
            if self.newline == 'Add to End':
                f.write('{}{}'.format(self.string, self.nl_code))
            elif self.newline == 'Add to Front':
                f.write('{}{}'.format(self.nl_code, self.string))
            elif self.newline == 'None':
                f.write(self.string)
            else:
                raise IOError('Unexpected Error Occurred')

            print(self.path, end="")

################################################################################
@func_log
def write_text(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        WT = Write_Text(argspec.path,
                        argspec.string,
                        argspec.position,
                        argspec.newline,
                        argspec.nl_code,
                        argspec.encoding,
                        argspec.file_exists,
                        argspec.overwrite)

        WT.check_file_exists()

        posit = WT.check_writing_position()

        if posit == 'end':
            WT.add_end_write()
        elif posit == 'begin':
            WT.add_beg_write()
        elif posit == 'overwrite':
            WT.over_write()

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
    with ModuleContext(
        owner='ARGOS-SERVICE-JAPAN',
        group='2',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Text Write',
        icon_path=get_icon_path(__file__),
        description='Write text to a file',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('path',
                          display_name='File Path',
                          input_method='fileread',
                          help='A file to write text to')
        mcxt.add_argument('string',
                          display_name='String to Write',
                          help='Input the string to write')
        mcxt.add_argument('position',
                          display_name='Writing Position',
                          default='Add to End',
                          choices=['Add to End', 'Add to Front'],
                          help='Select the position where you want to add')
        mcxt.add_argument('newline',
                          default='Add to End',
                          choices=['Add to End', 'Add to Front', 'None'],
                          display_name='New Line',
                          help='Select the position to insert the line break')
        # ######################################## for app dependent options
        mcxt.add_argument('--nl_code',
                          default='LF(\\n)',
                          choices=['CR(\\r)', 'LF(\\n)', 'CRLF(\\r\\n)'],
                          display_name='New Line Character',
                          show_default=True,
                          help='Select the newline character')
        mcxt.add_argument('--encoding',
                          default='utf-8',
                          display_name='Encoding',
                          show_default=True,
                          help='File Encoding')
        mcxt.add_argument('--file_exists',
                          display_name='File Not Exists',
                          default='New Create',
                          choices=['New Create', 'Return Failure'],
                          help='When the file already exists')
        mcxt.add_argument('--overwrite',
                          display_name='Overwrite',
                          action='store_true',
                          help='Overwrite File')

        argspec = mcxt.parse_args(args)
        return write_text(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
