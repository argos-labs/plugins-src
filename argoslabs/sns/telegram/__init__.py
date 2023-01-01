#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.sns.telegram`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Telegram
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
#  * [2020/07/22]
#     - build a plugin
#  * [2020/07/22]
#     - starting

################################################################################
import os
import sys
# import csv
from telepot import Bot
# from tempfile import gettempdir
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit


################################################################################
class telegramAPI(object):
    OP_TYPE = ['Find a chatid', 'Send a file or message']

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.token = argspec.token
        self.bot_ = Bot(self.token)
        self.chatid = argspec.chatid

    # ==========================================================================
    def chatid_(self):
        try:
            lst, key = [], []
            response = self.bot_.getUpdates()
            if len(response) > 0:
                for i in response:
                    if 'channel_post' in i:
                        t = i['channel_post']['chat']
                        key += list(t.keys())
                        lst.append(t)
                    if 'message' in i:
                        t = i['message']['chat']
                        key += list(t.keys())
                        lst.append(t)
                key = list(set(key))
                print(','.join(str(i) for i in key))
                lst = map(dict, set(tuple(sorted(d.items())) for d in lst))
                for i in lst:
                    d = dict.fromkeys(key)
                    d.update(i)
                    print(','.join(str(i) for i in list(d.values())))
        except Exception as e:
            print(str(e), end='')
        return 0

    # ==========================================================================
    # def chatid_(self):
    #     try:
    #         lst, key = [], []
    #         response = self.bot_.getUpdates()
    #         if self.argspec.folder:
    #             k = os.path.join(self.argspec.folder, 'chat.csv')
    #         else:
    #             k = os.path.join(gettempdir(), 'chat.csv')
    #         if len(response) > 0:
    #             with open(k, 'w', encoding='utf-8') as f:
    #                 c = csv.writer(f, lineterminator='\n')
    #                 for i in response:
    #                     if 'channel_post' in i:
    #                         t = i['channel_post']['chat']
    #                         key += list(t.keys())
    #                         lst.append(t)
    #                     if 'message' in i:
    #                         t = i['message']['chat']
    #                         key += list(t.keys())
    #                         lst.append(t)
    #                 key = list(set(key))
    #                 lst = map(dict, set(tuple(sorted(d.items())) for d in lst))
    #                 c.writerow([i for i in key])
    #                 for i in lst:
    #                     d = dict.fromkeys(key)
    #                     d.update(i)
    #                     c.writerow([i for i in d.values()])
    #             f.close()
    #         print()
    #     except Exception as e:
    #         print(str(e), end='')
    #     return 0
    #
    # ==========================================================================
    def sendmsg(self):
        try:
            self.bot_.sendMessage(self.chatid, self.argspec.msg)
            print(self.argspec.successoutput, end='')
        except Exception as e:
            print(str(e), end='')
        return 0

    # ==========================================================================
    def sendfile(self):
        try:
            with open(self.argspec.file, 'rb') as f:
                self.bot_.sendDocument(self.chatid, f)
                print(self.argspec.successoutput, end='')
            f.close()
        except Exception as e:
            print(str(e), end='')
        return 0


################################################################################
@func_log
def do_telegram(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        te = telegramAPI(argspec)
        if argspec.op == 'Find a chatid':
            return te.chatid_()
        else:
            if argspec.msg:
                return te.sendmsg()
            elif argspec.file:
                return te.sendfile()
            else:
                print("Cannot find messages or files", end='')
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
            group='5',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Telegram',
            icon_path=get_icon_path(__file__),
            description='Send Message or Files to Telegram',
    ) as mcxt:
        # ######################################### for app dependent options
        mcxt.add_argument('--chatid', display_name='Chat Id',
                          show_default=True, help='Chat Id')
        # ----------------------------------------------------------------------
        # mcxt.add_argument('--folder', display_name='Chat Folder',
        #                   help='A folder to save chatid.csv', input_method='fileread')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--msg', display_name='Message',
                          help='message')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--file', display_name='File',
                          help='File', input_method='fileread')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--successoutput', display_name='Success Output',
                          default=0, help='The output of success in STU')
        # ###################################### for app dependent parameters
        mcxt.add_argument('op', display_name='Telegram function type',
                          choices=telegramAPI.OP_TYPE,
                          help='type of operation')
        # ----------------------------------------------------------------------
        mcxt.add_argument('token', display_name='Token',
                          help='token from telegram')
        argspec = mcxt.parse_args(args)
        return do_telegram(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
