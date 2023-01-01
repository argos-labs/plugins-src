#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.qr_read`
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
#  * [2020/10/02]
#     Create

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import mimetypes
from PIL import Image, ImageOps, ImageSequence
from pyzbar.pyzbar import decode
import random
import string


################################################################################
class Read_QR(object):

    # ==========================================================================
    def __init__(self, file_path, read_err_opt):
        self.file_path = file_path
        self.file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        self.mime = None
        self.type = None
        self.img = None
        self.color_data = None
        self.data = None
        self.decoded_data = None
        self.num = None
        self.string = None
        self.read_err_opt = read_err_opt

    # ==========================================================================
    def file_path_check(self):
        if not os.path.isfile(self.file_path):
            raise IOError('File {} not found'.format(self.file_path))

        else:
            pass

    # ==========================================================================
    def file_type_check(self):
        self.mime = mimetypes.guess_type(self.file_path)[0]
        if self.mime == 'image/jpeg':
            self.type = 'jpg'
            return 'jpg'
        elif self.mime == 'image/jpx':
            self.type = 'jpx'
            return 'jpx'
        elif self.mime == 'image/png':
            self.type = 'png'
            return 'png'
        elif self.mime == 'image/gif':
            self.type = 'gif'
            return 'gif'
        elif self.mime == 'image/tiff':
            self.type = 'tif'
            return 'tif'
        elif self.mime == 'image/bmp':
            self.type = 'bmp'
            return 'bmp'
        elif self.mime == 'application/pdf':
            self.type = 'pdf'
            raise IOError('Sorry, PDF is not available')

        else:
            raise IOError('Cannot handle this filetype!')

    # ==========================================================================
    def convert_img(self):
        if self.type in ('jpg', 'jpx', 'gif', 'bmp'):
            self.img = Image.open(self.file_path)
            while os.path.exists('./{}.png'.format(self.file_name)) == True:
                self.file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

            else:
                self.img.save('./{}.png'.format(self.file_name), 'png')
                self.color_data = Image.open('./{}.png'.format(self.file_name))

        elif self.type == 'png':
            self.color_data = Image.open(self.file_path)

        else:
            raise IOError('Unexpected Error Occurred')

    # ==========================================================================
    def convert_color(self):
        # Convert grayscale
        self.data = self.color_data.convert('L')
        self.data = self.color_data

    # ==========================================================================
    def read_string(self):
        self.decoded_data = decode(self.data)
        self.num = len(self.decoded_data)

        """
        # Code for debugging
        
        print(self.decoded_data)
        print(len(self.decoded_data))
        """

        if self.num == 0:
            # Invert Color
            self.data = ImageOps.invert(self.data.convert('RGB'))
            self.decoded_data = decode(self.data)
            self.num = len(self.decoded_data)

            if self.num == 0:

                if self.read_err_opt == 'Return Failure':
                    raise IOError('Cannot Read the QR-Code!')

                elif self.read_err_opt == 'Ignore Failure':
                    print('Cannot Read the QR-Code!')

                else:
                    raise IOError('Unexpected Error Occurred')

            else:
                for self.string in self.decoded_data:
                    print(self.string.data.decode('utf-8', 'ignore'))

        else:
            for self.string in self.decoded_data:
                print(self.string.data.decode('utf-8', 'ignore'))

    # ==========================================================================
    def del_file(self):
        if self.type in ('jpg', 'jpx', 'gif', 'bmp'):
            os.remove('./{}.png'.format(self.file_name))

        else:
            pass


################################################################################
class Tiff_Read(Read_QR):

    # ==========================================================================
    def __init__(self, file_path, read_err_opt):
        super().__init__(file_path, read_err_opt)
        self.tif_data = None

    # ==========================================================================
    def split_tiff(self):
        self.tif_data = Image.open(self.file_path)
        for i, page in enumerate(ImageSequence.Iterator(self.tif_data)):
            page.save('./{}_{}.png'.format(self.file_name, i), format='png', quality=95)

    # ==========================================================================
    def tif_read(self):
        for i, page in enumerate(ImageSequence.Iterator(self.tif_data)):
            self.color_data = Image.open('{}_{}.png'.format(self.file_name, i))
            super().convert_color()
            super().read_string()

    # ==========================================================================
    def del_tif(self):
        for i, page in enumerate(ImageSequence.Iterator(self.tif_data)):
            os.remove('./{}_{}.png'.format(self.file_name, i))


################################################################################
@func_log
def read_qr(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        qr = Read_QR(argspec.file_path, argspec.read_err_opt)

        qr.file_path_check()

        if qr.file_type_check() in ('jpg', 'jpx', 'png', 'gif', 'bmp'):
            qr.convert_img()
            qr.convert_color()

        elif qr.file_type_check() == 'tif':
            tr = Tiff_Read(argspec.file_path, argspec.read_err_opt)
            tr.split_tiff()
            tr.tif_read()
            tr.del_tif()

        else:
            pass


        if qr.file_type_check() in ('jpg', 'jpx', 'png', 'gif', 'bmp'):
            qr.read_string()
            qr.del_file()

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
        owner='ARGOS-SERVICE-JAPAN',
        group='2',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='QR Read',
        icon_path=get_icon_path(__file__),
        description='Read QR-Code Plugin',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('file_path',
                          display_name='File Path',
                          input_method='fileread',
                          help='Select your image file')
        # ######################################## for app dependent options
        mcxt.add_argument('--read_err_opt',
                          display_name='Reading Error',
                          default='Return Failure',
                          choices=['Return Failure', 'Ignore Failure'],
                          help='When reading error occurred, Return or Ignore Failure')

        argspec = mcxt.parse_args(args)
        return read_qr(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
