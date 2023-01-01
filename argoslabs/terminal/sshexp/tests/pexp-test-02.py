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
        self.current_output_clean = self.exp.current_output_clean

    # ==========================================================================
    def sendline(self, send_string):
        if not self.opened:
            raise RuntimeError('First open to use sendline')
        self.exp.send(send_string)


################################################################################
def main_sw3560():
    with SshInteraction('192.168.168.1', 'admin', 'r') as exp:
        prompt = '(Switch[>#]|Password: )$'
        exp.expect(prompt)  # 'Switch>')
        exp.sendline('enable')
        exp.expect(prompt)  # 'Password: ')
        exp.sendline('r')
        exp.expect(prompt)  # 'Switch#')
        exp.sendline('show interfaces GigabitEthernet 0/1 | include packets.*bytes')
        exp.expect(prompt)  # 'Switch#')
        print("<<<%s>>>" % exp.current_output_clean)
        exp.sendline('exit')


################################################################################
def main_ubuntu():
    with SshInteraction('192.168.99.250', 'root', 'r') as exp:
        prompt = 'root@testweb.*# $'
        exp.expect(prompt)
        exp.sendline('date')
        exp.expect(prompt)
        print("<<<%s>>>" % exp.current_output_clean)
        exp.sendline('exit')


################################################################################
if __name__ == '__main__':
    main_sw3560()
    main_ubuntu()