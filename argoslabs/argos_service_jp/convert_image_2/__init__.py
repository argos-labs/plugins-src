#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.convert_image_2`
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
#  * [2021/01/09]
#     Create

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from PIL import Image, ImageSequence
import mimetypes
import pathvalidate
import re

################################################################################
class Conv_Img(object):

    # ==========================================================================
    def __init__(self, ori_file_path, dir_path, aft_file_type, validate, file_exists):
        self.ori_file_path = ori_file_path
        self.dir_path = dir_path
        self.aft_file_type = aft_file_type

        self.mime = None

        self.ori_file_name = None
        self.ori_split_name = None
        self.ori_basename = None
        self.ori_ext = None

        self.validate = validate

        self.aft_file_name = None
        self.aft_split_name = None
        self.aft_basename = None
        self.aft_ext = None

        self.aft_file_path = None
        self.file_exists = file_exists
        self.count = None

        self.img = None
        self.bg = None
        self.tif_page_count = None
        self.tif_data = None

    # ==========================================================================
    def check_file_exists(self):
        if not os.path.isfile(self.ori_file_path):
            raise IOError('File {} not found'.format(self.ori_file_path))

        else:
            pass

    # ==========================================================================
    def file_type_check(self):
        self.mime = mimetypes.guess_type(self.ori_file_path)[0]
        if self.mime != None:
            if self.mime == 'image/jpeg':
                return 'jpg'
            elif self.mime == 'image/jpx':  # JEPG2000
                return 'jpx'
            elif self.mime == 'image/png':
                return 'png'
            elif self.mime == 'image/gif':
                return 'gif'
            elif self.mime == 'image/tiff':
                return 'tif'
            elif self.mime == 'image/bmp':
                return 'bmp'
            elif self.mime.startswith('image/') == True:
                return 'another'

            else:
                raise IOError('Cannot handle this filetype!')

        elif os.path.splitext(self.ori_file_path)[1] == '.webp':
            return 'another'

        else:
            raise IOError('Cannot handle this filetype!')

    # ==========================================================================
    def file_name_split(self):
        self.ori_file_name = os.path.basename(self.ori_file_path)
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
    def file_type_check_by_ext(self):
        if self.ori_ext in ('jpg', 'jpeg', 'jpe', 'jfif', 'jfi'):
            return 'jpg'
        elif self.ori_ext in ('jp2', 'j2k', 'jpx'):
            return 'jpx'
        elif self.ori_ext == 'png':
            return 'png'
        elif self.ori_ext == 'gif':
            return 'gif'
        elif self.ori_ext in ('tif', 'tiff'):
            return 'tif'
        elif self.ori_ext in ('bmp', 'dib'):
            return 'bmp'

        elif self.ori_ext in ('webp', 'eps', 'ico', 'pcx', 'ppm', 'sgi', 'tga', 'xbm'):
            return 'another'

        else:
            raise IOError('Cannot handle this filetype!')

    # ==========================================================================
    def check_dir_exists(self):
        if not os.path.isdir(self.dir_path):
            raise IOError('Directory {} not found'.format(self.dir_path))

        else:
            self.dir_path = os.path.abspath(self.dir_path)

    # ==========================================================================
    def check_dir_path(self):
        if self.dir_path[-1] == os.sep:
            self.dir_path = self.dir_path[:-1]

        else:
            pass

    # File Name should be inherited from the original
    # ==========================================================================
    def check_filename(self, aft_file_name):
        self.aft_file_name = aft_file_name
        if pathvalidate.is_valid_filename(self.aft_file_name) == False:
            if self.validate == 'Return Failure':
                raise IOError('Cannot use the File Name')

            elif self.validate == 'Sanitize':
                self.aft_file_name = pathvalidate.sanitize_filename(
                    self.aft_file_name)

            else:
                pass

        elif self.aft_file_name == '':
            raise IOError('Input \"File Name\" field !!!')

        elif pathvalidate.is_valid_filename(self.aft_file_name) == True:
            pass

        else:
            raise IOError('Unexpected Error Occurred')

    # ==========================================================================
    def make_filepath(self):
        # If use another file type, edit here.
        if self.aft_file_type == 'PNG':
            self.aft_file_type = 'png'
        elif self.aft_file_type == 'JPEG':
            self.aft_file_type = 'jpg'
        elif self.aft_file_type == 'BMP':
            self.aft_file_type = 'bmp'
        elif self.aft_file_type == 'GIF':
            self.aft_file_type = 'gif'

        self.aft_split_name = self.aft_file_name.rsplit('.', 1)
        self.aft_basename = self.aft_split_name[0]
        if len(self.aft_split_name) == 1:
            pass

        else:
            self.aft_file_name = self.aft_basename
            self.aft_ext = self.aft_split_name[1]

            if str.upper(self.aft_ext) == 'PNG':
                self.aft_file_type = 'png'
            elif str.upper(self.aft_ext) in ('JPG', 'JPEG'):
                self.aft_file_type = 'jpg'
            elif str.upper(self.aft_ext) == 'BMP':
                self.aft_file_type = 'bmp'
            elif str.upper(self.aft_ext) == 'GIF':
                self.aft_file_type = 'gif'
            elif str.upper(self.aft_ext) in ('DIB',
                                             'EPS',
                                             'ICO',
                                             'JP2', 'JPX',
                                             'PCX',
                                             'PPM',
                                             'SGI',
                                             'TGA',
                                             'WEBP',
                                             'XBM'):
                self.aft_file_type = str.lower(self.aft_ext)
            else:
                raise IOError('Cannot use the extension!')

    # File Exists Check
    # ==========================================================================
    def file_exists_check(self):
        self.aft_file_path = '{}/{}.{}'.format(self.dir_path,
                                               self.aft_file_name,
                                               self.aft_file_type)
        if os.path.exists(self.aft_file_path):
            if self.file_exists == 'Return Failure':
                raise IOError('File is already exists!')

            elif self.file_exists == 'Overwrite':
                os.remove(self.aft_file_path)

            elif self.file_exists == 'Add (n) at End':
                self.count = 0
                while os.path.exists(self.aft_file_path) == True:
                    self.aft_file_name = re.sub(r'\([0-9]+\)$', '',
                                                self.aft_file_name)
                    self.count += 1
                    self.aft_file_name += '({})'.format(self.count)
                    self.aft_file_path = '{}\{}.{}'.format(self.dir_path,
                                                              self.aft_file_name,
                                                              self.aft_file_type)
                else:
                    pass

            else:
                raise IOError('Unexpected Error Occurred')

        else:
            pass

    # ==========================================================================
    def convert(self):
        with Image.open(self.ori_file_path) as self.img:
            if self.aft_file_type == 'jpg':
                if self.img.getbands() == ('R', 'G', 'B', 'A'):
                    self.img.load()
                    self.bg = Image.new("RGB", self.img.size, (255, 255, 255))
                    self.bg.paste(self.img, mask=self.img.split()[3])
                    self.bg.save('{}/{}.{}'.format(self.dir_path,
                                                   self.aft_file_name,
                                                   self.aft_file_type))
                else:
                    self.img.save('{}/{}.{}'.format(self.dir_path,
                                                    self.aft_file_name,
                                                    self.aft_file_type))

            else:
                self.img.save('{}/{}.{}'.format(self.dir_path,
                                                self.aft_file_name,
                                                self.aft_file_type))

        print('{}/{}.{}'.format(self.dir_path,
                                self.aft_file_name,
                                self.aft_file_type), end="")

    # ==========================================================================
    def check_tif(self):
        with Image.open(self.ori_file_path) as self.img:
            self.tif_page_count = self.img.n_frames
            if self.tif_page_count == 1:
                return 'single'
            elif self.tif_page_count > 1:
                return 'multi'
            else:
                raise IOError('Cannot deal with the TIFF file!')

    # ==========================================================================
    def convert_tif(self):
        with Image.open(self.ori_file_path) as self.tif_data:
            for i, page in enumerate(ImageSequence.Iterator(self.tif_data)):

                if self.aft_file_type == 'jpg':
                    page = page.convert("RGB")

                # File Exists Check ============================================
                self.aft_file_path = '{}/{}_{}.{}'.format(self.dir_path,
                                                          self.aft_file_name,
                                                          i,
                                                          self.aft_file_type)
                if os.path.exists(self.aft_file_path):
                    if self.file_exists == 'Return Failure':
                        raise IOError('File is already exists!')

                    elif self.file_exists == 'Overwrite':
                        os.remove(self.aft_file_path)

                    elif self.file_exists == 'Add (n) at End':
                        self.count = 0
                        while os.path.exists(self.aft_file_path) == True:
                            self.aft_file_name = re.sub(r'\([0-9]+\)$', '',
                                                        self.aft_file_name)
                            self.count += 1
                            self.aft_file_name += '({})'.format(self.count)
                            self.aft_file_path = '{}\{}_{}.{}'.format(self.dir_path,
                                                                      self.aft_file_name,
                                                                      i,
                                                                      self.aft_file_type)
                        else:
                            pass

                    else:
                        raise IOError('Unexpected Error Occurred')

                else:
                    pass
                # ==============================================================

                page.save('{}/{}_{}.{}'.format(self.dir_path,
                                               self.aft_file_name,
                                               i,
                                               self.aft_file_type))

                print('{}/{}_{}.{}'.format(self.dir_path,
                                           self.aft_file_name,
                                           i,
                                           self.aft_file_type))

################################################################################
@func_log
def convert_img(mcxt, argspec):

    mcxt.logger.info('>>>starting...')
    try:
        CI = Conv_Img(argspec.ori_file_path,
                      argspec.dir_path,
                      argspec.aft_file_type,
                      argspec.validate,
                      argspec.file_exists)

        CI.check_dir_exists()

        file_type = CI.file_type_check()
        CI.file_name_split()

        CI.check_dir_exists()
        CI.check_dir_path()

        if argspec.aft_file_name:
            CI.check_filename(argspec.aft_file_name)
        else:
            pass

        CI.make_filepath()

        if file_type in ('jpg', 'jpx', 'png', 'gif', 'bmp'):
            CI.file_exists_check()
            CI.convert()

        elif file_type == 'tif':
            tif = CI.check_tif()
            if tif == 'single':
                CI.file_exists_check()
                CI.convert()
            elif tif == 'multi':
                CI.check_tif()
                CI.convert_tif()

        elif file_type == 'another':
            CI.file_exists_check()
            CI.convert()

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
        display_name='Convert Image II',
        icon_path=get_icon_path(__file__),
        description='Converts the image format',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('ori_file_path',
                          display_name='File Path',
                          input_method='fileread',
                          help='Select your image file')
        mcxt.add_argument('dir_path',
                          display_name='Output Dir Path',
                          input_method='folderread',
                          help='Where you want to create')
        mcxt.add_argument('aft_file_type',
                          display_name='Output File Type',
                          default='PNG',
                          choices=['PNG', 'JPEG', 'BMP', 'GIF'])

        # ######################################## for app dependent options
        # File Name should be inherited from the original
        mcxt.add_argument('--aft_file_name',
                          display_name='Out File Name',
                          show_default=True,
                          help='File Name you want')
        mcxt.add_argument('--validate',
                          display_name='File Name Validation',
                          show_default=True,
                          default='Return Failure',
                          choices=['Return Failure', 'Sanitize'])
        mcxt.add_argument('--file_exists',
                          display_name='If File Exists',
                          default='Add (n) at End',
                          show_default=True,
                          choices=['Add (n) at End',
                                   'Return Failure',
                                   'Overwrite'],
                          help='When the file already exists')

        argspec = mcxt.parse_args(args)
        return convert_img(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
