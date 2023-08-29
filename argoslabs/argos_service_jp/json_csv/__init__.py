#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.json_csv`
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
#  * [2021/02/16]
#     Create

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import json
import csv
# import pandas as pd
import pathvalidate
import re
# from pandas.io.json import json_normalize


################################################################################
class Convert_File(object):

    # ==========================================================================
    def __init__(self, op, path, dir, encoding, validate, file_exists):
        self.op = op
        self.path = os.path.abspath(path)
        self.dir = os.path.abspath(dir)

        self.ori_file_name = None
        self.ori_split_name = None
        self.ori_basename = None
        self.ori_ext = None

        self.aft_file_name = None
        self.aft_ext = None

        self.file_path = None
        self.count = None

        self.validate = validate
        self.file_exists = file_exists

        self.encoding = encoding

        self.data = None
        self.json_list = []

        self.key = None

    # ==========================================================================
    def select_op(self):
        if self.op == 'JSON2CSV':
            return 'json'
        elif self.op == 'CSV2JSON':
            return 'csv'
        else:
            raise IOError('Unexpected Error Occurred')

    # ==========================================================================
    def check_file_exists(self):
        if not os.path.isfile(self.path):
            raise IOError('File {} not found'.format(self.path))

        else:
            pass

    # ==========================================================================
    def file_name_split(self):
        self.ori_file_name = os.path.basename(self.path)
        self.ori_split_name = self.ori_file_name.rsplit('.', 1)
        self.ori_basename = self.ori_split_name[0]
        if len(self.ori_split_name) == 1:
            raise IOError('Cannot deal with the file!')
        else:
            self.ori_file_name = self.ori_basename
            self.ori_ext = self.ori_split_name[1]
            self.ori_ext = str.lower(self.ori_ext)

        self.aft_file_name = self.ori_file_name

    # ==========================================================================
    def file_type_check(self):
        if self.ori_ext == 'json':
            if self.op == 'JSON2CSV':
                self.aft_ext = 'csv'
            else:
                raise IOError('Please Select \"JSON2CSV\" Operation!!!')
        elif self.ori_ext == 'csv':
            if self.op == 'CSV2JSON':
                self.aft_ext = 'json'
            else:
                raise IOError('Please Select \"CSV2JSON\" Operation!!!')
        else:
            raise IOError('Cannot handle this file format!!!')

    # ==========================================================================
    def check_dir_exists(self):
        if not os.path.isdir(self.dir):
            raise IOError('Directory {} not found'.format(self.dir))

        else:
            pass

    # ==========================================================================
    def check_dir_path(self):
        if self.dir[-1] == os.sep:
            self.dir = self.dir[:-1]

        else:
            pass

    # ==========================================================================
    def check_filename(self, file_name):
        self.aft_file_name = file_name
        if pathvalidate.is_valid_filename(self.aft_file_name) == False:
            if self.validate == 'Return Failure':
                raise IOError('Cannot use the File Name')

            elif self.validate == 'Sanitize':
                self.aft_file_name = pathvalidate.sanitize_filename(self.aft_file_name)

            else:
                pass

        elif self.aft_file_name == '':
            raise IOError('Input \"File Name\" field !!!')

        elif pathvalidate.is_valid_filename(self.aft_file_name) == True:
            pass

        else:
            raise IOError('Unexpected Error Occurred')

    # ==========================================================================
    def make_file_path(self):
        self.file_path = "{}{}{}.{}".format(self.dir,
                                            os.path.sep,
                                            self.aft_file_name,
                                            self.aft_ext)

    # ==========================================================================
    def check_exists_file(self):
        if os.path.exists(self.file_path):
            if self.file_exists == 'Return Failure':
                raise IOError('File is already exists!')

            elif self.file_exists == 'Overwrite':
                os.remove(self.file_path)

            elif self.file_exists == 'Add (n) at End':
                self.count = 0
                while os.path.exists(self.file_path) == True:
                    self.aft_file_name = re.sub(r'\([0-9]+\)$', '',
                                                self.aft_file_name)
                    self.count += 1
                    self.aft_file_name += '({})'.format(self.count)
                    self.file_path = '{}{}{}.{}'.format(self.dir,
                                                        os.path.sep,
                                                        self.aft_file_name,
                                                        self.aft_ext)
                else:
                    pass

            else:
                raise IOError('Unexpected Error Occurred')

        else:
            pass

    # ==========================================================================
    def key_val_check(self, key):
        self.key = key
        if self.key == None:
            self.key = 0
        elif self.key == "":
            self.key = ""
        else:
            pass

    # ==========================================================================
    def json_2_csv(self):
        """
        self.data = pd.read_json(self.path, encoding=self.encoding)
        # self.df = pd.DataFrame.from_dict(self.data, orient='index').T
        self.data.to_csv(self.file_path,
                         encoding=self.encoding)
        """

        with open(self.path, "r", encoding=self.encoding) as f:
            self.data = json.load(f)
            if self.key != None:
                self.target_dicts = self.data[self.key]
            else:
                self.target_dicts = self.data

        with open(self.file_path, "w", encoding=self.encoding, newline="") as f:
            csv.register_dialect('dialect', doublequote=True, quoting=csv.QUOTE_ALL)
            self.writer = csv.DictWriter(f, fieldnames=self.target_dicts[0].keys(), dialect='dialect')
            self.writer.writeheader()
            for target_dict in self.target_dicts:
                self.writer.writerow(target_dict)

        print(self.file_path, end="")

    # ==========================================================================
    def csv_2_json(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            for row in csv.DictReader(f):
                self.json_list.append(row)

        with open(self.file_path, "w", encoding=self.encoding) as f:
            json.dump(self.json_list, f)

        print(self.file_path, end="")

################################################################################
@func_log
def convert(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        CF = Convert_File(argspec.op,
                          argspec.path,
                          argspec.dir,
                          argspec.encoding,
                          argspec.validate,
                          argspec.file_exists)

        CF.check_file_exists()
        CF.file_name_split()
        CF.file_type_check()
        CF.check_dir_exists()
        CF.check_dir_path()

        if argspec.file_name:
            CF.check_filename(argspec.file_name)

        CF.make_file_path()
        CF.check_exists_file()

        if argspec.key:
            CF.key_val_check(argspec.key)

        op = CF.select_op()
        if op == 'json':
            CF.json_2_csv()
        elif op == 'csv':
            CF.csv_2_json()
        else:
            pass

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
        display_name='JSON<->CSV',
        icon_path=get_icon_path(__file__),
        description='Convert JSON <-> CSV file plugin',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          default='JSON2CSV',
                          display_name='Operation',
                          choices=['JSON2CSV', 'CSV2JSON'],
                          help='Select Operation you want')
        mcxt.add_argument('path',
                          display_name='File Path',
                          input_method='fileread',
                          help='Select your json/csv file')
        mcxt.add_argument('dir',
                          display_name='Directory Path',
                          input_method='folderread',
                          help='Where you want to create')
        # ######################################## for app dependent options
        mcxt.add_argument('--key',
                          display_name='Nested Data Key',
                          show_default=True,
                          help='For nested JSON data, input the Key')
        mcxt.add_argument('--encoding',
                          display_name='File Encoding',
                          default='utf-8',
                          help='Select the encoding format of the file want to convert')
        mcxt.add_argument('--file_name',
                          display_name='File Name',
                          help='Input if you want to change the file name')
        mcxt.add_argument('--validate',
                          display_name='File Name Validation',
                          default='Return Failure',
                          choices=['Return Failure', 'Sanitize'])
        mcxt.add_argument('--file_exists',
                          display_name='If File Exists',
                          default='Add (n) at End',
                          choices=['Return Failure', 'Add (n) at End',
                                   'Overwrite'],
                          help='When the file already exists')

        argspec = mcxt.parse_args(args)
        return convert(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
