#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_servise_jp.chatwork_notification`
====================================
.. moduleauthor:: Taiki Shimasaki <shimasaki@argos-service.com>
.. note:: ARGOS-LABS License

Description
===========
Chatwork notification plugin
"""
# Authors
# ===========
#
# * Taiki Shimasaki
#
# Change Log
# --------
#
#  * [2020/06/24]
#     - Create
#  * [2020/07/01]
#     - Add TO, file upload

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import requests
import mimetypes
import json

################################################################################
class ChatwrokAPI(object):
    # ==========================================================================
    ENDPOINT = 'https://api.chatwork.com/v2'

    # ==========================================================================
    def __init__(self, api_key, room_id, message):
        self.api_key = api_key
        self.room_id = room_id
        self.message = message
        self.post_url = '{}/rooms/{}/messages'.format(self.ENDPOINT, self.room_id)
        self.params = {'body': self.message}
        self.response = None
        self.unread = None
        self.file = None
        if self.api_key == '':
            raise IOError('')
        else:
            self.headers = {'X-ChatWorkToken': self.api_key}

    # ==========================================================================
    def mark_unread(self, unread):
        self.unread = unread
        if self.unread == 'OFF':
            self.unread = '0'
        elif self.unread == 'ON':
            self.unread = '1'
        else:
            pass
        self.post_url += '&self_unread={}'.format(self.unread)

    # ==========================================================================
    def check_destination(self, to):
        self.to = to
        if str.isdecimal(self.to) == True:
            self.message = '[To:{}]\n{}'.format(self.to, self.message)
        elif str.lower(self.to) == 'all':
            self.message = '[toall]\n{}'.format(self.message)
        else:
            pass
        self.params = {'body': self.message}

    # ==========================================================================
    def check_files(self, file):
        self.file = file
        self.post_url = self.post_url.replace('messages', 'files')
        if not os.path.exists(self.file):
            raise IOError('Cannot read file {}'.format(self.file))
        else:
            pass
        self.mime = mimetypes.guess_type(self.file)[0]
        self.filename = os.path.basename(self.file)
        self.filedata = open(self.file, 'rb').read()
        self.files = {
            'file': (self.filename, self.filedata, self.mime),
            'message': self.message
        }

    # ==========================================================================
    def send_files(self):
        self.response = requests.post(self.post_url, headers=self.headers, files=self.files)
        jd = self.response.json()
        json.dump(jd, sys.stdout)

    # ==========================================================================
    def send_files_only(self, file):
        self.file = file
        self.post_url = '{}/rooms/{}/files'.format(self.ENDPOINT, self.room_id)
        if not os.path.exists(self.file):
            raise IOError('Cannot read file {}'.format(self.file))
        else:
            pass
        self.mime = mimetypes.guess_type(self.file)[0]
        self.filename = os.path.basename(self.file)
        self.filedata = open(self.file, 'rb').read()
        self.files = {
            'file': (self.filename, self.filedata, self.mime)
        }
        self.response = requests.post(self.post_url, headers=self.headers, files=self.files)
        jd = self.response.json()
        json.dump(jd, sys.stdout)

    # ==========================================================================
    def send_message(self):
        self.response = requests.post(self.post_url, headers=self.headers, params=self.params)
        jd = self.response.json()
        json.dump(jd, sys.stdout)


################################################################################
@func_log
def chatwork_send(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        ms = ChatwrokAPI(argspec.api_key, argspec.room_id, argspec.message)
        if argspec.unread and argspec.file:
            ms.mark_unread(argspec.unread)
            ms.send_message()
            ms.send_files_only(argspec.file)
        else:
            if argspec.unread:
                ms.mark_unread(argspec.unread)
            else:
                pass
            if argspec.to:
                ms.check_destination(argspec.to)
            else:
                pass
            if argspec.file:
                ms.check_files(argspec.file)
                ms.send_files()
            else:
                pass
            ms.send_message()
        mcxt.logger.info('>>>end...')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stdout.write('%s%s' % (msg, os.linesep))
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

        owner='ARGOS-SERVICE-JAPAN',
        group='5',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Chatwork Notification',
        icon_path=get_icon_path(__file__),
        description='Send notification using Chatwork API',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('api_key',
                          display_name='API TOKEN',
                          input_method='password',
                          help='Chatwork API Token')
        mcxt.add_argument('room_id',
                          display_name='Room ID',
                          help='Chatwork Room ID')
        mcxt.add_argument('message',
                          display_name='Message')
        # ######################################## for app dependent options
        mcxt.add_argument('--unread',
                          display_name='Mark Unread',
                          default='OFF',
                          choices=['OFF', 'ON'],
                          help='Mark as unread')
        mcxt.add_argument('--to',
                          display_name='TO User',
                          help='Specify the destination, UserID or All')
        # Need select file type?
        mcxt.add_argument('--file',
                          display_name='Attachment File',
                          input_method='fileread',
                          help='Select your attachment file')
        argspec = mcxt.parse_args(args)
        return chatwork_send(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
