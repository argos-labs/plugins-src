#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.turvo.shipment`
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
#  * [2021/01/04]
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
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'Bearer ' + argspec.token,
        }
        if argspec.op == 'Create Shipment':
            if argspec.shipment_json:
                with open(argspec.shipment_json) as dt:
                    dt = json.load(dt)
            else:
                dt = {
                    "ltlShipment": argspec.ltlshipment,
                    "startDate": {
                        "date": argspec.startdate,
                        "timezone": argspec.timezone
                    },
                    "endDate": {
                        "date": argspec.enddate,
                        "timezone": argspec.timezone
                    },
                    "status": {
                        "code": {
                            "key": argspec.statuskey,
                            "value": argspec.status_value  # tendered
                        },
                        # "notes": "test note"
                    },
                    "equipment": [
                        {
                            "type": {
                                "key": argspec.equipment_key,
                                "value": argspec.equipment_value
                            },
                        }
                    ],
                    "lane": {
                        "start": argspec.start_lane,
                        "end": argspec.end_lane
                    },
                    "customerOrder": [
                        {
                            "customer": {
                                "id": argspec.customer_id
                            },
                        }
                    ],
                }
            params = {
                'fullResponse': 'true',
            }
            params = tuple([(k, v) for k, v in params.items()])
            url = argspec.endpoint + '/shipments'
            res = requests.post(url,
                                headers=headers, params=params,
                                data=json.dumps(dt))
            if res.status_code // 10 != 20:
                print(f'Error of API:{res.text}')
            else:
                print(res.json()['details']['id'], end='')
        if argspec.op == 'Delete Shipment':
            for i in argspec.shipment_id:
                url = argspec.endpoint + '/shipments'+'/'+i
                res = requests.delete(url, headers=headers)
                if res.status_code // 10 != 20:
                    print(f'Error of API:{res.text}')
                else:
                    print(f'Delete the shipment,{i},successfully.')

        if argspec.op == 'Retrieve Shipment':
            for i in argspec.shipment_id:
                url = argspec.endpoint + '/shipments'+'/'+i
                res = requests.get(url, headers=headers)
                if res.status_code // 10 != 20:
                    print(f'Error of API:{res.text}')
                else:
                    if not argspec.outputfile:
                        fn = i+'-results.json'
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
            group='turvo',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Turvo Shipment',
            icon_path=get_icon_path(__file__),
            description='Create or delete a shipment in Turvo',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Operation Type',
                          choices=['Create Shipment', 'Retrieve Shipment',
                                   'Delete Shipment'],
                          help='Choose the type of operations')
        # ----------------------------------------------------------------------
        mcxt.add_argument('token', display_name='Token',
                          help='Token')
        # ----------------------------------------------------------------------
        mcxt.add_argument('endpoint', display_name='Enpoint',
                          help='endpoint in Turvo')
        # ##################################### for app optional parameters
        mcxt.add_argument('--shipment_id', display_name='Shipment Id',
                          help='Shipment Id', show_default=True,
                          action='append')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--ltlshipment', display_name='LTL Shipment',
                          help='Flag on whether or not the shipment is LTL',
                          default=True, type=bool)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--startdate', display_name='Pickup Date',
                          help='Start date of the shipment',
                          default="2021-01-01")
        # ----------------------------------------------------------------------
        mcxt.add_argument('--enddate', display_name='Delivery Date',
                          help='End date of the shipment',
                          default="2021-01-02")
        # ----------------------------------------------------------------------
        mcxt.add_argument('--timezone', display_name='Timezone',
                          help='Timezone of the start and end date',
                          default="America/Los_Angeles")
        # ----------------------------------------------------------------------
        mcxt.add_argument('--statuskey', display_name='Status Key',
                          help='Set 4 digits of unique key of status',
                          default=2101, type=int)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--status_value', display_name='Status Value',
                          help='Set the value of status. Default is tendered.',
                          default="Tendered")
        # ----------------------------------------------------------------------
        mcxt.add_argument('--equipment_key', display_name='Equipment Key',
                          help='Set the key of the equipment',
                          default=1200, type=int)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--equipment_value', display_name='Equipment Value',
                          help='Set the value of the equipment. Default is other',
                          default="other")
        # ----------------------------------------------------------------------
        mcxt.add_argument('--start_lane', display_name='Pickup Location',
                          help='Set the start location of the shipment',
                          default="San Jose, CA")
        # ----------------------------------------------------------------------
        mcxt.add_argument('--end_lane', display_name='Delivery Location',
                          help='Set the end location of the shipment',
                          default="San Jose, CA")
        # ----------------------------------------------------------------------
        mcxt.add_argument('--customer_id', display_name='Customer Id',
                          help='Set the customer id. It will automatically '
                               'provide the customer name in the shipment',
                          default=65475, type=int)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--shipment_json', display_name='Shipment JSON',
                          help='A json file which includes the information of a shipment',
                          input_method='fileread')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--outputfile', display_name='Output',
                          input_method='filewrite',
                          help='An absolute output file path')
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
