#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.splitpdf`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Splitting and Merging PDF plugin
"""
# Authors
# ===========
#
# * Irene Cho
#
# --------
#
#  * [2020/12/01]
#     - starting

################################################################################
import os
import sys
import tempfile
from PyPDF2 import PdfFileReader, PdfFileMerger, PdfFileWriter
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import warnings

warnings.simplefilter("ignore", ResourceWarning)
################################################################################
@func_log
def pdf(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if argspec.folder and argspec.filename:
            lst = [argspec.folder + i for i in os.listdir(argspec.folder)]
            argspec.filename += lst
        elif not argspec.filename:
            argspec.filename = [argspec.folder+'/'+ i for i in os.listdir(argspec.folder)]
        if not argspec._output_folder and not argspec.output_file:
            argspec._output_folder = tempfile.mkdtemp()
        if argspec.op == 'Splitting':
            if not os.path.exists(argspec._output_folder):
                os.mkdir(argspec._output_folder)
            f = argspec.filename[0]
            if not os.path.exists(f):
                raise IOError('Cannot read pdf file "%s"' % f)
            pdf_ = PdfFileReader(f)
            fbasename = os.path.splitext(os.path.basename(f))[0]
            for p in range(pdf_.getNumPages()):
                pwriter = PdfFileWriter()
                pwriter.addPage(pdf_.getPage(p))
                out = f'{fbasename}_{p + 1}.pdf'
                output = os.path.join(argspec._output_folder, out)
                with open(output, 'wb') as o:
                    pwriter.write(o)
                o.close()
            print(os.path.abspath(argspec._output_folder), end='')
        else:
            pmerger = PdfFileMerger()
            for i in argspec.filename:
                if os.path.exists(i):
                    pmerger.append(i)
                else:
                    raise IOError(f'Cannot find the file: {i}')
            if argspec.output_file:
                output = argspec.output_file
            else:
                if not os.path.exists(argspec._output_folder):
                    os.mkdir(argspec._output_folder)
                output = os.path.join(argspec._output_folder, 'merged.pdf')
            with open(output, 'wb') as f:
                pmerger.write(f)
            f.close()
            print(os.path.abspath(output), end='')
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
            output_type='csv',
            display_name='PDF SplitMerge',
            icon_path=get_icon_path(__file__),
            description='Splitting or merging the pages of pdf files',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Operation Type',
                          choices=['Splitting', 'Merging'],
                          help='Choose the type of pdf operations')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--folder', display_name='PDF Folder',
                          input_method='folderread',  show_default=True,
                          help='An absolute folder path which saves the pdf file')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--filename', display_name='PDF File',
                          input_method='fileread', action='append', show_default=True,
                          help='Absolute file paths')
        # ##################################### for app optional parameters
        mcxt.add_argument('--output_folder', display_name='Output Folder',
                          input_method='folderwrite', help='An absolute output folder path')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--output_file', display_name='Filename for merge',
                          input_method='filewrite', help='An absolute output file path')
        argspec = mcxt.parse_args(args)
        return pdf(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
