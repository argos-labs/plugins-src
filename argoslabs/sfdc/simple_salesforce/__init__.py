"""
====================================
 :mod:`argoslabs.sfdc.simple_salesforce`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for simple salesforce
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
#  * [2020/05/05]
#     - change package name "SFDC" => "sfdc"  <Jerry Chae>
#  * [2020/04/27]
#     - build a plugin
#  * [2020/04/21]
#     - starting

################################################################################
import os
import sys
import json
from io import StringIO
from simple_salesforce import Salesforce, SFType
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit
import warnings


################################################################################
class SimpleAPI(object):
    OP_TYPE = [
        'Create', 'Update', 'Delete', 'Select-Query', 'Search'
    ]
    OP_TYPE2 = ['Account', 'Asset', 'Campaign', 'Case', 'Contact', 'Group',
                'Individual', 'Lead', 'Opportunity']

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.username = argspec.username
        self.password = argspec.password
        self.security_token = argspec.security_token
        self.sf = None
        self.sfo = None
        self.dict_dt = None
        self.id = None
        self.multidt = None
        self.singledt = None
        self.lst = None

    # ==========================================================================
    def get_api_result(self):
        self.sf = Salesforce(self.username, self.password, self.security_token)
        self.sfo = SFType(self.argspec.op2, self.sf.session_id,
                          self.sf.sf_instance)
        return self.sfo

    # ==========================================================================
    def printout(self):
        if len(self.dict_dt) > 0:
            cols = ['Items', ',', ','.join(list(self.dict_dt[0].keys())[1:])]
            with StringIO() as oust:
                for i in cols:
                    oust.write(i)
                oust.write('\n')
                for i in self.dict_dt:
                    oust.write(i['attributes']['type'])
                    for j in list(i.values())[1:]:
                        oust.write(',')
                        oust.write(str(j))
                    oust.write('\n')
                print(oust.getvalue(), end='')
        else:
            print("No value find", end='')

    # ==========================================================================
    def inputdata(self):
        if self.argspec.jsonfile:
            f = open(self.argspec.jsonfile)
            dt = json.load(f)
            self.multidt = []
            for i in dt.values():
                if isinstance(i, str):
                    self.multidt = [dt]
                elif i.values():
                    self.multidt.append(i)
            f.close()
            return self.multidt
        if self.argspec.data:
            self.singledt = {}
            for i in self.argspec.data:
                k = i.split('=')
                self.singledt[k[0]] = k[1]
            return self.singledt

    # ==========================================================================
    def create(self):
        self.inputdata()
        if self.singledt:
            self.multidt = [self.singledt]
        k = eval(
            "self.sf.bulk.%s.insert(%s)" % (self.argspec.op2, self.multidt))
        if k[0][0]['success']:
            return k[0][0]['id']
        else:
            return k

    # ==========================================================================
    def update(self):
        self.inputdata()
        if self.singledt:
            self.singledt['Id'] = self.argspec.id
            self.multidt = [self.singledt]
        k = eval(
            "self.sf.bulk.%s.update(%s)" % (self.argspec.op2, self.multidt))
        if k[0][0]['success']:
            return k[0][0]['id']
        else:
            return k

    # ==========================================================================
    def delete(self):
        self.sfo.delete(self.argspec.id)

    # ==========================================================================
    def select_query(self):
        fn = ','.join(self.argspec.fieldnames)
        self.dict_dt = self.sf.query(f"select {fn} from {self.argspec.op2}")[
            'records']
        self.printout()

    # ==========================================================================
    def search(self):
        k = "FIND {%s}" % self.argspec.value
        self.dict_dt = self.sf.search(k)['searchRecords']
        self.printout()

    # ==========================================================================
    def do(self, op):
        if op == 'Create':
            print(self.create(), end='')
        if op == 'Update':
            print(self.update(), end='')
        if op == 'Delete':
            self.delete()
        if op == 'Select-Query':
            self.select_query()
        if op == 'Search':
            self.search()


################################################################################
@func_log
def do_excek2(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    warnings.filterwarnings("ignore", category=ResourceWarning,
                            message="unclosed.*<ssl.SSLSocket.*>")
    try:
        si = SimpleAPI(argspec)
        si.get_api_result()
        si.do(argspec.op)
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS',
            group='3',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Simple-SFDC',
            icon_path=get_icon_path(__file__),
            description='simple salesforce python module',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--data', action='append',
                          display_name='Input schema.json',
                          help='schema.json to create or insert')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--jsonfile', display_name='Json file',
                          input_method='fileread',
                          help='Json inputfile')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--id', display_name='Data Id',
                          help='id for schema.json')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--fieldnames', action='append',
                          display_name='Select fields',
                          help='select query fieldnames')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--value', display_name='Search value',
                          help='search specific value and return Id')

        # ##################################### for app dependent parameters
        mcxt.add_argument('op2',
                          display_name='Items', choices=SimpleAPI.OP_TYPE2,
                          help='Simple salesforce class type')
        # ----------------------------------------------------------------------
        mcxt.add_argument('op',
                          display_name='Operations', choices=SimpleAPI.OP_TYPE,
                          help='Simple salesforce type of operation')
        # ----------------------------------------------------------------------
        mcxt.add_argument('username', display_name='Username', help='username')
        # ----------------------------------------------------------------------
        mcxt.add_argument('password', display_name='Password',
                          input_method='password', help='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('security_token', display_name='Security token',
                          input_method='password', help='security_token')
        argspec = mcxt.parse_args(args)
        return do_excek2(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
