#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.string.re`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for string regular-expression operation
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/11/29]
#     - return coder
#  * [2021/11/22]
#     - --replace 문자열도 base64 인코딩 하도록 함, '-'로 시작하는 경우 패러미터 파싱오류 발생
#  * [2021/08/04]
#     - tolower, toupper from file
#  * [2021/07/05]
#     - "String to handle" 패러미터에 input_method='base64' 지정 및 디코딩
#  * [2021/06/15]
#     - 패턴 패러미터에 input_method='base64' 지정 및 디코딩
#  * [2021/04/09]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/11/15]
#     - Need to Check  "String Manipulation" RE is not the same to find folder
#       only from "C:\Users\satto3\Desktop\Temp\Plugin Test\foo.txt" with RE "^.+\\"
#  * [2020/11/04]
#     - --apply-first 옵션 추가
#  * [2019/10/25]
#     - --file-encoding 옵션 추가
#  * [2019/09/23]
#     - add 'substring' operations
#  * [2019/09/12]
#     - add 'tolower', 'toupper' operations
#  * [2019/09/11]
#     - one replace result padding '\n' remove
#  * [2019/05/22]
#     - modify display_name and help string for limitrr
#  * [2019/05/02]
#     - starting

################################################################################
import re
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path, vv_base64_decode


################################################################################
@func_log
def do_re(mcxt, argspec):
    try:
        mcxt.logger.info('>>>starting...')
        argspec.pattern = vv_base64_decode(argspec.pattern)
        if argspec.string:
            argspec.string = vv_base64_decode(argspec.string)
        re_str = argspec.string
        if argspec.file:
            if not os.path.exists(argspec.file):
                raise RuntimeError('Cannot find file "%s" to handle string'
                                   % argspec.file)
            with open(argspec.file, encoding=argspec.file_encoding) as ifp:
                re_str = ifp.read()
        if not re_str:
            raise RuntimeError('Invalid string to operate')

        limit = argspec.limit
        re_flag = 0
        if argspec.ignore_case:
            re_flag |= re.IGNORECASE
        if argspec.multiline:
            re_flag |= re.MULTILINE
        # if argspec.dot_all:
        #     re_flag |= re.DOTALL
        if argspec.operation in ('tolower', 'toupper'):
            r = re_str.strip()
            if argspec.operation == 'tolower':
                if argspec.apply_first:
                    r = f'{r[0].lower()}{r[1:]}'
                else:
                    r = r.lower()
            else:
                if argspec.apply_first:
                    r = f'{r[0].upper()}{r[1:]}'
                else:
                    r = r.upper()
            sys.stdout.write(r)
            sys.stdout.flush()
            return 0
        if argspec.operation == 'substring':
            if argspec.ignore_case:
                re_str = re_str.lower()
                argspec.pattern = argspec.pattern.lower()
            fndx = re_str.find(argspec.pattern)
            sys.stdout.write('%s' % fndx)
            sys.stdout.flush()
            return 0

        r_list = list()
        re_compile = re.compile(argspec.pattern, re_flag)
        if argspec.operation == 'find':
            r_list = re_compile.findall(re_str)
        elif argspec.operation == 'split':
            if limit > 0:
                r_list = re_compile.split(re_str, maxsplit=limit)
            else:
                r_list = re_compile.split(re_str)
        elif argspec.operation == 'replace':
            re_replace = vv_base64_decode(argspec.replace)
            if not re_replace:
                re_replace = ''
            if limit > 0:
                r = re_compile.sub(re_replace, re_str, count=limit)
            else:
                r = re_compile.sub(re_replace, re_str)
            r_list = [r]
        if 0 < limit < len(r_list):
            r_list = r_list[:limit]
        if argspec.length:
            print(len(r_list))
        else:
            # for r in r_list:
            sys.stdout.write('\n'.join(r_list))
        sys.stdout.flush()
        return 0
    except Exception as e:
        msg = 'argoslabs.string.re Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        raise
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
        display_name='String Manipulation',
        icon_path=get_icon_path(__file__),
        description='String handling with regular expression',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--file',
                          input_method='fileread',
                          display_name='String from file',
                          show_default=True,
                          help='Instead of parameter using file as string.')
        mcxt.add_argument('--file-encoding',
                          display_name='File Encoding',
                          default='utf-8',
                          help='File encoding default is [[utf-8]]')
        mcxt.add_argument('--replace',
                          display_name='String to replace',
                          input_method='base64',
                          help='Replaced string for replace operation')
        mcxt.add_argument('--ignore-case', action='store_true',
                          display_name='Ignore Case',
                          help='If this flag is set case insensitive pattern is applied.')
        # multiline 과 dot-all 은 혹시 나중에 필요하면 적용
        # mcxt.add_argument('--dot-all', action='store_true',
        #                   display_name='Dot all match',
        #                   help='If this flag is set \\n is matched as a character.')
        mcxt.add_argument('--limit', type=int,
                          default=0,
                          display_name='Set number of result',
                          help='Set number of limit for the result of operation. [[0]] means no limit')
        mcxt.add_argument('--length', action='store_true',
                          default=0, show_default=True,
                          display_name='Hit Count',
                          help='If this flag is set then get the length of results instead of results.')
        mcxt.add_argument('--multiline', action='store_true',
                          display_name='MultiLine Flag',
                          help='If this flag is set multiple lines pattern is applied. That is to say "^" or "$" '
                               'does not applicable to each line, instead total lines as treated like one line.')
        mcxt.add_argument('--apply-first', action='store_true',
                          display_name='Apply 1st Char',
                          help='If this flag is set only first character is '
                               'applied for toupper, tolower operations.')
        # mcxt.add_argument('--find-group',
        #                   display_name='Find Group',
        #                   help='Group find with parenthesis, first matching group is "\\1"')
        # ##################################### for app dependent parameters
        mcxt.add_argument('operation',
                          display_name='String operation type',
                          default='find',
                          choices=['find', 'split', 'replace', 'tolower', 'toupper', 'substring'],
                          help='String operation using Regular Expression. Default operation is [[find]]')
        mcxt.add_argument('pattern',
                          display_name='Regular Expression pattern',
                          input_method='base64',
                          help='Pattern for Regular Expression')
        mcxt.add_argument('string', nargs='?',
                          display_name='String to handle',
                          input_method='base64',
                          help='String to handle')
        argspec = mcxt.parse_args(args)
        return do_re(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
