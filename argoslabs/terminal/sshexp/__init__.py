#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.terminal.sshexp`
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
#  * [2019/04/15]
#     - starting

################################################################################
import os
import sys
import paramiko
from paramiko_expect import SSHClientInteraction
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class SshInteraction(object):
    # ==========================================================================
    def __init__(self, host, username,
                 port=22,
                 password=None,
                 key_filename=None,
                 connect_timeout=10,
                 echo_display=False,
                 expect_timeout=60, ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.key_filename = key_filename
        # for options
        self.connect_timeout = connect_timeout
        self.echo_display = echo_display
        self.expect_timeout = expect_timeout
        # for internal
        self.ssh = None
        self.exp = None
        self.current_output_clean = None
        self.opened = False
        self.open()

    # ==========================================================================
    def __del__(self):
        self.close()

    # ==========================================================================
    def __enter__(self):
        return self

    # ==========================================================================
    # noinspection PyShadowingBuiltins
    def __exit__(self, type, value, traceback):
        self.close()

    # ==========================================================================
    def open(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            self.host, port=self.port,
            username=self.username,
            password=self.password,
            key_filename=self.key_filename,
        )
        self.exp = SSHClientInteraction(self.ssh, timeout=self.connect_timeout,
                                        display=self.echo_display)
        self.opened = True
        return self.opened

    # ==========================================================================
    def close(self):
        if self.opened:
            self.exp.close()
            self.ssh.close()
            self.opened = False
            return True
        return False

    # ==========================================================================
    def expect(self, re_string):
        if not self.opened:
            raise RuntimeError('First open to use expect')
        self.exp.expect(re_string, timeout=self.expect_timeout)
        self.current_output_clean = self.exp.current_output_clean

    # ==========================================================================
    def sendline(self, send_string):
        if not self.opened:
            raise RuntimeError('First open to use sendline')
        self.exp.send(send_string)


################################################################################
@func_log
def do_expect(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    # noinspection PyBroadException
    try:
        if argspec.display_index is None:
            argspec.display_index = []
        with SshInteraction(
            argspec.host, argspec.user,
            port=argspec.port,
            password=argspec.password,
            key_filename=argspec.key_filename,
            connect_timeout=argspec.connect_timeout,
            echo_display=argspec.echo_display,
        ) as exp:
            exp.expect(argspec.prompt)
            for i, cmd in enumerate(argspec.command):
                exp.sendline(cmd)
                exp.expect(argspec.prompt)
                if i + 1 in argspec.display_index:
                    sys.stdout.write(exp.current_output_clean)
            # if argspec.display_index >= len(argspec.command):
            #     exp.expect(argspec.prompt)
            #     sys.stdout.write(exp.current_output_clean)
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
        display_name='SSH Command',
        icon_path=get_icon_path(__file__),
        description='Termial operations with ssh',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--port',
                          display_name='Port',
                          type=int, default=22,
                          min_value=1, max_value=65525,
                          help='port number, default is [[22]]')
        mcxt.add_argument('--password',
                          display_name='Password',
                          input_method='password',
                          help='user password')
        mcxt.add_argument('--key-filename',
                          display_name='SSH keyfile',
                          help='SSH key filename')
        mcxt.add_argument('--connect-timeout',
                          display_name='Connect timeout',
                          type=int, default=10,
                          help='connection timeout, default is [[10]]')
        mcxt.add_argument('--expect-timeout',
                          display_name='Prompt Expect timeout',
                          type=int, default=60,
                          help='expectation string waiting timeout, default is [[60]]')
        mcxt.add_argument('--echo-display', action='store_true',
                          display_name='Echo On',
                          help='If this flag is set echo all command output')
        mcxt.add_argument('--display-index', nargs='+', type=int,
                          display_name='Display index',
                          help='1-based index to display the output from command list')
        # ##################################### for app dependent parameters
        mcxt.add_argument('host',
                          display_name='SSH Host',
                          help='hostname or ip address to connect')
        mcxt.add_argument('user',
                          display_name='SSH User',
                          help='user id to connect')
        mcxt.add_argument('prompt',
                          display_name='Prompt RegExp',
                          help='prompt to expected')
        mcxt.add_argument('command', nargs='+',
                          display_name='Commands at terminal',
                          help='one or more command to execute')

        argspec = mcxt.parse_args(args)
        return do_expect(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
