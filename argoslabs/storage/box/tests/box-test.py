import os
import sys
import logging
from io import StringIO
from alabslib.selenium import PySelenium
from tempfile import gettempdir
from boxsdk import OAuth2, Client
# from collections import namedtuple
from dataclasses import dataclass
from typing import Any


################################################################################
@dataclass
class ModuleContext:
    logger: Any = None

@dataclass
class ArgsSpec:
    op: Any = None
    csecret: Any = None
    cid: Any = None
    token: Any = None
    redirect_uri: Any = None
    user_id: Any = None
    pwd: Any = None
    files: Any = None
    folderid: Any = None
    fileid: Any = None
    output: Any = None


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
        code = cur.split('code=')[1]
        return code


################################################################################
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

            # log_f = os.path.join(gettempdir(), "a.log")
            # logger = get_logger(log_f, logsize=1024 * 1024 * 10)
            logger = logging.getLogger('argoslabs.storage.box')
            _kwargs = {
                'browser': 'Edge',
                'url': auth_url,
                'user_id': argspec.user_id,
                'pwd': argspec.pwd,
                'headless': True,
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
def test_me():

    mcxt = ModuleContext()
    mcxt.logger = logging.getLogger('argoslabs.storage.box')
    argspec = ArgsSpec()
    argspec.op = 'Get Access Token'
    argspec.csecret = '___'
    argspec.cid = '___'
    # argspec.redirect_uri = 'https://app.box.com'
    argspec.redirect_uri = 'https://app.mybox.com'
    # argspec.redirect_uri = 'https://www.example.com/oauth2callback'
    argspec.user_id = '___'
    argspec.pwd = '___'

    tab(mcxt, argspec)


################################################################################
if __name__ == '__main__':
    test_me()
