#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.ocr.xtractagetdoc`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Xtracta1
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

################################################################################
import os
import sys
import requests
import json
import warnings
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit


################################################################################
class GetdocAPI(object):

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.api_key = argspec.api_key
        self.g = None


    # ==========================================================================
    @staticmethod
    def _get_safe_next_filename(fn, ext):
        for n in range(1, 1000000):
            nfn = os.path.join(ext, f'{fn}({n}).json')
            if not os.path.exists(nfn):
                return nfn


    # ==========================================================================
    def get_doc(self, docid):
        url = f'https://api.docdigitizer.com/api/v1/documents/{docid}/assets'
        dt = {}
        headers = {
            "accept": "application/json",
            "Authorization": 'API_KEY ' + self.api_key
        }
        self.g = requests.get(url, headers=headers, data=dt)
        if self.g.status_code // 10 != 20:
            raise RuntimeError(f'Invalid Response '
                               f'{self.g.status_code} '
                               f'from {url}')
        t = self.g.content
        jf = self._get_safe_next_filename(docid, self.argspec.outputfolder)
        with open(jf, 'w') as outfile:
            json.dump(json.loads(t.decode('utf-8')), outfile, indent=4)
        print(f"{docid},{jf}")
        return 0


################################################################################
@func_log
def do_getdoc(mcxt, argspec):
    warnings.simplefilter("ignore", ResourceWarning)
    mcxt.logger.info('>>>starting...')
    try:
        xt = GetdocAPI(argspec)
        if argspec.docid:
            print('document_id,file')
            for i in argspec.docid:
                xt.get_doc(i)
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
            display_name='Docdigitizer Get Doc',
            icon_path=get_icon_path(__file__),
            description='Get document from Docdigitizer',
    ) as mcxt:
        # ######################################### for app dependent options
        # ###################################### for app dependent parameters
        mcxt.add_argument('api_key', display_name='API Key',
                          input_method='password',
                          help='API Key')
        # ----------------------------------------------------------------------
        mcxt.add_argument('docid', display_name='Document Id',
                          help='document id', action='append',
                          show_default=True)
        # ----------------------------------------------------------------------
        mcxt.add_argument('outputfolder', display_name='Output Folder',
                          help='Output Folder', input_method='folderread')
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
