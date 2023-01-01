#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.pdf2txt`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>, Kyobong Ahn <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS PDF Conversion(pdf -> txt) plugin
"""
# Authors
# ===========
#
# * Irene Cho
#
# --------
#
#  * [2021/07/20]
#     - updated from pypdf2 to pdfminer
#  * [2021/06/22]
#     - starting

################################################################################
import os
import csv
import sys
from io import StringIO
from pdfminer.converter import TextConverter,PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
@func_log
def pdf2doc(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        fn = argspec.filename
        output_string = StringIO()
        if not os.path.exists(fn):
            raise IOError('Cannot read pdf file "%s"' % fn)
        with open(fn, 'rb') as in_file:
            rsrcmgr = PDFResourceManager()
            dv = PDFPageAggregator(rsrcmgr, laparams=LAParams())
            interpreter0 = PDFPageInterpreter(rsrcmgr, dv)
            with StringIO() as outst:
                if argspec.coordinates:
                    outst.write('x0,y0,x1,y1,text')
                    outst.write('\n')
                for page in PDFPage.get_pages(in_file):
                    interpreter0.process_page(page)
                    layout = dv.get_result()
                    for ent in layout:
                        if isinstance(ent, LTTextBox):
                            x0,y0, x1,y1, text = round(ent.bbox[0],2),round(ent.bbox[1],2), \
                                               round(ent.bbox[2],2),\
                                               round(ent.bbox[3],2), ent.get_text()
                            if argspec.coordinates:
                                outst.write(f'{x0},{y0},{x1},{y1},{text}')
                            else:
                                outst.write(text)
                if not argspec.output:
                    argspec.output = fn[0:-4] + ".txt"
                with open(argspec.output, 'w', encoding='utf-8') as f:
                    f.write(outst.getvalue())
            f.close()
        print(os.path.abspath(argspec.output), end='')
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
            owner='ARGOS-LABS',
            group='2',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='PDF2TXT',
            icon_path=get_icon_path(__file__),
            description='Converting from pdf file to text file',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('filename', display_name='PDF File',
                          input_method='fileread', help = 'Select a pdf file')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--coordinates', display_name='Print Coordinates',
                          action='store_true', help = 'Print coordinates of text boxes')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--output', display_name='Output Filepath',
                          input_method='filewrite',
                          help = 'Specify an absolute file path to save the output')
        argspec = mcxt.parse_args(args)
        return pdf2doc(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass



