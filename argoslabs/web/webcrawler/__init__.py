#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.web.webcrawler`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Web Crawler
"""
# Authors
# ===========
#
# * Kyobong An
#
# --------
#
#  * [2023/06/21]
#     - starting

################################################################################
import re
import os
import sys
import requests
from bs4 import BeautifulSoup
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
# noinspection PyBroadException
class Webcrawler(object):
    def __init__(self, argspec, mcxt):
        self.argspec = argspec
        self.url = argspec.url
        self.width = argspec.width
        self.width_url = argspec.width_url
        self.depth = argspec.depth
        self.depth_url = argspec.depth_url
        # self.depth_url = 'https://www.bobaedream.co.kr/view?code=best&No='
        # self.domain_name = 'https://www.bobaedream.co.kr'
        self.domain_name = argspec.domain_name
        self.is_text = argspec.text_only
        self.soup_list = []
        self.soup_width_list = []
        # 수집한 url : 중복된 수집을 방지하기위함 / 너비탐색은 이중배열로 구성
        self.last_depth_url = [argspec.url]
        self.last_width_url = [[argspec.url]]
        # 현재 수집중인 페이지의 링크 체크
        self.links = []
        # 현재 수집중인 페이지의
        self.width_links = []

        # 연결 시도 횟수 / 간혹 페이지가 연결안될 경우가 있음 기본값 1회
        self.connection_attempt = argspec.connection_attempt

        # mcxt logger
        self.logger = mcxt

    # ==========================================================================
    @staticmethod
    def _get_safe_next_filename(fn):
        fn, ext = os.path.splitext(fn)
        for n in range(1, 1000000):
            nfn = f'{fn} ({n})' + ext
            if not os.path.exists(nfn):
                return nfn

    # ==========================================================================
    @staticmethod
    def _get_safe_width_filename(fn):
        fn, ext = os.path.splitext(fn)
        # ' (4)' or ' (1-3)
        if not re.search(r'\s\(([0-9]*)\)$|\s\(([0-9]+-+[0-9]*)\)$', fn):
            for n in range(1, 1000000):
                nfn = f'{fn} (0-{n})' + ext
                if not os.path.exists(nfn):
                    return nfn
        else:
            for n in range(1, 1000000):
                nfn = f'{fn.rpartition(")")[0]}-{n})' + ext
                if not os.path.exists(nfn):
                    return nfn

    # ==========================================================================
    def get_link_list(self, soup):
        a_s = soup.find_all('a')
        for a in a_s:
            if a.get('href'):
                href = a.get('href')
                if href.startswith('/'):
                    href = self.domain_name + href
                self.links.append(href)

    # ==========================================================================
    def get_width(self, dep_num):
        for width_num in range(self.width):
            width_url = None
            if self.links:
                if self.width_url:
                    for link in self.links:
                        # TODO: 앞부분비교만으로 부족할 가능성이 있음. 정규식같은 다른 비교방법필요.
                        if link.startswith(self.width_url) and link not in self.last_width_url[dep_num]:
                            width_url = link
                            break
                    if not width_url or width_url == self.last_width_url[dep_num][-1]:
                        self.logger.debug(f'No links on this page meet the criteria. current url: {width_url}  (depth)')
                        break
                else:
                    width_url = self.links[0]

            for i in range(self.connection_attempt):
                try:
                    response = requests.get(width_url)
                    break
                except Exception as e:
                    self.logger.debug(f'retry {i+1}')
                    self.logger.debug(e)
                    continue

            if self.argspec.encoding:
                response.encoding = self.argspec.encoding
            html_t = response.text
            soup = BeautifulSoup(html_t, self.argspec.parser)
            if self.argspec.text_only:
                self.soup_list[dep_num].append(soup.text)
            else:
                self.soup_list[dep_num].append(soup.prettify())

            self.last_width_url[dep_num].append(width_url)

    # ==========================================================================
    def get_html(self):
        for dep_num in range(self.depth + 1):
            if self.links:
                if self.depth_url:
                    for link in self.links:
                        # TODO: 앞부분비교만으로 부족할 가능성이 있음. 정규식같은 다른 비교방법필요.
                        if link.startswith(self.depth_url) and link not in self.last_depth_url:
                            self.url = link
                            break
                    if self.url == self.last_depth_url[-1]:
                        self.logger.debug(f'No links on this page meet the criteria. current url: {self.url}  (depth)')
                        break
                else:
                    self.url = self.links[0]

            for i in range(self.connection_attempt):
                try:
                    response = requests.get(self.url)
                    break
                except Exception as e:
                    self.logger.debug(f'retry {i+1}')
                    self.logger.debug(e)
                    continue

            if self.argspec.encoding:
                response.encoding = self.argspec.encoding
            html_t = response.text
            soup = BeautifulSoup(html_t, self.argspec.parser)
            if self.argspec.text_only:
                self.soup_list.append([soup.text])
            else:
                self.soup_list.append([soup.prettify()])

            # 현재 페이지 내에 링크 수집 self.links에 저장
            self.get_link_list(soup)
            self.last_depth_url.append(self.url)
            # depth 별로 width의 url을 순서대로 저장
            self.last_width_url.append([self.url])
            # width 수집
            self.get_width(dep_num)

        if self.argspec.save_file:
            for dep_num, out in enumerate(self.soup_list):
                self.save(out)
        else:
            for outs in self.soup_list:
                for out in outs:
                    print(out)

    def save(self, soup_list: list):
        save_file_path = self.argspec.save_file
        if os.path.exists(save_file_path):
            save_file_path = self._get_safe_next_filename(save_file_path)
        # depth로 수집할경우 (1) (2) / width로 수집할경우 (1-1), (1-2) ...
        # 맨처음페이지의 경우 width는 뒤에 (0-1), (0-2) ...
        for soup in soup_list:
            save_width_file_path = save_file_path
            if os.path.exists(save_file_path):
                save_width_file_path = self._get_safe_width_filename(save_file_path)
            with open(save_width_file_path, 'w', encoding='utf-8') as f:
                f.write(soup)
            print(save_width_file_path)


################################################################################
@func_log
def func(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        w = Webcrawler(argspec, mcxt.logger)
        w.get_html()
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99
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
            output_type='text',
            display_name='Web Crawler',
            icon_path=get_icon_path(__file__),
            description='Get the HTML source from the web.',
    ) as mcxt:
        # #####################################  for app dependent parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('url',
                          display_name='URL',
                          help='HTTP[S] URL')
        # ######################################  for app optional parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('--save-file', nargs='?', default=None,
                          show_default=True,
                          display_name='Save File',
                          input_method='filewrite',
                          help='save result to file')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--domain-name',
                          show_default=True,
                          display_name='Domain Name',
                          input_group='Internal link options',
                          help='The domain name to be prepended to the link path starting with "/"')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--depth-url',
                          show_default=True,
                          display_name='Depth URL',
                          input_group='Internal link options',
                          help='Enter the URL path to continuously crawl.')
        mcxt.add_argument('--depth', type=int, default=0,
                          show_default=True,
                          display_name='Depth',
                          input_group='Internal link options',
                          help='depth. default = 0')
        mcxt.add_argument('--width-url',
                          show_default=True,
                          display_name='Width URL',
                          input_group='Internal link options',
                          help='Enter the URL path to continuously crawl.')
        mcxt.add_argument('--width', type=int, default=0,
                          show_default=True,
                          display_name='Width',
                          input_group='Internal link options',
                          help='width. default = 0')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--parser',
                          display_name='HTML Parser',
                          # default='html.parser',
                          default='lxml',
                          choices=['lxml', 'html.parser'],
                          help='HTML parse type, default is [[lxml]]')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--text-only', display_name='Text Only',
                          action='store_true',
                          help='Gets only text from HTML source code.')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--connection-attempt', display_name='Connection Attempt',
                          type=int, default=1,
                          help='Setting the number of connection attempts')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--encoding', default='utf-8',
                          display_name='Encoding',
                          help='Encoding for web page')

        argspec = mcxt.parse_args(args)
        return func(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
