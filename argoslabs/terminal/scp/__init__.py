#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.terminal.scp`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for ssh-expect operation for terminal
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/04/12]
#     - starting

################################################################################
import os
import sys
import paramiko
from scp import SCPClient
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class SCP(object):
    # ==========================================================================
    def __init__(self, server, port, user, password=None, key_filename=None):
        self.ssh = self._open(server, port, user, password, key_filename)
        self.scp = SCPClient(self.ssh.get_transport())

    # ==========================================================================
    @staticmethod
    def _open(server, port, user, password=None, key_filename=None):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if password:
            client.connect(server, port, user, password)
        elif key_filename:
            client.connect(server, port, user, key_filename=key_filename)
        return client

    # ==========================================================================
    def get(self, remote_path, local_path='', recursive=False, preserve_times=False):
        self.scp.get(remote_path, local_path, recursive, preserve_times)

    # ==========================================================================
    def put(self, files, remote_path, recursive=False, preserve_times=False):
        self.scp.put(files, remote_path, recursive, preserve_times)


################################################################################
@func_log
def do_ssh(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    # noinspection PyBroadException
    try:
        if not (argspec.password or argspec.key_filename):
            raise ValueError('Password or SSH keyfile must be given')
        if not argspec.remote:
            raise ValueError('Remote is not given!')
        if not argspec.local:
            raise ValueError('Local is not given!')
        scp = SCP(argspec.host, argspec.port, argspec.user,
                  password=argspec.password, key_filename=argspec.key_filename)
        if argspec.op == 'Get':
            scp.get(argspec.remote, argspec.local,
                    recursive=argspec.recursive,
                    preserve_times=argspec.preserve_times)
        elif argspec.op == 'Put':
            scp.put(argspec.local, argspec.remote,
                    recursive=argspec.recursive,
                    preserve_times=argspec.preserve_times)
        else:
            raise ValueError(f'Invalid Operation "{argspec.op}"')
        print(argspec.local, end='')
        return 0
    except Exception as e:
        msg = 'Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
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
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='SSH Copy',
        icon_path=get_icon_path(__file__),
        description='Termial operations with ssh',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--port',
                          display_name='Port',
                          type=int, default=22,
                          help='port number, default is [[22]]')
        mcxt.add_argument('--password', show_default=True,
                          display_name='Password',
                          input_method='password',
                          help='user password')
        mcxt.add_argument('--key-filename',
                          display_name='SSH keyfile',
                          help='SSH key filename instead of password')
        mcxt.add_argument('--recursive', action='store_true',
                          display_name='Recursive',
                          help='If this flag is set get or put recursively '
                               'including all files and sub folders')
        mcxt.add_argument('--preserve-times', action='store_true',
                          display_name='Preserve Times',
                          help='If this flag is set preserve file time attribute')
        # ##################################### for app dependent parameters
        mcxt.add_argument('host',
                          display_name='SSH Host',
                          help='hostname or ip address to connect')
        mcxt.add_argument('user',
                          display_name='SSH User',
                          help='user id to connect')
        mcxt.add_argument('op',
                          display_name='Operation',
                          choices=['Get', 'Put'],
                          help='One of Get or Put from remote file system')
        mcxt.add_argument('remote',
                          display_name='Remote File/Folder',
                          help='Remote file or folder')
        mcxt.add_argument('local',
                          display_name='Local File/Folder',
                          input_method='fileread',
                          help='Remote file or folder')

        argspec = mcxt.parse_args(args)
        return do_ssh(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
