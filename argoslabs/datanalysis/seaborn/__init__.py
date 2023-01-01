#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.datanlaysis.seaborn`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Data Visualization Tool using Seaborn
"""
# Authors
# ===========
#
# * Kyobong An
#
# --------
#
#  * [2021/08/10]
#  라벨이나 타이틀의 폰트를 키우니까 짤리는 현상발견. subplots_adjust기능추가
#  * [2021/08/04]
#     - starting

################################################################################
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
# noinspection PyBroadException
class Seaborn(object):
    def __init__(self, argspec):
        self.argspec = argspec
        self.data = self.get_data(argspec.filename, argspec.sheet_name, argspec.encoding)
        self.xlabel = argspec.xlabel
        self.xfontsize = argspec.xfontsize
        self.xticks = argspec.xticks
        self.ylabel = argspec.ylabel
        self.yfontsize = argspec.yfontsize
        self.yticks = argspec.yticks
        self.title = argspec.title
        self.output = argspec.output
        self.plotdata = None

    # ==========================================================================
    @staticmethod
    def get_data(filename, sheet_name=None, encoding=None):
        if not os.path.exists(filename):
            raise IOError('Cannot read excel filename "%s"' % filename)
        ext = os.path.splitext(filename)[1]
        if ext.lower() in ('.csv', '.tsv'):
            df = pd.read_csv(filename, encoding=encoding)
        elif ext.lower() in ('.xls', '.xlsx'):
            if sheet_name:
                df = pd.read_excel(filename, sheet_name=sheet_name, engine='openpyxl')
            else:
                df = pd.read_excel(filename, engine='openpyxl')
        else:
            raise ReferenceError(
                f'Not supported file extension "{ext}" for input. '
                f'One of ".xls", ".xlsx", ".xlsm", ".csv", ".tsv"')
        return df

    def plot(self):
        if self.argspec.x == "":
            self.argspec.x = None
        if self.argspec.set_style:
            sns.set_theme(style=self.argspec.set_style)
        if self.argspec.palette:
            sns.set_palette(self.argspec.palette, self.argspec.n_colors, self.argspec.desat)
        if self.argspec.relational_plots:
            if self.argspec.relational_plots == 'relplot':
                s = sns.lineplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
            elif self.argspec.relational_plots == 'scatterplot':
                s = sns.scatterplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
            elif self.argspec.relational_plots == 'lineplot':
                s = sns.lineplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
        elif self.argspec.distribution_plots:
            if self.argspec.distribution_plots == 'displot':
                s = sns.displot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
            elif self.argspec.distribution_plots == 'histplot':
                s = sns.histplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
            elif self.argspec.distribution_plots == 'ecdfplot':
                s = sns.ecdfplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
            elif self.argspec.distribution_plots == 'rugplot':
                s = sns.rugplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
        elif self.argspec.categorical_plots:
            if self.argspec.categorical_plots == 'catplot':
                s = sns.catplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
            elif self.argspec.categorical_plots == 'stripplot':
                s = sns.stripplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
            elif self.argspec.categorical_plots == 'swarmplot':
                s = sns.swarmplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
            elif self.argspec.categorical_plots == 'boxplot':
                s = sns.boxplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
            elif self.argspec.categorical_plots == 'violinplot':
                s = sns.violinplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
            elif self.argspec.categorical_plots == 'boxenplot':
                s = sns.boxenplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
            elif self.argspec.categorical_plots == 'pointplot':
                s = sns.pointplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
            elif self.argspec.categorical_plots == 'barplot':
                s = sns.barplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
        elif self.argspec.regression_plots:
            if self.argspec.regression_plots == 'lmplot':
                s = sns.lmplot(x=self.argspec.x, y=self.argspec.y, data=self.data, hue=self.argspec.hue)
            elif self.argspec.regression_plots == 'regplot':
                s = sns.regplot(x=self.argspec.x, y=self.argspec.y, data=self.data)
            elif self.argspec.regression_plots == 'residplot':
                s = sns.residplot(x=self.argspec.x, y=self.argspec.y, data=self.data)

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
        if self.xlabel:
            plt.xlabel(self.xlabel, fontsize=self.xfontsize)
        if self.ylabel:
            plt.ylabel(self.ylabel, fontsize=self.yfontsize)

        plt.subplots_adjust(left=self.argspec.left,
                            right=self.argspec.right,
                            bottom=self.argspec.bottom,
                            top=self.argspec.top,)   # plot 주변의 공백 size
        #                     wspace=self.argspec.wspace,
        #                     hspace=self.argspec.hspace)  plot이 여러개일때 추가 할 옵션

        plt.title(self.title, fontsize=self.argspec.title_fontsize)
        if not self.output:
            self.output = os.path.dirname(self.argspec.filename) + '\\output.png'
        plt.savefig(self.output)
        print(self.output, end='')
        return 0


################################################################################
@func_log
def func(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        mat = Seaborn(argspec)
        mat.plot()

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
            display_name='Seaborn Plot',
            icon_path=get_icon_path(__file__),
            description='Data Visualization Tool using seaborn',
    ) as mcxt:
        # #####################################  for app dependent parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('filename', display_name='Excel File',
                          input_method='fileread',
                          help='Excel or CSV filename to handle for reading. '
                               '(Note. CSV is converted to excel first. Too big'
                               ' CSV input can take time.)')
        # ----------------------------------------------------------------------
        mcxt.add_argument('x', display_name='X axes', default=None,
                          help='Variables that specify positions on the x axes')
        # ######################################  for app optional parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('--y', display_name='Y axes', default=None, show_default=True,
                          help='Variables that specify positions on the y axes')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--relational-plots', show_default=True,
                          display_name='Relational plots',
                          choices=['relplot', 'scatterplot', 'lineplot'],
                          input_group='radio=Plot type;default',
                          help='Select the type Relational of plot')
        mcxt.add_argument('--distribution-plots', show_default=True,
                          display_name='Distribution plots',
                          choices=['displot', 'histplot', 'ecdfplot', 'rugplot'],
                          input_group='radio=Plot type',
                          help='Select the type of Distribution plot')
        mcxt.add_argument('--categorical-plots', show_default=True,
                          display_name='Categorical plots',
                          choices=['catplot', 'stripplot', 'swarmplot', 'boxplot', 'violinplot',
                                   'boxenplot', 'pointplot', 'barplot'],
                          input_group='radio=Plot type',
                          help='Select the type of Categorical plots plot')
        mcxt.add_argument('--regression-plots', show_default=True,
                          display_name='Regression plots',
                          choices=['lmplot', 'regplot', 'residplot'],
                          input_group='radio=Plot type',
                          help='Select the type of Categorical plots plot')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--output',
                          display_name='Output Path',
                          input_method='filewrite',
                          help='An absolute filepath to save a file')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--sheet-name',
                          default=None,
                          display_name='Sheet Name',
                          help='Choose sheet name.')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--hue',
                          default=None,
                          display_name='Hue',
                          help='Grouping variable that will produce elements with different colors.')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--title',
                          display_name='Plot Title',
                          help='Set the title of a plot')
        mcxt.add_argument('--title-fontsize', type=float,
                          display_name='Plot Title Fontsize',
                          help='Set the title fontsize of a plot')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--xlabel', display_name='X Label', default=None,
                          input_group='X axis',
                          help='Set X label in the plot')
        mcxt.add_argument('--xfontsize', display_name='X Fontsize', default=None,
                          input_group='X axis', type=float,
                          help='Set X label fontsize')
        mcxt.add_argument('--xticks', display_name='X Ticks',
                          input_group='X axis',
                          help='Set x axis tick labels of the grid. e.g. 1,100,10')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--ylabel', display_name='Y Label',
                          input_group='Y axis',
                          help='Set Y label in the plot')
        mcxt.add_argument('--yfontsize', display_name='Y Fontsize', default=None,
                          input_group='Y axis', type=float,
                          help='Set Y label fontsize')
        mcxt.add_argument('--yticks', display_name='Y Ticks',
                          input_group='Y axis',
                          help='Set y axis tick labels of the grid. 1,100,10')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--set-style', display_name='Plot Style',
                          choices=['darkgrid', 'whitegrid', 'dark', 'white', 'ticks'],
                          input_group='Style',
                          help='aesthetic style of the plots')
        mcxt.add_argument('--palette', display_name='Palette',
                          input_group='Style',
                          help='Enter a sequence color or palette.ex)"pastel","Bright","husl","Reds"')
        mcxt.add_argument('--n-colors', display_name='n_colors', default=None,
                          input_group='Style', type=int,
                          help='''Number of colors in the cycle.
                          The default number of colors will depend on the format of palette''')
        mcxt.add_argument('--desat', display_name='desat', default=None,
                          input_group='Style', type=float,
                          help='Proportion to desaturate each color by.')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--left', display_name='Left', default=None,
                          input_group='Subplots Adjust', type=float,
                          help='The position of the left edge of the subplots, as a fraction of the figure width.')
        mcxt.add_argument('--right', display_name='Right', default=None,
                          input_group='Subplots Adjust', type=float,
                          help='The position of the right edge of the subplots, as a fraction of the figure width.')
        mcxt.add_argument('--bottom', display_name='Bottom', default=None,
                          input_group='Subplots Adjust', type=float,
                          help='The position of the bottom edge of the subplots, as a fraction of the figure height.')
        mcxt.add_argument('--top', display_name='Top', default=None,
                          input_group='Subplots Adjust', type=float,
                          help='The position of the top edge of the subplots, as a fraction of the figure height.')
        # mcxt.add_argument('--wspace', display_name='Wspace', default=None,
        #                   input_group='Subplots Adjust', type=float,
        #                   help='The width of the padding between subplots, as a fraction of the average Axes width.')
        # mcxt.add_argument('--hspace', display_name='Hspace', default=None,
        #                   input_group='Subplots Adjust', type=float,
        #                   help='The height of the padding between subplots, as a fraction of the average Axes height.')
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
