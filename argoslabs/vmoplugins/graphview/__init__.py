#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.vmoplugins.graphview`
====================================
.. moduleauthor:: binhvmodev <binh.ha@vmodev.com>
Description
===========
VMO plugin module sample
"""
# Authors
# ===========
#
# * Binh
#
# Change Log
# --------
#
#  * [2021/04/05]
#     - starting

################################################################################

import sys
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from random import randint
from os import path
################################################################################
graph_type = {
    'sc': 'scatter',
    'ba': 'bar',
    'li': 'line',
    'ca': 'catplot',
}

################################################################################

@func_log
def do_seaborn(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    sns.set_style("darkgrid")
    try:
        input_file = os.path.abspath(argspec.input_file)
        # ##################################### open csv file
        csv_file = pd.read_csv(input_file, index_col=0)
        column_name = list(csv_file.columns)

        if argspec.graph == 'line':
            sns.lineplot(x=column_name[0], y=column_name[1], data=csv_file)
        if argspec.graph == 'scatter':
            sns.scatterplot(x=column_name[0], y=column_name[1], data=csv_file)
        if argspec.graph == 'bar':
            sns.barplot(x=column_name[0], y=column_name[1], data=csv_file)
        if argspec.graph == 'cat':
            sns.catplot(x=column_name[0], y=column_name[1], data=csv_file, kind="boxen")

        # ##################################### save file to folder
        output_file = argspec.output + 'photo-%s-%06d.png' % (argspec.graph,randint(1, 999999))
        if os.path.exists(output_file):
            os.remove(output_file)
        plt.savefig(output_file)
        print(os.path.abspath(output_file), end='')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg,os.linesep))
        return 9
    finally:
        sys.stdout.flush()
        # ##################################### print filepath and save to variable

    mcxt.logger.info('>>>end...')

################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='test',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='plotImage',
        icon_path=get_icon_path(__file__),
        description='generate image from csv file',
    ) as mcxt:
        mcxt.add_argument('graph', default='line',
                          display_name='choose graph view',
                          choices=list(graph_type.values()),
                          help='graph view to show(bar,line,etc)')
        mcxt.add_argument('input_file',
                            display_name='input path',
                            input_method='fileread',
                            help="input csv file", metavar="FILE")
        mcxt.add_argument('--data_range',
                            display_name='data range',
                            help="input data range")
        mcxt.add_argument('--data_value',
                            display_name='data value',
                            help="input data value")
        mcxt.add_argument('output',
                          display_name='output path',
                          action='store',
                          input_method='folderread',
                          help='folder to store image')
        # ##################################### for app dependent parameters
        argspec = mcxt.parse_args(args)
        return do_seaborn(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
