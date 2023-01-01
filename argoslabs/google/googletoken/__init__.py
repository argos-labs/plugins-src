"""
====================================
 :mod:`argoslabs.google.googletoken`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS create a google API token file
"""
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2020/07/27]
#     - Add Google Calendar
#  * [2020/06/16]
#     - Change the path of file token.pickle
#  * [2020/06/15]
#     - starting

################################################################################
from __future__ import print_function
import sys
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import warnings


################################################################################
class Googletoken(object):
    # ==========================================================================
    OP_TYPE = ['Google Drive','Google Sheet','Google Calendar']

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.service = None
        self.scopes =None

    # ==========================================================================
    def read_file(self):
        if self.argspec.op == 'Google Drive':
            self.scopes = ['https://www.googleapis.com/auth/drive']
        elif self.argspec.op == 'Google Sheet':
            self.scopes= ['https://www.googleapis.com/auth/spreadsheets']
        elif self.argspec.op == 'Google Calendar':
            self.scopes = ['https://www.googleapis.com/auth/calendar']
        flow = InstalledAppFlow.from_client_secrets_file(
            self.argspec.credentials, self.scopes)
        original = sys.stdout
        sys.stdout= open('file.txt', 'w', encoding='utf-8')
        creds = flow.run_local_server(authorization_prompt_message='')
        root = os.path.dirname(os.path.abspath(self.argspec.credentials))
        sys.stdout = original
        k = os.path.join(root, 'token.pickle')
        with open(k, 'wb') as token:
            pickle.dump(creds, token)
        sys.stdout.write(k)
        return 0

################################################################################
@func_log
def reg_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        warnings.simplefilter("ignore", ResourceWarning)
        res = Googletoken(argspec)
        res.read_file()
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        sys.stdout.flush()
        if os.path.exists('file.txt'):
           os.remove('file.txt')
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS-DEMO',
            group='9',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Google Token',
            icon_path=get_icon_path(__file__),
            description='Managing files in Google Drive',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='Function type',
                          choices=Googletoken.OP_TYPE,
                          help='Type of operation')
        mcxt.add_argument('credentials', display_name='Credentials',
                          help='Google API credentials Json format',
                          input_method='fileread')
        argspec = mcxt.parse_args(args)
        return reg_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
