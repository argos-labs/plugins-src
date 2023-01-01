#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.sns.slack`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Slack
"""
#
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2020/07/20]
#     - build a plugin
#  * [2020/07/20]
#     - starting

################################################################################
import os
import sys
import slack
from slacker import Slacker
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit


################################################################################
# noinspection PyBroadException
class SlackAPI(object):
    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.channel = argspec.channel

    # ==========================================================================
    def sendmsg(self):
        client = slack.WebClient(token=self.argspec.user_token)
        try:
            response = client.chat_postMessage(channel=self.channel,
                                               text=self.argspec.text)
            if response['ok']:
                print(self.argspec.successoutput, end='')
        except Exception as e:
            print(str(e), end='')
        return 0

    # ==========================================================================
    def sendfile(self):
        client = slack.WebClient(token=self.argspec.user_token)
        try:
            response = client.files_upload(channels=self.channel,
                                           file=self.argspec.file)
            if response['ok']:
                print(self.argspec.successoutput, end='')
        except Exception as e:
            print(str(e), end='')
        return 0

    # ==========================================================================
    def botmsg(self):
        slack_ = Slacker(token=None, incoming_webhook_url=self.argspec.webhookurl)
        if not self.argspec.text:
            print("Cannot find a message", end='')
            return 0
        try:
            res = slack_.incomingwebhook.post({"text": self.argspec.text})
            if res.status_code % 200 == 0:
                print(self.argspec.successoutput, end='')
            else:
                print(f'Invalid Response {res.status_code} from the url', end='')
        except Exception as e:
            print(str(e), end='')
        return 0

################################################################################
@func_log
def do_slack(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        slc = SlackAPI(argspec)
        if argspec.user_token:
            if argspec.text:
                return slc.sendmsg()
            elif argspec.file:
                return slc.sendfile()
            else:
               print("Cannot find messages or files", end='')
            return 0
        elif argspec.webhookurl:
            return slc.botmsg()
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
            group='5',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Slack',
            icon_path=get_icon_path(__file__),
            description='Send Message or Files to Slack',
    ) as mcxt:
        # ######################################### for app dependent options
        mcxt.add_argument('--text', display_name='Message',
                          help='message to send to Slack')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--file', display_name='File',
                          help='file to send', input_method='fileread')
        # ###################################### for app dependent parameters
        mcxt.add_argument('--webhookurl', display_name='Incoming Webhook URL',
                          show_default=True, help='webhookurl')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--user_token', display_name='User Token',
                          show_default=True,
                          help='Bot token')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--channel', display_name='Channel',
                          help='Channel in Slack')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--successoutput', display_name='Success Output',
                          default=0, help='The output of success in STU')
        # ----------------------------------------------------------------------
        argspec = mcxt.parse_args(args)
        return do_slack(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
