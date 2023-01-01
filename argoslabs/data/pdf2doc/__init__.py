#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.pdf2doc`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS PDF to Word plugin
"""
# Authors
# ===========
#
# * Irene Cho
#
# --------
#
#  * [2020/05/21]
#     - starting

################################################################################
import os
import sys
import win32com.client
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class pdf2docAPI(object):
    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.filename = argspec.filename
        self.out_file = self.argspec.output
        if not os.path.exists(self.filename):
            raise IOError('Cannot read pdf file "%s"' % self.filename)

    # ==========================================================================
    def pdf2doc(self):
        try:
            word = win32com.client.Dispatch("Word.Application")
        except Exception as err:
            return str(err)
        word.visible = 0
        wb = word.Documents.Open(self.filename)
        if not self.out_file:
            self.out_file = self.filename[0:-4] + ".docx"
        wb.SaveAs2(self.out_file, FileFormat=16)
        wb.Close()
        word.Quit()
        print(self.out_file,end='')

################################################################################
@func_log
def pdf2doc(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        f = pdf2docAPI(argspec)
        f.pdf2doc()
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
            display_name='PDF2Doc',
            icon_path=get_icon_path(__file__),
            description='Converting from pdf file to word file',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('filename', display_name='PDF File',
                          input_method='fileread', help = 'Selece a pdf file')
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
