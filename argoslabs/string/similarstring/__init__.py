#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.string.similarstring`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for string regular-expression operation
"""
# Authors
# ===========
#
# * Kyobong An
#
# Change Log
# --------
#
#  * [2023/05/30]
#     - 열선택 기능 추가 (Venkatesh 요청)
#  * [2021/11/11]
#     - starting

################################################################################
import os
import csv
import sys
from openpyxl.utils import column_index_from_string
from strsimpy.jaro_winkler import JaroWinkler
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from alabs.common.util.vvencoding import get_file_encoding


################################################################################
class Similar_Error(Exception):
    def __init__(self, *args):
        pass


################################################################################
class Similar_String(object):
    def __init__(self, argspec):
        self.argspec = argspec
        self.correctlist = self.open()
        self.similar_string = argspec.similar_string
        self.similarity_list = []
        self.comparison_string(self.similar_string)

    def open(self):
        with open(self.argspec.correctlist, 'r', encoding=get_file_encoding(self.argspec.correctlist))as f:
            rows = csv.reader(f)
            correctlist = []
            for row in list(rows)[self.argspec.header:]:
                correctlist.append(row[column_index_from_string(self.argspec.column)-1])
        return list(filter(None, correctlist))

    def comparison_string(self, similar_string):
        for correct_str in self.correctlist:    # 유사도를 측정하여 리스트 형식으로 저장
            if self.argspec.case:    # 옵션 선택시 소문자로 변경해서 비교
                self.similarity_list.append(
                    JaroWinkler().similarity(correct_str.lower(), similar_string.lower()))
            else:
                self.similarity_list.append(
                    JaroWinkler().similarity(correct_str, similar_string))

        # 유사도가 높은 값을 임계치(default=70)와 비교, *100 하는이유는 유사도 값이 0~1사이 값이기때문
        # 또한 csv output일때는 임계치보다 작더라도 통과
        if self.argspec.threshold <= max(self.similarity_list)*100 or self.argspec.csv_output:
            pass
        else:    # 임계치보다 작을 경우 에러 출력
            raise Similar_Error(f'The similarity({int(max(self.similarity_list)*100)})'
                                f' of "{similar_string}" is less than the threshold.')

        if self.argspec.csv_output:    # csv파일에 있는 문자열 각각의 유사도 출력.
            for i, correct_output in enumerate(self.correctlist):
                if i == 0:
                    print("string,similarity")
                print("%s,%d" % (correct_output, self.similarity_list[i]*100))
        else:
            print(self.correctlist[self.similarity_list.index(max(self.similarity_list))])


@func_log
def do_similar(mcxt, argspec):
    try:
        mcxt.logger.info('>>>starting...')
        Similar_String(argspec)

        sys.stdout.flush()
        return 0
    except Similar_Error as e:
        mcxt.logger.error(str(e))
        sys.stderr.write(str(e))
        return 1
    except Exception as e:
        msg = 'argoslabs.string.similarstring Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99
    finally:
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
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='String Similarity',
        icon_path=get_icon_path(__file__),
        description='similar String',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--header', nargs='?', type=int,
                          display_name='csv # headers',
                          default=0, const=0,
                          help="""exclude header lines for input csv file
  (defaut is 0 no header, and 1 means one header line to exclude)""")
        mcxt.add_argument('--threshold', type=int, default=70,
                          display_name='Similarity Threshold',
                          help='Threshold. default = 70')
        mcxt.add_argument('--column', default='A',
                          display_name='Assign a column',
                          help='Assign one column. default = A')
        # mcxt.add_argument('--threshold-max', type=int,
        #                   input_group='Similarity Threshold',
        #                   display_name='Max Value',
        #                   help='Maximum Threshold')
        # mcxt.add_argument('--threshold-min', type=int,
        #                   input_group='Similarity Threshold',
        #                   display_name='Min Value',
        #                   help='Minimum Threshold')
        mcxt.add_argument('--case',
                          display_name='Case Insensitive',
                          action='store_true',
                          help='Case Insensitive')
        mcxt.add_argument('--csv-output',
                          display_name='csv output',
                          action='store_true',
                          help='Case Insensitive')
        # ##################################### for app dependent parameters
        mcxt.add_argument('correctlist',
                          display_name='Correct String List',
                          input_method='fileread',
                          help='csv for the string list')
        mcxt.add_argument('similar_string',
                          display_name='Similar String',
                          help='given string to similar compare')
        argspec = mcxt.parse_args(args)
        return do_similar(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
