"""
====================================
 :mod:`argoslabs.web.selenium`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module to use Selenium
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/01/14]
#     - alabs.selenium 대신 alabslib.selenium으로 수정
#       <== C# ppm 에서 alabs.* 모듈과 VENV 설치시 동일 alabs.* 가 문제가 생겼음
#  * [2021/12/09]
#     - do_start의 결과를 return
#  * [2021/07/31]
#     - Change group "9: Utility Tools" => "10: Web Scraping"
#  * [2021/05/31]
#     - headless 옵션 추가
#  * [2021/04/21]
#     - alabs.selenium 버전 3.421.1428 이상 (자동 드라이버 다운로드 for Chrome, Edge)
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/12/20]
#     - get PySelenium class from alabs.selenium
#  * [2020/12/02]
#     - starting

################################################################################
import os
import re
import sys
import csv
import glob
import time
import traceback
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from alabs.common.util.vvlogger import get_logger
from tempfile import gettempdir
# for selenium
from alabslib.selenium import PySelenium
from selenium.webdriver.common.keys import Keys


################################################################################
@func_log
def do_pyselenium(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if not os.path.exists(argspec.script):
            raise IOError(f'Cannot read Script file "{argspec.script}"')
        with open(argspec.script, encoding=argspec.encoding) as ifp:
            script = ifp.read()
        params = {
            'browser': argspec.browser,
            'logger': mcxt.logger,
        }
        if argspec.parameters:
            try:
                for pl in argspec.parameters:
                    k, v = pl.split('::=', maxsplit=1)
                    params[k] = v
            except Exception:
                raise ReferenceError('parameter passing to Script')
        params['width'] = int(argspec.width)
        params['height'] = int(argspec.height)
        params['headless'] = argspec.headless
        exec(script, globals(), locals())
        globals().update(locals())
        # noinspection PyUnresolvedReferences
        return do_start(**params)
        # return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='10',  # Web Scraping
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Python Selenium',
        icon_path=get_icon_path(__file__),
        description='''Selenium Container for Python Script''',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('browser',
                          display_name='Brower to use',
                          choices=list(PySelenium.BROWSERS.keys()),
                          default='Chrome',
                          help='Select Browser for selenium web driver')
        mcxt.add_argument('script',
                          display_name='Selenium Python Script',
                          input_method='fileread',
                          help='Python Selenium Script')

        # ##################################### for app dependent options
        mcxt.add_argument('--parameters',
                          display_name='Parameters', action='append',
                          help='Parameters passing to Scirpt or URLs. Format is '
                               '"key::=value". Place holder is "{key}"')
        mcxt.add_argument('--encoding',
                          display_name='Encoding', default='utf-8',
                          help='Encoding for script, default is [[utf-8]]')
        mcxt.add_argument('--width',
                          display_name='Width', default='1200', type=int,
                          help='Browser width, default is [[1200]]')
        mcxt.add_argument('--height',
                          display_name='Height', default='800', type=int,
                          help='Browser height, default is [[800]]')
        mcxt.add_argument('--headless',
                          display_name='Headless', action='store_true',
                          help='If this flag is true then running without GUI')

        argspec = mcxt.parse_args(args)
        return do_pyselenium(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
