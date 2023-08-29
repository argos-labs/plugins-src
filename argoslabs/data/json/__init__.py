"""
====================================
 :mod:`argoslabs.data.json`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for select item from JSON
"""
#
# Authors
# ===========
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2023/02/14]
#     - 결과 값이 "0" 이거나 빈 배열일 경우 1로 리턴하는 경우 발생
#       return은 0 , 에러의 경우 99로 변경, print_format에 0일 경우 공백으로 나오는 부분처리.
#  * [2021/04/01]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2021/01/22]
#     - Irene, Venkatesh JSON 가져오는 것을 약간 수정
#       fields 라는 것 동일 반복 데이터를 가지고 있는 것 처리
#  * [2020/10/26]
#     - --encoding 옵션 추가
#  * [2019/12/10]
#     - 기존 성공이면 1을 리턴하는 대신 결과가 있으면 0, 없거나 실패하면 1 또는 2로 수정
#  * [2019/04/18]
#     - 일본어 등의 출력이 unicode로 되는 것을 utf8로 수정
#  * [2019/03/22]
#     - --rows, --cells, --cell-key 옵션 추가
#  * [2019/03/13]
#     - --errfile 용 수정 및 테스트 추가
#  * [2019/03/08]
#     - add icon
#  * [2019/03/07]
#     - starting, testing
#  [TODO] get 말고 set 필요?

################################################################################
import os
import re
import sys
import csv
import json
import collections
from io import StringIO
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from alabs.common.util.vvjson import get_xpath
try:
    from collections.abc import Mapping, Iterable
except ImportError:
    from collections import Mapping, Iterable


################################################################################
G_CELL_KEY = None


################################################################################
def get_header(r, hlist):
    if isinstance(r, (list, tuple)):
        for item in r:
            get_header(item, hlist)
    elif isinstance(r, dict):
        for k, v in r.items():
            if k not in hlist:
                hlist.append(k)


################################################################################
def get_cell_value(cv):
    return re.sub(r"\s+", ' ', str(cv))


################################################################################
def get_value(mcxt, argspec, r, hlist):
    vlist = []
    if isinstance(r, dict):
        for h in hlist:
            if h in r:
                v = r[h]
                if isinstance(v, str):
                    v = get_cell_value(v)
                vlist.append(v)
            else:
                vlist.append('')
    elif isinstance(r, (list, tuple)):
        for e in r:
            if isinstance(e, dict):
                if not argspec.cell_key:
                    raise RuntimeError('please set --cell-key')
                if argspec.cell_key not in e:
                    raise RuntimeError('Invalid --cell-key')
                v = get_cell_value(e[argspec.cell_key])
                vlist.append(v)
            else:
                vlist.append(get_cell_value(e))
    elif isinstance(r, str):
        vlist.append(r)
    else:
        errmsg = 'list of csv result must be a key:value format but "%s"' % str(type(r))
        mcxt.logger.error(errmsg)
        sys.stderr.write('RuntimeError: %s\n' % errmsg)
        raise RuntimeError(errmsg)
    return vlist


################################################################################
@func_log
def print_format(mcxt, argspec, r, ofp):
    if r is None or r == '':
        ofp.write('')
        return
    # lines = []
    if argspec.format == 'csv':
        sio = StringIO(newline='')
        cw = csv.writer(sio, quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
        if isinstance(r, (list, tuple)):
            # 만약 list의 각 항목이 dict이면 해당 key를 모두 모아 헤더로 사용
            hlist = None
            if isinstance(r[0], dict):
                hlist = []
                get_header(r, hlist)
                if not hlist:
                    errmsg = 'csv result must have header'
                    mcxt.logger.error(errmsg)
                    sys.stderr.write('RuntimeError: %s\n' % errmsg)
                    raise RuntimeError(errmsg)
                cw.writerow(hlist)
                # if hlist:
                #     lines.append(','.join(hlist))
            for item in r:
                v = get_value(mcxt, argspec, item, hlist)
                # lines.append(v)
                if 0 < argspec.exclude_index <= len(v) and \
                        v[argspec.exclude_index-1] == argspec.exclude_value:
                    continue
                cw.writerow(v)
            ofp.write(sio.getvalue())
        else:
            errmsg = 'CSV result must be a list but "%s"' % str(type(r))
            mcxt.logger.error(errmsg)
            sys.stderr.write('RuntimeError: %s\n' % errmsg)
            raise RuntimeError(errmsg)
    else:
        s = json.dumps(r, ensure_ascii=False) if isinstance(r, dict) else str(r)
        ofp.write(s)


################################################################################
# noinspection PyUnusedLocal
def and_filter(mcxt, argspec, r):
    if not argspec.and_filter:
        return True
    if not isinstance(r, dict):
        return True
    and_r = []
    for fd in argspec.and_filter:
        fk, fv = fd.split('=', maxsplit=1)
        if fk not in r:
            return False
        and_r.append(r[fk] == fv)
    return all(and_r)


################################################################################
# noinspection PyUnusedLocal
def or_filter(mcxt, argspec, r):
    if not argspec.or_filter:
        return True
    if not isinstance(r, dict):
        return True
    for fd in argspec.or_filter:
        fk, fv = fd.split('=', maxsplit=1)
        if fk not in r:
            continue
        if r[fk] == fv:
            return True
    return False


################################################################################
def do_filter(mcxt, argspec, org_r):
    if not (argspec.and_filter or argspec.or_filter):
        return org_r
    if isinstance(org_r, (list, tuple)):
        r = []
        for row in org_r:
            if and_filter(mcxt, argspec, row) and or_filter(mcxt, argspec, row):
                r.append(row)
        return r
    elif isinstance(org_r, dict):
        if and_filter(mcxt, argspec, org_r) and or_filter(mcxt, argspec, org_r):
            return org_r
        else:
            return {}
    else:
        return org_r


################################################################################
def _find_all_json(data, key, res):
    if isinstance(data, Mapping):
        for k, v in data.items():
            if k == key:
                if G_CELL_KEY:
                    res.append(v)
                else:
                    if isinstance(v, (list, tuple)):
                        res.extend(v)
                    else:
                        res.append(v)
            _find_all_json(v, key, res)
    elif isinstance(data, str):
        return
    elif isinstance(data, Iterable):
        for e in data:
            _find_all_json(e, key, res)


################################################################################
def find_all_json(d, key):
    res = []
    _find_all_json(d, key, res)
    return res


################################################################################
# noinspection PyUnusedLocal
def find_all_from_json(mcxt, argspec, js):
    return find_all_json(js, argspec.find_all)


################################################################################
@func_log
def do_json(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        global G_CELL_KEY
        G_CELL_KEY = argspec.cell_key
        if not os.path.exists(argspec.jsonfile):
            raise IOError('Cannot read JSON file "%s"' % argspec.jsonfile)
        with open(argspec.jsonfile, encoding=argspec.encoding) as ifp:
            js = json.load(ifp)
        if argspec.xpath == '/':
            r = js
        else:
            r = get_xpath(js, argspec.xpath,
                          raise_exception=argspec.raise_exception)
        if argspec.find_all:
            r = find_all_from_json(mcxt, argspec, r)
        r = do_filter(mcxt, argspec, r)
        if argspec.len:
            sys.stdout.write(str(len(r)))
        else:
            print_format(mcxt, argspec, r, sys.stdout)
        return 0
    except Exception as e:
        msg = 'Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write(msg)
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
        display_name='JSON Select',
        icon_path=get_icon_path(__file__),
        description='Extract some parts from JSON file',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--raise-exception', '-r', action='store_true',
                          display_name='Raise Except Flag',
                          help='If this option is on and invalid xpath expression then raise error, otherwise ')
        mcxt.add_argument('--format', '-f', default=None, action='store',
                          display_name='Opt Output Format',
                          choices=['csv'],
                          help='output format, default is [[csv]]')
        mcxt.add_argument('--len', '-l', action='store_true',
                          display_name='Get length',
                          help='Just get the length of elements')
        mcxt.add_argument('--and-filter', '-a', default=None, action='append',
                          display_name='AND Filter',
                          help='"AND" filter for matching key=value. eg) --and-filter "key=value"')
        mcxt.add_argument('--or-filter', '-o', default=None, action='append',
                          display_name='OR Filter',
                          help='"OR" filter for matching key=value. eg) --or-filter "key=value"')
        mcxt.add_argument('--find-all',
                          display_name='Find all Opt',
                          help='Find all matched keys from xpath')
        mcxt.add_argument('--cell-key', nargs='?',
                          display_name='Cell key',
                          help='in CSV output cell is dictionary then get the value from with this cell-key')
        mcxt.add_argument('--exclude-index', default=-1, const=-1,
                          display_name='Exclude index',
                          nargs='?', type=int,
                          help='in CSV output excluding cell index (1-based) with value of --exclude-value')
        mcxt.add_argument('--exclude-value',
                          display_name='Exclude value',
                          help='in CSV output excluding cell value with index of --exclude-index')
        mcxt.add_argument('--encoding',
                          display_name='Encoding', default='utf-8',
                          help='Encoding for JSON file, default is "utf-8"')
        # ##################################### for app dependent parameters
        # mcxt.add_argument('operation', default='get', action='store',
        #                   choices=['get', 'set'],
        #                   help='operation to set or get')
        mcxt.add_argument('jsonfile', action='store',
                          display_name='JSON file',
                          input_method='fileread',
                          help='json file to handling')
        mcxt.add_argument('xpath', action='store', help='xpath like notation to extract from JSON (x/y/z)')
        argspec = mcxt.parse_args(args)
        return do_json(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
