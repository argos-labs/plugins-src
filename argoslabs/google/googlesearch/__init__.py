#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
====================================
 :mod:`argoslabs.google.googlesearch`
====================================
.. moduleauthor:: Myeongkook Park <myeongkook@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
#
#
# * Myeongkook Park
# * Wanjin Choi
# Change Log
# --------
# [2025.05.27]
#  - 검색결과 10으로 고정되어있던 것을 옵션에 따라 결과값 나오도록 변경함.


################################################################################
import os
import sys
import csv
import traceback
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from googleapiclient.discovery import build

search_type = ['Web', 'Image']

################################################################################
@func_log
def customsearch(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """

    result_list = []
    # 확장자에 '.' 제거 ex : '.doc' -> 'doc'
    if argspec.fileType is not None:
        argspec.fileType = argspec.fileType.replace(".", "")

    search_count = round(int(argspec.count)/10)

    if argspec.searchType == 'Image':
        type_search = 'image'
        header = ['title', 'link', 'fileFormat', 'contextLink']
    else:
        type_search = 'searchTypeUndefined'
        header = ['title', 'link', 'snippet']
    try:
        mcxt.logger.info('>>>starting...')
        service = build("customsearch", "v1",
                        developerKey=argspec.key)
        result = service.cse().list(
            q=argspec.query,
            cx=argspec.cx,
            num=argspec.count,
            searchType=type_search,
            dateRestrict=argspec.dateRestrict,
            exactTerms=argspec.exactTerms,
            fileType=argspec.fileType,
            excludeTerms=argspec.excludeTerms,
            siteSearch=argspec.siteSearch
        ).execute()
        result_list.append(result)

        if search_count > 1:
            for i in range(search_count - 1):
                result = service.cse().list(
                    #검색키워드
                    q=argspec.query,
                    cx=argspec.cx,
                    num=argspec.count,
                    searchType=type_search,
                    #날짜기준 필터링 (d5는 최근 5일)
                    dateRestrict=argspec.dateRestrict,
                    #결과에 반드시 포함되어야하는 단어
                    exactTerms=argspec.exactTerms,
                    fileType=argspec.fileType,
                    # 결과에 제거해야되는단어
                    excludeTerms=argspec.excludeTerms,
                    #특정사이드
                    siteSearch=argspec.siteSearch,
                    start=result['queries']['nextPage'][0]['startIndex'],
                ).execute()
                result_list.append(result)
        c = csv.writer(sys.stdout, lineterminator='\n')
        c.writerow(header)
        for i in result_list:
            for r in i['items']:
                row = list()
                for h in header:
                    if h in r:
                        row.append(r[h])
                    elif h == 'contextLink':
                        row.append(r['image'][h])
                c.writerow(row)
        mcxt.logger.info('>>>end...')
        return 0
    except Exception as err:
        traceback.print_exc()
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
            group='9',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Google Search API',
            icon_path=get_icon_path(__file__),
            description='Search for Website or Image in Google by specifying search criteria.',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('key',
                          display_name='API Key',
                          input_method='password',
                          help='You can obtain the key from the following URL:https://developers.google.com/custom-search/v1/introduction')
        mcxt.add_argument('cx',
                          display_name='Search Engine ID',
                          input_method='password',
                          help='You can obtain the key from the following URL:https://programmablesearchengine.google.com')
        mcxt.add_argument('query',
                          display_name='Search Keyword',
                          help='Enter search keyword')
        mcxt.add_argument('searchType',
                          display_name='Search Type',
                          choices=search_type,
                          default=search_type[0],
                          help='Sets the type of search. The default is web site search.')
        mcxt.add_argument('count',
                          display_name='Number of Result',
                          type=int,
                          default=10,
                          help='Set the number of search results. Default is [10]')
        # ######################################## for app dependent options
        # Custom Search Json API Manual https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
        # 필수포함 단어 Type: str
        mcxt.add_argument('--exactTerms',
                          display_name='ExactTerms',
                          help='Identifies a phrase that all documents in the search results must contain.')
        # 검색기간 설정 Type: str d,w,m,y
        mcxt.add_argument('--dateRestrict',
                          display_name='DateRestrict',
                          help='Restricts results to URLs based on date.\n ex : -1 weak = w1, -5 days = d5')
        mcxt.add_argument('--fileType',
                          display_name='FileType',
                          help='Restricts results to files of a specified extension. A list of file types indexable by Google can be found in Search Console Help Center.("https://support.google.com/webmasters/answer/35287")')
        mcxt.add_argument('--excludeTerms',
                          display_name='ExcludeTerms',
                          help='Identifies a word or phrase that should not appear in any documents in the search results.')
        mcxt.add_argument('--siteSearch',
                          display_name='SiteSearch',
                          help='Specifies a given site which should always be included or excluded from results')
        argspec = mcxt.parse_args(args)
        return customsearch(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
