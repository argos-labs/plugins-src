#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.word2pdf`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Word to PDF plugin
"""
# Authors
# ===========
#
# * Kyobong An
#
# --------
#
#  * [2021/11/12]
#     - starting

################################################################################
import os
import sys
import win32com.client
from docx2pdf import convert
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class Doc2PDF(object):
    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.filename = argspec.filename
        if argspec.output:
            self.out_file = argspec.output
        else:
            self.out_file = self.get_output_file_path()
        if not os.path.exists(self.filename):
            raise IOError('Cannot read pdf file "%s"' % self.filename)
        if os.path.splitext(self.filename)[1] == '.doc':
            self.doc2pdf_convert()
        elif os.path.splitext(self.filename)[1] == '.docx':
            self.docx2pdf_convert()
        print(self.out_file)

    def get_output_file_path(self):
        return os.path.splitext(self.filename)[0] + '.pdf'

    def doc2pdf_convert(self):
        word = win32com.client.Dispatch('Word.Application')
        doc = word.Documents.Open(self.filename)
        doc.SaveAs(self.out_file, FileFormat=17)
        doc.Close()
        word.Quit()

    def docx2pdf_convert(self):
        convert(self.filename, self.out_file)


################################################################################
@func_log
def doc2pdf(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        Doc2PDF(argspec)
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99
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
            display_name='Word2PDF',
            icon_path=get_icon_path(__file__),
            description='Converting from pdf file to word file',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('filename', display_name='Doc/Docx File',
                          input_method='fileread',
                          help='Selece a doc or docx file')
        mcxt.add_argument('--output', show_default=True,
                          display_name='Output Filepath',
                          input_method='filewrite',
                          help='Specify an absolute file path to save the output')
        argspec = mcxt.parse_args(args)
        return doc2pdf(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
