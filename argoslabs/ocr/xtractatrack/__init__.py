#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.ocr.xtractatrack`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Xtracta Tracking
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


# multiple files track, user's option => any or all

################################################################################
import os
import csv
import sys
import json
import time
import requests
import xmltodict
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit


################################################################################
class trackingAPI(object):

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.api_key = argspec.api_key
        self.t = None

    # ==========================================================================
    @staticmethod
    def xmltojson(t):
        data_dict = xmltodict.parse(t)
        json_data = json.dumps(data_dict)
        return json.loads(json_data)

    # ==========================================================================
    def track_doc(self, docid):
        url = 'https://api-app.xtracta.com/v1/tracking'
        dt = {'api_key': self.api_key,
              'document_id': docid}
        x = requests.post(url, data=dt)
        self.t = self.xmltojson(x.content)
        m = self.t['tracking_response']['message']
        if x.status_code // 10 != 20 and not 'document_id' in m:
            raise IOError(m)
        else:
            return self.t

    # ==========================================================================
    def track_print(self, docid):
        st = self.t['tracking_response']['input']['status']
        start_time = time.time()
        seconds = self.argspec.timemax
        lst = []
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            lst.append([docid, st, time.ctime()])
            if st == 'OK' or st == 'Invalid':
                print(f"{docid},{st},{time.ctime()}")
                break
            elif elapsed_time > seconds:
                print(f"{docid},Timeout")
                break
            else:
                time.sleep(self.argspec.seconds)
                self.track_doc(docid)
                st = self.t['tracking_response']['input']['status']
        return st


################################################################################
@func_log
def do_getdoc(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        xt = trackingAPI(argspec)
        if argspec.csvfile:
            with open(argspec.csvfile) as csv_file:
                cf = csv.reader(csv_file, delimiter=',')
                print('document_id,status,success_time')
                for i in cf:
                    if i[0].isnumeric():
                        xt.track_doc(i[0])
                        try:
                            st = xt.track_print(i[0])
                            if argspec.any and st//10!=20:
                                break
                        except Exception:
                            print(f"{i[0]},Invalid")
                            if argspec.any:
                                break
                            else:
                                pass
        if argspec.docid:
            print('document_id,status,success_time')
            for i in argspec.docid:
                xt.track_doc(i)
                try:
                    xt.track_print(i)
                    if argspec.any and st // 10 != 20:
                        break
                except Exception:
                    print(f"{i},Invalid")
                    if argspec.any:
                        break
                    else:
                        pass
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
            display_name='Xtracta Tracking',
            icon_path=get_icon_path(__file__),
            description='Track the document from Xtracta',
    ) as mcxt:
        # ######################################### for app dependent options
        mcxt.add_argument('--seconds', display_name='Interval',
                          help='periodic processing time',
                          default=10, type=int)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--timemax', display_name='Timeout', help='Timeout',
                          default=100, type=int)
        # -----------------------------------------------------------------------
        mcxt.add_argument('--any', display_name='Any', help='Any or All',
                          action='store_true')
        # ###################################### for app dependent parameters
        mcxt.add_argument('api_key', display_name='API Key', help='API Key')
        #   ----------------------------------------------------------------------
        mcxt.add_argument('--csvfile', display_name='Upload CSV',
                          help='CSV File', input_method='fileread',
                          show_default=True)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--docid', display_name='Document Id',
                          help='document id', action='append',
                          show_default=True)
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
