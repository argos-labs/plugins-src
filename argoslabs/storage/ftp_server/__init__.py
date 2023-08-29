#!/usr/bin/env python
# coding=utf8


"""
====================================
 :mod:`argoslabs.storage.ftp_server`
====================================
.. moduleauthor:: Arun Kumar <ak080495@gmail.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS-LABS RPA ftp_server plugin module

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
from ftplib import FTP as FTP_TLS
import warnings


################################################################################
class FtpOp(object):
    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.ftps = None
        self.filename = None

    # ==========================================================================
    def start(self):
        self.ftps = FTP_TLS()
        try:
            self.ftps.connect(self.argspec.host, self.argspec.port)
        except Exception as e:
            raise Exception(f"Invalid Host and Port.")
        try:
            self.ftps.login(self.argspec.user, self.argspec.password)
        except Exception as e:
            raise Exception(f"Invalid User and Password.")

    # ==========================================================================
    def upload_files(self):
        if self.argspec.ftp_dir:
            self.ftps.cwd(self.argspec.ftp_dir)
        if not self.argspec.file:
            raise Exception("file required to upload.")
        file_name = os.path.basename(self.argspec.file)
        self.ftps.encoding = "utf-8"
        with open(self.argspec.file, "rb") as file:
            self.ftps.storbinary(f"STOR {file_name}", file)
        self.ftps.quit()
        print(f"{file_name}, was uploaded successfully", end='')

    # ==========================================================================
    def download_files(self):
        if self.argspec.ftp_dir:
            self.ftps.cwd(self.argspec.ftp_dir)
        if not self.argspec.filename:
            raise Exception("filename required to download.")
        self.ftps.encoding = "utf-8"
        if self.argspec.output:
            self.filename = f"{self.argspec.output}\{self.argspec.filename}"
        else:
            self.filename = self.argspec.filename
        with open(self.filename, 'wb') as fp:
            self.ftps.retrbinary(f'RETR {self.argspec.filename}', fp.write)
        self.ftps.quit()
        print(f"{self.argspec.filename}, was downloaded successfully", end='')


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
        f = FtpOp(argspec)
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
            display_name='FTP Server',
            icon_path=get_icon_path(__file__),
            description='FTP Server Module',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='OP Type', help='operation types',
                          choices=['Upload Files',
                                   'Download Files'])
        # ----------------------------------------------------------------------
        mcxt.add_argument('host', display_name='Host',
                          help='Host')
        # ----------------------------------------------------------------------
        mcxt.add_argument('user', display_name='User',
                          help='User ID',
                          input_method='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('password', display_name='Password',
                          help='User Password',
                          input_method='password')
        # ##################################### for app optional parameters
        mcxt.add_argument('--port', display_name='Port',
                          default=21,
                          help='Port')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--ftp_dir', display_name='FTP Directory',
                          default='/',
                          help='FTP Directory e.g. /download')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--filename', display_name='Filename',
                          help='Filename to download')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--file', display_name='File to Upload',
                          input_method='fileread',
                          help='File to upload to FTP Server')
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
