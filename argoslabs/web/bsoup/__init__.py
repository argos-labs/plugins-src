#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.web.bsoup`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module web bsoup using BeautifulSoup
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/07/31]
#     - Change group "9: Utility Tools" => "10: Web Scraping"
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/05/26]
#     - find op에 name에서 td[3]과 같이 인덱스 추가 (1-based) for ASJ-480
#  * [2019/09/30]
#     - table > tbody > ... 등에서 tbody 넣거나 빼고 검색하도록 함
#  * [2019/05/31]
#     - --encoding 옵션 삭제(?) html 인코딩 상관없이 동작하도록
#  * [2019/05/22]
#     - --limit 옵션 추가
#  * [2019/05/15]
#     - re-replace 추가
#  * [2019/05/11]
#     - starting

################################################################################
import os
import re
import csv
import sys
import json
import yaml
import copy
from bs4 import BeautifulSoup
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class BSoup(object):
    # ==========================================================================
    XPATH_REC = [
        ('attr', re.compile(r'\*\[@(\w+)="([^"]+)"\]', re.IGNORECASE), 2),
        ('index', re.compile(r'(\w+)\[(\d+)\]', re.IGNORECASE), 2),
    ]

    # ==========================================================================
    def __init__(self, htmlfile, specfile, parser='html.parser', encoding='utf8',
                 limit=0):
        if not os.path.exists(htmlfile):
            raise RuntimeError('HTML file "%s" not found' % htmlfile)
        if not os.path.exists(specfile):
            raise RuntimeError('Specification file "%s" not found' % specfile)

        self.htmlfile = htmlfile
        self.specfile = specfile
        self.parser = parser
        self.encoding = encoding
        self.limit = int(limit)
        # for internal
        self.soup = None
        self.spec = None
        self.is_opened = False
        # for csv result
        self.header = list()
        self.rows = list()

    # ==========================================================================
    def open(self):
        # rb로 안 읽으면 인코딩을 찾아야 하는데, 이것이 문제임
        with open(self.htmlfile, 'rb') as ifp:
            # hstr = ifp.read()
            self.soup = BeautifulSoup(ifp, self.parser)
        _, ext = os.path.splitext(self.specfile)
        with open(self.specfile, encoding=self.encoding) as ifp:
            if ext.lower().startswith('.js'):  # try to parse as JSON
                self.spec = json.load(ifp)
            elif ext.lower().startswith('.ya'):  # try to parse as YAML
                if yaml.__version__ >= '5.1':
                    self.spec = yaml.load(ifp, Loader=yaml.FullLoader)
                else:
                    self.spec = yaml.load(ifp)
            else:
                raise RuntimeError('Specification file must has extension of {".yaml", ".jsn", ".yaml", "yml"}')
        self.is_opened = True
        return self.is_opened

    # ==========================================================================
    def close(self):
        if self.is_opened:
            self.is_opened = False

    # ==========================================================================
    @staticmethod
    def _get_kwargs(d):
        td = copy.copy(d)
        if 'op' in td:
            del td['op']
        return td

    # ==========================================================================
    def _xpath2selector(self, xp, exclude_tbody=False):
        stl = list()
        for pn in xp.split('/'):
            if not pn:
                continue
            pn = pn.lower()
            # table 과 tr 사이에 tbody가 나오는데 이는 필요없었음
            if exclude_tbody and pn in ('tbody',):
                continue
            if stl:
                stl.append(' > ')
            m_eles = list()
            for mname, rec, grp_cnt in self.XPATH_REC:
                m = rec.match(pn)
                if m:
                    m_eles.append(mname)
                    for i in range(grp_cnt):
                        m_eles.append(m.group(i+1))
                    break
            if m_eles:
                if m_eles[0] == 'attr':
                    if m_eles[1] == 'id':
                        stl.append('#%s' % m_eles[2])
                    elif m_eles[1] == 'class':
                        stl.append('.%s' % m_eles[2])
                    else:
                        raise NotImplementedError('_xpath2selector: need parse %s for beautifulsoup' % pn)
                elif m_eles[0] == 'index':
                    stl.append(m_eles[1])
                    stl.append(':nth-of-type(%s)' % m_eles[2])
            else:
                stl.append(pn)
        return ''.join(stl)

    # ==========================================================================
    def _do_csv_columns(self, spec):
        self.header = list()
        if 'columns' not in spec:
            raise RuntimeError('"columns" spec needed in "%s"' % spec)
        for col, colspec in enumerate(spec['columns']):
            if 'header' in colspec:
                self.header.append(colspec['header'])
            else:
                self.header.append('N/A')
            if 'find' not in colspec:
                raise RuntimeError('"find" spec needed in "%s"' % colspec)
            findspeclist = colspec['find']

            p_tag = self.soup

            taglist = None
            next_ndx = 0
            find_all_no_result = False
            for ndx, findspec in enumerate(findspeclist):
                if not p_tag:
                    break
                if findspec['op'] == 'select_one':
                    _kwargs = self._get_kwargs(findspec)
                    _xpath = _kwargs['xpath']
                    if 'xpath' in _kwargs:
                        _kwargs['selector'] = self._xpath2selector(_xpath)
                        del _kwargs['xpath']
                    _p_tag = p_tag.select_one(**_kwargs)
                    if _p_tag is None and 'selector' in _kwargs and _kwargs['selector'].find('tbody') >= 0:
                        _kwargs['selector'] = self._xpath2selector(_xpath, exclude_tbody=True)
                        _p_tag = p_tag.select_one(**_kwargs)
                    p_tag = _p_tag
                    next_ndx = ndx + 1
                elif findspec['op'] == 'find':
                    _kwargs = self._get_kwargs(findspec)
                    if _kwargs['name'].endswith(']'):
                        bsp = _kwargs['name'].find('[')
                        if bsp > 0:
                            ele_ndx = int(_kwargs['name'][bsp+1:-1].strip())
                            _kwargs['name'] = _kwargs['name'][:bsp]
                            _taglist = p_tag.find_all(**_kwargs)
                            p_tag = _taglist[ele_ndx - 1]
                    else:
                        p_tag = p_tag.find(**_kwargs)
                    next_ndx = ndx + 1
                elif findspec['op'] == 'find_all':
                    _kwargs = self._get_kwargs(findspec)
                    taglist = p_tag.find_all(**_kwargs)
                    next_ndx = ndx + 1
                    if not taglist:
                        find_all_no_result = True
                    break
                else:
                    raise RuntimeError('"find" spec invalid op "%s"' % findspec['op'])

            if find_all_no_result:
                break
            if not taglist:
                if not p_tag:
                    continue
                taglist = [p_tag]
            if not (taglist and isinstance(taglist, list)):
                continue

            for row, tag in enumerate(taglist):
                for findspec in findspeclist[next_ndx:]:
                    if findspec['op'] == 'select_one':
                        _kwargs = self._get_kwargs(findspec)
                        _xpath = _kwargs['xpath']
                        if 'xpath' in _kwargs:
                            _kwargs['selector'] = self._xpath2selector(_xpath)
                            del _kwargs['xpath']
                        _tag = tag.select_one(**_kwargs)
                        if _tag is None and 'selector' in _kwargs and _kwargs['selector'].find('tbody') >= 0:
                            _kwargs['selector'] = self._xpath2selector(_xpath, exclude_tbody=True)
                            _tag = tag.select_one(**_kwargs)
                        tag = _tag
                    elif findspec['op'] == 'find':
                        _kwargs = self._get_kwargs(findspec)
                        if _kwargs['name'].endswith(']'):
                            bsp = _kwargs['name'].find('[')
                            if bsp > 0:
                                ele_ndx = int(_kwargs['name'][bsp+1:-1].strip())
                                _kwargs['name'] = _kwargs['name'][:bsp]
                                _taglist = tag.find_all(**_kwargs)
                                tag = _taglist[ele_ndx - 1]
                        else:
                            tag = tag.find(**_kwargs)

                    if not tag:
                        break
                    # 경우에 따라 해당 태극 그 다음 시블링에 있는 경우가 있어서
                    # 해당 텍스트가 없으면 다음 시블링으로 넘어가 보도록 함 2019.07.10
                    while not tag.text.strip():
                        # tp = tag.parent
                        tag = tag.findNext(**_kwargs)
                        if not tag:
                            break
                    if not tag:
                        break
                if len(self.rows) <= row:
                    self.rows.append([])
                if not tag:
                    self.rows[row].append('')
                    continue
                if 'text-item' in colspec:
                    text_item = colspec['text-item']
                    rs = tag[text_item].strip()
                else:
                    rs = tag.text.strip()
                # if 'index-modular' in colspec:
                #     devisor = colspec['index-modular'].get("devisor")
                #     remainder = colspec['index-modular'].get("remainder")
                #     if row % devisor != remainder:
                #         continue
                if 'split' in colspec:
                    sv = colspec.get('split')
                    if isinstance(sv, int):
                        sl = rs.split()
                        if sv >= len(sl):
                            rs = ''
                        else:
                            rs = sl[sv]
                    elif isinstance(sv, dict):
                        sep = sv.get('separator', None)
                        ndx = sv.get('index', -1)
                        if sep and ndx >= 0:
                            sl = rs.split(sep)
                            if ndx >= len(sl):
                                rs = ''
                            else:
                                rs = sl[ndx]
                if 're-search' in colspec:
                    _match = colspec['re-search'].get("match")
                    _index = int(colspec['re-search'].get("index"))
                    rm = re.search(_match, rs)
                    rs = rm.group(_index)
                if 're-replace' in colspec:
                    _from = colspec['re-replace'].get("from")
                    _to = colspec['re-replace'].get("to")
                    if not _to:
                        _to = ''
                    if _from:
                        rs = re.sub(_from, _to, rs)
                self.rows[row].append(rs)

    # ==========================================================================
    def _print_result(self):
        skip_empty_row = False
        if 'skip-empty-row' in self.spec:
            skip_empty_row = self.spec['skip-empty-row']
        if skip_empty_row:
            del_rows = list()
            for i, row in enumerate(self.rows):
                if not any(row):
                    del_rows.append(i)
            del_rows.reverse()
            for di in del_rows:
                del self.rows[di]
        if self.rows:
            wr = csv.writer(sys.stdout, lineterminator='\n')
            wr.writerow(self.header)
            # for i, row in enumerate(self.rows):  is_empty_row 때문에 수정
            cnt = 0
            for row in self.rows:
                # if skip_empty_row and not any(row):
                #     continue
                wr.writerow(row)
                cnt += 1
                if 0 < self.limit <= cnt:
                    break
        else:
            if 'no-result' in self.spec:
                print(self.spec['no-result'])
            else:
                print("No Result")

    # ==========================================================================
    def _do_csv(self, spec):
        if 'columns' in spec:
            self._do_csv_columns(spec)
        elif 'or' in spec:
            for colspec in spec.get('or', []):
                self._do_csv_columns(colspec)
                if self.rows:
                    break
        self._print_result()
        return 0 if self.rows else 1

    # ==========================================================================
    def do_parse(self):
        if not self.is_opened:
            raise RuntimeError('First open()')
        if 'csv' in self.spec:
            spec = self.spec.get('csv', {})
            return self._do_csv(spec)
        else:
            raise RuntimeError('Not supported extraction method like {"csv"}')


################################################################################
@func_log
def do_bsoup(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    # noinspection PyBroadException
    try:
        bs = BSoup(argspec.htmlfile, argspec.spec_file,
                   parser=argspec.parser, encoding=argspec.encoding,
                   limit=argspec.limit)
        bs.open()
        return bs.do_parse()
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
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
        group='10',  # Web Scraping
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Web Extract',
        icon_path=get_icon_path(__file__),
        description='''Web HTML extracting data from extracting rule.''',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--spec-file',
                          display_name='Rule File',
                          show_default=True,
                          input_method='fileread',
                          help='Rule Specification file for extracting. File must has extension of {".yaml", ".jsn", ".yaml", "yml"}')
        mcxt.add_argument('--limit',
                          # type=int,   # TODO : 현재 STU에서 변수를 사용할 수 있어야 하므로 일단 푼다.!!
                          display_name='# of Results',
                          default=0,
                          help='Set number of result. [[0]] means no limit.')
        mcxt.add_argument('--encoding',
                          display_name='File encoding',
                          default='utf8',
                          help='File encoding, default is [[utf8]]')
        mcxt.add_argument('--parser',
                          display_name='HTML Parser',
                          # default='html.parser',
                          default='lxml',
                          choices=['lxml', 'html.parser'],
                          help='HTML parse type, default is [[lxml]]')

        # ##################################### for app dependent parameters
        mcxt.add_argument('htmlfile',
                          display_name='HTML File',
                          input_method='fileread',
                          help='HTML file to read')
        argspec = mcxt.parse_args(args)
        return do_bsoup(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
