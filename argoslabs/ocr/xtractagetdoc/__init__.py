#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.ocr.xtractagetdoc`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Xtracta1
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
class getdocAPI(object):

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.api_key = argspec.api_key

    # ==========================================================================
    @staticmethod
    def xmltojson(t):
        data_dict = xmltodict.parse(t)
        json_data = json.dumps(data_dict)
        return json.loads(json_data)

    # ==========================================================================
    @staticmethod
    def _get_safe_next_filename(fn, ext):
        for n in range(1, 1000000):
            nfn = os.path.join(ext, f'{fn}({n}).json')
            if not os.path.exists(nfn):
                return nfn

    # ==========================================================================
    def get_doc(self, docid):
        url = 'https://api-app.xtracta.com/v1/documents'
        dt = {'api_key': self.api_key,
              'document_id': docid}
              #pass workdocument id
        x = requests.post(url, data=dt)
        if x.status_code // 10 != 20:
            raise RuntimeError(f'Invalid Response {x.status_code}'
                               f'from {url}')
        t = self.xmltojson(x.content)
        jf = self._get_safe_next_filename(docid, self.argspec.outputfolder)
        with open(jf, 'w') as outfile:
            json.dump(t, outfile, indent=4)
        return 0


################################################################################
@func_log
def do_getdoc(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        xt = getdocAPI(argspec)
        if argspec.docid:
            for i in argspec.docid:
                xt.get_doc(i)
            print(os.path.abspath(argspec.outputfolder), end='')
        elif argspec.csvfile:
            with open(argspec.csvfile) as csv_file:
                cf = csv.reader(csv_file, delimiter=',')
                for i in cf:
                    if i[0].isnumeric():
                        xt.get_doc(i[0])
                csv_file.close()
            print(os.path.abspath(argspec.outputfolder), end='')
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
            display_name='Xtracta Get Doc',
            icon_path=get_icon_path(__file__),
            description='Get document from Xtracta',
    ) as mcxt:
        # ######################################### for app dependent options
        # ###################################### for app dependent parameters
        mcxt.add_argument('api_key', display_name='API Key', help='API Key')
        # ----------------------------------------------------------------------
        mcxt.add_argument('outputfolder', display_name='Output Folder',
                          help='Output Folder', input_method='folderread')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--docid', display_name='Document Id',
                          help='document id', action='append',
                          show_default=True)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--csvfile', display_name='Track CSV', help='csv',
                          show_default=True, input_method='fileread',)
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
