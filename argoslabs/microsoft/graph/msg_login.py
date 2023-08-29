"""
====================================
 :mod:`argoslabs.microsoft.graph.msg_login`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/02/22]
#     - Attended msg_login
#  * [2022/02/20]
#     - starting




################################################################################
import sys
# from pprint import pprint
# from argoslabs.microsoft.graph.ms_graph.client import MicrosoftGraphClient
from ms_graph.client import MicrosoftGraphClient


################################################################################
scopes = [
    "Calendars.ReadWrite",
    "Files.ReadWrite.All",
    "User.ReadWrite.All",
    "Notes.ReadWrite.All",
    "Directory.ReadWrite.All",
    "User.Read.All",
    "Directory.Read.All",
    "Directory.ReadWrite.All",
    # "offline_access",
    # "openid",
    # "profile",
]


################################################################################
def msg_login(client_id, client_secret, redirect_uri, credential_file, is_print=True):
    # Initialize the Client.
    graph_client = MicrosoftGraphClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scopes,
        credentials=credential_file,
    )
    # Login to the Client.
    graph_client.login()
    if is_print:
        print('__!!~~>>>argoslabs.microsoft.graph logined')
    return graph_client


################################################################################
if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit(98)
    msg_login(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    sys.exit(0)
