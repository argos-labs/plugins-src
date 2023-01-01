#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.system.modex`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Modex Plugin
"""
# Authors
# ===========
#
# * Irene Cho
#
# --------
#
#  * [2021/02/16]
#     - starting

################################################################################
import os
import sys
import json
import requests
from requests_toolbelt import MultipartEncoder
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import warnings

warnings.simplefilter("ignore", ResourceWarning)


################################################################################
@func_log
def modex(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if argspec.op == 'Get API Key':
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            data = {
                'username': argspec.username,
                'password': argspec.password,
                'client_id': argspec.clientid,
                'client_secret': argspec.clientsecret,
                'grant_type': 'password'
            }
            res = requests.post('https://bcdb.modex.tech/oauth/token',
                                headers=headers, data=data)
            if res.status_code // 10 != 20:
                print(f'Error of API:{res.text}')
            else:
                print(res.json()['access_token'], end='')

        elif argspec.op == 'Create Schema of Entity':
            headers = {
                'Authorization': 'Bearer ' + argspec.api_key,
                'Content-Type': 'application/json'
            }
            url = argspec.endpoint + '/data/catalog/_JsonSchema/' + argspec.entity_title
            if not argspec.entity_json:
                print(f'Error of API:Cannot find the entity file')
                # else:
                #     data = {"$schema": argspec.schema_type, "$id": argspec.entity_title,
                #             "type": argspec.entity_title,
                #             "title": argspec.entity_title,
                #             "properties": {"field1": {"type": "abc", "identity": 1}}}
            else:
                with open(argspec.entity_json) as dt:
                    data = json.load(dt)
                res = requests.post(url, headers=headers, data=json.dumps(data))
                if res.status_code // 10 != 20:
                    print(f'Error of API:{res.text}')
                else:
                    print(res.json()['recordId'], end='')

        if argspec.op == 'Get Schema of Entity':
            headers = {
                'Authorization': 'Bearer ' + argspec.api_key,
                'Content-Type': 'application/json'
            }
            if argspec.entity_title:
                url = argspec.endpoint + '/data/catalog/_JsonSchema/' + argspec.entity_title
            else:
                url = argspec.endpoint + '/data/catalog/_JsonSchema?skip=0&limit=10'
            res = requests.get(url, headers=headers)
            if res.status_code // 10 != 20:
                print(f'Error of API:{res.text}')
            else:
                if not argspec.outputfile:
                    fn = 'schema.json'
                    argspec.outputfile = os.path.join(os.getcwd(), fn)
                with open(argspec.outputfile, 'w') as f:
                    json.dump(res.json(), f, indent=4)
                print(os.path.abspath(argspec.outputfile), end='')

        elif argspec.op == 'Insert Record into Entity':
            headers = {
                'Authorization': 'Bearer ' + argspec.api_key,
                'Content-Type': 'application/json'
            }
            url = argspec.endpoint + '/data/' + argspec.entity_title
            if not argspec.record_json:
                print(f'Error of API:Cannot find the entity file')
            else:
                with open(argspec.record_json) as dt:
                    data = json.load(dt)
                res = requests.post(url, headers=headers, data=json.dumps(data))
                if res.status_code // 10 != 20:
                    print(f'Error of API:{res.text}')
                else:
                    print(res.json()['recordId'], end='')

        if argspec.op == 'Get Record from Entity':
            headers = {
                'Authorization': 'Bearer ' + argspec.api_key,
                'Content-Type': 'application/json'
            }
            if argspec.record_id:
                url = argspec.endpoint + '/data/' + argspec.entity_title + '/' + \
                      argspec.record_id + '?skip=0&limit=100'
            else:
                url = argspec.endpoint + '/data/' + argspec.entity_title + '?skip=0&limit=100'
            res = requests.get(url, headers=headers)
            if res.status_code // 10 != 20:
                print(f'Error of API:{res.text}')
            else:
                if not argspec.outputfile:
                    fn = argspec.entity_title + '-records' + '.json'
                    argspec.outputfile = os.path.join(os.getcwd(), fn)
                with open(argspec.outputfile, 'w') as f:
                    json.dump(res.json(), f, indent=4)
                print(os.path.abspath(argspec.outputfile), end='')

        elif argspec.op == 'Upload File':
            f = open(argspec.attachment, 'rb')
            data = {'qqfile': (os.path.basename(argspec.attachment), f, argspec.attachment_type),
                    'referenceId': argspec.record_id,
                    'referenceName': argspec.entity_title,
                    'qquuid': 'fdskghksfdgifodsgijkfdmghhh',
                    'qqfilename': os.path.basename(argspec.attachment)
                    }
            m = MultipartEncoder(data,
                                 boundary='----WebKitFormBoundary7MA4YWxkTrZu0gW')
            headers = {
                'Content-Type': m.content_type,
                'Authorization': 'Bearer ' + argspec.api_key
            }
            url = argspec.endpoint + '/data/file/upload'
            res = requests.post(url, headers=headers, data = m.to_string())
            f.close()
            if res.status_code // 10 != 20:
                print(f'Error of API:{res.text}')
            else:
                print(argspec.record_id, end='')
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
            group='8',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Modex API',
            icon_path=get_icon_path(__file__),
            description='Create or retrieve entity at Modex',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Operation Type',
                          choices=['Get API Key', 'Create Schema of Entity',
                                   'Get Schema of Entity', 'Insert Record into Entity',
                                   'Get Record from Entity', 'Upload File'],
                          help='Choose the type of operations')
        # ----------------------------------------------------------------------
        mcxt.add_argument('endpoint', display_name='Endpoint',
                          help='Endpoint')
        # ##################################### for app optional parameters
        mcxt.add_argument('--api_key', display_name='API Key',
                          show_default=True,
                          help='Api key in Codat')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--username', display_name='Username',
                          help='Modex Username')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--password', display_name='Password',
                          input_method='password', help='Modex Password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--clientid', display_name='Client ID',
                          help='Modex Client ID')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--clientsecret', display_name='Client Secret',
                          input_method='password', help='Modex Client Secret')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--entity_title', display_name='Entity Title',
                          help='Entity Title')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--record_id', display_name='Record ID',
                          help='Record ID')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--entity_json', display_name='Entity Datafile',
                          help='A json file which includes the information of the entity',
                          input_method='fileread')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--record_json', display_name='Record Datafile',
                          help='A json file which includes the information of the data',
                          input_method='fileread')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--attachment', display_name='Attachment',
                          help='Upload a file to entity',
                          input_method='fileread')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--attachment_type', display_name='Attachment Type',
                          help='Type of Attachment', default='image/png')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--outputfile', display_name='Output',
                          input_method='filewrite',
                          help='An absolute output file path')
        argspec = mcxt.parse_args(args)
        return modex(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
