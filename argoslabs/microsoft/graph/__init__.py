"""
====================================
 :mod:`argoslabs.microsoft.graph`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/02/22]
#     - Attended login
#  * [2022/02/20]
#     - starting

################################################################################
import os
import sys
import json
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import time
import traceback
import subprocess
from alabslib.selenium import PySelenium
from argoslabs.microsoft.graph.msg_login import msg_login
from pprint import pprint


################################################################################
BROWSERS = [
    'Chrome',
    'Edge',
]


################################################################################
# We are using Selenium browser to get redirected URI
class MSGraphAuth(PySelenium):
    # ==========================================================================
    def __init__(self, url, **kwargs):
        self.url = kwargs['url'] = url
        self.cur_url = None
        PySelenium.__init__(self, **kwargs)

    # ==========================================================================
    def start(self):
        try:
            while True:
                time.sleep(1)
                # e = self.get_by_xpath('body')
                cur_url = self.driver.current_url
                if cur_url.find('?code=') > 0:
                    self.cur_url = cur_url
                    time.sleep(2)
                    break
        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('add_data Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))


################################################################################
def graph_login(client_id, client_secret, redirect_uri, credential_file,
                auth_browser=BROWSERS[0]):
    po = None
    try:
        cmd = [
            # 'CMD.EXE', '/C',
            sys.executable,
            '-m',
            'argoslabs.microsoft.graph.msg_login',
            client_id,
            client_secret,
            redirect_uri,
            credential_file,
        ]
        po = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        url_prompt = 'Please go to URL provided authorize your account: '
        red_prompt = 'Paste the full URL redirect here: '
        out = None
        for out in po.stdout:
            out = out.decode('utf-8').strip()
            # print(f'<{out}>')
            if out.startswith(url_prompt):
                url = out[len(url_prompt):]
                # wo = webbrowser.open(url)
                # i = url
                with MSGraphAuth(url, browser=auth_browser) as ga:
                    ga.start()
                    red_url = ga.cur_url + '\n'
                    out = po.communicate(red_url.encode('utf-8'))[0]
                    out = out.decode('utf-8').strip()
                    print(out)
                    break
        if out is not None and out.find('__!!~~>>>argoslabs.microsoft.graph logined') >= 0:
            return True
        return False
    finally:
        if po is not None:
            po.wait()


################################################################################
class GraphOp(object):
    OPS = [
        'List Users',
        'Get Root Drive',
        # 'Get Children',
    ]

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        # for internal
        self.gc = None

    # ==========================================================================
    def login(self):
        r = graph_login(
            self.argspec.client_id,
            self.argspec.client_secret,
            self.argspec.redirect_uri,
            self.argspec.credential_file,
            auth_browser=self.argspec.auth_browser
        )
        if not r:
            raise RuntimeError(f'Cannot authenticate Microsoft Graph API')
        self.gc = msg_login(
            self.argspec.client_id,
            self.argspec.client_secret,
            self.argspec.redirect_uri,
            self.argspec.credential_file,
            is_print=False,
        )

    # ==========================================================================
    def list_users(self):
        if not self.gc:
            raise RuntimeError(f'First login needed!')
        user_services = self.gc.users()
        rj = user_services.list_users()
        print(json.dumps(rj))

    # ==========================================================================
    def get_root_drive(self):
        if not self.gc:
            raise RuntimeError(f'First login needed!')
        drive_services = self.gc.drives()
        rj = drive_services.get_root_drive()
        # rj = drive_services.get_root_drive_children()
        print(json.dumps(rj))

    # ==========================================================================
    def get_children(self):
        drive_services = self.gc.drives()
        rj = drive_services.get_root_drive()
        # rj = drive_services.get_root_drive_children()
        print(json.dumps(rj))

        user_id = rj['lastModifiedBy']['user']['id']
        drive_id = rj['id']
        drive_item_services = self.gc.drive_item()
        # dij = drive_item_services.get_user_drive_item(user_id=user_id, item_id=item_id)
        # if not self.argspec.children_folder:
        #     item_id = drive_id
        # else:
        #     dij = drive_item_services.get_drive_item_by_path(
        #         user_id=user_id, item_path=self.argspec.children_folder)
        #     pprint(dij)
        #     item_id = dij['id']
        cj = drive_item_services.get_drive_children_by_path(
            drive_id=drive_id, path=self.argspec.children_folder)
        pprint(cj)


################################################################################
@func_log
def do_msg(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        # if not argspec.apikey:
        #     raise IOError('Invalid API key' % argspec.apikey)
        # if not os.path.exists(argspec.image):
        #     raise IOError('Cannot Open image file "%s"' % argspec.image)
        gop = GraphOp(argspec)
        gop.login()
        if argspec.op == GraphOp.OPS[0]:    # "List Users"
            gop.list_users()
        elif argspec.op == GraphOp.OPS[1]:  # "Get Root Drive"
            gop.get_root_drive()
        elif argspec.op == GraphOp.OPS[2]:  # "Get Children"
            gop.get_children()
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
    try:
        with ModuleContext(
            owner='ARGOS-LABS',
            group='2',  # business apps
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Microsoft Graph API',
            icon_path=get_icon_path(__file__),
            description='Microsoft Graph API portal',
        ) as mcxt:
            # ##################################### for app dependent parameters
            mcxt.add_argument('client_id',
                              display_name='Client ID', input_method='password',
                              help='Client ID for Microsoft Graph registered App')
            mcxt.add_argument('client_secret',
                              display_name='Client Secret', input_method='password',
                              help='Client Secret for Microsoft Graph Security Certificate')
            mcxt.add_argument('redirect_uri',
                              display_name='Redirect URI',
                              help='Redirect URI at Microsoft Graph registered App')
            mcxt.add_argument('credential_file',
                              display_name='Credential File',
                              input_method='fileread',
                              help='Authenticate at browser if not valid credential')
            mcxt.add_argument('op',
                              display_name='Operation',
                              choices=GraphOp.OPS,
                              help='Operations for Graph API')
            ######################################## for app dependent options
            # mcxt.add_argument('--children-folder',
            #                   display_name='Folder',
            #                   default='',
            #                   help='Folder for getting children items, empty means root')
            mcxt.add_argument('--auth-browser',
                              display_name='Browser',
                              choices=BROWSERS,
                              default=BROWSERS[0],
                              help='Browser for getting ')
            argspec = mcxt.parse_args(args)
            return do_msg(mcxt, argspec)
    except Exception as err:
        sys.stderr.write(f'{str(err)}')
        return 98


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
