#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.aws_s3_operation`
====================================
.. moduleauthor:: Taiki Shimasaki <shimasaki@argos-service.com>
.. note:: ARGOS-LABS License

Description
===========
Input Plugin Description
"""
# Authors
# ===========
#
# * Taiki Shimasaki
#
# Change Log
# --------
#
#  * [2021/04/12]
#     Create

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgumentParser, ArgsError, ArgsExit, get_icon_path
import boto3
from boto3.session import Session
from os.path import expanduser
import re
import shutil
import PySimpleGUIQt as sg
# from hurry.filesize import size

################################################################################
# Change Popup Theme here
sg.theme('DefaultNoMoreNagging')

################################################################################
class S3_Operation(object):

    # ==========================================================================
    def __init__(self, op):
        self.op = op
        self.path = None
        # self.path_list = []

        self.home_path = expanduser("~")
        self.auth_file = None

        self.profile = None
        self.session = None

        self.aws_folder = None
        self.credentials_file = None
        self.config_file = None

        self.key_id = None
        self.secret_key = None
        self.default_region = None

        self.credentials_contents = None
        self.config_contents = None

        self.bucket_path = None

        self.file = None
        self.file_name = None
        self.dir = None

        self.file_path = None
        self.source = None

        self.bucket = None
        self.folder = None
        self.dl_file = None
        self.dl_file_path = None
        self.response = None
        self.response_key = None

        self.layout = []
        self.dummy_text = '************'

    # ==========================================================================
    def aws_folder_check(self):
        self.aws_folder = '{}{}.aws'.format(self.home_path, os.sep)

        if not os.path.isdir(self.aws_folder):
            # os.makedirs(self.aws_folder, exist_ok=True)
            self.auth_file = 'no_folder'
        else:
            pass

    # ==========================================================================
    def select_profile(self, profile):
        self.profile = profile
        self.session = Session(profile_name=self.profile)

    # ==========================================================================
    def credentials_file_check(self, key_id, secret_key):
        self.key_id = key_id
        self.secret_key = secret_key

        self.session = Session(aws_access_key_id=self.key_id,
                               aws_secret_access_key=self.secret_key)

        # It overwrites the file (No use)
        """
        self.credentials_file = '{}{}credentials'.format(self.aws_folder, os.sep)

        self.credentials_contents = '[argos]\n' \
                                    'aws_access_key_id = {}\n' \
                                    'aws_secret_access_key = {}'.format(self.key_id,
                                                                        self.secret_key)

        if not os.path.isfile(self.credentials_file):
            with open(self.credentials_file, mode="w") as f:
                f.write(self.credentials_contents)

            if self.auth_file == 'no_folder':
                pass
            else:
                self.auth_file = 'credentials'

        else:
            raise IOError(r'".aws/credentials" file is already exists!')
        """

    # ==========================================================================
    def config_file_check(self, default_region):
        self.default_region = default_region

        self.session = Session(region_name=self.default_region)

        # It overwrites the file (No use)
        """
        self.config_file = '{}{}config'.format(self.aws_folder, os.sep)

        self.config_contents = '[argos]\n' \
                               'region = {}\n' \
                               'output = json'.format(self.default_region)

        if not os.path.isfile(self.config_file):
            with open(self.config_file, mode="w") as f:
                f.write(self.config_contents)

            if self.auth_file == 'no_folder':
                pass
            elif self.auth_file == 'credentials':
                self.auth_file = 'both'
            else:
                self.auth_file = 'config'

        else:
            raise IOError(r'".aws/config" file is already exists!')
        """

    # ==========================================================================
    def select_op(self):
        if self.op == 'Upload':
            return 'up'
        elif self.op == 'Download':
            return 'dl'
        elif self.op == 'Get List':
            return 'ls'
        elif self.op == 'Delete Files':
            return 'df'
        elif self.op == 'Make Bucket':
            return 'mb'
        elif self.op == 'Remove Bucket':
            return 'rb'
        elif self.op == 'Copy':
            return 'cp'
        elif self.op == 'Exists Check':
            return 'ex'
        elif self.op == 'Sync':
            return 'sync'
        else:
            raise IOError('Unexpected error occurred')

    # ==========================================================================
    def f_check(self, path):
        self.path = path

        if self.op == 'Upload':
            if os.path.isdir(self.path):
                raise IOError('This local path must be a file path!')
            elif os.path.isfile(self.path):
                self.file = self.path
            else:
                raise IOError('{} is not exists!'.format(self.path))

        elif self.op == 'Download':
            if os.path.isdir(self.path):
                self.dir = self.path
            elif os.path.isfile(self.path):
                raise IOError('This local path must be a directory path!')
            else:
                raise IOError('{} is not exists!'.format(self.path))

    # ==========================================================================
    def file_check(self):
        self.file = os.path.abspath(self.file)

        if not os.path.isfile(self.file):
            raise IOError('{} is not exists!'.format(self.file_name))
        else:
            self.file_name = os.path.basename(self.file)

    # ==========================================================================
    def dir_check(self):
        self.dir = os.path.abspath(self.dir)

        if not os.path.isdir(self.dir):
            raise IOError('{} is not exists!'.format(self.dir))
        else:
            pass

    # ==========================================================================
    def bucket_sep(self, bucket_path):
        self.bucket_path = bucket_path

        if self.bucket_path:
            if self.bucket_path.startswith('/'):  # 先頭/削除
                self.bucket_path = self.bucket_path[1:]
            elif self.bucket_path.endswith('/'):  # 最後/削除
                self.bucket_path = self.bucket_path[:-1]
            elif self.bucket_path.startswith('/') and self.bucket_path.endswith('/'):  # 前後両方/削除
                self.bucket_path = self.bucket_path[1:]
                self.bucket_path = self.bucket_path[:-1]
            else:
                pass
        else:
            pass

        if '/' in self.bucket_path:
            self.bucket = self.bucket_path.split('/', 1)[0]
            if self.bucket_path.split('/', 1)[1]:
                self.folder = self.bucket_path.split('/', 1)[1]
            else:
                self.folder = None
        else:
            self.bucket = self.bucket_path

    # ==========================================================================
    def file_upload(self):
        s3 = self.session.resource('s3')
        bucket = s3.Bucket(self.bucket)
        if self.folder:
            self.response = bucket.upload_file(self.file,
                                               '{}/{}'.format(self.folder,
                                                              self.file_name))
        else:
            self.response = bucket.upload_file(self.file, self.file_name)

        print('{}/{}/{}'.format(self.bucket, self.folder, self.file_name))

    # ==========================================================================
    def file_download(self):
        if '/' in self.folder:
            self.dl_file = self.folder.rsplit('/', 1)[1]
            self.folder = self.folder.rsplit('/', 1)[0]
            self.dl_file_path = '{}/{}'.format(self.dir, self.dl_file)
        else:
            raise IOError('This Bucket path must be a file path!')

        s3 = self.session.resource('s3')
        bucket = s3.Bucket(self.bucket)
        if self.folder:
            self.response = bucket.download_file('{}/{}'.format(self.folder, self.dl_file),
                                                 self.dl_file_path)
        else:
            self.response = bucket.download_file(self.dl_file,
                                                 self.dl_file_path)

        print('{}{}{}'.format(self.dir, os.sep, self.dl_file))

    # ==========================================================================
    def delete_files(self):
        if self.folder:
            self.file = self.folder
        else:
            raise IOError('Not Exists file path')

        s3 = self.session.resource('s3')
        bucket = s3.Bucket(self.bucket)

        self.response = bucket.objects.filter(Prefix=self.file).delete()

        print(self.response)

    # ==========================================================================
    def exists_check(self):
        bucket_path = self.bucket
        file_path = self.folder

        s3 = self.session.client('s3')

        result = s3.list_objects(Bucket=bucket_path, Prefix=file_path)

        if "Contents" in result:
            # self.exists = True
            return True
        else:
            # self.exists = False
            return False

    # ==========================================================================
    def copy_files(self, file_path):
        self.file_path = file_path  # base
        self.file_name = os.path.basename(self.file_path)  # base_name&ext
        self.filename, self.ext = os.path.splitext(self.file_name)
        folder_base = self.folder  # bucket_tar_folder

        if self.folder:
            self.folder = folder_base + '/' + self.file_name  # tarfol+file
        else:
            self.folder = self.file_name

        if self.file_path:
            if self.file_path.startswith('/'):  # 先頭/削除
                self.file_path = self.file_path[1:]
            elif self.file_path.endswith('/'):  # 最後/削除
                self.file_path = self.file_path[:-1]
            elif self.file_path.startswith('/') and self.file_path.endswith('/'):  # 前後両方/削除
                self.file_path = self.file_path[1:]
                self.file_path = self.file_path[:-1]
            else:
                pass
        else:
            pass

        if '/' in self.file_path:
            self.bucket_path = self.file_path.split('/', 1)[0]
            if self.file_path.split('/', 1)[1]:
                self.file_path = self.file_path.split('/', 1)[1]
            else:
                raise IOError('File Name is NOT exists!')
        else:
            raise IOError('File Name is NOT exists!')

        count = 0

        if self.ext != '':
            while self.exists_check() == True:
                self.file_name = os.path.basename(self.folder)
                self.filename, self.ext = os.path.splitext(self.file_name)
                self.filename = re.sub(r'\([0-9]+\)$', '', self.filename)
                count += 1
                self.filename += '({})'.format(count)
                self.file_name = '{}{}'.format(self.filename, self.ext)

                self.folder = folder_base + '/' + self.file_name  # target_folder&name&ext

            else:
                pass

        else:
            while self.exists_check() == True:
                self.file_name = os.path.basename(self.folder)
                self.filename, self.ext = os.path.splitext(self.file_name)
                self.filename = re.sub(r'\([0-9]+\)$', '', self.filename)
                count += 1
                self.filename += '({})'.format(count)
                self.file_name = '{}'.format(self.filename)

                self.folder = folder_base + '/' + self.file_name  # target_folder&name&ext

            else:
                pass

        self.source = {
            'Bucket': self.bucket_path,
            'Key': self.file_path
        }
        s3 = self.session.resource('s3')

        self.response = s3.meta.client.copy(self.source, self.bucket, self.folder)

        print(self.response)

        self.folder = folder_base  # initialize

    # ==========================================================================
    def get_list(self, bucket_path):
        self.bucket_path = bucket_path
        s3 = self.session.client('s3')

        if self.bucket_path == None:
            self.response = s3.list_buckets()
            self.response = self.response['Buckets']

            for buckets in self.response:
                self.response_key = buckets['Name']

                print(self.response_key)

        elif self.bucket_path:
            self.response = s3.list_objects_v2(Bucket=self.bucket_path)
            self.response = self.response['Contents']
            for contents in self.response:
                self.response_key = contents['Key']

                print(self.response_key)

    # ==========================================================================
    def make_bucket(self, bucket_path):
        self.bucket_path = bucket_path
        s3 = self.session.client('s3')

        self.response = s3.create_bucket(Bucket=self.bucket_path)

        print(self.response)

    # ==========================================================================
    def del_auth_files(self):
        if self.auth_file == 'no_folder':
            shutil.rmtree(self.aws_folder)
        elif self.auth_file == 'credentials':
            os.remove(self.credentials_file)
        elif self.auth_file == 'config':
            os.remove(self.config_file)
        elif self.auth_file == 'both':
            os.remove(self.credentials_file)
            os.remove(self.config_file)
        else:
            pass

    # ==========================================================================
    def def_layout(self, file_count):
        if self.op == 'Upload':
            self.layout = [
                [sg.Text("{}".format(self.dummy_text), size=(20, 2), key="text")],
                [sg.ProgressBar(file_count, size=(20, 20), key='progbar')]
            ]

        elif self.op == 'Download':
            self.layout = [
                [sg.Text("{}".format(self.dummy_text), size=(20, 2), key="text")],
                [sg.ProgressBar(file_count, orientation='h', size=(20, 20), key='progbar')]
            ]

        else:
            pass

        return self.layout

################################################################################
@func_log
def operate_s3(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        S3_OP = S3_Operation(argspec.op)

        # Auth File Check & Create ---------------------------------------------
        S3_OP.aws_folder_check()
        if not argspec.profile == 'default':
            S3_OP.select_profile(argspec.profile)

        else:
            S3_OP.select_profile(argspec.profile)

            if argspec.key_id or argspec.secret_key:
                S3_OP.credentials_file_check(argspec.key_id, argspec.secret_key)
            else:
                pass

            if not argspec.default_region == 'us-east-2':
                S3_OP.config_file_check(argspec.default_region)
            else:
                pass

        # Check OP -------------------------------------------------------------
        OP = S3_OP.select_op()

        # Change List ----------------------------------------------------------
        if OP in ('up', 'dl'):
            if not argspec.path and argspec.bucket_path:
                raise IOError('Input Bucket Path and File or Folder!')
            else:
                argspec.path = [argspec.path]
                argspec.bucket_path = [argspec.bucket_path]

        # Operations -----------------------------------------------------------
        if OP == 'up':
            if argspec.add_path:
                argspec.path.extend(argspec.add_path)
            else:
                pass

            if len(argspec.bucket_path) > 1:
                raise IOError('Must be only one \"Bucket Path\"!')

            elif argspec.show_progress == 'OFF':
                for path in argspec.path:
                    S3_OP.f_check(path)
                    S3_OP.file_check()
                    S3_OP.bucket_sep(argspec.bucket_path[0])

                    S3_OP.file_upload()

            elif argspec.show_progress == 'ON':
                file_count = len(argspec.path)
                layout = S3_OP.def_layout(file_count)
                window = sg.Window("Uploading Status", layout)

                for path in argspec.path:
                    event, values = window.read(timeout=0)
                    if event == event is None:
                        break

                    filename = os.path.basename(path)
                    window["text"].update('Now Uploading...\n{}'.format(filename))
                    window["progbar"].UpdateBar(argspec.path.index(path) + 1)

                    S3_OP.f_check(path)
                    S3_OP.file_check()
                    S3_OP.bucket_sep(argspec.bucket_path[0])

                    S3_OP.file_upload()

                window.close()

            else:
                pass


        elif OP == 'dl':
            if argspec.add_path:
                argspec.bucket_path.extend(argspec.add_path)
            else:
                pass

            if len(argspec.path) > 1:
                raise IOError('Must be only one \"Folder Path\"!')

            elif argspec.show_progress == 'OFF':
                for bucket_path in argspec.bucket_path:
                    S3_OP.f_check(argspec.path[0])
                    S3_OP.dir_check()
                    S3_OP.bucket_sep(bucket_path)
                    S3_OP.file_download()

            elif argspec.show_progress == 'ON':
                file_count = len(argspec.bucket_path)
                layout = S3_OP.def_layout(file_count)
                window = sg.Window("Downloading Status", layout)

                for bucket_path in argspec.bucket_path:
                    event, values = window.read(timeout=0)
                    if event == event is None:
                        break

                    filename = os.path.basename(bucket_path)
                    window["text"].update('Now Downloading...\n{}'.format(filename))
                    window["progbar"].UpdateBar(argspec.bucket_path.index(bucket_path) + 1)

                    S3_OP.f_check(argspec.path[0])
                    S3_OP.dir_check()
                    S3_OP.bucket_sep(bucket_path)
                    S3_OP.file_download()

                window.close()

            else:
                pass


        elif OP == 'df':
            del_file_path = [argspec.bucket_path]

            if argspec.add_path:
                del_file_path.extend(argspec.add_path)
            else:
                pass

            for file_path in del_file_path:
                S3_OP.bucket_sep(file_path)

                S3_OP.delete_files()


        elif OP == 'cp':
            cp_file_path = [argspec.path]

            if argspec.add_path:
                cp_file_path.extend(argspec.add_path)
            else:
                pass

            S3_OP.bucket_sep(argspec.bucket_path)

            for file_path in cp_file_path:

                S3_OP.copy_files(file_path)

        elif OP == 'ex':
            argspec.bucket_path = [argspec.bucket_path]

            if argspec.add_path:
                argspec.bucket_path.extend(argspec.add_path)
            else:
                pass
            for bucket_path in argspec.bucket_path:
                S3_OP.bucket_sep(bucket_path)
                if S3_OP.exists_check() == True:
                    print('{} is exists!'.format(bucket_path))
                else:
                    print('{} is NOT exists!'.format(bucket_path))

        elif OP == 'ls':
            S3_OP.get_list(argspec.bucket_path)

        elif OP == 'mb':
            S3_OP.make_bucket(argspec.bucket_path)

        else:
            raise IOError('Unexpected error occurred')

        # Del Auth Files -------------------------------------------------------
        # S3_OP.del_auth_files()

        mcxt.logger.info('>>>end...')
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
        owner='ARGOS-SERVICE-JAPAN',
        group='8',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='AWS S3',
        icon_path=get_icon_path(__file__),
        description='Plugin to manipulate AWS S3',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Operation',
                          choices=['Upload',
                                   'Download',
                                   'Get List',
                                   'Delete Files',
                                   'Copy',
                                   'Exists Check',
                                   # 'Make Bucket'
                                   ],
                          help='Select Operation')
        mcxt.add_argument('--bucket_path',
                          display_name='Bucket Path',
                          show_default=True,
                          help='Input your Bucket Name [[Bucket/Folder(/File)]]')
        mcxt.add_argument('--path',
                          display_name='File or Folder',
                          show_default=True,
                          input_method='fileread',
                          help='Select a Local File or Folder')
        # ######################################## for app dependent options
        mcxt.add_argument('--add_path',
                          display_name='Additional Paths',
                          show_default=True,
                          action='append',
                          # input_method='fileread',
                          help='Input the additional file or bucket paths')
        mcxt.add_argument('--profile',
                          input_group='AWS Account Settings',
                          display_name='Profile Name',
                          show_default=True,
                          default='default',
                          help='Input your Profile Name')
        mcxt.add_argument('--key_id',
                          input_group='AWS Account Settings',
                          input_method='password',
                          display_name='Access Key ID',
                          show_default=True,
                          help='Input your Access Key ID')
        mcxt.add_argument('--secret_key',
                          input_group='AWS Account Settings',
                          input_method='password',
                          show_default=True,
                          display_name='Secret Access Key',
                          help='Input your Secret Access Key')
        mcxt.add_argument('--default_region',
                          input_group='AWS Account Settings',
                          default='us-east-2',
                          display_name='Default Region',
                          help='AWS region of the server that sends the requests by default')
        mcxt.add_argument('--show_progress',
                          default='ON',
                          choices=['ON', 'OFF'],
                          display_name='Show Progress',
                          help='Toggle whether to show the Progress Window')

        argspec = mcxt.parse_args(args)
        return operate_s3(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
