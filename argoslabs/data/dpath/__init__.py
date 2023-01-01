"""
====================================
 :mod:`argoslabs.data.dpath`
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
#  * [2021/03/27]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/11/30]
#     - starting

################################################################################
import os
import re
import sys
import csv
import json
import yaml
import dpath.util
# from io import StringIO
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
# from alabs.common.util.vvjson import get_xpath
# try:
#     from collections.abc import Mapping, Iterable
# except ImportError:
#     from collections import Mapping, Iterable


################################################################################
OPS = [
    'get', 'search', 'values', 'set', 'new',
]


################################################################################
def csv_dump(d, ofp):
    # only list is possible
    if not isinstance(d, list):
        raise ValueError(f'CSV output needs list but "{type(d)}"')
    # only dict type for each rd is possible
    for rd in d:
        if not isinstance(rd, dict):
            raise ValueError(f'CSV output needs item of list must dict but "{type(d)}"')

    c = csv.writer(ofp, lineterminator='\n')
    # get header
    header = list()
    for rd in d:
        for k in rd.keys():
            if k not in header:
                header.append(k)
    c.writerow(header)
    # get csv rd
    for rd in d:
        row = list()
        for h in header:
            if h in rd:
                row.append(str(rd[h]))
            else:
                row.append('')
        c.writerow(row)


################################################################################
@func_log
def ext_job(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        if not os.path.exists(argspec.in_file):
            raise IOError('Cannot read file "%s"' % argspec.in_file)
        _, ext = os.path.splitext(argspec.in_file)
        if ext.lower() in ('.json', '.jsn'):
            with open(argspec.in_file, encoding=argspec.encoding) as ifp:
                d = json.load(ifp)
        elif ext.lower() in ('.yaml', '.yml'):
            with open(argspec.in_file, encoding=argspec.encoding) as ifp:
                if yaml.__version__ >= '5.1':
                    # noinspection PyUnresolvedReferences
                    d = yaml.load(ifp, Loader=yaml.FullLoader)
                else:
                    d = yaml.load(ifp)
        else:
            raise ValueError('Input file extension must one of {"json", "jsn", "yaml", "yml"}')
        try:
            if argspec.op == 'get':
                ed = dpath.util.get(d, argspec.dpath)
            elif argspec.op == 'search':
                ed = dpath.util.search(d, argspec.dpath)
            elif argspec.op == 'values':
                ed = dpath.util.values(d, argspec.dpath)
            elif argspec.op == 'set':
                val = argspec.set_value
                if isinstance(val, str):
                    val = val.strip()
                if val[0] in ('[', '{'):
                    val = eval(val)
                ed = dpath.util.set(d, argspec.dpath, val)
                # ed contains the number of set so re-return input json
                ed = d
            elif argspec.op == 'new':
                val = argspec.set_value
                if isinstance(val, str):
                    val = val.strip()
                if val[0] in ('[', '{'):
                    val = eval(val)
                ed = dpath.util.new(d, argspec.dpath, val)

        except KeyError:
            msg = f'Invalid key "{argspec.dpath}"'
            mcxt.logger.error(msg)
            sys.stderr.write(msg)
            return 1
        ofp = sys.stdout
        if argspec.output_format == 'JSON':
            json.dump(ed, ofp)
        elif argspec.output_format == 'YAML':
            yaml.dump(ed, ofp)
        elif argspec.output_format == 'CSV':
            csv_dump(ed, ofp)
        sys.stdout.flush()
        return 0
    except Exception as e:
        msg = 'Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write(msg)
        return 2
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
        display_name='JSON/YAML Ext',
        icon_path=get_icon_path(__file__),
        description='Extract data from JSON/YAML file',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--output-format', default='JSON', action='store',
                          display_name='Specify Output Format',
                          choices=['JSON', 'YAML', 'CSV'],
                          help='output format, default is [[csv]]')
        mcxt.add_argument('--set-value', action='store',
                          display_name='Set/New Value',
                          help='Value for set or new operation')
        mcxt.add_argument('--encoding',
                          display_name='Encoding', default='utf-8',
                          help='Encoding for JSON file, default is "utf-8"')
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', action='store',
                          display_name='Operation',
                          choices=OPS, default='get',
                          help='json/yaml file to handle')
        mcxt.add_argument('in_file', action='store',
                          display_name='JSON/YAML file',
                          input_method='fileread',
                          help='json/yaml file to handle')
        # mcxt.add_argument('out_file', action='store',
        #                   display_name='Output file which format may be JSON, YAML or CSV',
        #                   input_method='filewrite',
        #                   help='json/yaml/csv file to output')
        mcxt.add_argument('dpath', action='store',
                          help='dpath like notation to extract from JSON (/x/y/z)')
        argspec = mcxt.parse_args(args)
        return ext_job(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
