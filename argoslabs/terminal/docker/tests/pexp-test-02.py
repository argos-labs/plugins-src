import os
import json
import paramiko
from paramiko_expect import SSHClientInteraction


################################################################################
class SshInteraction(object):
    # ==========================================================================
    def __init__(self, host, username, password, port=22,
                 connect_timeout=10, echo_display=False,
                 expect_timeout=60, ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
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
        self.ssh.connect(self.host, port=self.port,
                         username=self.username, password=self.password)
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
        self.current_output_clean = self.exp.current_output_clean.strip()

    # ==========================================================================
    def sendline(self, send_string):
        if not self.opened:
            raise RuntimeError('First open to use sendline')
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
            wd = wd.replace('~', out)
        return wd

    # ==========================================================================
    def do_cmd(self, cmd):
        self.sendline(cmd)
        self.expect(self.prompt)
        if self.current_output_clean.startswith('?2004l'):  # for escape sequence
            self.current_output_clean = self.current_output_clean[6:]
        return self.current_output_clean

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
        return out == '0'

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
def main_ubuntu():
    host = '192.168.35.129'
    user = 'ubuntu'
    passwd = 'r'
    with SshInteraction(host, user, passwd) as exp:
        prompt = fr'{user}@.*\$ '
        exp.expect(prompt)
        exp.sendline('docker info')
        exp.expect(prompt)
        print("<<<%s>>>" % exp.current_output_clean)
        exp.sendline('exit')


################################################################################
def main_raspberrypi():
    # args = ('192.168.35.129', 'ubuntu', 'r')
    args = ('192.168.35.12', 'pi', 'r')
    with DockerSsh(*args, expect_timeout=600) as dk:
        # out = dk.do_docker_cmd('run --rm hello-world')
        # out = dk.do_docker_cmd('run --rm -it instrumentisto/nmap -sT -O -v 192.168.35.129')
        # out = dk.docker_compose_start('speedtest.yaml')
        out = dk.docker_compose_status('speedtest.yaml')
        print(out)


################################################################################
if __name__ == '__main__':
    # main_sw3560()
    main_raspberrypi()
