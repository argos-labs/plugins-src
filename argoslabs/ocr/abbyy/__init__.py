#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.ocr.abbyy`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for ABBYY
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
import csv
import sys
import json
import magic
import base64
import requests
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit


################################################################################
class uploadAPI(object):

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.restask = None
        self.lst = []
        msg = argspec.api_id + ':' + argspec.api_token
        msg = msg.encode('ascii')
        t = base64.b64encode(msg)
        t = 'Basic ' + t.decode("ascii")
        self.headers = {
            'Accept': 'application/json',
            'Authorization': t,
        }

    # ==========================================================================
    def upload_doc(self, filename):
        k = open(filename, 'rb')
        ft = magic.from_file(filename, mime=True)
        f1 = (os.path.basename(filename), k, ft)
        res = requests.post('https://api-us.flexicapture.com/v2/file',
                            headers=self.headers, files={'file': f1})
        k.close()
        if not res.status_code // 10 == 20:
            raise RuntimeError(res.content)
        t = json.loads(res.content)
        dic = {}
        dic['id'] = t[0]["id"]
        dic['token'] = t[0]["token"]
        self.lst.append(dic)
        return self.lst

    # ==========================================================================
    def task_status(self):
        self.headers['Content-Type'] = 'application/json'
        data = eval(
            '{ "properties": { "region": "US", "export_format": "csv",'' "verification_type": "NoVerification", },'' '
            '"files": self.lst }')
        self.restask = requests.post(
            'https://api-us.flexicapture.com/v2/task/capture/documents',
            headers=self.headers, data=str(data))
        if not self.restask.status_code // 10 == 20:
            raise RuntimeError(self.restask.content)
        return self.restask

    # ==========================================================================
    def print_doc(self):
        t = json.loads(self.restask.content)
        # print(f'{t[0]["id"]},{t[0]["token"]},{t[0]["name"]}')
        print(t['id'], end='')
        return 0


################################################################################
@func_log
def do_upload(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        xt = uploadAPI(argspec)
        # print('id,token,filename')
        if argspec.filename:
            for i in argspec.filename:
                if os.path.exists(i):
                    xt.upload_doc(i)
            xt.task_status()
            xt.print_doc()
        elif argspec.csvfile:
            with open(argspec.csvfile) as csv_file:
                cf = csv.reader(csv_file, delimiter=',')
                for i in cf:
                    if i:
                        if os.path.exists(i[1]):
                            xt.upload_doc(i[1])
                xt.task_status()
                xt.print_doc()
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
            display_name='ABBYY Upload',
            icon_path=get_icon_path(__file__),
            description='Upload document to ABBYY',
    ) as mcxt:
        # ######################################### for app dependent options
        mcxt.add_argument('api_id', display_name='API Id', help='API Key')
        # ----------------------------------------------------------------------
        mcxt.add_argument('api_token', display_name='API Token', input_method='password',
                          help='API Token')
        # ###################################### for app dependent parameters
        mcxt.add_argument('--csvfile', display_name='FolderMon CSV',
                          help='The csv output from the folder monitor plugin',
                          input_method='fileread',
                          show_default=True)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--filename', display_name='File', action='append',
                          help='Individual files to attach', input_method='fileread',
                          show_default=True)
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
