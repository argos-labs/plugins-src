#!/usr/bin/env python
# coding=utf8


"""
====================================
 :mod:`argoslabs.storage.boxii`
====================================
.. moduleauthor:: Arun Kumar <ak080495@gmail.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS-LABS RPA Boxsdk plugin module

"""
# Authors Irene Cho
# ===========
#
# * Arun Kumar ,
#
# Change Log
# --------
#
#  * [2022/07/18]
#     - file list
#  * [2022/07/19]
#     - conf files
#  * [2022/07/20]
#     - generate token
#  * [2022/07/20]
#     - generate token show fix


################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from io import StringIO
from boxsdk import OAuth2, Client
from boxsdk.exception import BoxAPIException
from alabslib.selenium import PySelenium
# from alabs.common.util.vvlogger import get_logger
# from tempfile import gettempdir
import logging
import inspect
import warnings
import time
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
            '//*[@id="login"]')
        e.send_keys(self.user_id)
        e = self.get_by_xpath(
            '//*[@id="password"]')
        e.send_keys(self.pwd)
        e = self.get_by_xpath(
            '/html/body/div[3]/div/div[1]/div[2]/div/div[1]/form/div[1]/div[2]/input')
        self.safe_click(e)
        self.implicitly_wait()
        e = self.get_by_xpath(
            '//*[@id="consent_accept_button"]')
        self.safe_click(e)
        self.implicitly_wait()
        cur = self.driver.current_url
        code = cur.split('code=')[1]
        return code


################################################################################
class BoxOp(object):
    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec

    # ==========================================================================
    def move_file_folder(self, client,mcxt):
        outst = StringIO()
        if not self.argspec.dest_folderid:
            msg = "Dest Folder ID required"
            raise Exception(msg)
        if not self.argspec.additional_fileid and not self.argspec.additional_folderid:
            msg = "Additional File ID or Additional Folder ID required to Move"
            raise Exception(msg)
        destination_folder = client.folder(self.argspec.dest_folderid)
        if self.argspec.additional_fileid:
            for fileid in self.argspec.additional_fileid:
                _item = client.file(fileid).move(
                    parent_folder=destination_folder
                )
                outst.write(_item.name + ',' + str(_item.id))
                outst.write('\n')
        if self.argspec.additional_folderid:
            for folderid in self.argspec.additional_folderid:
                _item = client.folder(folderid).move(
                    parent_folder=destination_folder
                )
                outst.write(_item.name + ',' + str(_item.id))
                outst.write('\n')
        print(outst.getvalue(), end='')

    # ==========================================================================
    def delete_file_folder(self, client, mcxt):
        outst = StringIO()
        if not self.argspec.additional_fileid and not self.argspec.additional_folderid:
            msg = "Additional File ID or Additional Folder ID required to Delete"
            raise Exception(msg)
        if self.argspec.additional_fileid:
            for fileid in self.argspec.additional_fileid:
                _item = client.file(fileid).delete()
                if _item==True:
                    message = ''
                else:
                    message = ' not'
                outst.write(f'File Id {fileid}{message} deleted.')
                outst.write('\n')
        if self.argspec.additional_folderid:
            for folderid in self.argspec.additional_folderid:
                _item = client.folder(folderid).delete()
                outst.write(f'Folder Id {folderid} deleted.')
                outst.write('\n')
        print(outst.getvalue(), end='')

    # ==========================================================================
    def create_sharelink(self, client, mcxt):
        outst = StringIO()
        outst.write(f'file_id,shared_link')
        outst.write('\n')
        if not self.argspec.additional_fileid and not self.argspec.additional_folderid:
            msg = "Additional File ID or Additional Folder ID required to Create Link"
            raise Exception(msg)
        if self.argspec.additional_fileid:
            for fileid in self.argspec.additional_fileid:
                link = client.file(fileid).get_shared_link(
                    access='open',
                    allow_download=True
                )
                outst.write(f'{fileid},{link}')
                outst.write('\n')
        if self.argspec.additional_folderid:
            for folderid in self.argspec.additional_folderid:
                link = client.folder(folderid).get_shared_link(
                access='open',
                allow_download=True
                )
                outst.write(f'{folderid},{link}')
                outst.write('\n')
        print(outst.getvalue(), end='')

    # ==========================================================================
    def remove_sharelink(self, client, mcxt):
        outst = StringIO()
        outst.write(f'file_id,shared_link')
        outst.write('\n')
        if not self.argspec.additional_fileid and not self.argspec.additional_folderid:
            msg = "Additional File ID or Additional Folder ID required to Remove Link"
            raise Exception(msg)
        if self.argspec.additional_fileid:
            for fileid in self.argspec.additional_fileid:
                link = client.file(fileid).remove_shared_link()
                outst.write(f'{fileid},{"removed" if link else "failed to remove"}')
                outst.write('\n')
        if self.argspec.additional_folderid:
            for folderid in self.argspec.additional_folderid:
                link = client.folder(folderid).remove_shared_link()
                outst.write(f'{folderid},{"removed" if link else "failed to remove"}')
                outst.write('\n')
        print(outst.getvalue(), end='')

    # ==========================================================================
    def copy_file_folder(self, client,mcxt):
        outst = StringIO()
        if not self.argspec.dest_folderid:
            msg = "Dest Folder ID required"
            raise Exception(msg)
        if not self.argspec.additional_fileid and not self.argspec.additional_folderid:
            msg = "Additional File ID or Additional Folder ID required to Copy"
            raise Exception(msg)
        destination_folder = client.folder(self.argspec.dest_folderid)
        if self.argspec.additional_fileid:
            for fileid in self.argspec.additional_fileid:
                _item = client.file(fileid).copy(
                    parent_folder=destination_folder
                )
                outst.write(_item.name + ',' + str(_item.id))
                outst.write('\n')
        if self.argspec.additional_folderid:
            for folderid in self.argspec.additional_folderid:
                _item = client.folder(folderid).copy(
                    parent_folder=destination_folder
                )
                outst.write(_item.name + ',' + str(_item.id))
                outst.write('\n')
        print(outst.getvalue(), end='')


################################################################################
@func_log
def ctr(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        warnings.simplefilter("ignore", ResourceWarning)
        f = BoxOp(argspec)
        if argspec.token:
            oauth = OAuth2(
                client_id=argspec.cid, client_secret=argspec.csecret,
                access_token=argspec.token
            )
        else:
            oauth = OAuth2(client_id=argspec.cid, client_secret=argspec.csecret)
        client = Client(oauth)
        if not argspec.op:
            raise Exception("Select OP Type")
        elif argspec.op == 'Get Access Token':
            auth_url = oauth.get_authorization_url(argspec.redirect_uri)[0]
            def do_start(**kwargs):
                with sel(
                        kwargs['url'],
                        kwargs['user_id'],
                        kwargs['pwd'],
                        headless=kwargs.get('headless', True),
                        browser=kwargs.get('browser', 'Chrome'),
                        width=int(kwargs.get('width', '1200')),
                        height=int(kwargs.get('height', '800')),
                        logger=kwargs['logger']) as ws:
                    return ws.start()
            logger = logging.getLogger('argoslabs.storage.boxii')
            _kwargs = {
                'browser': 'Chrome',
                'url': auth_url,
                'user_id': argspec.user_id,
                'pwd': argspec.pwd,
                'headless': True,
                'logger': logger,
            }
            code = do_start(**_kwargs)
            access_token = oauth.authenticate(code)[0]
            print(str(access_token), end='')

        elif argspec.op == 'File/Folder Lists':
            outst = StringIO()
            outst.write('type,id,name')
            outst.write('\n')
            items = client.folder(argspec.folderid).get_items()
            for i in items:
                outst.write(i.type + ',' + str(i.id) + ',' + i.name)
                outst.write('\n')
            print(outst.getvalue(), end='')

        elif argspec.op == 'Upload Files':
            outst = StringIO()
            outst.write('name,id')
            outst.write('\n')
            cnt = 0
            err = ''
            for ent in argspec.files:
                try:
                    _item = client.folder(argspec.folderid).upload(file_path=ent)
                    outst.write(_item.name+','+str(_item.id))
                    outst.write('\n')
                    cnt += 1
                except BoxAPIException as msg:
                    err = str(msg)
                    pass
            if cnt==0:
                msg = str(err)
                mcxt.logger.error(msg)
                sys.stderr.write('%s%s' % (msg, os.linesep))
                return 1
            else:
                print(outst.getvalue(), end='')

        elif argspec.op == 'Download Files/Folder':
            items = []
            if argspec.folderid is None and argspec.fileid is None:
                msg = "Folder ID or File ID required"
                mcxt.logger.error(msg)
                sys.stderr.write('%s%s' % (msg, os.linesep))
                return 1
            if argspec.output is None:
                msg = "Output Path required"
                mcxt.logger.error(msg)
                sys.stderr.write('%s%s' % (msg, os.linesep))
                return 1
            if argspec.folderid:
                items += client.folder(argspec.folderid).get_items()
            if argspec.fileid:
                for id in argspec.fileid:
                    items.append(client.file(id).get())
            for ent in items:
                outst = StringIO()
                if ent.type == 'folder':
                    pass
                else:
                    location = os.path.join(argspec.output, ent.name)
                    i=1
                    def create_dir(cf_ent, _location):
                        if not os.path.exists(_location):
                            return _location
                        cf_ent += 1
                        return create_dir(cf_ent,_location.replace("("+str(cf_ent-1)+")"
                                                                   ,"("+str(cf_ent)+")"))
                    if os.path.exists(location):
                        base = os.path.basename(location)
                        _a = os.path.splitext(base)[0]
                        tem_location = os.path.join(argspec.output, os.path.splitext(base)[0]
                                                    + "("+str(i)+")"
                                                    +os.path.splitext(base)[1])
                        location = create_dir(i,tem_location)
                    output_file = open(location, 'wb')
                    client.file(ent.id).download_to(output_file)
                    outst.write(location)
                    outst.write('\n')
                    print(outst.getvalue(), end='')

        elif argspec.op == 'Move Files/Folder':
            f.move_file_folder(client, mcxt)

        elif argspec.op == 'Delete Files/Folder':
            f.delete_file_folder(client, mcxt)

        elif argspec.op == 'Create or update Shared Link':
            f.create_sharelink(client, mcxt)

        elif argspec.op == 'Remove Shared Link':
            f.remove_sharelink(client, mcxt)

        elif argspec.op == 'Copy Files/Folder':
            f.copy_file_folder(client, mcxt)
        else:
            raise Exception("Select OP Type")
        mcxt.logger.info('>>>end...')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='8',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Box II',
        icon_path=get_icon_path(__file__),
        description='Box SDK Module',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='OP Type', help='operation types',
                          choices=['Get Access Token', 'File/Folder Lists',
                                   'Upload Files',
                                   'Download Files/Folder',
                                   'Copy Files/Folder',
                                   'Move Files/Folder',
                                   'Delete Files/Folder',
                                   'Create or update Shared Link',
                                   'Remove Shared Link'])
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
        # ----------------------------------------------------------------------
        mcxt.add_argument('--additional_fileid',
                          display_name='Additional File ID',
                          action='append',
                          help='File ID to move/copy/delete file & create/remove shared link')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--additional_folderid',
                          display_name='Additional Folder ID',
                          action='append',
                          help='Folder ID to move/copy/delete folder & create/remove shared link')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--dest_folderid', display_name='Dest Folder ID',
                          help='Destination Folder ID to move/copy')
        argspec = mcxt.parse_args(args)
        return ctr(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
