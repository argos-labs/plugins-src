#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.create_newfile`
====================================
.. moduleauthor:: Taiki Shimasaki <shimasaki@argos-service.com>
.. note:: ARGOS-LABS License

Description
===========
Plugin to create a new empty file
"""
# Authors
# ===========
#
# * Taiki Shimasaki
#
# Change Log
# --------
#
#  * [2020/07/31]
#     Create
#  * [2020/08/03]
#     Add Select Extension Function
#  * [2020/08/07]
#     Add No Extension Option & Function

################################################################################
import os
import pathlib
import sys

from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import re
import openpyxl
from datetime import datetime
import pathvalidate

################################################################################
class CreateFile(object):

    # ==========================================================================
    def __init__(self, dir_path, filename, ext, other_ext):
        self.create = None
        self.dir_path = dir_path
        self.filename = filename
        self.ext = ext
        self.other_ext = other_ext
        self.filename_check = None
        self.filename_len = None
        self.file_path = None
        self.sheetname = None

    # ==========================================================================
    def check_ext_input(self):
        if self.ext in ('txt', 'docx', 'xlsx', 'pptx', 'pdf', 'csv', 'log', 'xml', 'html'):
            if self.other_ext == self.ext:
                self.ext = self.other_ext

            elif self.other_ext != None:
                raise IOError('Uncheck the [Other Extension] !!!')

            else:
                pass

        elif self.other_ext == '':
            if self.ext == 'No Extension':
                self.ext = 'No Extension'

            elif self.ext == 'INPUT [Other Extension(Adv)]':
                self.ext = 'No Extension'

            else:
                raise IOError('Input extension in [Other Extension(Adv)]!!!')

        elif self.ext == 'INPUT [Other Extension(Adv)]':
            self.ext = self.other_ext

        else:
            pass

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
    def check_extension(self):
        if self.ext == None:
            raise IOError('Input extension [Other Extension] field')

        elif re.search(r'[\\/:*?"<>|]+', self.ext) != None:
            raise IOError('Cannot use the extension')

        else:
            pass

    # ==========================================================================
    def check_sheetname(self, sheetname, sheet_len_opt):
        self.sheetname = sheetname
        if self.sheetname != None:
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

        # Sheetname field uncheck check
        elif self.ext not in ('xlsx', 'xls', 'xlsm'):
            if self.sheetname == '':
                raise IOError('Uncheck the [Excel Sheetname] !!!')

            else:
                pass

        else:
            pass

    # ==========================================================================
    def add_timestamp(self, timestamp):
        self.timestamp = timestamp
        self.time = datetime.now().strftime('%Y_%m%d_%H%M%S')
        if self.timestamp == 'prefix':
            self.filename = '{}_'.format(self.time) + self.filename

        elif self.timestamp == 'suffix':
            self.filename += '_{}'.format(self.time)

        else:
            raise IOError('Unexpected Error Occurred')

    # ==========================================================================
    def check_excel(self):
        if self.ext in ('xls', 'xlsx', 'xlsm'):
            return True
        else:
            return False

    # ==========================================================================
    def make_filepath(self):
        if self.ext == 'No Extension':
            self.file_path = '{}\{}'.format(self.dir_path, self.filename)
            self.filename_len = len(self.filename)

        else:
            self.file_path = '{}\{}.{}'.format(self.dir_path, self.filename, self.ext)
            self.filename_len = len(self.filename) + 1 + len(self.ext)

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
                if self.ext in ('xlsx', 'xls', 'xlsm'):
                    return 'excel'

                else:
                    pass

            else:
                raise IOError('Unexpected Error Occurred')

        else:
            pass

    # =========================================================================
    def add_n(self):
        self.count = 0
        if self.ext != 'No Extension':
            while os.path.exists(self.file_path) == True:
                self.filename = re.sub(r'\([0-9]+\)$', '', self.filename)
                self.count += 1
                self.filename += '({})'.format(self.count)
                self.file_path = '{}\{}.{}'.format(self.dir_path, self.filename, self.ext)

            else:
                self.filename_len = len(self.filename) + 1 + len(self.ext)

        else:
            while os.path.exists(self.file_path) == True:
                self.filename = re.sub(r'\([0-9]+\)$', '', self.filename)
                self.count += 1
                self.filename += '({})'.format(self.count)
                self.file_path = '{}\{}'.format(self.dir_path, self.filename)

            else:
                self.filename_len = len(self.filename) + 1 + len(self.ext)

    # ==========================================================================
    def word_count(self):
        if self.ext in ('xls', 'xlsx', 'xlsm'):
            if self.filename_len > 206:
                raise IOError('File name is too long !!!')

            elif self.filename_len > 255:
                raise IOError('File name is too long !!!')

            else:
                pass

    # ==========================================================================
    def path_len(self):
        if len(self.file_path) > 260:
            raise IOError('File Path is too long !!!')

        else:
            pass

    # ==========================================================================
    def createexcel(self):
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

    # ==========================================================================
    def createfile(self):
        self.create = pathlib.Path(self.file_path)
        self.create.touch()
        return sys.stdout.write(self.file_path)


################################################################################
@func_log
def create_newfile(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    nf = CreateFile(argspec.dir_path, argspec.filename, argspec.ext, argspec.other_ext)
    try:
        nf.check_ext_input()
        nf.check_dir_exist()
        nf.check_dir_path()
        nf.check_filename(argspec.validate)
        nf.check_extension()

        if argspec.sheetname:
            nf.check_sheetname(argspec.sheetname, argspec.sheet_len_opt)
        else:
            pass

        if argspec.timestamp in ('prefix', 'suffix'):
            nf.add_timestamp(argspec.timestamp)
        elif argspec.timestamp == 'None':
            pass
        else:
            raise IOError('Unexpected Error Occurred')

        nf.make_filepath()

        if nf.file_exists_check(argspec.file_exists) == 'add_n':
            nf.add_n()
            nf.path_len()
            nf.word_count()

            if nf.check_excel() == True:
                nf.createexcel()
            else:
                nf.createfile()

        elif nf.file_exists_check(argspec.file_exists) == 'excel':
            nf.createfile()

        else:
            nf.path_len()
            nf.word_count()
            if nf.check_excel() == True:
                nf.createexcel()
            else:
                nf.createfile()

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
        group='6',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Create Newfile',
        icon_path=get_icon_path(__file__),
        description='Creating new empty file',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('dir_path',
                          display_name='Directory Path',
                          input_method='folderread',
                          help='Where you want to create')
        mcxt.add_argument('filename',
                          display_name='File Name',
                          help='File name you want')
        mcxt.add_argument('ext',
                          choices=['txt',
                                   'docx',
                                   'xlsx',
                                   'pptx',
                                   'csv',
                                   'log',
                                   'xml',
                                   'html',
                                   'INPUT [Other Extension(Adv)]',
                                   'No Extension'],
                          display_name='Extension',
                          help='Extension want to create')
        mcxt.add_argument('timestamp',
                          show_default=True,
                          display_name='Add Timestamp',
                          default='None',
                          choices=['None', 'prefix', 'suffix'],
                          help='Add timestamp to filename')
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
        mcxt.add_argument('--other_ext',
                          display_name='Other Extension',
                          help='Input here, if you want to use other extension')
        mcxt.add_argument('--sheetname',
                          display_name='Excel Sheetname',
                          help='Sheetname in the case of Excel')
        mcxt.add_argument('--sheet_len_opt',
                          display_name='Sheetname Length Option',
                          default='Return Failure',
                          choices=['Return Failure', 'Cut to 31 char'],
                          help='If Use [Sheetname], when the sheetname exceeds 31 characters')

        argspec = mcxt.parse_args(args)
        return create_newfile(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass