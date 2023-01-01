#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.ocr.abbyydownload`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for ABBYY Download
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
import time
import base64
import calendar
import requests
from tempfile import gettempdir
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit


################################################################################
class uploadAPI(object):

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.id = argspec.result_id
        self.token = argspec.result_token
        self.output = argspec.output
        msg = argspec.api_id + ':' + argspec.api_token
        msg = msg.encode('ascii')
        t = base64.b64encode(msg)
        t = 'Basic ' + t.decode("ascii")
        self.headers = {
            'Accept': 'application/json',
            'Authorization': t,
        }

    # ==========================================================================
    def download_doc(self, source, name, id, token):
        self.headers['Content-Type'] = 'application/json'
        pth = 'https://api-us.flexicapture.com/v2/file'
        url = pth + '/' + id + '/' + token
        resdown = requests.get(url, headers=self.headers, stream=True)
        if not resdown.status_code // 10 == 20:
            raise RuntimeError(resdown.content)
        else:
            fo = str(source).split('.')[0] + '-' + name
            pth = os.path.join(self.output, fo)
            output = open(pth, 'wb')
            output.write(resdown.content)
            output.close()
        return 0


################################################################################
@func_log
def do_upload(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if not argspec.output:
            t = os.path.join(gettempdir(), str(calendar.timegm(time.gmtime())))
            os.mkdir(t)
            argspec.output = t
        xt = uploadAPI(argspec)
        if argspec.statuscsv:
            with open(argspec.statuscsv, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    xt.download_doc(row['source'], row['result_name'],
                                    row['result_id'],
                                    row['result_token'])
        else:
            if len(argspec.result_id) == len(argspec.result_token) == len(
                    argspec.result_name):
                lst = list(zip(argspec.result_name, argspec.result_id,
                               argspec.result_token))
                l = 1
                for i, j, k in lst:
                    print('\n', end='')
                    xt.download_doc(l, i, j, k)
                    l += 1
            else:
                raise IOError('The number of ids, tokens and names are different.')
        print(argspec.output)
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
            display_name='ABBYY Download',
            icon_path=get_icon_path(__file__),
            description='Download document from ABBYY',
    ) as mcxt:
        # ######################################### for app dependent options
        mcxt.add_argument('--statuscsv', display_name='ABBYY Status CSV',
                          help='File Token', input_method='fileread',
                          show_default=True)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--result_name', display_name='Result Name',
                          help='File Token', action='append')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--result_id', display_name='Result Id',
                          help='File Id', action='append')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--result_token', display_name='Result Token',
                          help='File Token', action='append')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--output', display_name='Output Folder',
                          help='Output file', input_method='folderread' )
        # ######################################### for app dependent parameters
        mcxt.add_argument('api_id', display_name='API Id', help='API Key')
        # ----------------------------------------------------------------------
        mcxt.add_argument('api_token', display_name='API Token',
                          input_method='password',
                          help='API Token')
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
