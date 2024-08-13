"""
====================================
 :mod:`argoslabs.datanalysis.pandas3`
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
#  * [2024/07/22]
#     - numpy 버전 고정
#     - to_excel의 encoding 인자 삭제
#  * [2021/04/06]
#     - --in-encodings에 default 삭제(오류로 인해서), eval()사용시 문자열의 에러가 있어 수정
#  * [2021/04/06]
#     - 그룹에 "4-Data Science" 넣음
#  * [2020/09/15]
#     - --in-csv-seps, --in-encodings
#     - --out-header, --out-index, --out-csv-sep, --out-encoding 분리
#  * [2020/09/11]
#     - "Header" => "Header Row", "Out Index" => "Show Index"
#  * [2020/09/10]
#     - suppress output for exec
#  * [2020/09/07]
#     - starting

################################################################################
import os
import sys
# noinspection PyUnresolvedReferences,PyPackageRequirements
import numpy as np
# noinspection PyPackageRequirements
import pandas as pd
from tempfile import gettempdir
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import warnings
warnings.filterwarnings("ignore")


################################################################################
def pandas_safe_eval(es, default=None):
    # noinspection PyBroadException
    try:
        if not es:
            return default
        r = eval(es)
        return r
    except Exception:
        # return default
        return es if es else default


################################################################################
def pandas_safe_eval_from_list(ndx, el, default=None):
    # noinspection PyBroadException
    try:
        if not (el and isinstance(el, list)):
            return default
        if len(el) <= ndx:
            return default
        # r = eval(el[ndx])
        r = pandas_safe_eval(el[ndx], default)
        return r
    except Exception:
        return default


################################################################################
def read_file(ndx, argspec, dfs, in_file):
    if not os.path.exists(in_file):
        raise IOError(f'Cannot read file "{in_file}"')

    sheet_name = pandas_safe_eval_from_list(ndx, argspec.sheet_names, default=0)
    header = pandas_safe_eval_from_list(ndx, argspec.headers, default=0)
    index_col = pandas_safe_eval_from_list(ndx, argspec.index_cols)
    usecols = pandas_safe_eval_from_list(ndx, argspec.usecols)
    dtype = pandas_safe_eval_from_list(ndx, argspec.dtypes)
    csv_sep = pandas_safe_eval_from_list(ndx, argspec.in_csv_seps, default=',')
    encoding = pandas_safe_eval_from_list(ndx, argspec.in_encodings, default='utf-8')

    _, ext = os.path.splitext(in_file)
    if ext.lower() in ('.xls', '.xlsx', '.xlsm'):
        df = pd.read_excel(in_file, sheet_name=sheet_name,
                           header=header, index_col=index_col,
                           usecols=usecols, dtype=dtype)
    elif ext.lower() in ('.csv', '.tsv'):
        df = pd.read_csv(in_file, sep=csv_sep,
                         header=header, index_col=index_col,
                         usecols=usecols, dtype=dtype,
                         encoding=encoding)
    elif ext.lower() in ('.json',):
        df = pd.read_json(in_file, encoding=encoding)
    else:
        raise ReferenceError(f'Not supported file extension "{ext}" for input. '
                             f'One of ".xls", ".xlsx", ".xlsm", ".csv", ".tsv", ".json"')
    dfs.append(df)


################################################################################
# noinspection PyUnresolvedReferences
@func_log
def do_pandas3(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    # suppress output for exec
    t_stdout = sys.stdout
    exec_out = os.path.join(gettempdir(), 'pandas3-exec-stdout.txt')
    sys.stdout = open(exec_out, 'w', encoding=argspec.out_encoding)
    try:
        # 1) READ in_file
        df = None
        dfs = list()
        for i, in_file in enumerate(argspec.in_files):
            read_file(i, argspec, dfs, in_file)

        # 2) do dataframe job
        ldict = {'dfs': dfs, 'df': df, 'argspec': argspec}
        if argspec.stats:
            exec('\n'.join(argspec.stats), globals(), ldict)
            df = ldict['df']
        if argspec.stat_file and os.path.exists(argspec.stat_file):
            with open(argspec.stat_file, encoding=argspec.out_encoding) as ifp:
                exec(ifp.read(), globals(), ldict)
                df = ldict['df']

        # noinspection PyUnusedLocal
        dfs = ldict['dfs']

        # 3) Save
        _, ext = os.path.splitext(argspec.out_file)
        out_header = pandas_safe_eval(argspec.out_header, True)
        if ext.lower() in ('.xls', '.xlsx'):
            df.to_excel(argspec.out_file,  # sheet_name=sheet_name, ERROR
                        index=argspec.out_index,
                        header=out_header)
        elif ext.lower() in ('.csv', '.tsv'):
            df.to_csv(argspec.out_file, sep=argspec.out_csv_sep,
                      encoding=argspec.out_encoding, index=argspec.out_index,
                      header=out_header)
        elif ext.lower() in ('.json',):
            df.to_json(argspec.out_file,
                       encoding=argspec.out_encoding, index=argspec.out_index)
        else:
            raise ReferenceError(f'Not supported file extension "{ext}" for output. '
                                 f'One of ".xls", ".xlsx", ".csv", ".tsv", ".json"')
        # sys.stdout.close()  # suppress I/O error
        sys.stdout = t_stdout
        print(os.path.abspath(argspec.out_file), end='')
        return 0
    except Exception as err:
        # sys.stdout.close()  # suppress I/O error
        sys.stdout = t_stdout
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
        display_name='pandas III',
        icon_path=get_icon_path(__file__),
        description='PANDAS data analysis tool III',
    ) as mcxt:
        # ############################################ for app dependent options
        mcxt.add_argument('--stats', action='append',
                          display_name='Statements',
                          help='Statements, you can use df for DataFrame, pd for pandas and np for numpy')
        mcxt.add_argument('--stat-file',
                          display_name='Statements File',
                          input_method='fileread',
                          help='Statements file, you can use in file df for DataFrame, pd for pandas and np for numpy')
        mcxt.add_argument('--sheet-names', action='append',
                          display_name='Sheet Names',
                          # default='0',
                          help='Choose sheet name or index (0-indexed) for input. None for all sheets')
        mcxt.add_argument('--headers', action='append',
                          display_name='Header Rows',
                          # default='0',
                          help='Choose header index(0-indexed), None for no header')
        mcxt.add_argument('--index-cols', action='append',
                          display_name='Index Cols',
                          default=None,
                          help='Column (0-indexed) to use as the row labels of the DataFrame')
        mcxt.add_argument('--usecols', action='append',
                          display_name='Use Cols',
                          default=None,
                          help='Returns a subset of the columns, (int, str, list-like, or callable default None). Not for the json input.')
        mcxt.add_argument('--dtypes', action='append',
                          display_name='Data Types',
                          default=None,
                          help="Data type for data or columns. E.g. {'a': np.float64, 'b': np.int32, 'c': 'Int64'}")
        mcxt.add_argument('--in-csv-seps', action='append',
                          display_name='In CSV Seps',
                          help='CSV separators for input files, default is [[,]]')
        mcxt.add_argument('--in-encodings', action='append',
                          display_name='In Encodings',
                          help='Character encoding for input files, default is [[utf-8]]')
        mcxt.add_argument('--out-header',
                          display_name='Out Header',
                          default='True',
                          help='Choose output header bool or list of str, default [[True]]')
        mcxt.add_argument('--out-index',
                          display_name='Out Show Index', action='store_true',
                          help='If set, save index column to out file.')
        mcxt.add_argument('--out-csv-sep',
                          display_name='Out CSV Sep',
                          default=",",
                          help='CSV separator for output file, default is [[,]]')
        mcxt.add_argument('--out-encoding',
                          display_name='Out Encoding',
                          default="utf-8",
                          help='Character encoding for output file, default is [[utf-8]]')
        # ######################################### for app dependent parameters
        mcxt.add_argument('out_file',
                          display_name='Out file', input_method='filewrite',
                          help='Output file for data analysis. Extensions is one of ".csv, .json, .xls, .xlsx"')
        mcxt.add_argument('in_files', nargs='+',
                          display_name='In files', input_method='fileread',
                          help='Input files for data analysis. Extensions is one of ".csv, .json, .xls, .xlsx, .xlsm"')
        argspec = mcxt.parse_args(args)
        return do_pandas3(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
