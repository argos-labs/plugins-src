#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.turvo.updoc`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Splitting and Merging PDF plugin
"""
# Authors
# ===========
#
# * Irene Cho
#
# --------
#
#  * [2020/12/22]
#     - starting

################################################################################
import os
import sys
import json
import requests
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import warnings

warnings.simplefilter("ignore", ResourceWarning)


################################################################################
@func_log
def turvo(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        attribute, context = None, None
        if argspec.op == 'Other':
            attribute = {"lookupKey": "3009", "name": argspec.name,
                         "description": argspec.description, "account":
                             {"name": argspec.account_name}}
            context = {"id": int(argspec.shipment_id), "type": "Shipment"}
        elif argspec.op == 'Proof of Delivery':
            attribute = {"lookupKey": "3010", "name": argspec.name,
                         "description": argspec.description, "account":
                             {"name": argspec.account_name}}
            context = {"id": int(argspec.shipment_id), "type": "Shipment"}
        context = json.dumps(context)
        attribute = json.dumps(attribute)
        params = {
            'fullResponse': 'true',
            'context': context,
            'attributes': attribute
        }
        params = tuple([(k, v) for k, v in params.items()])
        headers = {
            'nonce': 'pubtesting4',
            'Authorization': 'Bearer ' + argspec.token,
        }
        # if not argspec.outputfolder:
        #     argspec.outputfolder = os.path.dirname(
        #         os.path.abspath(argspec.file[0]))
        for i in argspec.file:
            fo = open(i, 'rb')
            files = {
                'file': fo,
            }
            url = argspec.endpoint +'/documents'
            res = requests.post(url, headers=headers, params=params, files=files)
            fo.close()
            if res.status_code // 10 != 20:
                print(f'Error of API:{res.text}')
                break
        print(argspec.shipment_id,end='')
                # outputfile = os.path.basename(i).split('.')[0] + '-results.json'
                # outputfile = os.path.join(argspec.outputfolder, outputfile)
                # with open(outputfile, 'w') as f:
                #     json.dump(res.json(), f, indent=4)
                # print(os.path.abspath(argspec.outputfolder), end='')
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
            group='turvo',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Turvo Upload Doc',
            icon_path=get_icon_path(__file__),
            description='Turvo Upload Documents',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Operation Type',
                          choices=['Proof of Delivery', 'Other'],
                          help='Choose the type of pdf operations')
        # ----------------------------------------------------------------------
        mcxt.add_argument('token', display_name='Token', help='Token')
        # ----------------------------------------------------------------------
        mcxt.add_argument('endpoint', display_name='Endpoint',
                          help='endpoint in Turvo')
        # ----------------------------------------------------------------------
        mcxt.add_argument('file', display_name='Upload File', nargs='+',
                          input_method='fileread', help='Upload File')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--shipment_id', display_name='Shipment Id',
                          help='Shipment Id', show_default='True')
        # ##################################### for app optional parameters
        mcxt.add_argument('--name', display_name='Doc Name',
                          help='Document Name')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--description', display_name='Doc Description',
                          help='Document Description')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--account_name', display_name='Account Name',
                          help='Account Name')
        # # ----------------------------------------------------------------------
        # mcxt.add_argument('--outputfolder', display_name='Output Folder',
        #                   input_method='folderwrite',
        #                   help='An absolute output folder path')
        argspec = mcxt.parse_args(args)
        return turvo(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
