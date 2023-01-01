"""
====================================
 :mod:`argoslabs.data.fileconv`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module data csv2tsv
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/11/23] Kyobong
#     - conditional formatting 기능추가 xlsx2xls을 사용할때 조건부 서식을 유지하기위함.
#  * [2021/04/01]
#     - 그룹에 "6-Files and Folders" 넣음
#  * [2021/01/20]
#     - xrld 버전을 1.2.0 으로 고정해야 했음
#  * [2020/07/27]
#     - xlsx2csv, xlsx2xls 기능 추가 (장소장님 요청; 남동발전소)
#  * [2020/03/25]
#     - xls2csv 기능 추가 (한솔씨 요청)
#  * [2020/03/07]
#     - xls2xlsx 기능 추가 (Shige 요청, SAP 관련 작업에서 필요)
#     - display_name: "Data Conv" => "File Conv"
#     - stdout 에는 target 파일명 출력 (Shige 요청)
#  * [2019/12/18]
#     - csv2_sv 에서 "delimiter" must be a 1-character string 오류 수정
#  * [2019/09/16]
#     - check error of same src and target is not allowed
#  * [2019/06/03]
#     - add get_file_encoding for detect encoding
#  * [2019/05/10]
#     - add json2xml, xml2json
#  * [2019/05/02]
#     - starting

################################################################################
import os
import sys
import csv
import json
# noinspection PyPackageRequirements
import xlrd
# noinspection PyPackageRequirements
import pyexcel
# noinspection PyPackageRequirements
import xmltodict
import win32com.client
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from alabs.common.util.vvencoding import get_file_encoding
import warnings


################################################################################
def xls2csv(s, t):
    wb = xlrd.open_workbook(s)
    for sh in wb.sheets():
        with open(t, 'w', encoding='utf-8') as ofp:
            c = csv.writer(ofp, lineterminator='\n', quoting=csv.QUOTE_ALL)
            for rownum in range(sh.nrows):
                row = sh.row_values(rownum)
                c.writerow(row)
    return 0


################################################################################
@func_log
def table_convert(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        if not (argspec.src and os.path.exists(argspec.src)):
            raise RuntimeError('Cannot read src "%s"' % argspec.src)
        argspec.src = os.path.abspath(argspec.src)
        argspec.target = os.path.abspath(argspec.target)
        if argspec.src == argspec.target:
            raise RuntimeError('Cannot same source or target "%s"' % argspec.src)

        if argspec.operation == 'xlsx2xls' and argspec.conditional_formatting:
            excel = win32com.client.gencache.EnsureDispatch('Excel.Application')
            excel.Visible = False
            excel.DisplayAlerts = False
            wb = excel.Workbooks.Open(argspec.src)
            wb.SaveAs(argspec.target, FileFormat=56)
            wb.Close()
            excel.Quit()
            return 0

        elif argspec.operation in ('xls2xlsx', 'xlsx2csv', 'xlsx2xls'):
            warnings.simplefilter("ignore", category=PendingDeprecationWarning)
            pyexcel.save_book_as(file_name=argspec.src,
                                 dest_file_name=argspec.target)
            print(argspec.target, end='')
            return 0

        elif argspec.operation == 'xls2csv':
            xls2csv(argspec.src, argspec.target)
            print(argspec.target, end='')
            return 0

        dt_encoding = get_file_encoding(argspec.src, argspec.encoding)
        if dt_encoding != argspec.encoding:
            mcxt.logger.info('User encoding is "%s" but detected encoding is "%s"'
                             % (argspec.encoding, dt_encoding))
            argspec.encoding = dt_encoding
        with open(argspec.src, encoding=argspec.encoding) as ifp, \
                open(argspec.target, 'w', newline='',
                     encoding=argspec.encoding) as ofp:
            if argspec.operation.startswith('csv2'):
                if argspec.operation == 'csv2tsv':
                    argspec.target_sep = '\t'
                elif argspec.operation == 'csv2_sv':
                    if not argspec.target_sep:
                        raise RuntimeError('invalid target separator')
                csvin = csv.reader(ifp, skipinitialspace=True)
                # delimiter는 몽땅
                tsvout = csv.writer(ofp, delimiter=argspec.target_sep[0])
                for row in csvin:
                    tsvout.writerow(row)
            elif argspec.operation == 'json2xml':
                # jd = json.load(ifp.read())
                # dict2xml(jd, ofp)
                x = xmltodict.unparse(json.loads(ifp.read()), pretty=True)
                ofp.write(x)
            elif argspec.operation == 'xml2json':
                j = json.dumps(xmltodict.parse(ifp.read()), indent=4)
                ofp.write(j)
        print(argspec.target, end='')
        return 0
    except Exception as e:
        msg = 'argoslabs.data.csv2tsv Error: %s' % str(e)
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
        group='6',  # 'Files and Folders',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='File Conv',
        icon_path=get_icon_path(__file__),
        description='CSV TSV file format conversion',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--target-sep',
                          display_name='Target separator',
                          default='\t',
                          help='Target separator for csv2_sv operation, default is [[\\t]]')
        mcxt.add_argument('--encoding',
                          display_name='File Encoding',
                          default='utf8',
                          help='File encoding for source or target file,'
                               ' default is [[utf8]]. If not valid encoding try to detect.')
        mcxt.add_argument('--conditional-formatting',
                          display_name='conditional formatting',
                          action='store_true',
                          help='Option to keep conditional formatting in "xlsx 2 xls"')
        # ##################################### for app dependent parameters
        mcxt.add_argument('operation',
                          display_name='Operation',
                          choices=['csv2tsv', 'csv2_sv', 'json2xml', 'xml2json',
                                   'xls2xlsx', 'xls2csv', 'xlsx2xls', 'xlsx2csv'],
                          default='csv2tsv',
                          help='name to say hello')
        mcxt.add_argument('src',
                          display_name='Source File',
                          input_method='fileread',
                          help='Source file name')
        mcxt.add_argument('target',
                          display_name='Target File',
                          input_method='filewrite',
                          help='Target file name to write')
        argspec = mcxt.parse_args(args)
        return table_convert(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
