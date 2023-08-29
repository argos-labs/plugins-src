#!/usr/bin/env python
# coding=utf8


"""
====================================
 :mod:`argoslabs.storage.oci`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS-LABS RPA Ocisdk plugin module

"""
# Authors Arun Kumar
# ===========
#
# * Arun Kumar ,
#
# Change Log
# --------
#



################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import oci
import shutil
import warnings

################################################################################
class OciOp(object):
    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.object_storage = None
        self.namespace = None


    # ==========================================================================
    def start(self):
        config = {
            "user": self.argspec.user,
            "fingerprint": self.argspec.fingerprint,
            "key_file": self.argspec.key_file,
            "tenancy": self.argspec.tenancy,
            "region": self.argspec.region
        }
        self.object_storage = oci.object_storage.ObjectStorageClient(config)
        self.namespace = self.object_storage.get_namespace().data


    # ==========================================================================
    def update_file_name(self,file_name,list_object):
        for n in range(1, 1000000):
            split_tup = os.path.splitext(file_name)
            nfn = f'{split_tup[0]}({n}){split_tup[1]}'
            find_match = self.check_file_oci_store(list_object, nfn)
            if len(find_match) == 0:
                return nfn


    # ==========================================================================
    @staticmethod
    def check_file_oci_store(list_object, file_name):
        find_match = [x for x in list_object if x.name == file_name]
        return find_match


    # ==========================================================================
    def list_file_oci_store(self):
        list_objects_response = self.object_storage.list_objects(
            namespace_name=self.namespace,
            bucket_name=self.argspec.bucket_name
        )
        list_object = list_objects_response.data.objects
        return list_object


    # ==========================================================================
    def upload_files(self):
        if self.argspec.upload_folder:
            file_name = f'{self.argspec.upload_folder}{os.path.basename(self.argspec.file)}'
        else:
            file_name = os.path.basename(self.argspec.file)
        list_object = self.list_file_oci_store()
        find_match = self.check_file_oci_store(list_object, file_name)
        if len(find_match) == 0:
            pass
        else:
            file_name = self.update_file_name(file_name,list_object)
        with open(self.argspec.file, "rb") as in_file:
            self.object_storage.put_object(
                namespace_name=self.namespace,
                bucket_name=self.argspec.bucket_name,
                object_name=file_name,
                put_object_body=in_file,
            )
        print(f"{file_name}, was uploaded successfully", end='')


    # ==========================================================================
    @staticmethod
    def _get_safe_next_filename(file_name):
        for n in range(1, 1000000):
            split_tup = os.path.splitext(file_name)
            nfn = f'{split_tup[0]}({n}){split_tup[1]}'
            if not os.path.exists(nfn):
                return nfn


    # ==========================================================================
    def download_files(self):
        get_object_response = self.object_storage.get_object(
            namespace_name=self.namespace,
            bucket_name=self.argspec.bucket_name,
            object_name=self.argspec.object_name
        )
        file_name = f'{self.argspec.output}/{self.argspec.object_name}'
        if os.path.exists(file_name):
            file_name = self._get_safe_next_filename(file_name)
        with open(file_name, 'wb') as out_file:
            shutil.copyfileobj(get_object_response.data.raw, out_file)
        print(file_name, end='')


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
        warnings.simplefilter("ignore", UserWarning)
        f = OciOp(argspec)
        f.start()
        if not argspec.op:
            raise Exception("Select OP Type")
        elif argspec.op == 'Upload Files':
            f.upload_files()
        elif argspec.op == 'Download Files':
            f.download_files()
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
        display_name='OCI',
        icon_path=get_icon_path(__file__),
        description='OCI SDK Module',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='OP Type', help='operation types',
                          choices=['Upload Files',
                                   'Download Files'])
        # ----------------------------------------------------------------------
        mcxt.add_argument('user', display_name='User',
                          help='User OCID',
                          input_method='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('fingerprint', display_name='Fingerprint',
                          help='Fingerprint must match keyfile',
                          input_method='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('key_file', display_name='Key File',
                          help='private key file',
                          input_method='fileread')
        # ----------------------------------------------------------------------
        mcxt.add_argument('tenancy', display_name='Tenancy',
                          help='Tenancy OCID',
                          input_method='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('region', display_name='Region',
                          help='OCI Region',
                          input_method='password')
        # ##################################### for app optional parameters
        mcxt.add_argument('--file', display_name='File to Upload',
                          input_method='fileread',
                          help='File to upload to OCI')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--bucket_name', display_name='Bucket Name',
                          help='Bucket Name of OCI')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--upload_folder', display_name='Upload Folder',
                          help='Folder path to upload file.e.g.- fo_name/, fo_name/sub_fo_name/')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--object_name', display_name='Object Name',
                          help='Object Name File name from OCI')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--output', display_name='Output Path',
                          input_method='folderwrite',
                          help='An absolute filepath to save a file')
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
