#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.ocr.xtracta`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Xtracta
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
#  * [2020/08/18]
#     - build a plugin
#  * [2020/08/18]
#     - starting

# multiple files

################################################################################
import os
import csv
import sys
import json
import requests
import xmltodict
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit


################################################################################
class uploadAPI(object):

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.api_key = argspec.api_key
        self.workflow = argspec.workflow
        self.res = None

    # ==========================================================================
    @staticmethod
    def xmltojson(t):
        data_dict = xmltodict.parse(t)
        json_data = json.dumps(data_dict)
        return json.loads(json_data)

    # ==========================================================================
    def upload_doc(self, filename):
        url = 'https://api-app.xtracta.com/v1/documents/upload'
        dt = {'api_key': self.api_key, 'workflow_id': self.workflow}
        f = open(filename, 'rb')
        self.res = requests.post(url, data=dt, files={'userfile': f})
        f.close()
        if not self.res.status_code // 10 == 20:
            raise RuntimeError(self.res.content)
        return self.res

    # ==========================================================================
    def print_doc(self):
        t = self.xmltojson(self.res.content)
        print(f"{t['xml']['document_id']},{t['xml']['message']}")
        return 0


################################################################################
@func_log
def do_upload(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        xt = uploadAPI(argspec)
        print('document_id,message')
        if argspec.filename:
            for i in argspec.filename:
                if os.path.exists(i):
                    xt.upload_doc(i)
                    xt.print_doc()
        elif argspec.csvfile:
            with open(argspec.csvfile) as csv_file:
                cf = csv.reader(csv_file, delimiter=',')
                for i in cf:
                    if i:
                        if os.path.exists(i[1]):
                            xt.upload_doc(i[1])
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
            group='AWS',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Xtracta Upload',
            icon_path=get_icon_path(__file__),
            description='Upload document to Xtracta',
    ) as mcxt:
        # ######################################### for app dependent options
        # ###################################### for app dependent parameters
        mcxt.add_argument('api_key', display_name='API Key', help='API Key')
        # ----------------------------------------------------------------------
        mcxt.add_argument('workflow', display_name='Workflow Id',
                          help='Workflow')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--csvfile', display_name='FileMon CSV',
                          help='CSV File', input_method='fileread',
                          show_default=True)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--filename', display_name='File', action='append',
                          help='File', input_method='fileread',
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
