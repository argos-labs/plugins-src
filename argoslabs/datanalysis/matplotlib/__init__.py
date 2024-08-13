#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.datanlaysis.matplotlib`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Data Visualization Tool using Matplotlib
"""
# Authors
# ===========
#
# * Irene Cho
#
# --------
#  * [2024/06/24]
#     - numpy 버전 수정
#
#  * [2021/03/30]
#     - starting

################################################################################
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
# noinspection PyBroadException
class matplot(object):
    def __init__(self, argspec):
        self.argspec = argspec
        self.filename = argspec.filename
        if not os.path.exists(self.filename):
            raise IOError('Cannot read excel filename "%s"' % self.filename)
        self.xcol = argspec.pd_xcol
        self.ycol = argspec.pd_ycol
        self.output = argspec.output
        self.figsize = argspec.figsize

    # ==========================================================================
    def get_plot(self):
        f = self.argspec.filename
        _, ext = os.path.splitext(f)
        xlst, ylst = None, None
        h = 0
        if self.argspec.no_header:
            h = None
        if ext.lower() in ('.csv', '.tsv'):
            df = pd.read_csv(f, header=h,
                             encoding=self.argspec.encoding)
        elif ext.lower() in ('.xls', '.xlsx'):
            df = pd.read_excel(self.argspec.filename, header=h,
                               sheet_name=self.argspec.sheet_name)
        else:
            raise ReferenceError(
                f'Not supported file extension "{ext}" for input. '
                f'One of ".xls", ".xlsx", ".xlsm", ".csv", ".tsv"')
        if h != 0:  # non-header
            try:
                xlst = df[int(self.xcol)]
                if self.ycol:
                    ylst = df[int(self.argspec.pd_ycol)]
            except Exception:
                raise ReferenceError("Cannot find the index number")
        else:
            try:
                xlst = eval('df.' + self.xcol)
                if self.ycol:
                    ylst = eval('df.' + self.ycol)
            except Exception:
                raise ReferenceError("Cannot find the column name and ranges")
        label = self.argspec.plot_label
        if self.figsize:
            s = self.figsize.split(',')
            if len(s) != 2:
                raise RuntimeError('Check out the format of Plot Size e.g.10,10')
            plt.figure(figsize=(int(s[0]), int(s[1])))
        if self.argspec.plotype == 'Scatter':
            if self.argspec.size:
                s = float(self.argspec.size)
            else:
                s = self.argspec.size
            plt.scatter(xlst, ylst, s=s, label=label)
        elif self.argspec.plotype == 'Linear':
            xlst = np.array(xlst)
            ylst = np.array(ylst)
            plt.plot(xlst, ylst, label=label)

        elif self.argspec.plotype == 'Bar':
            plt.bar(xlst, ylst, label=label)
        elif self.argspec.plotype == 'Pie':
            plt.pie(xlst, autopct='%1.1f%%', labels=self.argspec.pie_label)
        if label or self.argspec.pie_label:
            plt.legend()
        if self.argspec.xticks:
            t = self.argspec.xticks.split(',')
            if len(t) != 3:
                raise RuntimeError(
                    'Check out the format of X Ticks e.g. 0,100,10')
            plt.xticks(range(int(t[0]), int(t[1]), int(t[2])))
        if self.argspec.yticks:
            t = self.argspec.yticks.split(',')
            if len(t) != 3:
                raise RuntimeError(
                    'Check out the format of Y Ticks e.g. 0,100,10')
            plt.yticks(range(int(t[0]), int(t[1]), int(t[2])))
        plt.xlabel(self.argspec.xlabel)
        plt.ylabel(self.argspec.ylabel)
        plt.title(self.argspec.title)
        if not self.output:
            self.output = os.path.dirname(self.filename) + 'output.png'
        plt.savefig(self.output)
        print(self.output, end='')
        return 0


################################################################################
@func_log
def func(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        mat = matplot(argspec)
        mat.get_plot()
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
            group='4',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Data Plot1',
            icon_path=get_icon_path(__file__),
            description='Data Visualization Tool using matplotlib',
    ) as mcxt:
        # #####################################  for app dependent parameters
        mcxt.add_argument('plotype', display_name='Plot Type',
                          choices=['Scatter', 'Linear', 'Bar', 'Pie'],
                          help='Select the type of plot')
        # ----------------------------------------------------------------------
        mcxt.add_argument('filename', display_name='Excel File',
                          input_method='fileread',
                          help='Excel or CSV filename to handle for reading. '
                               '(Note. CSV is converted to excel first. Too big'
                               ' CSV input can take time.)')
        # ----------------------------------------------------------------------
        mcxt.add_argument('pd_xcol', display_name='X Col[Range]',
                          help='range of the csv')
        # ######################################  for app optional parameters
        mcxt.add_argument('--pd_ycol', display_name='Y Col[Range]',
                          help='range of the csv', show_default=True)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--no_header', display_name='No Header',
                          action='store_true',
                          help='None for no header')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--sheet-name',
                          display_name='Sheet Name',
                          default=0,
                          help='Choose sheet name or index (0-indexed) for input. None for all sheets')
        # ------------------------------ ----------------------------------------
        mcxt.add_argument('--xlabel', display_name='X Label',
                          help='Set X label in the plot')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--ylabel', display_name='Y Label',
                          help='Set Y label in the plot')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--xticks', display_name='X Ticks',
                          help='Set X ticks e.g. 1,100,10')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--yticks', display_name='Y Ticks',
                          help='Set Y ticks e.g. 1,100,10')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--size', display_name='Scatter Points Size',
                          help='Set the size of the data points in a scatter plot')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--title', display_name='Plot Title',
                          help='Set the title of a plot')
        # ------------------------------ ----------------------------------------
        mcxt.add_argument('--figsize', display_name='Plot Size',
                          help='Set the figure size by inch e.g. 5,5')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--plot_label', display_name='Data Label',
                          help='Label of the plot')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--pie_label', display_name='Pie Chart Labels',
                          action='append',
                          help='Label of the pie chart')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--output', display_name='Output Path',
                          input_method='filewrite',
                          help='An absolute filepath to save a file')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--encoding',
                          default='utf-8',
                          display_name='Encoding',
                          help='Encoding for CSV file, default is [[utf-8]]')
        argspec = mcxt.parse_args(args)
        return func(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
