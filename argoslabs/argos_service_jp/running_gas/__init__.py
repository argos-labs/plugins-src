#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.running_gas`
====================================
.. moduleauthor:: Taiki Shimasaki <shimasaki@argos-service.com>
.. note:: ARGOS-LABS License

Description
===========
Input Plugin Description
"""
# Authors
# ===========
#
# * Taiki Shimasaki
#
# Change Log
# --------
#
#  * [2021/08/17]
#     Create

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import requests
import json


################################################################################
class RunGAS(object):

    # ==========================================================================
    def __init__(self, url):
        self.url = url

        self.payload = {
            "data": [""]
        }

    # ==========================================================================
    def add_data(self, data):
        # print(data)
        self.payload = {
            "data": data
        }
        # print(self.payload)

    # ==========================================================================
    def post(self):
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(self.url,
                                 data=json.dumps(self.payload),
                                 headers=headers)

        if response.status_code == 200:
            print(response.text)

        else:
            print(response.text)
            raise IOError('Error: {}, Something error occurred!'
                          .format(response.status_code))

    # ==========================================================================
    def get(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            print(response.text)

        else:
            print(response.text)
            raise IOError('Error: {}, Something error occurred!'
                          .format(response.status_code))


################################################################################
@func_log
def run_gas(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        RG = RunGAS(argspec.url)

        if argspec.data:
            RG.add_data(argspec.data)

        if argspec.func == 'doPost':
            RG.post()
        elif argspec.func == 'doGet':
            RG.get()

        mcxt.logger.info('>>>end...')
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
        owner='ARGOS-SERVICE-JAPAN',
        group='3',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Running GAS',
        icon_path=get_icon_path(__file__),
        description='Running GAS published as a WebApps',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('url',
                          display_name='URL',
                          help='URL of the GAS WebApp')
        mcxt.add_argument('func',
                          display_name='Function',
                          default='doPost',
                          choices=['doPost', 'doGet'],
                          help='Select the function to be used in GAS')
        # ######################################## for app dependent options
        mcxt.add_argument('--data',
                          display_name='Params',
                          action='append',
                          help='Any additional parameters you want to send as \"params\"')

        argspec = mcxt.parse_args(args)
        return run_gas(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
