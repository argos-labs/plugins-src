#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.string.basicstring`
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
#  * [2022/03/02]
#     - Slice & Index 기능추가
#  * [2021/10/25]
#     - tuple 제거 list로 사용. "Boolean" display_name 변경 -> "True/False"
#  * [2021/10/19]
#     - expandtabs 사용할때는 '\t'을 '\\t' 으로 들어오기때문에 변환해주어야함
#  * [2021/10/18]
#     - list와 tuple에 인풋 메서드 base64에러 때문에 적용할수 없음 추후 필요할시 수정
#  * [2021/10/12]
#     - starting

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path, vv_base64_decode
from alabs.common.util.vvencoding import get_file_encoding


class False_Value(Exception):
    pass


def base64_appnd(s):
    r = []
    for i in s:
        r.append(vv_base64_decode(i))
    return r


################################################################################
class Basic_String(object):
    def __init__(self, argspec):
        self.argspec = argspec

        if self.argspec.file_path:
            self.string = self.fileopen()
        else:
            self.string = vv_base64_decode(argspec.string)
        if argspec.str1:
            self.str1 = vv_base64_decode(argspec.str1)
        if argspec.str2:
            self.str2 = vv_base64_decode(argspec.str2)
        self.int1 = argspec.int1
        self.int2 = argspec.int2
        # self.chr = vv_base64_decode(argspec.chr)
        if argspec.chr:
            self.chr = chr(argspec.chr)
        if argspec.list:
            # self.list = base64_appnd(argspec.list)
            self.list = argspec.list
        self.output = None

    def fileopen(self):
        encoding = get_file_encoding(self.argspec.file_path)
        with open(self.argspec.file_path, encoding=encoding) as ifp:
            s = ifp.read()
            ifp.close()
        return s

    def boolean(self):
        if self.argspec.boolean == 'isalnum':
            self.output = self.string.isalnum()
        elif self.argspec.boolean == 'isalpha':
            self.output = self.string.isalpha()
        elif self.argspec.boolean == 'isascii':
            self.output = self.string.isascii()
        elif self.argspec.boolean == 'isdecimal':
            self.output = self.string.isdecimal()
        elif self.argspec.boolean == 'isdigit':
            self.output = self.string.isdigit()
        elif self.argspec.boolean == 'islower':
            self.output = self.string.islower()
        elif self.argspec.boolean == 'isnumeric':
            self.output = self.string.isnumeric()
        elif self.argspec.boolean == 'isspace':
            self.output = self.string.isspace()
        elif self.argspec.boolean == 'istitle':
            self.output = self.string.istitle()
        elif self.argspec.boolean == 'isupper':
            self.output = self.string.isupper()

        if not self.output:
            raise False_Value

    def convert(self):
        if self.argspec.convert == 'capitalize':
            self.output = self.string.capitalize()
        elif self.argspec.convert == 'lower':
            self.output = self.string.lower()
        elif self.argspec.convert == 'replace':    # .replace(str,str,int) int = -1은 전부
            self.output = self.string.replace(self.str1, self.str2, self.int1)
        elif self.argspec.convert == 'swapcase':
            self.output = self.string.swapcase()
        elif self.argspec.convert == 'title':
            self.output = self.string.title()
        elif self.argspec.convert == 'upper':
            self.output = self.string.upper()

    def fill(self):
        if self.argspec.fill == 'center':    # .center(int,chr)
            self.output = self.string.center(self.int1, self.chr)
        elif self.argspec.fill == 'ljust':    # .ljust(int,chr)
            self.output = self.string.ljust(self.int1, self.chr)
        elif self.argspec.fill == 'rjust':    # .rjust(int,chr)
            self.output = self.string.rjust(self.int1, self.chr)
        elif self.argspec.fill == 'zfill':    # .zfill(int)
            self.output = self.string.zfill(self.int1)

    def find(self):
        if self.argspec.find == 'count':    # .count(str)
            self.output = self.string.count(self.str1)
        elif self.argspec.find == 'find':    # .find(str)
            self.output = self.string.find(self.str1)
        elif self.argspec.find == 'index':    # .index(str)
            self.output = self.string.index(self.str1)
        elif self.argspec.find == 'rfind':    # .rfind(str,int,int)
            self.output = self.string.rfind(self.str1, self.int1, self.int2)
        elif self.argspec.find == 'rindex':    # .rindex(str)
            self.output = self.string.rindex(self.str1)

    def join(self):
        if self.argspec.join == 'join':    # .join(list)
            if self.list:
                self.output = self.string.join(self.list)

    def split(self):
        if self.argspec.split == 'expandtabs':    # .expandtabs(int)
            self.string = self.string.replace('\\t', '\t')  # /t가 '//t'로 들어옴 그래서 변환.
            self.output = self.string.expandtabs(self.int1)
        elif self.argspec.split == 'partition':    # .partition(str)
            self.output = self.string.partition(self.str1)
        elif self.argspec.split == 'rpartition':    # .rpartition(str)
            self.output = self.string.rpartition(self.str1)
        elif self.argspec.split == 'rsplit':    # .rsplit(str,int)
            self.output = self.string.rsplit(self.str1, self.int1)
        elif self.argspec.split == 'split':    # .split(str,int)
            self.output = self.string.split(self.str1, self.int1)
        elif self.argspec.split == 'splitlines':    # .splitlines(boolean)
            if self.argspec.sub_boolean == 'True':
                self.output = self.string.splitlines(True)
            else:
                self.output = self.string.splitlines(False)

        if self.argspec.split != 'expandtabs':
            self.output = ','.join(self.output)

    def strip(self):
        if self.argspec.strip == 'lstrip':
            self.output = self.string.lstrip()
        elif self.argspec.strip == 'rstrip':
            self.output = self.string.rstrip()
        elif self.argspec.strip == 'strip':
            self.output = self.string.strip()

    def swith(self):
        if self.argspec.swith == 'endswith':    # .endswith(str or tuple)
            if self.argspec.list:
                self.output = self.string.endswith(tuple(self.list))
            else:
                self.output = self.string.endswith(self.str1)
        elif self.argspec.swith == 'startswith':    # .startswith(str, int, int)
            self.output = self.string.startswith(self.str1, self.int1, self.int2)

        if self.output is False:
            raise False_Value

    def slice(self):
        if self.argspec.slice.find(':') >= 0:
            s_rage = self.argspec.slice.split(':')
            for i, s in enumerate(s_rage):
                if s:
                    s_rage[i] = int(s)
                else:
                    s_rage[i] = None

            self.output = self.string[s_rage[0]:s_rage[1]]
        else:
            self.output = self.string[int(self.argspec.slice)]


@func_log
def do_basic(mcxt, argspec):
    try:
        mcxt.logger.info('>>>starting...')
        b_str = Basic_String(argspec)

        if b_str.argspec.boolean:
            b_str.boolean()
        elif b_str.argspec.convert:
            b_str.convert()
        elif b_str.argspec.fill:
            b_str.fill()
        elif b_str.argspec.find:
            b_str.find()
        elif b_str.argspec.join:
            b_str.join()
        elif b_str.argspec.split:
            b_str.split()
        elif b_str.argspec.strip:
            b_str.strip()
        elif b_str.argspec.swith:
            b_str.swith()
        elif b_str.argspec.slice:
            b_str.slice()

        if b_str.output is True:
            print('True')
        else:
            print(b_str.output)
        sys.stdout.flush()
        return 0
    except False_Value:
        print('False')
        return 1
    except Exception as e:
        msg = 'argoslabs.string.basicstring Error: %s' % str(e)
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
        display_name='Basic String Manipulation',
        icon_path=get_icon_path(__file__),
        description='String handling',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--int1', type=int,
                          display_name='int 1',
                          help='String argument of type int')
        mcxt.add_argument('--int2', type=int,
                          display_name='int 2',
                          help='String argument of type int')
        mcxt.add_argument('--str1',
                          input_method='base64',
                          display_name='string 1',
                          help='String argument of type string')
        mcxt.add_argument('--str2',
                          input_method='base64',
                          display_name='string 2',
                          help='String argument of type string1')
        mcxt.add_argument('--chr', type=ord,
                          # input_method='base64',
                          display_name='character',
                          help='String argument of type chracter')
        mcxt.add_argument('--list',
                          action='append',
                          # input_method='base64',
                          display_name='list',
                          help='String argument of type list')
        # mcxt.add_argument('--tuple',
        #                   action='append',
        #                   # input_method='base64',
        #                   display_name='tuple',
        #                   help='String argument of type tuple')
        mcxt.add_argument('--sub-boolean',
                          choices=['True', 'False'],
                          display_name='sub True/False',
                          help='String argument of type boolean')

        # ##################################### for app dependent parameters
        mcxt.add_argument('--string', show_default=True,
                          display_name='String to handle',
                          input_group='radio=String;default',
                          input_method='base64',
                          help='String to handle')
        mcxt.add_argument('--file-path', show_default=True,
                          input_method='fileread',
                          input_group='radio=String',
                          display_name='String from file',
                          help='Instead of parameter using file as string.')
        mcxt.add_argument('--boolean', show_default=True,
                          display_name='True/False',
                          input_group='radio=String operation type;default',
                          choices=['isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'islower',
                                   'isnumeric', 'isspace', 'istitle', 'isupper'],
                          help='String method of type boolean.')
        mcxt.add_argument('--convert', show_default=True,
                          display_name='Convert',
                          input_group='radio=String operation type',
                          choices=['capitalize', 'lower', 'replace', 'swapcase', 'title', 'upper'],
                          help='String method to change the case of a string')
        mcxt.add_argument('--fill', show_default=True,
                          display_name='Fill',
                          input_group='radio=String operation type',
                          choices=['center', 'ljust', 'rjust', 'zfill'],
                          help='String method to fill a string')
        mcxt.add_argument('--find', show_default=True,
                          display_name='Find',
                          input_group='radio=String operation type',
                          choices=['count', 'find', 'index', 'rfind', 'rindex'],
                          help='String method to find the position of a string')
        mcxt.add_argument('--join', show_default=True,
                          display_name='Join',
                          choices=['join'],
                          input_group='radio=String operation type',
                          help='join strings.')
        mcxt.add_argument('--split', show_default=True,
                          display_name='Split',
                          input_group='radio=String operation type',
                          choices=['expandtabs', 'partition', 'rpartition', 'rsplit', 'split', 'splitlines'],
                          help='Split a string.')
        mcxt.add_argument('--strip', show_default=True,
                          display_name='Strip',
                          input_group='radio=String operation type',
                          choices=['lstrip', 'rstrip', 'strip'],
                          help='remove spaces')
        mcxt.add_argument('--swith', show_default=True,
                          display_name='Swith',
                          input_group='radio=String operation type',
                          choices=['endswith', 'startswith'],
                          help='String method that tells if a particular string exists in a string.')
        mcxt.add_argument('--slice', show_default=True,
                          display_name='Index & Slice',
                          input_group='radio=String operation type',
                          help='String slicing & index. e.g. "apple"[3:5] = le')
        argspec = mcxt.parse_args(args)
        return do_basic(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
