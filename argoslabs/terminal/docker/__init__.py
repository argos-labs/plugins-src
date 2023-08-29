#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.terminal.docker`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for docker/docker-compose remote service using ssh-expect operation
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/04/08]
#     - test
#  * [2022/04/07]
#     - starting

################################################################################
import os
import sys
import json
import shutil
import tempfile
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
        self.last_cmd = None
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
        coc = self.exp.current_output_clean
        if self.last_cmd and coc.startswith(self.last_cmd):
            coc = coc[len(self.last_cmd):].lstrip('\n')
        self.current_output_clean = coc

    # ==========================================================================
    def sendline(self, send_string):
        if not self.opened:
            raise RuntimeError('First open to use sendline')
        self.last_cmd = send_string
        self.exp.send(send_string)


################################################################################
class DockerSsh(SshInteraction):
    # TODO: color prompt does not support, .bashrc disable force_color_pormpt=yes
    # ==========================================================================
    def __init__(self, *args,
                 prompt=None,
                 working_directory='~/.argos-rpa.svc',
                 **kwargs):
        SshInteraction.__init__(self, *args, **kwargs)
        if not prompt:
            username = args[1]
            prompt = fr'.*{username}@.*\$ ' if username != 'root' else fr'.*{username}@.*# '
        self.prompt = prompt
        self.expect(self.prompt)
        self.docker_info = None
        self.get_docker_info()
        self.working_directory = self._change_home(working_directory)

    # ==========================================================================
    def _change_home(self, wd):
        if wd.startswith('~'):
            out = self.do_cmd('echo $HOME')
            wd = wd.replace('~', out.strip())
        return wd

    # ==========================================================================
    def do_cmd(self, cmd):
        self.sendline(cmd)
        self.expect(self.prompt)
        if self.current_output_clean.startswith('?2004l'):  # for escape sequence
            self.current_output_clean = self.current_output_clean[6:]
        return self.current_output_clean.strip()

    # ==========================================================================
    def check_cmds(self):
        out = self.do_cmd('which docker')
        if not out:
            raise EnvironmentError(f'docker is not installed on this system')
        out = self.do_cmd('which docker-compose')
        if not out:
            raise EnvironmentError(f'docker-compose is not installed on this system')

    # ==========================================================================
    def get_docker_info(self):
        self.check_cmds()
        out = self.do_cmd("docker info --format '{{json .}}'")
        try:
            fndx = out.find('{')
            if fndx > 0:
                out = out[fndx:]
            self.docker_info = json.loads(out)
        except Exception:
            raise EnvironmentError(f'JSON parsing error to get docker info for "{out}"')

    # ==========================================================================
    def do_docker_cmd(self, cmd):
        out = self.do_cmd(f'docker {cmd}')
        return out

    # ==========================================================================
    def _path_exists(self, p):
        out = self.do_cmd(f'ls "{p}" >/dev/null 2>/dev/null; echo $?')
        return out.strip() == '0'

    # ==========================================================================
    def _copy_l2r(self, s, r_t):
        if not os.path.exists(s):
            raise IOError(f'Cannot get source file "{s}"')
        with open(s, encoding='utf-8') as ifp:
            self.sendline(f"cat <<'EOF' > '{r_t}'")
            for i, line in enumerate(ifp):
                line = line.rstrip()
                self.expect(r'.*> ')
                self.sendline(line)
            self.expect(r'.*> ')
            self.sendline('EOF')
            self.expect(self.prompt)
        return self._path_exists(r_t)

    # ==========================================================================
    def _docker_compose_init(self, yaml_file, is_overwrite=False):
        if not os.path.exists(yaml_file):
            raise IOError(f'Cannot get Docker Compose file "{yaml_file}"')
        bn = os.path.basename(yaml_file)
        svc_name, _ = os.path.splitext(bn)
        svc_folder = f'{self.working_directory}/{svc_name}'
        self.do_cmd(f'mkdir -p "{svc_folder}"')
        svc_yaml = f'{svc_folder}/{bn}'
        if not (self._path_exists(svc_yaml) and not is_overwrite):
            r = self._copy_l2r(yaml_file, svc_yaml)
            if not r:
                raise RuntimeError(f'Target Service Yaml file "{svc_yaml}" does not exists')
        return svc_yaml

    # ==========================================================================
    def docker_compose_start(self, yaml_file):
        svc_yaml = self._docker_compose_init(yaml_file, is_overwrite=True)
        out = self.do_cmd(f'docker-compose -f "{svc_yaml}" up -d')
        return out

    # ==========================================================================
    def docker_compose_stop(self, yaml_file):
        svc_yaml = self._docker_compose_init(yaml_file)
        out = self.do_cmd(f'docker-compose -f "{svc_yaml}" down')
        return out

    # ==========================================================================
    def docker_compose_status(self, yaml_file):
        svc_yaml = self._docker_compose_init(yaml_file)
        out = self.do_cmd(f'docker-compose -f "{svc_yaml}" ps')
        return out


################################################################################
OPS = [
    'Docker Info',
    'Docker Command',
    'Start Docker Compose',
    'Stop Docker Compose',
    'State of Docker Compose',
]


################################################################################
@func_log
def do_docker(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    # noinspection PyBroadException
    try:
        with DockerSsh(
            argspec.host, argspec.user,
            port=argspec.port,
            password=argspec.password,
            key_filename=argspec.key_filename,
            connect_timeout=argspec.connect_timeout,
            echo_display=False,
        ) as dk:
            if argspec.op == OPS[0]:  # Docker Info
                json.dump(dk.docker_info, sys.stdout)
            elif argspec.op == OPS[1]:  # Docker Command
                if not argspec.docker_command:
                    raise ValueError('Invalid Docker Command')
                r = dk.do_docker_cmd(argspec.docker_command)
                print(r, end='')
            elif argspec.op in (OPS[2], OPS[3], OPS[4]):  # Start Docker Compose
                if not (argspec.docker_compose_yaml and os.path.exists(argspec.docker_compose_yaml)):
                    raise IOError('Invalid Docker Compose Yaml file')
                tmp_d = tempfile.mkdtemp()
                try:
                    with open(argspec.docker_compose_yaml, encoding='utf-8') as ifp:
                        dcy = ifp.read()
                    for param in argspec.params:
                        param = param.strip()
                        k, v = param.split('::=', maxsplit=1)
                        dcy = dcy.replace(f'{{{{{k}}}}}', v)
                    dcy_f = os.path.join(tmp_d, os.path.basename(argspec.docker_compose_yaml))
                    with open(dcy_f, 'w', encoding='utf-8') as ofp:
                        ofp.write(dcy)
                    if argspec.op == OPS[2]:  # Start Docker Compose
                        r = dk.docker_compose_start(dcy_f)
                    elif argspec.op == OPS[3]:  # Stop Docker Compose
                        r = dk.docker_compose_stop(dcy_f)
                    elif argspec.op == OPS[4]:  # State of Docker Compose
                        r = dk.docker_compose_status(dcy_f)
                    print(r, end='')
                finally:
                    shutil.rmtree(tmp_d)
            else:
                raise ValueError(f'Invalid Operation "{argspec.op}"')
        return 0
    except ValueError as e:
        msg = 'ValueError: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    except IOError as e:
        msg = 'IOError: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 2
    except Exception as e:
        msg = 'Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    try:
        with ModuleContext(
            owner='ARGOS-LABS',
            group='9',  # Utility Tools
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Docker Remote Service',
            icon_path=get_icon_path(__file__),
            description='Remote Service handling using docker/compose',
        ) as mcxt:
            # ##################################### for app dependent parameters
            mcxt.add_argument('op',
                              display_name='Operation',
                              choices=OPS,
                              help='Operation for renote service')
            mcxt.add_argument('host',
                              display_name='SSH Host',
                              help='hostname or ip address to connect')
            mcxt.add_argument('user',
                              display_name='SSH User',
                              help='user id to connect')

            # ##################################### for app dependent options
            mcxt.add_argument('--docker-command',
                              display_name='Command',
                              show_default=True,
                              input_group="Docker Command/Compose",
                              help='docker-compose.yaml file path')
            mcxt.add_argument('--docker-compose-yaml',
                              display_name='Compose YAML',
                              show_default=True,
                              input_method='fileread',
                              input_group="Docker Command/Compose",
                              help='docker-compose.yaml file path')
            mcxt.add_argument('--params',
                              display_name='Parameters',
                              show_default=True,
                              action='append',
                              input_group="Docker Command/Compose",
                              help='Parameters for Docker Compose yaml, key::=value format with "{{key}}" place holder')

            mcxt.add_argument('--port',
                              display_name='Port',
                              type=int, default=22,
                              min_value=1, max_value=65525,
                              input_group="Host Info",
                              help='port number, default is [[22]]')
            mcxt.add_argument('--password',
                              display_name='Password',
                              input_method='password',
                              input_group="Host Info",
                              help='user password')
            mcxt.add_argument('--key-filename',
                              display_name='SSH keyfile',
                              input_group="Host Info",
                              help='SSH key filename')
            mcxt.add_argument('--prompt',
                              display_name='Prompt RegExp',
                              input_group="Prompt/Timeout",
                              help='prompt to expected, default is "{username}@.*\$ "')
            mcxt.add_argument('--connect-timeout',
                              display_name='Connect timeout',
                              type=int, default=10,
                              input_group="Prompt/Timeout",
                              help='connection timeout, default is [[10]] secs')
            mcxt.add_argument('--expect-timeout',
                              display_name='Prompt Expect timeout',
                              type=int, default=600,
                              input_group="Prompt/Timeout",
                              help='expectation string waiting timeout, default is [[600]] secs')
            # mcxt.add_argument('--echo-display', action='store_true',
            #                   display_name='Echo On',
            #                   help='If this flag is set echo all command output')

            argspec = mcxt.parse_args(args)
            return do_docker(mcxt, argspec)
    except Exception as err:
        sys.stderr.write(f'Error: {err}')
        return 98


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
