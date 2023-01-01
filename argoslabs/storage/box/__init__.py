"""
====================================
 :mod:`argoslabs.storage.box`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS BOX SDK
"""
# Authors
# ===========
#
# * Irene Cho, Jerry Chae
#
# --------
#
#  * [2022/03/30]
#     - alabs.selenium => alabslib.selenium
#  * [2021/06/15]
#     - Add Selenium Option
#  * [2021/06/09]
#     - starting

################################################################################
import os
import sys
from io import StringIO
from tempfile import gettempdir
from boxsdk import OAuth2, Client
from alabslib.selenium import PySelenium
from alabs.common.util.vvlogger import get_logger
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path



################################################################################
class sel(PySelenium):
    # ==========================================================================
    def __init__(self, url, user_id, pwd, **kwargs):
        kwargs['url'] = url
        PySelenium.__init__(self, **kwargs)
        self.user_id = user_id
        self.pwd = pwd

    # ==========================================================================
    def start(self):
        e = self.get_by_xpath(
            '/html/body/div[3]/div/div[1]/div[2]/div/div[1]/form/div[1]/div[1]/div[1]/input')
        e.send_keys(self.user_id)
        e = self.get_by_xpath(
            '/html/body/div[3]/div/div[1]/div[2]/div/div[1]/form/div[1]/div[1]/div[2]/input')
        e.send_keys(self.pwd)
        e = self.get_by_xpath(
            '/html/body/div[3]/div/div[1]/div[2]/div/div[1]/form/div[1]/div[2]/input')
        self.safe_click(e)
        self.implicitly_wait()
        e = self.get_by_xpath(
            '/html/body/div[3]/div/div/div/form/div/div[1]/button')
        self.safe_click(e)
        self.implicitly_wait()
        cur = self.driver.current_url
        if cur.find('code=') < 0:
            raise ReferenceError(f'Cannot find "Access Token" from redirect URI')
        code = cur.split('code=')[1]
        return code


################################################################################
@func_log
def tab(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if argspec.token:
            oauth = OAuth2(
                client_id=argspec.cid, client_secret=argspec.csecret,
                access_token=argspec.token
            )
        else:
            oauth = OAuth2(client_id=argspec.cid, client_secret=argspec.csecret)
        client = Client(oauth)
        if argspec.op == 'Get Access Token':
            auth_url = oauth.get_authorization_url(
                argspec.redirect_uri)[0]

            def do_start(**kwargs):
                with sel(
                        kwargs['url'],
                        kwargs['user_id'],
                        kwargs['pwd'],
                        headless=kwargs.get('headless', False),
                        browser=kwargs.get('browser', 'Chrome'),
                        width=int(kwargs.get('width', '1200')),
                        height=int(kwargs.get('height', '800')),
                        logger=kwargs['logger']) as ws:
                    return ws.start()

            log_f = os.path.join(gettempdir(), "a.log")
            logger = get_logger(log_f, logsize=1024 * 1024 * 10)
            _kwargs = {
                # 'browser': 'Edge',
                'browser': 'Chrome',
                'url': auth_url,
                'user_id': argspec.user_id,
                'pwd': argspec.pwd,
                # 'headless': True,
                'headless': False,
                'logger': logger,
            }
            code = do_start(**_kwargs)
            access_token = oauth.authenticate(code)[0]
            print(access_token, end='')

        if argspec.op == 'File/Folder Lists':
            with StringIO() as outst:
                items = client.folder(argspec.folderid).get_items()
                outst.write('type,id,name')
                outst.write('\n')
                for i in items:
                    outst.write(i.type + ',' + str(i.id) + ',' + i.name)
                    outst.write('\n')
                print(outst.getvalue(), end='')
        elif argspec.op == 'Upload Files':
            cnt = 0
            for ent in argspec.files:
                try:
                    client.folder(argspec.folderid).upload(ent)
                    cnt += 1
                except Exception as err:
                    msg = str(err)
                    mcxt.logger.error(msg)
                    sys.stderr.write('%s%s' % (msg, os.linesep))
                    return 9
            print(f'Successfully uploaded {cnt} files', end='')
        elif argspec.op == 'Download Files/Folder':
            items = []
            try:
                if argspec.folderid:
                    items += client.folder(argspec.folderid).get_items()
                if argspec.fileid:
                    for id in argspec.fileid:
                        items.append(client.file(id).get())
                for ent in items:
                    with StringIO() as outst:
                        location = os.path.join(argspec.output, ent.name)
                        output_file = open(location, 'wb')
                        client.file(ent.id).download_to(output_file)
                        outst.write(location)
                        outst.write('\n')
                        print(outst.getvalue(), end='')
            except Exception as err:
                msg = str(err)
                mcxt.logger.error(msg)
                sys.stderr.write('%s%s' % (msg, os.linesep))
                return 9
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
            display_name='BOX',
            icon_path=get_icon_path(__file__),
            description='Managing BOX',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='OP Type', help='operation types',
                            choices=['Get Access Token', 'File/Folder Lists',
                                    'Upload Files',
                                    'Download Files/Folder'])
        # ----------------------------------------------------------------------
        mcxt.add_argument('csecret', display_name='Client Secret',
                            help='Client Secret',
                            input_method='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('cid', display_name='Client ID', help='Client ID')
        # ##################################### for app optional parameters
        mcxt.add_argument('--token', display_name='Token', help='Token',
                            input_method='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--redirect_uri', display_name='Redirect URI',
                            help='Redirect URI')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--user_id', display_name='User ID',
                            help='user id')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--pwd', display_name='Password',
                            help='Password', input_method='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--files', display_name='Files to Upload',
                            input_method='fileread', action='append',
                            help='Files to upload to BOX')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--folderid', display_name='Folder ID',
                            help='Folder ID from BOX')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--fileid', display_name='File ID', action='append',
                            help='File ID from BOX')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--output', display_name='Output Path',
                            input_method='folderwrite',
                            help='An absolute filepath to save a file')
        argspec = mcxt.parse_args(args)
        return tab(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
