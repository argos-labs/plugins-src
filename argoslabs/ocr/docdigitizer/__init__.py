#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.ocr.docdigitizer`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for docdigitizer
"""
#
# Authors
# ===========
#
# * Arun Kumar
#
# Change Log
# --------
#

################################################################################
import os
import sys
import json
import requests
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit


################################################################################
class UploadAPI(object):

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.api_key = argspec.api_key
        self.res = None


    # ==========================================================================
    def upload_doc(self, file):
        url = 'https://api.docdigitizer.com/api/v1/documents/annotate'
        payload = {}
        if self.argspec.callback_method:
            payload["callback_method"]=self.argspec.callback_method
        if self.argspec.callback_url:
            payload["callback_url"]=self.argspec.callback_url
        if self.argspec.callback_headers:
            for i in self.argspec.callback_headers:
                index = i.split(':')
                payload[f"callback_headers[{index[0]}]"]=index[1]
        f = open(file, 'rb')
        headers = {
            "accept": "application/json",
            "Authorization": 'API_KEY ' + self.api_key
        }
        if self.argspec.tag:
            headers["X-Docdigitizer-Tag"]=self.argspec.tag
        self.res = requests.post(url, headers=headers, data=payload, files={'files': f})
        f.close()
        if not self.res.status_code // 10 == 20:
            raise RuntimeError(self.res.content)
        return self.res


    # ==========================================================================
    def print_doc(self):
        print(
            f"{json.loads(self.res.content.decode('utf-8'))['task']['document_id']},"
            f"{json.loads(self.res.content.decode('utf-8'))['task']['status']}"
        )
        return 0


################################################################################
@func_log
def do_upload(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        xt = UploadAPI(argspec)
        print('document_id,status')
        if argspec.file:
            if os.path.exists(argspec.file):
                xt.upload_doc(argspec.file)
                xt.print_doc()
            else:
                raise RuntimeError(f"{argspec.file} doesn't exist")
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
            display_name='Docdigitizer Upload',
            icon_path=get_icon_path(__file__),
            description='Upload document to docdigitizer',
    ) as mcxt:
        # ######################################### for app dependent options
        # ###################################### for app dependent parameters
        mcxt.add_argument('api_key', display_name='API Key',
                          input_method='password',
                          help='API Key')
        # ----------------------------------------------------------------------
        mcxt.add_argument('file', display_name='File',
                          help='accept pdf,jpeg,png,tiff file size limit of 25Mb', input_method='fileread',
                          show_default=True)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--callback_url', display_name='Callback URL',
                          help='URL of the customer callback service.')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--callback_method', display_name='Callback Method',
                          help='HTTP method to be used to call the callback service.'
                               ' We accept only GET or POST(GET is used by default).')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--callback_headers', display_name='Callback Headers',
                          action="append",
                          help='This is a dictionary of key and value pairs of strings.'
                               'Eg. Authorization:apikey')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--tag', display_name='Tag',
                          help='this is an optional header that you can use to '
                               'put your own tags. Tags are comma separated.')
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
