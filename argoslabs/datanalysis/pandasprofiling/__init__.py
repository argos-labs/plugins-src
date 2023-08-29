"""
====================================
 :mod:`argoslabs.datanalysis.pandasprofiling`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS data analysis using PANDAS profiling
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2023/07/24] Kyobong
#     - "Select Range" 메소드 display_name 오류 변경
#  * [2021/04/06]
#     - 그룹에 "4-Data Science" 넣음
#  * [2020/05/07]
#     - title, html_style 추가
#  * [2020/04/30]
#     - profiling에서 중간 프로세싱 결과가 stderr로 출력되는 것을 별도 처리
#  * [2020/04/27]
#     - pandas_safe_eval 함수 추가
#  * [2020/04/26]
#     - starting

################################################################################
import os
import sys
import shutil
# for tkinter
# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    import tkinter as tk
except Exception:
    # sys.path.append(os.path.dirname(__file__))
    os.environ['MPLBACKEND'] = 'agg'
import warnings
import tempfile
# noinspection PyUnresolvedReferences,PyPackageRequirements
import numpy as np
# noinspection PyPackageRequirements
import pandas as pd
import pandas_profiling as pp
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
def pandas_safe_eval(es):
    # noinspection PyBroadException
    try:
        if not es:
            return None
        r = eval(es)
        return r
    except Exception:
        return es


################################################################################
@func_log
def do_pandasprofiling(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    saved_stderr = None
    tmpdir = tempfile.mkdtemp(prefix='pandas_profiling_')
    try:
        # warnings.warn("deprecated", DeprecationWarning)
        warnings.simplefilter("ignore")
        # 1) READ in_file
        if not os.path.exists(argspec.in_file):
            raise IOError(f'Cannot read file "{argspec.in_file}"')

        sheet_name = pandas_safe_eval(argspec.sheet_name)
        header = pandas_safe_eval(argspec.header)
        index_col = pandas_safe_eval(argspec.index_col)
        usecols = pandas_safe_eval(argspec.usecols)
        dtype = pandas_safe_eval(argspec.dtype)

        _, ext = os.path.splitext(argspec.in_file)
        if ext.lower() in ('.xls', '.xlsx'):
            df = pd.read_excel(argspec.in_file, sheet_name=sheet_name,
                               header=header, index_col=index_col,
                               usecols=usecols, dtype=dtype,
                               encoding=argspec.encoding)
        elif ext.lower() in ('.csv', '.tsv'):
            df = pd.read_csv(argspec.in_file, sep=argspec.csv_sep,
                             header=header, index_col=index_col,
                             usecols=usecols, dtype=dtype,
                             encoding=argspec.encoding)
        elif ext.lower() in ('.json',):
            df = pd.read_json(argspec.in_file, encoding=argspec.encoding)
        else:
            raise ReferenceError(f'Not supported file extension "{ext}" for input. '
                                 f'One of ".xls", ".xlsx", ".csv", ".tsv", ".json"')

        # 2) iloc (Select Ranges)
        if argspec.select_range:
            df = eval(f'df.iloc[{argspec.select_range}]')

        # 3) Profiling
        saved_stderr = sys.stderr
        tmp_stderr = os.path.join(tmpdir, 'stderr.txt')
        with open(tmp_stderr, 'w', encoding='utf-8') as stderr:
            sys.stderr = stderr
            kwargs = {
                'html': eval(argspec.html_style)
            }
            if argspec.title:
                kwargs['title'] = str(argspec.title)
            ppr = pp.ProfileReport(df, **kwargs)

            # 4) Save
            _, ext = os.path.splitext(argspec.out_file)
            if ext.lower() not in ('.html', '.json'):
                raise ReferenceError(f'Not supported file extension "{ext}" for output. '
                                     f'One of ".html", ".json"')
            ppr.to_file(output_file=argspec.out_file)
            print(os.path.abspath(argspec.out_file), end='')
        sys.stderr = saved_stderr
        saved_stderr = None
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        if saved_stderr is not None:
            sys.stderr = saved_stderr
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
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
        owner='ARGOS-LABS',
        group='4',  # Data Science
        version='1',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='pandas profiling',
        icon_path=get_icon_path(__file__),
        description='PANDAS data analysis profiling',
    ) as mcxt:
        # ############################################ for app dependent options
        mcxt.add_argument('--title', show_default=True,
                          display_name='Title of the report',
                          help='Title of the report')
        mcxt.add_argument('--html-style', show_default=True,
                          display_name='HTML Style',
                          default="{'style':{'full_width':True}}",
                          help="HTML Style, default is [[{'style':{'full_width':True}}]]")
        mcxt.add_argument('--select-range', show_default=True,
                          display_name='Select Range',
                          help='Select Range (iloc[...] method of DataFrame), ex) [[0:3,[2,4]]]')
        mcxt.add_argument('--sheet-name',
                          display_name='Sheet Name',
                          default='0',
                          help='Choose sheet name or index (0-indexed) for input. None for all sheets')
        mcxt.add_argument('--header',
                          display_name='Header',
                          default='0',
                          help='Choose header index(0-indexed), None for no header')
        mcxt.add_argument('--index-col',
                          display_name='Index Col',
                          default=None,
                          help='Column (0-indexed) to use as the row labels of the DataFrame')
        mcxt.add_argument('--usecols',
                          display_name='Use Cols',
                          default=None,
                          help='Returns a subset of the columns, (int, str, list-like, or callable default None). Not for the json input.')
        mcxt.add_argument('--dtype',
                          display_name='Data Type',
                          default=None,
                          help="Data type for data or columns. E.g. {'a': np.float64, 'b': np.int32, 'c': 'Int64'}")
        mcxt.add_argument('--csv-sep',
                          display_name='CSV Sep',
                          default=",",
                          help='CSV separator for input or output file, default is [[,]]')
        mcxt.add_argument('--encoding',
                          display_name='Encoding',
                          default="utf-8",
                          help='Character encoding for input or output file, default is [[utf-8]]')
        # ######################################### for app dependent parameters
        mcxt.add_argument('in_file',
                          display_name='In file', input_method='fileread',
                          help='Input file for data analysis. Extensions is one of ".csv, .json, .xls, .xlsx"')
        mcxt.add_argument('out_file',
                          display_name='Out file', input_method='filewrite',
                          help='Output file for data analysis. Extensions is one of ".html, .json"')
        argspec = mcxt.parse_args(args)
        return do_pandasprofiling(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
