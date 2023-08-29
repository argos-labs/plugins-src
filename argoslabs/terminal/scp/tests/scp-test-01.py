import paramiko
from scp import SCPClient

def createSSHClient(server, port, user,
                    password=None, key_filename=None):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if password:
        client.connect(server, port, user, password)
    elif key_filename:
        client.connect(server, port, user, key_filename=key_filename)
    return client


server = '10.211.55.55'
port = 22
user = 'toor'
# password = 'r'
# key_filename = r'C:\Users\mcchae\Documents\id-rsa.ppk'
key_filename = r'/Users/mcchae/.ssh/id_rsa.pub'

ssh = createSSHClient(server, port, user, key_filename=key_filename)
scp = SCPClient(ssh.get_transport())
scp.get('/home/toor/work/hosts')
