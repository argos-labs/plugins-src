#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.excel_newfile`
====================================
.. moduleauthor:: Taiki Shimasaki <shimasaki@argos-service.com>
.. note:: ARGOS-LABS License

Description
===========
Plugin to create a new empty excel file
"""
# Authors
# ===========
#
# * Taiki Shimasaki
#
# Change Log
# --------
#
#  * [2020/08/07]
#     Create

################################################################################
import os
import pathlib
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import re
import openpyxl
import pathvalidate

################################################################################
class CreateExcel(object):

    # ==========================================================================
    def __init__(self, file_type, dir_path, filename):
        self.create = None
        self.file_type = file_type
        self.dir_path = dir_path
        self.filename = filename
        self.filename_len = None
        self.sheetname = None
        self.sheet_len = None
        self.filename_check = None
        self.file_path = None

    # ==========================================================================
    def check_dir_exist(self):
        if not os.path.isdir(self.dir_path):
            raise IOError('Directory {} not found'.format(self.dir_path))

        else:
            pass

    # ==========================================================================
    def check_dir_path(self):
        if self.dir_path[-1] in ('/', '\\'):
            self.dir_path = self.dir_path[:-1]

        else:
            pass

    # ==========================================================================
    def check_filename(self, validate):
        self.validate = validate
        if pathvalidate.is_valid_filename(self.filename) == False:
            if self.validate == 'Return Failure':
                raise IOError('Cannot use the filename')

            elif self.validate == 'Sanitize':
                self.filename = pathvalidate.sanitize_filename(self.filename)

            else:
                pass

        elif self.filename == '':
            raise IOError('Input [File Name] field !!!')

        elif pathvalidate.is_valid_filename(self.filename) == True:
            pass

        else:
            raise IOError('Unexpected Error Occurred')

    # ==========================================================================
    def check_sheetname(self, sheetname, sheet_len_opt):
        self.sheetname = sheetname
        if self.sheetname != None:
            if self.file_type == 'Excel':
                # sheetname illegal char check
                if re.search(r'[\'*/:?\\\[\]’＇＊／：？［＼］￥]+', self.sheetname) != None:
                    raise IOError('Cannot use the sheetname')

                elif self.sheetname == '':
                    raise IOError('Input [Sheetname] field !!!')

                else:
                    pass

                self.sheet_len = len(self.sheetname)
                self.sheet_len_opt = sheet_len_opt
                # sheetname length check
                if self.sheet_len > 31:
                    if self.sheet_len_opt == 'Return Failure':
                        raise IOError('Sheetname must be no more than 31 characters !!!')

                    elif self.sheet_len_opt == 'Cut to 31 char':
                        self.sheetname = self.sheetname[:(31 - self.sheet_len)]

                    else:
                        pass

                else:
                    pass

            else:
                raise IOError('Uncheck [Sheetname] field !!!')

        else:
            pass

    # ==========================================================================
    def make_filepath(self):
        if self.file_type == 'Excel':
            self.file_path = '{}\{}.xlsx'.format(self.dir_path, self.filename)
            self.filename_len = len(self.filename)

        elif self.file_type == 'CSV':
            self.file_path = '{}\{}.csv'.format(self.dir_path, self.filename)
            self.filename_len = len(self.filename)

        else:
            pass

    # ==========================================================================
    def file_exists_check(self, file_exists):
        self.file_exists = file_exists
        if os.path.exists(self.file_path):
            if self.file_exists == 'Return Failure':
                raise IOError('File is already exists!')

            elif self.file_exists == 'Overwrite':
                os.remove(self.file_path)

            elif self.file_exists == 'Add (n) at End':
                return 'add_n'

            elif self.file_exists == 'Ignore Failure':
                return 'ignore'

            else:
                raise IOError('Unexpected Error Occurred')

        else:
            pass

    # =========================================================================
    def add_n(self):
        self.count = 0
        if self.file_type == 'Excel':
            while os.path.exists(self.file_path) == True:
                self.filename = re.sub(r'\([0-9]+\)$', '', self.filename)
                self.count += 1
                self.filename += '({})'.format(self.count)
                self.file_path = '{}\{}.xlsx'.format(self.dir_path, self.filename)

            else:
                self.filename_len = len(self.filename)

        elif self.file_type == 'CSV':
            while os.path.exists(self.file_path) == True:
                self.filename = re.sub(r'\([0-9]+\)$', '', self.filename)
                self.count += 1
                self.filename += '({})'.format(self.count)
                self.file_path = '{}\{}.csv'.format(self.dir_path, self.filename)

            else:
                self.filename_len = len(self.filename)

        else:
            raise  IOError('Unexpected Error Occurred')

    # =========================================================================
    def path_len(self):
        if len(self.file_path) > 260:
            raise IOError('File Path is too long !!!')

        else:
            pass

    # =========================================================================
    def word_count(self):
        if self.file_type == 'Excel':
            if self.filename_len > 202:
                raise IOError('File name is too long !!!')

            else:
                pass

        elif self.file_type == 'CSV':
            if self.filename_len > 251:
                raise IOError('File name is too long !!!')

    # ==========================================================================
    def createexcel(self):
        if self.file_type == 'Excel':
            self.wb = openpyxl.Workbook()
            self.sheet = self.wb.active
            if self.sheetname == None:
                self.sheetname = 'sheet1'
            else:
                pass
            self.sheet.title = '{}'.format(self.sheetname)
            self.wb.save(self.file_path)
            self.wb.close()
            return sys.stdout.write(self.file_path)

        elif self.file_type == 'CSV':
            self.create = pathlib.Path(self.file_path)
            self.create.touch()
            return sys.stdout.write(self.file_path)

        else:
            raise IOError('Unexpected Error Occurred')

################################################################################
@func_log
def create_newexcel(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    ne = CreateExcel(argspec.file_type, argspec.dir_path, argspec.filename)
    try:
        ne.check_dir_exist()
        ne.check_dir_path()
        ne.check_filename(argspec.validate)
        ne.check_sheetname(argspec.sheetname, argspec.sheet_len_opt)
        ne.make_filepath()

        if ne.file_exists_check(argspec.file_exists) == 'ignore':
            pass

        elif ne.file_exists_check(argspec.file_exists) == 'add_n':
            ne.add_n()
            ne.path_len()
            ne.word_count()
            ne.createexcel()

        else:
            ne.path_len()
            ne.word_count()
            ne.createexcel()

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
        owner='ARGOS-SERVICE-JAPAN',
        group='2',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Excel Newfile',
        icon_path=get_icon_path(__file__),
        description='Creating new empty excel file',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('file_type',
                          display_name='File Type',
                          default='Excel',
                          choices=['Excel', 'CSV'],
                          help='Select creating file type')
        mcxt.add_argument('dir_path',
                          display_name='Directory Path',
                          input_method='folderread',
                          help='Where you want to create')
        mcxt.add_argument('filename',
                          display_name='File Name',
                          help='File name you want')
        mcxt.add_argument('file_exists',
                          display_name='If File Exists',
                          default='Return Failure',
                          choices=['Return Failure', 'Add (n) at End', 'Overwrite', 'Ignore Failure'],
                          help='When the file already exists')
        mcxt.add_argument('validate',
                          display_name='File Name Validation',
                          default='Return Failure',
                          choices=['Return Failure', 'Sanitize'])
        # ######################################## for app dependent options
        mcxt.add_argument('--sheetname',
                          display_name='Excel Sheetname',
                          help='Sheetname in the case of Excel')
        mcxt.add_argument('--sheet_len_opt',
                          display_name='Sheetname Length Option',
                          default='Return Failure',
                          choices=['Return Failure', 'Cut to 31 char'],
                          help='When the sheetname exceeds 31 characters')

        argspec = mcxt.parse_args(args)
        return create_newexcel(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass