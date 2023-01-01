#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.xmlextract`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
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
#  * [2021/04/01]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/05/07]
#     - change xpath with nargs=+
#  * [2020/05/06]
#     - starting for training of Cognizant

################################################################################
import os
import sys
import csv
# noinspection PyPackageRequirements
from lxml import etree
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
# noinspection PyProtectedMember,PyBroadException
def get_xpath_data(xml_file, xpaths, include_header=True):
    if not os.path.exists(xml_file):
        raise IOError(f'Cannot get XML file "{xml_file}"')
    if not xpaths:
        raise ValueError(f'Invalid XPath')
    with open(xml_file, encoding='utf-8') as ifp:
        et = etree.parse(ifp)
        cols = []
        max_row = 0
        for xpath in xpaths:
            r = et.xpath(xpath)
            if isinstance(r, list):
                col = []
                for i, e in enumerate(r):
                    if isinstance(e, etree._Element):
                        if i == 0 and include_header:
                            col.append(e.tag)
                        col.append(e.text.strip())
            if len(col) > max_row:
                max_row = len(col)
            cols.append(col)
        c = csv.writer(sys.stdout, lineterminator='\n')
        for j in range(max_row):
            row = []
            for i in range(len(cols)):
                rv = None
                try:
                    rv = cols[i][j]
                except Exception:
                    pass
                row.append(rv)
            c.writerow(row)
        return max_row


################################################################################
@func_log
def xml_extract(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        r = get_xpath_data(argspec.xml, argspec.xpath,
                           include_header=argspec.header)
        return 0 if r > 0 else 2
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
        display_name='XML Extract',
        icon_path=get_icon_path(__file__),
        description='XML Extract plugin',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('xml', input_method='fileread',
                          display_name='XML File',
                          help='xml file to extract data')
        mcxt.add_argument('xpath', show_default=True,
                          nargs='+',
                          display_name='XPath',
                          help='one or more xpath to set the data')

        # ######################################## for app dependent options
        mcxt.add_argument('--header',
                          action='store_true',
                          display_name='Show Header',
                          help='If this flag is set header(tag) is included '
                               'in data.')

        argspec = mcxt.parse_args(args)
        return xml_extract(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
