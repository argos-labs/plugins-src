#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.codat.invoice`
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
#  * [2021/03/27]
#     - 그룹에 "3-Cloud Solutions" 넣음
#  * [2021/01/25]
#     - starting

################################################################################
import os
import sys
import json
import requests
from io import StringIO
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import warnings

warnings.simplefilter("ignore", ResourceWarning)


################################################################################
@func_log
def codat(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + argspec.api_key,
        }
        if argspec.op == 'Get Customer ID':
            url = argspec.endpoint + '/companies/' + argspec.company_id + '/data/customers'
            res = requests.get(url, headers=headers)
            if res.status_code // 10 != 20:
                print(f'Error of API:{res.text}')
            else:
                with StringIO() as outst:
                    outst.write('name,id')
                    for i in res.json()['customers']:
                        try:
                            i, c = i["customerName"], i['id']
                            outst.write('\n')
                            outst.write(i + ',' + c)
                        except:
                            pass
                    print(outst.getvalue(), end='')

        # if argspec.op == 'Create Customer Account':
        #     url = argspec.endpoint + '/companies/' + argspec.company_id + \
        #           '/connections/' + argspec.connection_id + '/push/customers'
        #     dt = {'"customerName"': "Argos-labs"}
        #     res = requests.post(url, headers=headers, data =json.dumps(dt))
        #     if res.status_code // 10 != 20:
        #         print(f'Error of API:{res.text}')
        #     else:
        #         print(res.json()['data']['id'])

        if argspec.op == 'Get Connection ID':
            url = argspec.endpoint + '/companies/' + argspec.company_id + '/connections'
            res = requests.get(url, headers=headers)
            if res.status_code // 10 != 20:
                print(f'Error of API:{res.text}')
            else:
                print(res.json()[0]['id'], end='')

        if argspec.op == 'Create Invoice':
            if argspec.invoice_json:
                with open(argspec.invoice_json) as dt:
                    dt = json.load(dt)
            else:
                dt = {'customerRef': {'id': argspec.customer_id},
                      # "issueDate": argspec.issueDate,
                      # "dueDate":  argspec.dueDate,
                      }
            url = argspec.endpoint + '/companies/' + argspec.company_id + '/connections/' + argspec.connection_id + '/push/invoices'
            res = requests.post(url, headers=headers, data=json.dumps(dt))
            if res.status_code // 10 != 20:
                print(f'Error of API:{res.json()}')
            else:
                print(res.json()['data']['id'], end='')

        if argspec.op == 'Retrieve Invoice':
            if argspec.invoice_id:
                for i in argspec.invoice_id:
                    url = argspec.endpoint + '/companies/' + argspec.company_id + \
                          '/data/invoices/' + i
                    res = requests.get(url, headers=headers)
                    if res.status_code // 10 != 20:
                        print(f'Error of API:{res.text}')
                    else:
                        if not argspec.outputfile:
                            fn = i[0:5] + '-invoice.json'
                            argspec.outputfile = os.path.join(os.getcwd(), fn)
                        with open(argspec.outputfile, 'w') as f:
                            json.dump(res.json(), f, indent=4)
                if len(argspec.invoice_id) != 1:
                    print(os.path.abspath(os.path.dirname(argspec.outputfile)),
                          end='')
                else:
                    print(os.path.abspath(argspec.outputfile), end='')
            else:
                url = argspec.endpoint + '/companies/' + argspec.company_id + \
                      '/data/invoices/'
                res = requests.get(url, headers=headers)
                if res.status_code // 10 != 20:
                    print(f'Error of API:{res.text}')
                else:
                    if not argspec.outputfile:
                        fn = argspec.company_id[0:5] + '-invoices' + '.json'
                        argspec.outputfile = os.path.join(os.getcwd(), fn)
                    with open(argspec.outputfile, 'w') as f:
                        json.dump(res.json(), f, indent=4)
                    print(os.path.abspath(argspec.outputfile), end='')
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
            group='3',  # Cloud Solutions
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Codat API',
            icon_path=get_icon_path(__file__),
            description='Create or retrieve invoices at Codat',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Operation Type',
                          choices=['Get Customer ID', 'Get Connection ID',
                                   'Create Invoice', 'Retrieve Invoice'],
                          help='Choose the type of operations')
        # ----------------------------------------------------------------------
        mcxt.add_argument('endpoint', display_name='Endpoint',
                          help='Endpoint')
        # ----------------------------------------------------------------------
        mcxt.add_argument('api_key', display_name='API Key',
                          help='Api key in Codat')
        # ----------------------------------------------------------------------
        mcxt.add_argument('company_id', display_name='Company Id',
                          help='Company')
        # ##################################### for app optional parameters
        mcxt.add_argument('--connection_id', display_name='Connection Id',
                          help='Connection id', show_default=True)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--invoice_id', display_name='Invoice Id',
                          help='Invoice id', show_default=True, action='append')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--invoice_json', display_name='Invoice Datafile',
                          help='A json file which includes the information of the invoice',
                          input_method='fileread')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--customer_id', display_name='Customer ID',
                          help='the customer ID that the invoice has been issued to')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--outputfile', display_name='Output',
                          input_method='filewrite',
                          help='An absolute output file path')
        argspec = mcxt.parse_args(args)
        return codat(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
