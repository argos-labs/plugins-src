"""
====================================
 :mod:`argoslabs.microsoft.teams`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS managing Ms Teams
"""
# Authors
# ===========
#
# * Arun Kumar
#
# Change Log
# --------
#
#  * [2022/08/14]
#     - send message to Channel
#

################################################################################
import os
import sys
import requests
import warnings
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from io import StringIO


################################################################################
class MSTeams(object):
    # ==========================================================================
    OP_TYPE = [
        'Get Users List',
        'Get Chat Members List',
        'Chat Send Message',
        'Get Channel Members List',
        'Channel Send Message'
    ]

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.http_headers = None
        self.endpoint = None
        self.body = None

    # ==========================================================================
    def get_access_token(self):
        _kwargs = {
            'tenant_id': self.argspec.tenant
        }
        endpoint = self.get_endpoint(**_kwargs)
        http_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = self.get_request_body(
            client_id=self.argspec.client_id,
            username=self.argspec.username,
            password=self.argspec.password
        )
        req = requests.post(
            endpoint,
            headers=http_headers,
            data=body
        )
        if req.status_code == 200:
            result = req.json()
            self.http_headers = {
                'Authorization': 'Bearer ' + result['access_token'],
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            return self.http_headers
        else:
            raise Exception(
                "Grant Permission openid, profile, user.Read, offline_access")

    # ==========================================================================
    def get_endpoint(self, **kwargs):
        if 'tenant_id' in kwargs:
            self.endpoint = f"https://login.microsoft.com/" \
                            f"{kwargs['tenant_id']}/" \
                            f"oauth2/v2.0/token"
        elif 'team_id' and 'channel_id' and 'get_detail' in kwargs:
            self.endpoint = f"https://graph.microsoft.com/v1.0/teams/" \
                            f"{kwargs['team_id']}/" \
                            f"channels/" \
                            f"{kwargs['channel_id']}"
        elif 'team_id' and 'channel_id' and 's_message' in kwargs:
            self.endpoint = f"https://graph.microsoft.com/v1.0/teams/" \
                            f"{kwargs['team_id']}/" \
                            f"channels/" \
                            f"{kwargs['channel_id']}/" \
                            f"messages"
        elif 'group_id' and 'parent_id' and 'filename' and 'c_session' in kwargs:
            self.endpoint = f'https://graph.microsoft.com/v1.0/groups/' \
                            f'{kwargs["group_id"]}/' \
                            f'drive/items/' \
                            f'{kwargs["parent_id"]}:/' \
                            f'{kwargs["filename"]}:/' \
                            f'createUploadSession'
        elif 'group_id' and 'parent_id' and 'filename' in kwargs:
            self.endpoint = f'https://graph.microsoft.com/v1.0/groups/' \
                            f'{kwargs["group_id"]}/' \
                            f'drive/items/' \
                            f'{kwargs["parent_id"]}:/' \
                            f'{kwargs["filename"]}:/' \
                            f'content'
        elif 'parentreference_drive_id' and 'parentreference_id' in kwargs:
            self.endpoint = f'https://graph.microsoft.com/v1.0/drives/' \
                            f'{kwargs["parentreference_drive_id"]}/' \
                            f'items/' \
                            f'{kwargs["parentreference_id"]}'
        elif 'channel_link' in kwargs:
            result = self.extract_team_id_channel_id_from_channel_link(
                kwargs['channel_link']
            )
            team_id = result[7]
            channel_id = result[5]
            self.endpoint = f"https://graph.microsoft.com/v1.0/teams/" \
                            f"{team_id}/" \
                            f"channels/" \
                            f"{channel_id}/" \
                            f"messages"
        elif 'group_id' in kwargs:
            self.endpoint = f'https://graph.microsoft.com/v1.0/groups/' \
                            f'{kwargs["group_id"]}/' \
                            f'drive'
        elif 'chat_id' and 'message' in kwargs:
            self.endpoint = f'https://graph.microsoft.com/v1.0/chats/' \
                            f'{kwargs["chat_id"]}/' \
                            f'messages'
        elif 'cht_user_list' and 'chat_id' in kwargs:
            self.endpoint = f'https://graph.microsoft.com/v1.0/chats/' \
                            f'{kwargs["chat_id"]}/' \
                            f'members'
        elif 'user_list' in kwargs:
            self.endpoint = f'https://graph.microsoft.com/v1.0/users'
        elif 'team_id' and 'channel_id' and 'chl_user_list' in kwargs:
            self.endpoint = f"https://graph.microsoft.com/v1.0/teams/" \
                            f"{kwargs['team_id']}/" \
                            f"channels/" \
                            f"{kwargs['channel_id']}/" \
                            f"members"
        else:
            self.endpoint = None
        return self.endpoint

    # ==========================================================================
    @staticmethod
    def extract_team_id_channel_id_from_channel_link(channel_link):
        re_data = {
            '%3a': ':',
            '%40': '@',
            'groupId=': '|',
            '/': '|',
            '&tenantId=': '|'
        }
        for x, y in re_data.items():
            channel_link = channel_link.replace(x, y)
        result = channel_link.split('|')
        return result

    # ==========================================================================
    def get_request_body(self, **kwargs):
        if 'client_id' and 'username' and 'password' in kwargs:
            self.body = dict(
                client_id=kwargs['client_id'],
                scope='user.read openid profile offline_access',
                username=kwargs['username'],
                password=kwargs['password'],
                grant_type='password'
            )
        elif 'message' and 'parentreference_list' in kwargs:
            att_id = ''
            att_list = []
            for parentreference in kwargs['parentreference_list']:
                att_id += f"<attachment id=\"{parentreference['attachment_id']}\">" \
                          f"</attachment>"
                condition = parentreference['name'].lower(). \
                    endswith(('.doc', '.xls', '.xlsx', '.docx', '.csv'))
                if not condition:
                    name = parentreference['name']
                else:
                    name = parentreference[
                               'name'] + '&action=default&mobileredirect=true'
                att_list.append(
                    dict(
                        id=parentreference['attachment_id'],
                        contentType='reference',
                        contentUrl=parentreference['contentUrl'],
                        name=name
                    )
                )
            self.body = dict(body={
                "contentType": "html",
                "content": f"{kwargs['message'] if kwargs['message'] else ''}"
                           f"{att_id}"
            }, attachments=att_list)
        elif 'message' in kwargs:
            self.body = dict(body={
                "content": kwargs['message']
            })
        return self.body

    # ==========================================================================
    def get_team_name(self, endpoint):
        req = requests.get(endpoint, headers=self.http_headers)
        if req.status_code // 100 == 2:
            return req.json()['displayName']
        else:
            print(req.text, end='')
            req.raise_for_status()

    # ==========================================================================
    def create_upload_session(self, group_id,
                              parent_id, filename, file):
        endpoint = self.get_endpoint(
            group_id=group_id,
            parent_id=parent_id,
            filename=filename,
            c_session=True
        )
        body = dict(item={
            "@microsoft.graph.conflictBehavior": "rename"
        },
            deferCommit='true'
        )
        req = requests.post(endpoint, headers=self.http_headers, json=body)
        if req.status_code // 100 == 2:
            upload_url = req.json()['uploadUrl']
            self.upload_large_file_to_sideshare(upload_url, file)
            return upload_url
        else:
            print(req.text, end='')
            req.raise_for_status()

    # ==========================================================================
    def upload_large_file_to_sideshare(self, upload_url, file):
        f = open(file, "rb")
        data = f.read()
        file_stat = os.stat(
            file
        )
        self.http_headers['Content-Range'] = f'bytes 0-' \
                                             f'{file_stat.st_size - 1}/' \
                                             f'{file_stat.st_size}'
        self.http_headers['Content-Length'] = f'{file_stat.st_size}'
        req = requests.put(
            upload_url,
            headers=self.http_headers,
            data=data
        )
        if req.status_code // 100 == 2:
            return
        else:
            print(req.text, end='')
            req.raise_for_status()

    # ==========================================================================
    def upload_file_to_sideshare(self, endpoint,
                                 file,
                                 group_id,
                                 parent_id,
                                 filename):
        file_stat = os.stat(file)
        if file_stat.st_size // 1000000 < 2:
            f = open(file, "rb")
            req = requests.put(
                endpoint,
                headers=self.http_headers,
                data=f.read()
            )
        else:
            upload_url = self.create_upload_session(
                group_id,
                parent_id,
                filename,
                file
            )
            del self.http_headers['Content-Range']
            self.http_headers['Content-Length'] = '0'
            req = requests.post(
                upload_url,
                headers=self.http_headers
            )
        if req.status_code // 100 == 2:
            result = dict(
                driveId=req.json()['parentReference']['driveId'],
                id=req.json()['parentReference']['id'],
                contentUrl=req.json()['webUrl'],
                name=req.json()['name'],
                attachment_id=req.json()['cTag'][4:40]
            )
            return result
        else:
            print(req.text, end='')
            req.raise_for_status()

    # ==========================================================================
    def get_attachment_id(self, endpoint):
        req = requests.get(
            endpoint,
            headers=self.http_headers,
            stream=False
        )
        if req.status_code // 100 == 2:
            result = req.json()['eTag'].split('{')[1].split('}')[0]
            return result
        else:
            print(req.text, end='')
            req.raise_for_status()

    # ==========================================================================
    def send_channelmessage_with_file(self, team_id,
                                      channel_id, message, file):
        endpoint = self.get_endpoint(
            team_id=team_id,
            channel_id=channel_id,
            get_detail=True
        )
        team_name = self.get_team_name(endpoint)

        parentreference_list = []
        for _file in file:
            filename = os.path.basename(_file)
            endpoint = self.get_endpoint(
                group_id=team_id,
                parent_id='root',
                filename=f"{team_name}/"
                         f"{filename}"
            )
            parentreference = self.upload_file_to_sideshare(
                endpoint,
                _file,
                group_id=team_id,
                parent_id='root',
                filename=f"{team_name}/"
                         f"{filename}"
            )
            parentreference_list.append(parentreference)
        body = self.get_request_body(
            parentreference_list=parentreference_list,
            message=message
        )
        endpoint = self.get_endpoint(
            team_id=team_id,
            channel_id=channel_id,
            s_message=True
        )
        req = requests.post(
            endpoint,
            headers=self.http_headers,
            json=body
        )
        if req.status_code // 100 == 2:
            result = req.json()
            print(f'message_id,{result["id"]}', end='')
        else:
            print(req.text, end='')
            req.raise_for_status()

    # ==========================================================================
    def channel_message(self, channel_link=None,
                        team_id=None,
                        channel_id=None,
                        message=None,
                        file=None):
        if not channel_link and not team_id and not channel_id:
            raise Exception('Channel Link or Channel Id and Team Id required.')
        if not message and not file:
            raise Exception('Message or File required.')
        if channel_link:
            result = self.extract_team_id_channel_id_from_channel_link(
                channel_link
            )
            team_id = result[7]
            channel_id = result[5]
        if file:
            self.send_channelmessage_with_file(
                team_id,
                channel_id,
                message,
                file
            )
        else:
            endpoint = self.get_endpoint(
                team_id=team_id,
                channel_id=channel_id,
                s_message=True
            )
            body = self.get_request_body(
                message=message
            )
            req = requests.post(
                endpoint,
                headers=self.http_headers,
                json=body
            )
            if req.status_code // 100 == 2:
                result = req.json()
                print(f'message_id,{result["id"]}', end='')
            else:
                if req.json()['error']:
                    permissions = req.json()['error']['message'].split("'")[1]
                    raise Exception(f'Grant Permissions {permissions}')
                print(req.text, end='')
                req.raise_for_status()

    # ==========================================================================
    def chat_message(self, chat_id=None, message=None):
        if not chat_id:
            raise Exception("Chat Id required.")
        if not message:
            raise Exception("Message required.")
        endpoint = self.get_endpoint(
            chat_id=chat_id,
            message=True
        )
        body = self.get_request_body(
            message=message
        )
        req = requests.post(
            endpoint,
            headers=self.http_headers,
            json=body
        )
        if req.status_code // 100 == 2:
            result = req.json()
            print(f'message_id,{result["id"]}', end='')
        else:
            if req.json()['error']:
                permissions = req.json()['error']['message'].split("'")[1]
                raise Exception(f'Grant Permissions {permissions}')
            print(req.text, end='')
            req.raise_for_status()

    # ==========================================================================
    def get_user_list(self):
        endpoint = self.get_endpoint(
            user_list=True
        )
        req = requests.get(endpoint, headers=self.http_headers, stream=False)
        if req.status_code // 100 == 2:
            result = req.json()
            outst = StringIO()
            outst.write('id,displayName,jobTitle,officeLocation,businessPhones')
            outst.write('\n')
            for user in result['value']:
                outst.write(f"{user['id']},"
                            f"{user['displayName']},"
                            f"{user['jobTitle']},"
                            f"{user['officeLocation']},"
                            f"{user['businessPhones'][0]}")
                outst.write('\n')
            print(outst.getvalue(), end='')
        else:
            raise Exception(
                f'Grant Permissions User.Read.All, User.ReadBasic.All')

    # ==========================================================================
    def get_chat_user_list(self, chat_id):
        if not chat_id:
            raise Exception("Chat Id required.")
        endpoint = self.get_endpoint(
            cht_user_list=True,
            chat_id=chat_id
        )
        req = requests.get(endpoint, headers=self.http_headers, stream=False)
        if req.status_code // 100 == 2:
            result = req.json()
            outst = StringIO()
            outst.write('id,displayName,email')
            outst.write('\n')
            for user in result['value']:
                outst.write(f"{user['userId']},"
                            f"{user['displayName']},"
                            f"{user['email']}")
                outst.write('\n')
            print(outst.getvalue(), end='')
        else:
            print(req.text, end='')
            req.raise_for_status()

    # ==========================================================================
    def get_channel_user_list(self, channel_link=None,
                              team_id=None,
                              channel_id=None):
        if not channel_link and not team_id and not channel_id:
            raise Exception('Channel Link or Channel Id and Team Id required.')
        if channel_link:
            result = self.extract_team_id_channel_id_from_channel_link(
                channel_link
            )
            team_id = result[7]
            channel_id = result[5]
        endpoint = self.get_endpoint(
            chl_user_list=True, team_id=team_id, channel_id=channel_id
        )
        req = requests.get(endpoint, headers=self.http_headers, stream=False)
        if req.status_code // 100 == 2:
            result = req.json()
            outst = StringIO()
            outst.write('id,displayName,jobTitle,officeLocation,businessPhones')
            outst.write('\n')
            for user in result['value']:
                outst.write(f"{user['userId']},"
                            f"{user['displayName']},"
                            f"{user['email']}")
                outst.write('\n')
            print(outst.getvalue(), end='')
        else:
            if req.json()['error']:
                permissions = req.json()['error']['message'].split("'")[1]
                raise Exception(f'Grant Permissions {permissions}')
            print(req.text, end='')
            req.raise_for_status()

    # ==========================================================================
    def do(self, op):
        if op == 'Channel Send Message':
            self.channel_message(
                self.argspec.channel_link,
                self.argspec.team_id,
                self.argspec.channel_id,
                self.argspec.message,
                self.argspec.file
            )
        elif op == 'Chat Send Message':
            self.chat_message(
                self.argspec.chat_id,
                self.argspec.message
            )
        elif op == 'Get Users List':
            self.get_user_list()
        elif op == 'Get Chat Members List':
            self.get_chat_user_list(self.argspec.chat_id)
        elif op == 'Get Channel Members List':
            self.get_channel_user_list(
                self.argspec.channel_link,
                self.argspec.team_id,
                self.argspec.channel_id
            )


################################################################################
@func_log
def reg_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        warnings.simplefilter("ignore", ResourceWarning)
        res = MSTeams(argspec)
        res.get_access_token()
        res.do(argspec.op)
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
            owner='ARGOS-LABS-DEMO',
            group='2',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Microsoft Teams',
            icon_path=get_icon_path(__file__),
            description='Microsoft Teams',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='Function Type',
                          choices=MSTeams.OP_TYPE,
                          help='Type of operation')
        mcxt.add_argument('tenant', display_name='Tenant Id',
                          help='Tenant Id')
        mcxt.add_argument('client_id', display_name='Client Id',
                          help='Client Id')
        mcxt.add_argument('username', display_name='Username',
                          help='Username')
        mcxt.add_argument('password', display_name='Password',
                          help='Password',
                          input_method='password')
        # ######################################## for app dependent options
        mcxt.add_argument('--channel_link', display_name='Channel Link',
                          help='channel_link')
        mcxt.add_argument('--team_id', display_name='Team Id',
                          help='team_id')
        mcxt.add_argument('--channel_id', display_name='Channel Id',
                          help='channel_id')
        mcxt.add_argument('--chat_id', display_name='Chat Id',
                          help='chat_id')
        mcxt.add_argument('--message', display_name='Message',
                          help='message')
        mcxt.add_argument('--file', display_name='File',
                          action='append',
                          input_method='fileread',
                          help='file')
        argspec = mcxt.parse_args(args)
        return reg_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
