#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.ocr.docdigitizertrack`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for docdigitizer Tracking
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
#  * [2020/08/18]
#     - build a plugin
#  * [2020/08/18]
#     - starting


# multiple files track, user's option => any or all

################################################################################
import os
import sys
import json
import time
import requests
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit


################################################################################
class TrackingAPI(object):

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.api_key = argspec.api_key
        self.t = None

    # ==========================================================================
    def track_doc(self, docid):
        url = f'https://api.docdigitizer.com/api/v1/documents/{docid}'
        headers = {
            "accept": "application/json",
            "Authorization": 'API_KEY ' + self.api_key
        }
        self.t = requests.get(url,headers=headers, data={})
        if not self.t.status_code // 10 == 20:
            raise RuntimeError(self.t.content)
        return self.t


    # ==========================================================================
    def track_print(self,docid):
        st = json.loads(self.t.content.decode('utf-8'))['document']['annotation_status']
        start_time = time.time()
        sec = self.argspec.timemax
        lst = []
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            lst.append([docid, st, time.ctime()])
            if st == 'success' or st == 'Invalid':
                # print(f"{docid},{st},{time.ctime()}")
                print(
                    f"{docid},{json.loads(self.t.content.decode('utf-8'))['document']['annotation_status']}"
                )
                break
            elif elapsed_time > sec:
                print(f"{docid},Timeout")
                break
            else:
                time.sleep(self.argspec.sec)
                self.track_doc(docid)
                st = json.loads(self.t.content.decode('utf-8'))['document'][
                    'annotation_status']
        return 0


################################################################################
@func_log
def do_getdoc(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        xt = TrackingAPI(argspec)
        if argspec.docid:
            print('document_id,status')
            for i in argspec.docid:
                xt.track_doc(i)
                try:
                    xt.track_print(i)
                except Exception:
                    print(f"{i},Invalid")
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
            display_name='Docdigitizer Tracking',
            icon_path=get_icon_path(__file__),
            description='Track the document from Docdigitizer',
    ) as mcxt:
        # ######################################### for app dependent options
        # ###################################### for app dependent parameters
        mcxt.add_argument('api_key', display_name='API Key',
                          input_method='password',
                          help='API Key')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--docid', display_name='Document Id',
                          help='document id', action='append',
                          show_default=True)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--sec', display_name='Time Interval',
                          help='periodic processing time',
                          default=10, type=int)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--timemax', display_name='Timeout', help='Timeout',
                          default=100, type=int)
        argspec = mcxt.parse_args(args)
        return do_getdoc(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
