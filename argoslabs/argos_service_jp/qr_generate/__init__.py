#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.qr_generate`
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
#  * [2020/10/12]
#     Create

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import pathvalidate
from chardet.universaldetector import UniversalDetector
import qrcode
from PIL import Image
import re

################################################################################
class Generate_QR(object):

    # ==========================================================================
    def __init__(self, dir_path, file_name, file_type, string, validate, fail_opt):
        self.dir_path = dir_path
        self.file_name = file_name
        self.file_path = None
        self.file_type = file_type
        self.from_file = None
        self.encoding = None
        self.string = string
        self.validate = validate
        self.fail_opt = fail_opt
        self.qr_data = None
        self.split_name = None
        self.basename = None
        self.ext = None
        self.file_exists = None
        self.box_size = None
        self.version = None
        self.err_cor_lev = None
        self.cell_color = None
        self.back_color = None
        self.img = None

    # ==========================================================================
    def check_dir_exists(self):
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
    def check_filename(self):
        if pathvalidate.is_valid_filename(self.file_name) == False:
            if self.validate == 'Return Failure':
                raise IOError('Cannot use the File Name')

            elif self.validate == 'Sanitize':
                self.file_name = pathvalidate.sanitize_filename(self.file_name)

            else:
                pass

        elif self.file_name == '':
            raise IOError('Input \"File Name\" field !!!')

        elif pathvalidate.is_valid_filename(self.file_name) == True:
            pass

        else:
            raise IOError('Unexpected Error Occurred')

    # ==========================================================================
    def string_from_file(self, from_file):
        self.from_file = from_file
        if not os.path.isfile(self.from_file):
            raise IOError('File {} is not found'.format(self.from_file))
        else:
            pass

        # Check encoding
        detector = UniversalDetector()
        with open(self.from_file, mode='rb') as f:
            for l in f:
                detector.feed(l)
                if detector.done:
                    break
        detector.close()

        self.encoding = detector.result['encoding']

        with open(self.from_file, mode='r', encoding=self.encoding) as f:
            self.string = f.read()

    # ==========================================================================
    def check_string(self):
        if self.string == '':
            if self.fail_opt == 'Return Failure':
                raise IOError('Input \"String to Generate\" Field!')
            elif self.fail_opt == 'Ignore Failure':
                print('Input \"String to Generate\" Field!')

        else:
            pass

    # ==========================================================================
    def make_filepath(self):
        # If use another file type, edit here.
        if self.file_type == 'PNG':
            self.file_type = 'png'
        elif self.file_type == 'JPEG':
            self.file_type = 'jpg'
        elif self.file_type == 'BMP':
            self.file_type = 'bmp'
        elif self.file_type == 'GIF':
            self.file_type = 'gif'

        self.split_name = self.file_name.rsplit('.', 1)
        self.basename = self.split_name[0]
        if len(self.split_name) == 1:
            pass

        else:
            self.file_name = self.basename
            self.ext = self.split_name[1]

            if str.upper(self.ext) == 'PNG':
                self.file_type = 'png'
            elif str.upper(self.ext) in ('JPG', 'JPEG'):
                self.file_type = 'jpg'
            elif str.upper(self.ext) == 'BMP':
                self.file_type = 'bmp'
            elif str.upper(self.ext) == 'GIF':
                self.file_type = 'gif'
            else:
                raise IOError('Please double-check the extension!')

        self.file_path = '{}\{}.{}'.format(self.dir_path, self.file_name, self.file_type)

    # ==========================================================================
    def file_exists_check(self, file_exists):
        self.file_exists = file_exists
        if os.path.exists(self.file_path):
            if self.file_exists == 'Return Failure':
                raise IOError('File is already exists!')

            elif self.file_exists == 'Overwrite':
                pass

            elif self.file_exists == 'Add (n) at End':
                return 'add_n'

            elif self.file_exists == 'Ignore Failure':
                print('File is already exists!')
                return 'ignore'

            else:
                raise IOError('Unexpected Error Occurred')

        else:
            pass

    # ==========================================================================
    def add_n(self):
        self.count = 0
        while os.path.exists(self.file_path) == True:
            self.file_name = re.sub(r'\([0-9]+\)$', '', self.file_name)
            self.count += 1
            self.file_name += '({})'.format(self.count)
            self.file_path = '{}\{}.{}'.format(self.dir_path, self.file_name, self.file_type)
        else:
            pass

    # ==========================================================================
    def path_len(self):
        if len(self.file_path) > 260:
            raise IOError('File Path is too long !!!')

        else:
            pass

    # ==========================================================================
    def option_input(self, box_size, version, err_cor_lev):
        if box_size == '':
            raise IOError('Input \"Cell Size\" Field !')
        else:
            self.box_size = int(box_size)

        self.version = int(version)

        self.err_cor_lev = err_cor_lev
        if self.err_cor_lev == 'L (7%)':
            self.err_cor_lev = qrcode.constants.ERROR_CORRECT_L
        elif self.err_cor_lev == 'M (15%)':
            self.err_cor_lev = qrcode.constants.ERROR_CORRECT_M
        elif self.err_cor_lev == 'Q (25%)':
            self.err_cor_lev = qrcode.constants.ERROR_CORRECT_Q
        elif self.err_cor_lev == 'H (30%)':
            self.err_cor_lev = qrcode.constants.ERROR_CORRECT_H

    # ==========================================================================
    def color_input(self, cell_color, back_color):
        if cell_color == '':
            raise IOError('Input \"Cell Color\" Field !')
        else:
            self.cell_color = cell_color

        if back_color == '':
            raise IOError('Input \"Background Color\" Field !')
        else:
            self.back_color = back_color

    # ==========================================================================
    def create_qr(self):
        self.qr_data = qrcode.QRCode(
            # QR-Code Options
            box_size=self.box_size,
            version=self.version,
            error_correction=self.err_cor_lev
        )
        self.qr_data.add_data(self.string)

        # Check the length of the string, if the QR-Code Version40
        """
        if sys.getsizeof(self.qr_data) > 3706:
            if self.fail_opt == 'Return Failure':
                raise IOError('The string may be too long!')
            elif self.fail_opt == 'Ignore Failure':
                print('The string may be too long!')
            else:
                raise IOError('Unexpected Error Occurred')
        else:
            pass
        """

        self.qr_data.make()

        self.img = self.qr_data.make_image(fill_color=self.cell_color,
                                           back_color=self.back_color)
        self.img.save(self.file_path)

        print(self.file_path)



################################################################################
@func_log
def generate_qr(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        qr = Generate_QR(argspec.dir_path,
                         argspec.file_name,
                         argspec.file_type,
                         argspec.string,
                         argspec.validate,
                         argspec.fail_opt)

        # File Operation
        qr.check_dir_exists()
        qr.check_dir_path()
        qr.check_filename()
        if not argspec.from_file == None:
            qr.string_from_file(argspec.from_file)
        else:
            pass
        qr.check_string()
        qr.make_filepath()
        f_ex = qr.file_exists_check(argspec.file_exists)
        if f_ex == 'add_n':
            qr.add_n()
        elif f_ex == 'ignore':
            mcxt.logger.info('>>>end...')
            return 0
        else:
            pass
        qr.path_len()

        # Option Operation
        qr.option_input(argspec.box_size, argspec.version, argspec.err_cor_lev)
        qr.color_input(argspec.cell_color, argspec.back_color)

        qr.create_qr()

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
        display_name='QR Generate',
        icon_path=get_icon_path(__file__),
        description='Generate QR-Code Plugin',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('dir_path',
                          display_name='Directory Path',
                          input_method='folderread',
                          help='Where you want to create')
        mcxt.add_argument('file_name',
                          display_name='File Name',
                          help='File Name you want')
        mcxt.add_argument('file_type',
                          display_name='File Type',
                          default='PNG',
                          choices=['PNG', 'JPEG', 'BMP', 'GIF'])
        mcxt.add_argument('string',
                          display_name='String to Generate',
                          help='Input the string you want to generate')
        # ######################################## for app dependent options
        mcxt.add_argument('--from_file',
                          display_name='String from File',
                          show_default=True,
                          input_method='fileread',
                          help='Instead of parameter using file as string')
        """
        # If need to choose an encoding format
        mcxt.add_argument('--file_encode',
                          display_name='File Encode',
                          default='Auto',
                          choices=['Auto', 'ascii', 'utf_8', 'euc_jp', 'shift_jis', 'cp932'],
                          help='Encoding format for using files')
        """
        mcxt.add_argument('--validate',
                          display_name='File Name Validation',
                          show_default=True,
                          default='Return Failure',
                          choices=['Return Failure', 'Sanitize'])
        mcxt.add_argument('--box_size',
                          display_name='Cell Size',
                          default='10',
                          help='Input the size of cells (px)')
        mcxt.add_argument('--version',
                          display_name='Version',
                          default='1',
                          choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                   '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                                   '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                                   '31', '32', '33', '34', '35', '36', '37', '38', '39', '40'],
                          help='Select the number of cells')
        mcxt.add_argument('--err_cor_lev',  # Error Correct Level
                          display_name='Error Correct Level',
                          default='H (30%)',
                          choices=['L (7%)', 'M (15%)', 'Q (25%)', 'H (30%)'],
                          help='Select the Error Correct Level')
        mcxt.add_argument('--cell_color',
                          display_name='Cell Color',
                          default='#000000',
                          help='Input a color name or code for the cell')
        mcxt.add_argument('--back_color',
                          display_name='Background Color',
                          default='#FFFFFF',
                          help='Input a color name or code for the background')
        mcxt.add_argument('--fail_opt',
                          display_name='Failure Option',
                          default='Return Failure',
                          show_default=True,
                          choices=['Return Failure', 'Ignore Failure'],
                          help='When this plugin fails, switches behavior')
        mcxt.add_argument('--file_exists',
                          display_name='If File Exists',
                          default='Return Failure',
                          show_default=True,
                          choices=['Return Failure', 'Add (n) at End',
                                   'Overwrite', 'Ignore Failure'],
                          help='When the file already exists')


        argspec = mcxt.parse_args(args)
        return generate_qr(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
