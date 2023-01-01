"""
====================================
 :mod:`argoslabs.sfdc.newuser`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for creating a new user in SFDC
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
#  * [2020/05/01]
#     - build a plugin
#  * [2020/05/01]
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
class NewuserAPI(object):
    OP_TYPE = ['Pacific/Kiritimati', 'Pacific/Chatham', 'Pacific/Auckland',
               'Pacific/Enderbury', 'Pacific/Fiji', 'Pacific/Tongatapu',
               'Asia/Kamchatka', 'Pacific/Norfolk', 'Australia/Lord_Howe',
               'Australia/Sydney', 'Pacific/Guadalcanal', 'Australia/Adelaide',
               'Australia/Darwin', 'Asia/Seoul', 'Asia/Tokyo', 'Asia/Hong_Kong',
               'Asia/Kuala_Lumpur', 'Asia/Manila', 'Asia/Shanghai',
               'Asia/Singapore', 'Asia/Taipei', 'Australia/Perth',
               'Asia/Bangkok', 'Asia/Ho_Chi_Minh', 'Asia/Jakarta',
               'Asia/Rangoon', 'Asia/Dhaka', 'Asia/Yekaterinburg',
               'Asia/Kathmandu', 'Asia/Colombo', 'Asia/Kolkata', 'Asia/Karachi',
               'Asia/Tashkent', 'Asia/Kabul', 'Asia/Dubai', 'Asia/Tbilisi',
               'Europe/Moscow', 'Asia/Tehran', 'Africa/Nairobi', 'Asia/Baghdad',
               'Asia/Kuwait', 'Asia/Riyadh', 'Europe/Minsk', 'Africa/Cairo',
               'Africa/Johannesburg', 'Asia/Jerusalem', 'Europe/Athens',
               'Europe/Bucharest', 'Europe/Helsinki', 'Europe/Istanbul',
               'Africa/Algiers', 'Europe/Amsterdam', 'Europe/Berlin',
               'Europe/Brussels', 'Europe/Paris', 'Europe/Prague',
               'Europe/Rome', 'Europe/Dublin', 'Europe/Lisbon', 'Europe/London',
               'GMT', 'Atlantic/Cape_Verde', 'America/Sao_Paulo',
               'Atlantic/South_Georgia', 'America/Argentina/Buenos_Aires',
               'America/Santiago', 'America/St_Johns', 'America/Halifax',
               'America/Puerto_Rico', 'Atlantic/Bermuda', 'America/Caracas',
               'America/Bogota', 'America/Indiana/Indianapolis', 'America/Lima',
               'America/New_York', 'America/Panama', 'America/Chicago',
               'America/El_Salvador', 'America/Mexico_City',
               'America/Denver****America/Denver', 'America/Phoenix',
               'America/Los_Angeles', 'America/Tijuana', 'America/Anchorage',
               'Pacific/Honolulu', 'Pacific/Niue', 'Pacific/Pago_Pago']
    OP_TYPE2 = ['UTF-8', 'ISO-8859-1', 'Shift_JIS', 'ISO-2022-JP', 'EUC-JP',
                'ks_c_5601-1987', 'Big5', 'GB2312']
    OP_TYPE3 = ['Create', 'Search Profile Id']

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.username = argspec.username
        self.password = argspec.password
        self.security_token = argspec.security_token
        self.sf = None
        self.sfo = None
        self.multidt = None
        self.singledt = None
        self.dict_dt = None

    # ==========================================================================
    def get_api_result(self):
        self.sf = Salesforce(self.username, self.password, self.security_token)
        self.sfo = SFType('User', self.sf.session_id, self.sf.sf_instance)
        return self.sfo

    # ==========================================================================
    def inputdata(self):
        if self.argspec.jsonfile:
            f = open(self.argspec.jsonfile)
            self.multidt = json.load(f)
            f.close()
        else:
            self.singledt = {'username': self.argspec.newusername,
                             'Lastname': self.argspec.lastname,
                             'email': self.argspec.email,
                             'Alias': self.argspec.alias,
                             'TimeZoneSidKey': self.argspec.timezone,
                             'LocaleSidKey': self.argspec.localkey,
                             'EmailEncodingKey': self.argspec.encoding,
                             'LanguageLocaleKey': self.argspec.lngkey,
                             'ProfileId': self.argspec.profileid,
                             'isActive': self.argspec.isactive}

    # ==========================================================================
    def create(self):
        self.inputdata()
        k = None
        if self.multidt:
            k = self.sfo.create(self.multidt)
        elif self.singledt:
            k = self.sfo.create(self.singledt)
        return k['id']

    # ==========================================================================
    def printout(self):
        if len(self.dict_dt) > 0:
            cols = ', '.join(list(self.dict_dt[0].keys())[1:])
            with StringIO() as oust:
                for i in cols:
                    oust.write(i)
                oust.write('\n')
                for i in self.dict_dt:
                    k = ', '.join(list(i.values())[1:])
                    for j in k:
                        oust.write(str(j))
                    oust.write('\n')
                print(oust.getvalue(), end='')
        else:
            print("No value find")

    # ==========================================================================
    def select_query(self):
        self.dict_dt = self.sf.query("select name,id from profile")['records']
        return self.printout()

    # ==========================================================================
    def do(self, op):
        if op == 'Create':
            print(self.create())
        if op == 'Search Profile Id':
            self.select_query()


################################################################################
@func_log
def do_excek2(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    warnings.filterwarnings("ignore", category=ResourceWarning,
                            message="unclosed.*<ssl.SSLSocket.*>")
    try:
        si = NewuserAPI(argspec)
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
            display_name='Newuser-SFDC',
            icon_path=get_icon_path(__file__),
            description='simple salesforce python module',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--newusername', display_name='New username',
                          help='email format ex.sample@sales.com')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--lastname', display_name='Lastname',
                          help='lastname of the user')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--email', display_name='Email', help='user email')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--alias', display_name='Alias',
                          help='short name to identify the user on list pages')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--profileid', display_name='ProfileId',
                          help='specify the type of profile ')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--localkey', display_name='LocaleSidKey',
                          default='en_US', help='localesidkey')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--lngkey', display_name='LanguageLocaleKey',
                          default='en_US', help='language key')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--encoding', display_name='EmailEncodingKey',
                          choices=NewuserAPI.OP_TYPE2,
                          default='UTF-8', help='encoding')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--timezone', display_name='TimeZoneSidKey',
                          choices=NewuserAPI.OP_TYPE,
                          help='timezone')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--isactive', display_name='IsActive',
                         default=False,
                          help='assign license ')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--jsonfile', display_name='Json file',
                          input_method='fileread', help='Json inputfile')

        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Operations',
                          choices=NewuserAPI.OP_TYPE3,
                          help='Simple salesforce type of operation')

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
