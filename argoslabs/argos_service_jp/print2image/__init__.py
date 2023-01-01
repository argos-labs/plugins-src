#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.print2image`
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
#  * [2020/10/23]
#     Create

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import shutil
import pathvalidate
import win32com.client
import comtypes
import comtypes.client
import excel2img
import random
import string
import re
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (PDFInfoNotInstalledError,
                                  PDFPageCountError,
                                  PDFSyntaxError)
from PIL import Image
from pathlib import Path

################################################################################
class Print2Image(object):

    # ==========================================================================
    def __init__(self, ori_file_path, dir_path, aft_file_type,
                 dpi, validate, file_exists, rm_nl, read_only):
        self.ori_file_path = os.path.abspath(ori_file_path)
        self.ori_split_name = None
        self.ori_file_name = None
        self.ori_basename = None
        self.ori_ext = None

        self.now_dir = os.path.abspath(os.path.dirname(__file__))
        self.random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.random_file = self.random_name + '.pdf'
        self.converted_pdf_path = os.path.join(self.now_dir, self.random_file)

        self.aft_file_path = None
        self.dir_path = dir_path
        self.aft_file_name = None
        self.aft_file_type = aft_file_type
        self.aft_split_name = None
        self.aft_basename = None
        self.aft_ext = None
        self.exl_png_path = None
        self.dpi = int(dpi)
        self.validate = validate

        self.file_exists = file_exists
        self.count = None

        poppler_dir = Path(__file__).parent.absolute() / 'poppler-0.68.0/bin'
        os.environ["PATH"] += os.pathsep + str(poppler_dir)

        self.rm_nl = rm_nl
        if read_only == 'True':
            self.read_only = True
        else:
            self.read_only = False

    # ==========================================================================
    def check_file_exists(self):
        if not os.path.isfile(self.ori_file_path):
            raise IOError('File {} not found'.format(self.ori_file_path))

        else:
            pass

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

    # Check the original file format
    # ==========================================================================
    def file_type_check(self):
        if self.ori_ext in ('doc', 'docx', 'docm', 'dot', 'dotm', 'dotx', 'odt'):
            return 'word'
        elif self.ori_ext in ('xls', 'xlsx', 'xlsm', 'xlsb', 'xlt', 'xltm', 'xltx', 'ods'):
            return 'excel'
        elif self.ori_ext in ('ppt', 'pptx', 'pptm', 'ppt', 'odp'):
            return 'powerpoint'
        elif self.ori_ext == 'pdf':
            return 'pdf'
        else:
            raise IOError('Cannot handle this file format!!!')

    # ==========================================================================
    def check_dir_exists(self):
        if not os.path.isdir(self.dir_path):
            raise IOError('Directory {} not found'.format(self.dir_path))

        else:
            pass

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
        elif self.aft_file_type == 'PDF':
            self.aft_file_type = 'pdf'

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
            elif str.upper(self.aft_ext) == 'PDF':
                self.aft_file_type = 'pdf'
            else:
                raise IOError('Cannot use the extension!')

    # ==========================================================================
    def check_pdf(self):
        if self.aft_file_type == 'pdf':
            return 'pdf'

        else:
            return 'img'

    # ==========================================================================
    def word_2_pdf(self):
        word = win32com.client.Dispatch("Word.Application")
        wdFormatPDF = 17

        doc = word.Documents.Open(str(self.ori_file_path), ReadOnly=self.read_only)

        try:
            doc.SaveAs(str(self.converted_pdf_path), FileFormat=wdFormatPDF)

        except Exception as e:
            print(e)

        finally:
            doc.Close()
            word.Quit()

        self.ori_file_path = self.converted_pdf_path
        return self.ori_file_path

    # ==========================================================================
    def excel_2_img(self):
        exl = win32com.client.Dispatch("Excel.Application")

        workbook = exl.Workbooks.Open(str(self.ori_file_path), ReadOnly=self.read_only)
        sheets = workbook.Worksheets

        try:
            if self.aft_file_type in ('png', 'bmp', 'gif'):
                for i, sheet in enumerate(sheets):
                    self.aft_file_path = '{}\{}_{}.{}'.format(self.dir_path,
                                                              self.aft_file_name,
                                                              i, self.aft_file_type)

                    # File Exists Check ========================================
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
                                                                      i, self.aft_file_type)
                            else:
                                pass

                        else:
                            raise IOError('Unexpected Error Occurred')

                    else:
                        pass

                    # ==========================================================
                    excel2img.export_img(self.ori_file_path, self.aft_file_path, sheet.name)
                    if self.rm_nl == 'OFF':
                        print(self.aft_file_path)
                    elif self.rm_nl == 'ON':
                        print(self.aft_file_path, end="")

            elif self.aft_file_type == 'jpg':
                for i, sheet in enumerate(sheets):
                    self.exl_png_path = '{}\{}_{}.png'.format(self.now_dir, self.random_name, i)
                    excel2img.export_img(self.ori_file_path, self.exl_png_path, sheet.name)

                    self.aft_file_path = '{}\{}_{}.jpg'.format(self.dir_path, self.aft_file_name, i)

                    # File Exists Check ========================================
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
                                self.aft_file_path = '{}\{}_{}.{}'.format(
                                    self.dir_path,
                                    self.aft_file_name,
                                    i, self.aft_file_type)
                            else:
                                pass

                        else:
                            raise IOError('Unexpected Error Occurred')

                    else:
                        pass
                    # ==========================================================

                    conv_img = Image.open(self.exl_png_path)
                    conv_img.save(self.aft_file_path)

                    os.remove(self.exl_png_path)
                    if self.rm_nl == 'OFF':
                        print(self.aft_file_path)
                    elif self.rm_nl == 'ON':
                        print(self.aft_file_path, end="")

        except Exception as e:
            print(e)

        finally:
            workbook.Close()
            exl.Quit()

    # ==========================================================================
    def excel_2_pdf(self):
        self.aft_file_path = '{}\{}.pdf'.format(self.dir_path, self.aft_file_name)

        # File Exists Check ====================================================
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
        # ======================================================================

        exl = win32com.client.Dispatch("Excel.Application")
        workbook = exl.Workbooks.Open(str(self.ori_file_path), ReadOnly=self.read_only)
        sheets = workbook.Worksheets

        try:
            sheets.Select()
            exl.ActiveSheet.ExportAsFixedFormat(0, self.aft_file_path, 0, True, True)

            if self.rm_nl == 'OFF':
                print(self.aft_file_path)
            elif self.rm_nl == 'ON':
                print(self.aft_file_path, end="")

        except Exception as e:
            print(e)

        finally:
            workbook.Close()
            exl.Quit()

    # ==========================================================================
    def pp_2_pdf(self):
        self.converted_pdf_path = os.path.abspath(self.converted_pdf_path)
        powerpoint = win32com.client.DispatchEx("Powerpoint.Application")
        powerpoint.Visible = True  # Do Not False

        presentation = powerpoint.Presentations.Open(str(self.ori_file_path), ReadOnly=True)

        try:
            presentation.Export(str(self.converted_pdf_path), FilterName="pdf")

        except Exception as e:
            print(e)

        finally:
            presentation.Close()
            powerpoint.Quit()

        self.ori_file_path = self.converted_pdf_path
        return self.ori_file_path

    # ==========================================================================
    def pp_2_pdf_sub(self):
        formatType = 32
        self.converted_pdf_path = os.path.abspath(self.converted_pdf_path)
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        powerpoint.Visible = 1

        presentation = powerpoint.Presentations.Open(self.ori_file_path, ReadOnly=self.read_only)

        try:
            presentation.SaveAs(self.converted_pdf_path, formatType)

        except Exception as e:
            print(e)

        finally:
            presentation.Close()
            powerpoint.Quit()

        self.ori_file_path = self.converted_pdf_path
        return self.ori_file_path

    # ==========================================================================
    def pdf_convert(self):
        images = convert_from_path(self.ori_file_path, self.dpi)
        for i, image in enumerate(images):
            self.aft_file_path = '{}\{}_{}.{}'.format(self.dir_path, self.aft_file_name,
                                                      i, self.aft_file_type)

            # File Exists Check ================================================
            if os.path.exists(self.aft_file_path):
                if self.file_exists == 'Return Failure':
                    raise IOError('File is already exists!')

                elif self.file_exists == 'Overwrite':
                    os.remove(self.aft_file_path)

                elif self.file_exists == 'Add (n) at End':
                    self.count = 0
                    while os.path.exists(self.aft_file_path) == True:
                        self.aft_file_name = re.sub(r'\([0-9]+\)$', '', self.aft_file_name)
                        self.count += 1
                        self.aft_file_name += '({})'.format(self.count)
                        self.aft_file_path = '{}\{}_{}.{}'.format(self.dir_path,
                                                                  self.aft_file_name,
                                                                  i, self.aft_file_type)
                    else:
                        pass

                else:
                    raise IOError('Unexpected Error Occurred')

            else:
                pass
            # ==================================================================

            image.save(self.aft_file_path)
            if self.rm_nl == 'OFF':
                print(self.aft_file_path)
            elif self.rm_nl == 'ON':
                print(self.aft_file_path, end="")

    # ==========================================================================
    def cp_dpf(self):
        self.aft_file_path = '{}\{}.pdf'.format(self.dir_path, self.aft_file_name)
        shutil.copy(self.ori_file_path, self.aft_file_path)

    # ==========================================================================
    def mv_pdf(self):
        self.aft_file_path = '{}\{}.pdf'.format(self.dir_path, self.aft_file_name)
        shutil.move(self.ori_file_path, self.aft_file_path)
        print(self.aft_file_path, end="")

    # ==========================================================================
    def del_converted_pdf(self):
        os.remove(self.converted_pdf_path)

################################################################################
@func_log
def print2image(mcxt, argspec):

    mcxt.logger.info('>>>starting...')
    try:
        pr_img = Print2Image(argspec.ori_file_path,
                             argspec.dir_path,
                             argspec.aft_file_type,
                             argspec.dpi,
                             argspec.validate,
                             argspec.file_exists,
                             argspec.rm_nl,
                             argspec.read_only)
        pr_img.check_file_exists()
        pr_img.file_name_split()

        f_ty = pr_img.file_type_check()

        pr_img.check_dir_exists()
        pr_img.check_dir_path()

        if argspec.aft_file_name:
            pr_img.check_filename(argspec.aft_file_name)
        else:
            pass
        pr_img.make_filepath()

        if pr_img.check_pdf() == 'img':
            if f_ty == 'pdf':
                pass

            elif f_ty == 'word':
                pr_img.word_2_pdf()

            elif f_ty == 'excel':
                pr_img.excel_2_img()
                mcxt.logger.info('>>>end...')
                return 0

            elif f_ty == 'powerpoint':
                pr_img.pp_2_pdf()

            else:
                pass

            pr_img.pdf_convert()

            if f_ty in ('word', 'excel', 'powerpoint'):
                pr_img.del_converted_pdf()

            mcxt.logger.info('>>>end...')
            return 0


        elif pr_img.check_pdf() == 'pdf':
            if f_ty == 'pdf':
                pr_img.cp_dpf()
                mcxt.logger.info('>>>end...')
                return 0

            elif f_ty == 'word':
                pr_img.word_2_pdf()

            elif f_ty == 'excel':
                pr_img.excel_2_pdf()
                mcxt.logger.info('>>>end...')
                return 0

            elif f_ty == 'powerpoint':
                pr_img.pp_2_pdf()

            else:
                pass

            pr_img.mv_pdf()

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
        display_name='Print 2 Image',
        icon_path=get_icon_path(__file__),
        description='Convert each document files to image files',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('ori_file_path',
                          display_name='File Path',
                          input_method='fileread',
                          help='Select your document file')
        mcxt.add_argument('dir_path',
                          display_name='Directory Path',
                          input_method='folderread',
                          help='Where you want to create')
        mcxt.add_argument('aft_file_type',
                          display_name='File Type',
                          default='PNG',
                          choices=['PNG', 'JPEG', 'BMP', 'GIF', 'PDF'])
        # ######################################## for app dependent options
        # File Name should be inherited from the original
        mcxt.add_argument('--aft_file_name',
                          display_name='File Name',
                          show_default=True,
                          help='File Name you want')
        mcxt.add_argument('--validate',
                          display_name='File Name Validation',
                          show_default=True,
                          default='Return Failure',
                          choices=['Return Failure', 'Sanitize'])
        mcxt.add_argument('--dpi',
                          display_name='DPI',
                          default='120')
        mcxt.add_argument('--file_exists',
                          display_name='If File Exists',
                          default='Add (n) at End',
                          show_default=True,
                          choices=['Return Failure', 'Add (n) at End',
                                   'Overwrite'],
                          help='When the file already exists')
        mcxt.add_argument('--rm_nl',
                          display_name='Remove end\'s \\n',
                          choices=['OFF', 'ON'],
                          default='OFF',
                          help='By default, \\n is automatically inserted at end')
        mcxt.add_argument('--read_only',
                          display_name='Read-Only',
                          choices=['True', 'False'],
                          default='True',
                          help="Open the file as Read-Only")

        argspec = mcxt.parse_args(args)
        return print2image(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
