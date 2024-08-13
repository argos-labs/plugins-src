"""
====================================
 :mod:`argoslabs.datanalysis.pandasbasic`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS data analysis using PANDAS basic
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#  * [2024/06/27]
#     - to_excel() encoding 인자 삭제
#
#  * [2023/07/24] Kyobong
#     - "Select Range" 메소드 display_name 오류 변경
#  * [2021/04/02]
#     - 그룹에 "4-Data Science" 넣음
#  * [2020/08/09]
#     - 엑셀에서는 encoding 인자가 없음
#  * [2020/04/27]
#     - pandas_safe_eval 함수 추가
#  * [2020/04/26]
#     - --usecols 옵션 추가
#     - --dtype 옵션 추가
#  * [2020/04/09]
#     - add replace
#  * [2020/04/08]
#     - starting

################################################################################
import os
import sys
import warnings
# noinspection PyUnresolvedReferences,PyPackageRequirements
import numpy as np
# noinspection PyPackageRequirements
import pandas as pd
# from tempfile import gettempdir
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
def do_pandas(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        # warnings.warn("deprecated", DeprecationWarning)
        warnings.simplefilter("ignore")
        # 1) READ in_file
        if not os.path.exists(argspec.in_file):
            raise IOError(f'Cannot read file "{argspec.in_file}"')

        sheet_name = pandas_safe_eval(argspec.sheet_name)
        header = pandas_safe_eval(argspec.header)
        index_col = pandas_safe_eval(argspec.index_col) if argspec.index_col else None
        usecols = pandas_safe_eval(argspec.usecols) if argspec.usecols else None
        dtype = pandas_safe_eval(argspec.dtype) if argspec.dtype else None

        _, ext = os.path.splitext(argspec.in_file)
        if ext.lower() in ('.xls', '.xlsx', '.xlsm'):
            df = pd.read_excel(argspec.in_file, sheet_name=sheet_name,
                               header=header, index_col=index_col,
                               usecols=usecols, dtype=dtype)
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

        # 2) Filter
        if argspec.filter:
            for f in argspec.filter:
                df = eval(fr'df[{f}]')

        # 3) Replace
        if argspec.replace:
            for r in argspec.replace:
                col, rep = r.split('::=', maxsplit=1)
                rstr = fr'df["{col}"].str.replace({rep})'
                df[col] = eval(rstr)
        # 4) Assign
        if argspec.assign:
            for a in argspec.assign:
                estr = fr'df.assign({a})'
                df = eval(estr)

        # 5) Drop
        if argspec.drop_cols:
            df = df.drop(columns=argspec.drop_cols)

        # 6) iloc (Select Ranges)
        if argspec.select_range:
            df = eval(f'df.iloc[{argspec.select_range}]')

        # 7) Save
        _, ext = os.path.splitext(argspec.out_file)
        if ext.lower() in ('.xls', '.xlsx'):
            df.to_excel(argspec.out_file, # sheet_name=sheet_name, ERROR
                         index=argspec.out_index)
        elif ext.lower() in ('.csv', '.tsv'):
            df.to_csv(argspec.out_file, sep=argspec.csv_sep,
                      encoding=argspec.encoding, index=argspec.out_index)
        elif ext.lower() in ('.json',):
            df.to_json(argspec.out_file,
                       encoding=argspec.encoding, index=argspec.out_index)
        else:
            raise ReferenceError(f'Not supported file extension "{ext}" for output. '
                                 f'One of ".xls", ".xlsx", ".csv", ".tsv", ".json"')
        print(os.path.abspath(argspec.out_file), end='')
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
        owner='ARGOS-LABS',
        group='4',  # Data Science
        version='1',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='pandas I',
        icon_path=get_icon_path(__file__),
        description='PANDAS data analysis tool I',
    ) as mcxt:
        # ############################################ for app dependent options
        mcxt.add_argument('--filter', show_default=True,
                          display_name='Filters', action='append',
                          help="Filters for DataFrame, eg) [[df['A'] > 0]]")
        mcxt.add_argument('--replace',
                          display_name='Replace Col', action='append',
                          help=r"Replace Col, eg) [[col::='ISO\s','NEW']]")
        mcxt.add_argument('--assign',
                          display_name='Add Cols', action='append',
                          help=r"Add column specs (assign method for DataFrame), "
                               r"eg) [[NewCol=lambda x: x['B'].str.extract('^([\w\d\.]+)\s')]]")
        mcxt.add_argument('--drop-cols',
                          display_name='Drop Cols', action='append',
                          help='Column names to drop')
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
        mcxt.add_argument('--out-index',
                          display_name='Out Index', action='store_true',
                          help='If set, save index column to out file.')
        # ######################################### for app dependent parameters
        mcxt.add_argument('in_file',
                          display_name='In file', input_method='fileread',
                          help='Input file for data analysis. Extensions is one of ".csv, .json, .xls, .xlsx, .xlsm"')
        mcxt.add_argument('out_file',
                          display_name='Out file', input_method='filewrite',
                          help='Output file for data analysis. Extensions is one of ".csv, .json, .xls, .xlsx"')
        argspec = mcxt.parse_args(args)
        return do_pandas(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
