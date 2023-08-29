#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.web.bsoup_table`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS extract tables from a html file using beautifulsoup
"""
# Authors
# ===========
#
# * Irene Cho
#
# --------
#
#  * [2021/03/23]
#     - starting

################################################################################
import os
import sys
import shutil
import requests
from bs4 import BeautifulSoup

from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class ResponseError(Exception):
    pass


################################################################################
class bs4_table(object):
    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.rng = argspec.rng
        self.idx = argspec.idx
        self.substr = argspec.substr
        if not self.idx:
            self.idx = []
        if self.rng:
            r = self.rng.split(':')
            self.idx += range(int(r[0]), int(r[1]) + 1)

    # ==========================================================================
    @staticmethod
    def alltab(all_table):
        res = []
        for table in all_table:
            for table_row in table.findAll('tr'):
                h = table_row.findAll('th')
                c = table_row.findAll('td')
                re = []
                if h:
                    if len(res) > 0:
                        res.append([])
                    for column in h:
                        re.append(column.text.replace('\n', ' ').strip())
                    res.append(re)
                if c:
                    for column in c:
                        re.append(column.text.replace('\n', ' ').strip())
                    res.append(re)
        return res

    # ==========================================================================
    def by_idx(self, all_table):
        final_res = []
        for i in self.idx:
            _tab = all_table[i - 1]
            res = []
            for row in _tab.findAll('tr'):
                h = row.findAll('th')
                c = row.findAll('td')
                temp = []
                if h:
                    for ent in h:
                        temp.append(ent.text.replace('\n', ' ').strip())
                    res.append(temp)
                if c:
                    for column in c:
                        temp.append(column.text.replace('\n', ' ').strip())
                    res.append(temp)
            if len(final_res) > 0:
                final_res.append([])
            final_res += res
        return final_res

    # ==========================================================================
    def by_substr(self, all_table):
        i, n = 0, len(all_table)
        final_res = []
        while n > 0:
            find_tab = False
            res = []
            _tab = all_table[i]
            for row in _tab.findAll('tr'):
                h = row.findAll('th')
                c = row.findAll('td')
                temp = []
                if h:
                    for ent in h:
                        val = ent.text.replace('\n', ' ').strip()
                        temp.append(val)
                        if self.substr == val:
                            find_tab = True
                    res.append(temp)
                if c:
                    for ent in c:
                        val = ent.text.replace('\n', ' ').strip()
                        temp.append(val)
                        if self.substr == val:
                            find_tab = True
                    res.append(temp)
            if find_tab:
                if len(final_res) > 0:
                    final_res.append([])
                final_res += res
            i += 1
            n -= 1
        return final_res


################################################################################
@func_log
def tab(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if argspec.url:
            re = requests.get(argspec.url, allow_redirects=True)
            if re.status_code // 10 != 20:
                raise ResponseError(f'Response Error: WEB return '
                                    f'{re.status_code}')
            html = re.content
        else:
            with open(argspec.filepath, encoding=argspec.encoding) as f:
                html = f.read()
            f.close()
        soup = BeautifulSoup(html, features="lxml")
        all_table = soup.find_all("table")
        cl = bs4_table(argspec)
        if argspec.idx or argspec.rng:
            r = cl.by_idx(all_table)
        elif argspec.substr:
            r = cl.by_substr(all_table)
        else:
            r = cl.alltab(all_table)
        for i, ent in enumerate(r):
            if i == len(r) - 1:
                print(','.join([ent0 for ent0 in ent]), end='')
            else:
                print(','.join([ent0 for ent0 in ent]))
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
    with ModuleContext(
            owner='ARGOS-LABS',
            group='10',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='HTML Table',
            icon_path=get_icon_path(__file__),
            description='Extract tables from html',
    ) as mcxt:
        # ##################################### for app dependent parameters
        # ##################################### for app optional parameters
        mcxt.add_argument('--url', show_default=True,
                          display_name='URL',
                          input_group='radio=url_or_file;default',
                          help='URL to save')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--filepath', display_name='HTML File',
                          show_default=True,
                          input_method='fileread',
                          input_group='radio=url_or_file',
                          help='An absolute filepath of a html file')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--idx', display_name='Table Index', type=int,
                          input_group='table index',
                          action='append', help='Multiple indexes of tables')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--rng', display_name='Range of Table',
                          input_group='table index',
                          help='Range of tables')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--substr', display_name='String to Find',
                          help='Find tables which includes a specific string')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--encoding', display_name='Encoding',
                          default='utf-8',
                          help='Choose a proper encoding')
        # ----------------------------------------------------------------------
        # mcxt.add_argument('--output', display_name='Output Path',
        #                   input_method='filewrite',
        #                   help='An absolute filepath to save a file')
        argspec = mcxt.parse_args(args)
        return tab(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
