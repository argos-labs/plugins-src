#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.chatwork_get_messages`
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
#  * [2021/04/20]
#     Create

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import requests
import json


################################################################################
class Get_Message(object):

    # ==========================================================================
    ENDPOINT = 'https://api.chatwork.com/v2'

    # ==========================================================================
    def __init__(self,  api_key, room_id):
        self.api_key = api_key
        self.room_id = room_id

        self.force = None

        self.post_url = '{}/rooms/{}/messages'.format(self.ENDPOINT, self.room_id)

        if self.api_key == '':
            raise IOError('')
        else:
            self.headers = {'X-ChatWorkToken': self.api_key}

        self.response = None
        self.key_name = None
        self.out_num = None

    # ==========================================================================
    def check_force(self, force):
        self.force = force
        if self.force == 'Since Last Time':
            self.force = '0'
        elif self.force == 'Latest 100':
            self.force = '1'
        else:
            pass

        self.post_url += '?force={}'.format(self.force)

    # ==========================================================================
    def get(self, out_num, key_name):
        self.response = requests.get(self.post_url, headers=self.headers)
        if out_num:
            self.out_num = int(out_num)
        else:
            pass
        self.key_name = key_name

        if not self.response.text:
            print('No Data')

        else:
            jd = self.response.json()
            jd = jd[::-1]

            if self.out_num:
                if self.key_name:
                    if self.key_name in jd[0]:
                        for l in jd[:self.out_num]:
                            print(l[self.key_name])
                    else:
                        raise IOError('The Key \'{}\' is not exists!'.format(self.key_name))

                else:
                    for l in jd[:self.out_num]:
                        print(l)

            else:
                if self.key_name:
                    if self.key_name in jd[0]:
                        for l in jd:
                            print(l[self.key_name])
                    else:
                        raise IOError('The Key \'{}\' is not exists!'.format(self.key_name))

                else:
                    for l in jd:
                        print(l)


################################################################################
@func_log
def get_messages(mcxt, argspec):

    mcxt.logger.info('>>>starting...')
    try:
        gm = Get_Message(argspec.api_key, argspec.room_id)

        if argspec.force:
            gm.check_force(argspec.force)
        else:
            pass

        gm.get(argspec.out_num, argspec.key_name)

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
        group='5',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Chatwork GetMessages',
        icon_path=get_icon_path(__file__),
        description='Get Messages using Chatwork API',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('api_key',
                          display_name='API TOKEN',
                          input_method='password',
                          help='Chatwork API Token')
        mcxt.add_argument('room_id',
                          display_name='Room ID',
                          help='Chatwork Room ID')
        # ######################################## for app dependent options
        mcxt.add_argument('--out_num',
                          display_name='Num of Output',
                          show_default=True,
                          help='Number of messages to output.')
        mcxt.add_argument('--key_name',
                          display_name='Key Name',
                          help='Input the Key name to be extracted.')
        mcxt.add_argument('--force',
                          display_name='Target',
                          default='Latest 100',
                          choices=['Latest 100', 'Since Last Time'],
                          help='Whether to get the latest 100 messages.')

        argspec = mcxt.parse_args(args)
        return get_messages(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
