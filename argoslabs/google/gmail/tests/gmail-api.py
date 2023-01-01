
import os
import sys
import csv
import email
import base64
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


################################################################################
class GMailApi(object):
    # ==========================================================================
    SERVICE_NAME = 'gmail'
    SERVICE_VER = 'v1'
    SCOPES_DICT = {
        'Label': ['https://www.googleapis.com/auth/gmail.readonly'],
        'List': [
            'https://mail.google.com/',
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.metadata',
        ]
    }
    OPLIST = list(SCOPES_DICT.keys())

    # ==========================================================================
    def _get_service(self, op):
        scopes = self.SCOPES_DICT[op]
        flow = InstalledAppFlow.from_client_secrets_file(self.cred_file, scopes)
        creds = flow.run_local_server(port=0)
        service = build(self.SERVICE_NAME, self.SERVICE_VER, credentials=creds)
        return service

    # ==========================================================================
    def __init__(self, cred_file, op):
        if not os.path.exists(cred_file):
            raise IOError(f'Cannot read GMail credention JSON file "{cred_file}"')
        if op not in self.OPLIST:
            raise ValueError(f'Not supported operation "{op}"')
        self.cred_file = cred_file
        self.op = op
        self.service = self._get_service(op)

    # ==========================================================================
    def _get_label(self, user_id='me'):
        results = self.service.users().labels().list(userId=user_id).execute()
        labels = results.get('labels', [])
        return labels

    # ==========================================================================
    def _list_messages_matching_query(self, user_id='me', query=''):
        """List all Messages of the user's mailbox matching the query.

        Args:
          self: this
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          query: String used to filter messages returned.
          Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

        Returns:
          List of Messages that match the criteria of the query. Note that the
          returned list contains Message IDs, you must use get with the
          appropriate ID to get the details of a Message.
        """
        try:
            response = self.service.users().messages().list(
                userId=user_id, q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(
                    userId=user_id, q=query, pageToken=page_token).execute()
                messages.extend(response['messages'])
            return messages
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    # ==========================================================================
    def _list_messages_with_labels(self, user_id='me', label_ids=[]):
        """List all Messages of the user's mailbox with label_ids applied.

        Args:
          self: this
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          label_ids: Only return Messages with these labelIds applied.

        Returns:
          List of Messages that have all required Labels applied. Note that the
          returned list contains Message IDs, you must use get with the
          appropriate id to get the details of a Message.
        """
        try:
            response = self.service.users().messages().list(
                userId=user_id, labelIds=label_ids).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(
                    userId=user_id, labelIds=label_ids,
                    pageToken=page_token).execute()
                messages.extend(response['messages'])
            return messages
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    # ==========================================================================
    def _get_message(self, msg_id, user_id='me'):
        """Get a Message with given ID.

        Args:
          self: this
          msg_id: The ID of the Message required.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.

        Returns:
          A Message.
        """
        try:
            message = self.service.users().messages().get(
                userId=user_id, id=msg_id).execute()
            # print('Message snippet: %s' % message['snippet'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    # ==========================================================================
    def _get_mime_message(self, msg_id, user_id='me'):
        """Get a Message and use it to create a MIME Message.

        Args:
          self: this
          msg_id: The ID of the Message required.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.

        Returns:
          A MIME Message, consisting of data from Message.
        """
        try:
            message = self.service.users().messages().get(
                userId=user_id, id=msg_id, format='raw').execute()
            print('Message snippet: %s' % message['snippet'])
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            mime_msg = email.message_from_string(msg_str)
            return mime_msg
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    # ==========================================================================
    def _get_thread(self, thread_id, user_id='me'):
        """Get a Thread.

        Args:
          self: this
          thread_id: The ID of the Thread required.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.

        Returns:
          Thread with matching ID.
        """
        try:
            thread = self.service.users().threads().get(
                userId=user_id, id=thread_id).execute()
            messages = thread['messages']
            print('thread id: %s - number of messages '
                  'in this thread: %d') % (thread['id'], len(messages))
            return thread
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    # ==========================================================================
    def label(self):
        labels = self._get_label()
        if not labels:
            print('No labels found.')
        else:
            c = csv.writer(sys.stdout, lineterminator='\n')
            c.writerow(('id', 'name', 'type'))
            for label in labels:
                c.writerow((label['id'], label['name'], label['type']))

    # ==========================================================================
    def list(self):
        for md in self._list_messages_matching_query():
            msg = self._get_message(md['id'])
            thread = self._get_thread(md['threadId'])
            print(msg, thread)
            break

    # ==========================================================================
    def do(self):
        if self.op == 'Label':
            self.label()
        elif self.op == 'List':
            self.list()


################################################################################
def test():
    # ga = GMailApi('mcchae@gmail.com-credentials.json', 'Label')
    ga = GMailApi('mcchae@gmail.com-credentials.json', 'List')
    ga.do()


################################################################################
if __name__ == '__main__':
    test()
