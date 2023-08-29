#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.sns.line`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS SNS Line plugin module
"""
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2020/03/04]
#     - add icon
#  * [2020/03/04]
#     - starting

################################################################################
import os
import sys
import requests
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class LineAPI(object):
    # ==========================================================================
    URL_STATUS = 'https://notify-api.line.me/api/status'
    URL_NOTICE = 'https://notify-api.line.me/api/notify'

    # ==========================================================================
    def __init__(self, key):
        self.key = key
        self.headers = {'Authorization': 'Bearer {}'.format(self.key)}
        # for internal
        self.response = None

    # ==========================================================================
    def check_status(self):
        self.response = requests.get(self.URL_STATUS,
                                     headers=self.headers)
        if self.response.status_code // 10 != 20:
            return False
        return True

    # ==========================================================================
    def notice(self, message):
        files = {'message': (None, message)}
        self.response = requests.post(self.URL_NOTICE,
                                      headers=self.headers, files=files)
        if self.response.status_code // 10 != 20:
            raise RuntimeError(f'Invalid Response {self.response.status_code} '
                               f'from {self.URL_NOTICE}')
        jd = self.response.json()
        return jd


################################################################################
@func_log
def line_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        lv = LineAPI(argspec.key)
        if lv.check_status():
            jd = lv.notice(argspec.message)
            print('status,message')
            print(f"{jd.get('status', 'Invalid Status')},"
                  f"{jd.get('message', 'Invalid Message')}", end='' )
            return 0
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
        owner='ARGOS-LABS-SNS',
        group='5',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='LINE Notify',
        icon_path=get_icon_path(__file__),
        description='Send a notification to Line '
                    '{{https://notify-bot.line.me/doc/en/}}',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('key', display_name='token', input_method='password',
                          help='customized token')
        mcxt.add_argument('message', display_name='message',
                          # input_method='textarea',
                          help='customized message')
        argspec = mcxt.parse_args(args)
        return line_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
