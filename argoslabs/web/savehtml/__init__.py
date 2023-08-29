#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.web.savehtml`
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
#  * [2020/08/13]
#     - starting

################################################################################
import os
import sys
import shutil
import requests
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class ResponseError(Exception):
    pass


################################################################################
HTML_METHODS = {
    'GET': requests.get,
    'POST': requests.post,
    'PUT': requests.post,
    'DELETE': requests.delete,
}


################################################################################
@func_log
def do_savehtml(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    # noinspection PyBroadException
    try:
        reqf = HTML_METHODS.get(argspec.op, None)
        if reqf is None:
            raise ValueError(f'Invalid op "{argspec.op}"')
        headers = {
            'User-agent': argspec.user_agent,
        }
        r = reqf(argspec.url, headers=headers, stream=True)
        if r.status_code // 10 != 20:
            raise ResponseError(f'Response Error: WEB return '
                                f'{r.status_code}')
        with open(argspec.htmlfile, 'wb') as ofp:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, ofp)
        print(os.path.abspath(argspec.htmlfile), end='')
        return 0
    except ResponseError as err:
        msg = f'Getting content from URL "{argspec.url}" {str(err)}'
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 2
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
        display_name='Html Extract',
        icon_path=get_icon_path(__file__),
        description='''Download using URL and save as HTML file.''',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('url',
                          display_name='URL',
                          help='URL to save')
        mcxt.add_argument('op',
                          display_name='Req Method', choices=list(HTML_METHODS.keys()),
                          default='GET',
                          help='HTTP method to request')
        mcxt.add_argument('htmlfile',
                          display_name='HTML File',
                          input_method='filewrite',
                          help='HTML file to write')

        # ##################################### for app dependent options
        mcxt.add_argument('--user-agent',
                          display_name='User Agent',
                          default='Mozilla/5.0',
                          help='Rule Specification file for extracting. File must has extension of {".yaml", ".jsn", ".yaml", "yml"}')

        argspec = mcxt.parse_args(args)
        return do_savehtml(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
