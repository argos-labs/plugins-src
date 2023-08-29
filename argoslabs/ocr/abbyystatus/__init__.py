#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.ocr.abbyystatus`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for ABBYY Status
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
#  * [2020/11/11]
#     - build a plugin
#  * [2020/11/11]
#     - starting

# multiple files

################################################################################
import os
import re
import sys
import json
import time
import base64
import requests
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit


################################################################################
class uploadAPI(object):

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.resgettask = None
        self.result_id = None
        self.result_token = None
        self.result_name = None
        msg = argspec.api_id + ':' + argspec.api_token
        msg = msg.encode('ascii')
        t = base64.b64encode(msg)
        t = 'Basic ' + t.decode("ascii")
        self.headers = {
            'Accept': 'application/json',
            'Authorization': t,
        }

    # ==========================================================================
    def task_status(self, task_id):
        pth = 'https://api-us.flexicapture.com/v2/task/' + task_id
        self.resgettask = requests.get(pth, headers=self.headers)
        t = json.loads(self.resgettask.content)
        if not self.resgettask.status_code // 10 == 20:
            raise RuntimeError(self.resgettask.content)
        return t

    # ==========================================================================
    def print_doc(self):
        t = json.loads(self.resgettask.content)
        for i in range(len(t['documents'])):
            f = t['documents'][i]['files']
            target = list(
                filter(lambda v: re.match('^target', v), list(f.keys())))
            # target_name = list((f[i]['name'] for i in target))
            for j in target:
                print('\n', end='')
                print(f"{t['id']},{f['source']['name']},{f[j]['name']},{f[j]['id']},"
                      f"{f[j]['token']}", end='')
        return 0


################################################################################
@func_log
def do_upload(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        xt = uploadAPI(argspec)
        t = None
        print('task_id,source,result_name,result_id,result_token', end='')
        for j in argspec.task_id:
            for i in range(argspec.repeat):
                t = xt.task_status(j)['status']
                if t == 'Done':
                    xt.print_doc()
                    break
                elif t == 'WaitForAction':
                    raise IOError(t)
                    # print('\n',end='')
                    # print(f'{j},WaitForAction', end='')
                    break
                else:
                    time.sleep(argspec.wait)
        #if not t in ('WaitForAction', 'Done'):
        if not t == 'Done':
            raise IOError(t)
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
            group='1',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='ABBYY Status',
            icon_path=get_icon_path(__file__),
            description='Check the status of a document in ABBYY',
    ) as mcxt:
        # ######################################### for app dependent options
        mcxt.add_argument('--repeat', display_name='Repeat Time', type=int,
                          help='The number of times to check the status',
                          default=10)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--wait', display_name='Time Interval', type=int,
                          default=30,
                          help='Time waits for processing tasks')
        # ######################################### for app dependent parameters
        mcxt.add_argument('api_id', display_name='API Id', help='API Key')
        # ----------------------------------------------------------------------
        mcxt.add_argument('api_token', display_name='API Token',
                          input_method='password',
                          help='API Token')
        # ----------------------------------------------------------------------
        mcxt.add_argument('task_id', display_name='Task Id', nargs='+',
                          help='Task Id')
        argspec = mcxt.parse_args(args)
        return do_upload(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
