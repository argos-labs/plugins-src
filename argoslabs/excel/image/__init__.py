"""
====================================
 :mod:`argoslabs.excel.image`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS managing Ms Teams
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
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import win32com.client as client
import warnings
from PIL import ImageGrab


################################################################################
class Excel2image(object):
    # ==========================================================================
    FILE_TYPE = ['JPEG','PNG','GIF','BMP']


    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec


    # ==========================================================================
    def convert(self):
        if not self.argspec.file_path.endswith(".xlsx"):
            raise IOError('xlsx file only."%s"' % self.argspec.file_path)
        excel = client.Dispatch("Excel.Application")
        excel.DisplayAlerts = 0
        excel.Visible = False
        wb = excel.Workbooks.Open(self.argspec.file_path)
        try:
            ws = wb.Worksheets(self.argspec.sheetname)
            # lastRow = ws.UsedRange.Rows.Count
            # lastCol = ws.UsedRange.Columns.Count
            # ws.Range(ws.Cells(1, 1),ws.Cells(lastRow, lastCol)).Copy()
            ws.UsedRange.Rows.Cells.Copy()
            img = ImageGrab.grabclipboard()
            path_to_img = self.argspec.directory_path
            if self.argspec.filetype=='PNG':
                imgFile = os.path.join(path_to_img,
                                       f'{self.argspec.filename}.png')
                img.save(imgFile)
                print(imgFile, end='')
            elif self.argspec.filetype=='JPEG':
                imgFile = os.path.join(path_to_img,
                                       f'{self.argspec.filename}.jpg')
                img.save(imgFile)
                print(imgFile, end='')
            elif self.argspec.filetype=='BMP':
                imgFile = os.path.join(path_to_img,
                                       f'{self.argspec.filename}.bmp')
                img.save(imgFile)
                print(imgFile, end='')
            elif self.argspec.filetype=='GIF':
                imgFile = os.path.join(path_to_img,
                                       f'{self.argspec.filename}.gif')
                img.save(imgFile)
                print(imgFile, end='')
        except Exception as err:
            wb.Close()
            excel.Application.Quit()
            raise Exception(str(err))


################################################################################
@func_log
def reg_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        warnings.simplefilter("ignore", ResourceWarning)
        f = Excel2image(argspec)
        f.convert()
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
            owner='ARGOS-LABS-DEMO',
            group='9',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Excel2Image',
            icon_path=get_icon_path(__file__),
            description='convert Excel to image',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('file_path', display_name='File path',
                          input_method='fileread',
                          help='xlsx file path')
        # ----------------------------------------------------------------------
        mcxt.add_argument('directory_path', display_name='Directory Path',
                          help='Output Folder', input_method='folderread')
        # ##################################### for app optional parameters
        mcxt.add_argument('--filename', display_name='File Name',default='result',
                          help='File Name without extension and without space')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--sheetname', display_name='Sheet Name',default='Sheet1',
                          help='Sheet name default Sheet1')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--filetype', display_name='FILE TYPE',
                          choices=Excel2image.FILE_TYPE,
                          default='JPEG',
                          help='Output File Type')
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
