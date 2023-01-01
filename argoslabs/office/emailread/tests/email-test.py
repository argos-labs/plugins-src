
# import poplib
# from email import parser
#
# pop_conn = poplib.POP3_SSL('pop.gmail.com')
# pop_conn.user('username')
# pop_conn.pass_('password')
# #Get messages from server:
# messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
# # Concat message pieces:
# messages = ["\n".join(mssg[1]) for mssg in messages]
# #Parse message intom an email object:
# messages = [parser.Parser().parsestr(mssg) for mssg in messages]
# for message in messages:
#     print(message['subject'])
# pop_conn.quit()
#



import os
import re
import time
import email
import smtplib
import chardet
import imaplib
import tempfile
import datetime
from random import randint
# noinspection PyPackageRequirements
import html2text
from pprint import pprint
# from alabs.common.util.vvlogger import get_logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


################################################################################
class ImapMailClient(object):
    ASCENDING = 0
    DESCENDING = 1
    RE_W1 = re.compile(r'^>+\s$')  # , re.MULTILINE)
    RE_W2 = re.compile(r'[ \t]+')  # , re.MULTILINE)
    RE_W3 = re.compile(r'[\r\n]+') # , re.MULTILINE)

    # ==========================================================================
    def __init__(self, server, user, passwd, port=0,
                 use_ssl=True,
                 mailbox='inbox',
                 search_filter='(ALL)',
                 orderby=DESCENDING,
                 mail_protocol='(RFC822)',
                 save_folder=None,
                 delete=False,
                 logger=None
                 ):
        self.server, self.port, self.user, self.passwd = server, port, user, passwd
        self.use_ssl = use_ssl
        self.mailbox = mailbox
        self.search_filter = search_filter
        self.mail_protocol = mail_protocol
        self.orderby = orderby
        if not save_folder:
            save_folder = tempfile.mkdtemp(prefix='imap_mail_client_')
        self.save_folder = save_folder
        self.delete = delete
        # if logger is None:
        #     logger = get_logger(logger)
        self.logger = logger
        # for internal
        self.m = None
        self.is_opened = False
        self.open()

    # ==========================================================================
    def open(self):
        if self.use_ssl:
            if not self.port:
                self.port = 993
            self.m = imaplib.IMAP4_SSL(self.server, self.port)
        else:
            if not self.port:
                self.port = 143
            self.m = imaplib.IMAP4(self.server, self.port)
        result, data = self.m.login(self.user, self.passwd)
        if result != 'OK':
            raise Exception("Error connecting to mailbox: {}".format(data))
        self.is_opened = True
        return True

    # ==========================================================================
    def close(self):
        if not self.is_opened:
            return False
        if self.m is not None:
            self.m.close()
            self.m = None
        self.is_opened = False

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
    # noinspection PyMethodMayBeStatic
    def _decode_header(self, msg):
        dh = email.header.decode_header(msg)
        is_valid = True
        if not isinstance(dh, list):
            is_valid = False
        if len(dh) != 1:
            is_valid = False
        if not isinstance(dh[0], tuple):
            is_valid = False
        if len(dh[0]) != 2:
            is_valid = False
        if not is_valid:
            raise RuntimeError('Invalid result of decode_header: %s' % dh)
        if not dh[0][1]:
            return dh[0][0]
        r = dh[0][0].decode(dh[0][1])
        return r

    # ==========================================================================
    def read_list(self):
        result, data = self.m.select(self.mailbox)
        if result != 'OK':
            raise Exception("Error reading inbox: {}".format(data))
        result, data = self.m.search(None, self.search_filter)
        if data == ['0']:
            return None
        id_list = data[0].split()
        if self.orderby == self.DESCENDING:
            id_list = id_list[::-1]
        for m_id in id_list:
            yield m_id

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _message_from_string(self, s):
        try:
            r = email.message_from_string(s.decode('utf-8'))
            return r
        except UnicodeDecodeError as err:
            # chardet.detect(rawdata)
            # {'encoding': 'EUC-JP', 'confidence': 0.99}
            print(err)
            cd = chardet.detect(s)
            if cd['confidence'] < 0.7:
                raise
            r = email.message_from_string(s.decode(cd['encoding']))
            return r

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _get_time(self, dt):
        return datetime.datetime.fromtimestamp(
            email.utils.mktime_tz(email.utils.parsedate_tz(dt))).strftime('%y%m%d-%H%M%S')

    # ==========================================================================
    def _get_attach_filename(self, mail_id, fn):
        if not self.save_folder:
            os.makedirs(self.save_folder)
        if fn.startswith('=?') and fn.endswith('?='):
            fn = self._decode_header(fn)
        afn = os.path.join(self.save_folder, '%s_%s' % (mail_id.decode(), fn))
        while os.path.exists(afn):
            afn = os.path.join(self.save_folder,
                               '%s_%s_%s' % (mail_id.decode(), randint(10000,99999), fn))
        return afn

    # ==========================================================================
    def read_mail_id(self, mail_id):
        result, data = self.m.fetch(mail_id, self.mail_protocol)
        if result != 'OK':
            raise Exception("Error reading email: {}".format(data))
        if self.delete:
            self.m.store(mail_id, '+FLAGS', '\\Deleted')
        message = self._message_from_string(data[0][1])
        res = {
            'From': email.utils.parseaddr(message['From'])[1],
            'From name':  self._decode_header(email.utils.parseaddr(message['From'])[0]),
            'Time': self._get_time(message['Date']),
            'To': email.utils.parseaddr(message['To'])[1],
            'To name':  self._decode_header(email.utils.parseaddr(message['To'])[0]),
            'Subject': self._decode_header(message["Subject"]),
            'Text': '',
            'File': None
        }
        for part in message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get_content_maintype() == 'text':
                # reading as HTML (not plain text)

                payload = part.get_payload(decode=True)
                body = self._message_from_string(payload)
                text = html2text.html2text(body.as_string())
                text = self.RE_W1.sub('', text)
                text = self.RE_W2.sub(' ', text)
                text = self.RE_W3.sub('\n', text)
                res['Text'] = text[:400]

            # elif part.get_content_maintype() == 'application' and part.get_filename():
            elif part.get_filename():
                fname = self._get_attach_filename(mail_id, part.get_filename())
                attachment = open(fname, 'wb')
                attachment.write(part.get_payload(decode=True))
                attachment.close()
                if res['File']:
                    res['File'].append(fname)
                else:
                    res['File'] = [fname]
        return res

    # # ==========================================================================
    # def send_mail(self, from, to):
    #     new_message = email.message.Message()
    #     new_message["From"] = "hello@itsme.com"
    #     new_message["Subject"] = "My new mail."
    #     new_message.set_payload("This is my message.")
    #
    #     connection.append('INBOX', '', imaplib.Time2Internaldate(time.time()), str(new_message))


################################################################################
class EMailSend(object):
    # ==========================================================================
    def __init__(self, server, user, passwd, port=0, use_ssl=True, use_tls=False):
        self.server = server
        self.user = user
        self.passwd = passwd
        self.port = port
        self.use_ssl = use_ssl
        self.use_tls = use_tls
        # for internal
        self.sm = None
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
        if self.use_ssl:
            if not self.port:
                self.port = 465
            self.sm = smtplib.SMTP_SSL(self.server, self.port)
        else:
            self.sm = smtplib.SMTP(self.server, self.port)
            if self.use_tls:
                if not self.port:
                    self.port = 587
                self.sm.starttls()
            else:
                if not self.port:
                    self.port = 25
        self.sm.login(self.user, self.passwd)

    # ==========================================================================
    def close(self):
        if self.sm is not None:
            self.sm.quit()
            self.sm = None

    # ==========================================================================
    def send(self, receiver, subject, text_body=None, html_body=None):
        """
        이메일 송신
        :param receiver: 전송대상의 이메일 또는 목록
        :param subject: 이메일 제목
        :param text_body: text 메일 내용
        :param html_body: html 메일 내용
            text_body와 html_body 둘 중 하나는 값이 있어야 함
        :return: 고유 문자 발송 ID 리턴
        """
        msg = MIMEMultipart('alternative')
        msg['From'] = self.user
        msg['To'] = receiver
        msg['Subject'] = subject

        if not (text_body or html_body):
            raise ValueError('both text_body and html_body is not valid')

        if html_body:
            msg.attach(MIMEText(html_body, 'html'))
        else:
            msg.attach(MIMEText(text_body, 'plain'))
        return self.sm.sendmail(self.user, receiver, msg.as_string())


################################################################################
if __name__ == '__main__':
    s_kwargs = {
        # 'server': 'mail2.vivans.net',
        # 'user': 'mcchae@vivans.net',
        # 'passwd': 'ghkd67vv',

        'server': 'imap.gmail.com',
        'user': 'mcchae@gmail.com',
        'passwd': 'ghkd67GG',

    }

    r_kwargs = {
        # 'server': 'imap.gmail.com',
        # 'port': 993,
        # 'user': 'mcchaehm@gmail.com',
        # 'passwd': 'ghkd67hm',
        # 'search_filter': 'All',

        # 'server': 'imap.gmail.com',
        # 'user': 'mcchae@gmail.com',
        # 'passwd': 'ghkd67GG',
        # 'search_filter': 'UnSeen',

        # 'server': 'mail2.vivans.net',
        # 'user': 'mcchae@vivans.net',
        # 'passwd': 'ghkd67vv',
        # 'search_filter': 'UnSeen',

        'server': 'imap.gmail.com',
        'user': 'mcchae@argos-labs.com',
        'passwd': 'ghkd67vv',
        'search_filter': '(UNSEEN)',
        'delete': True,
    }

    with EMailSend(**s_kwargs) as sm:
        text_body = """
        안뇽하셔요?
        테스트 입니다.

        고맙습니다.
        아무개드림
        """
        r = sm.send(r_kwargs['user'], '[%s] 안녕? 이것은 테스트 제목임~~^^'
                    % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    text_body=text_body)
    time.sleep(10)
    with ImapMailClient(**r_kwargs) as mc:
        for m_id in mc.read_list():
            pprint(mc.read_mail_id(m_id))
