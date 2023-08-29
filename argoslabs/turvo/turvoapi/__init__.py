#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.turvo.turvoapi`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Splitting and Merging PDF plugin
"""
# Authors
# ===========
#
# * Irene Cho
#
# --------
#
#  * [2020/12/22]
#     - starting

################################################################################
import os
import sys
import re
import requests
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import warnings

warnings.simplefilter("ignore", ResourceWarning)


################################################################################
@func_log
def turvo(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        params = {
            "grant_type": "password",
            'client_id': argspec.client_id,
            'client_secret': argspec.client_secret,
            "username": argspec.username,
            "password": argspec.password,
            "scope": "read+trust+write",
            "type": "business"
        }
        # res = requests.post('https://my-sandbox.turvo.com/api/oauth/token',
        #                     params=params)
        url = re.sub('pub','',argspec.endpoint)+'oauth/token'
        res = requests.post(url, params=params)
        if res.status_code // 10 != 20:
            print(f'Error of API:{res.text}')
        print(res.json().get('access_token'), end='')
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
            group='turvo',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Turvo Token',
            icon_path=get_icon_path(__file__),
            description='Get a token from Turvo API',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('client_id', display_name='Client Id',
                          help='Client Id')
        # ----------------------------------------------------------------------
        mcxt.add_argument('client_secret', display_name='Client Secret',
                          help='Client Secret', input_method='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('username', display_name='Username',
                          help='Username')
        # ----------------------------------------------------------------------
        mcxt.add_argument('password', display_name='Password',
                          input_method='password', help='Password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('endpoint', display_name='Endpoint', help='Endpoint')
        # ##################################### for app optional parameters
        argspec = mcxt.parse_args(args)
        return turvo(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
