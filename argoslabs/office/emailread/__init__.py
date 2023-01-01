"""
====================================
 :mod:`argoslabs.office.emailread`
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
#  * [2021/04/09] Kyobong An
#     - 가져올 메일이 없을때 1을 리턴하던것을 0으로 변경, 나머지에러는 리턴 99. decode의 에러에 대해서도(errors ='ignore')
#  * [2021/04/09]
#     - 그룹에 "5-Email/Messenger" 넣음
#  * [2020/08/23]
#     - msgid 결과 추가
#  * [2020/04/30]
#     - txt attachment error
#     - # 검색 날짜는 UTC 기준으로 해야 함 (실제 포함 날짜는 로컬날짜로 보임)
#  * [2020/03/13]
#     - test for jerrychae@outlook.com
#     - monitor returns the number of matched emails, timeout 0
#  * [2019/06/18]
#     - search non-ascii
#  * [2019/05/30]
#     - starting

################################################################################

import os
import re
import sys
import csv
import email
import chardet
import imaplib
import tempfile
import datetime
import argparse
import traceback
from random import randint
# noinspection PyPackageRequirements
# import html2text
from alabs.common.util.vvargs import ModuleContext, func_log,  \
    ArgsError, ArgsExit, get_icon_path
from alabs.common.util.timer import Timer
from fnmatch import fnmatch


################################################################################
class ImapMailClient(object):
    HEADER = ['time', 'from', 'from name', 'to', 'to name', 'subject',
              'body_file', 'attachments', 'msgid']
    ASCENDING = 0
    DESCENDING = 1
    RE_W1 = re.compile(r'^>+\s$')   # , re.MULTILINE)
    RE_W2 = re.compile(r'[ \t]+')   # , re.MULTILINE)
    RE_W3 = re.compile(r'[\r\n]+')  # , re.MULTILINE)
    SEARCH_TYPE = {
        'ALL': 'ALL',
        'UNREAD': 'UNSEEN',
        'READ': 'SEEN',
    }

    # ==========================================================================
    def __init__(self, server, user, passwd, port=0,
                 use_ssl=True,
                 mailbox='inbox',
                 search_type='UNSEEN',
                 search_from=None,
                 search_to=None,
                 search_subject=None,
                 search_body=None,
                 search_since=None,
                 search_before=None,
                 orderby=DESCENDING,
                 mail_protocol='(RFC822)',
                 save_folder=None,
                 attachment_match="*",
                 delete=False,
                 limit=50,
                 store_body=False,
                 after_unread=False,
                 logger=None,
                 ):
        self.server, self.port, self.user, self.passwd = server, port, user, passwd
        self.use_ssl = use_ssl
        self.mailbox = mailbox
        self.search_type = search_type
        self.search_from = search_from
        self.search_to = search_to
        self.search_subject = search_subject
        self.search_body = search_body
        self.search_since = search_since
        self.search_before = search_before
        self.mail_protocol = mail_protocol
        self.orderby = orderby
        if not save_folder:
            save_folder = tempfile.mkdtemp(prefix='email_save_')
        self.save_folder = save_folder
        self.attachment_match = attachment_match
        self.delete = delete
        self.limit = limit
        self.store_body = store_body
        self.after_unread = after_unread
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
            self.m.logout()
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
    def __exit__(self, *args):
        self.close()

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _decode_header(self, msg):
        # noinspection PyUnresolvedReferences
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
        r = dh[0][0].decode(dh[0][1], errors='ignore')
        return r

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _get_date_criteria(self, dstr):
        dt = datetime.datetime.strptime(dstr, "%Y-%m-%d").date()
        return dt.strftime('%d-%b-%Y')

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _safe_encoding(self, s):
        # noinspection PyBroadException
        try:
            r = s.encode('utf-8').decode('utf-8')
            return r
        except Exception:
            # chardet.detect(rawdata)
            # {'encoding': 'EUC-JP', 'confidence': 0.99}
            pass

    # ==========================================================================
    def read_list(self):
        result, data = self.m.select(self.mailbox)
        if result != 'OK':
            raise Exception("Error reading inbox: {}".format(data))
        criteria = []
        if self.search_type:
            criteria.append(self.search_type)
        if self.search_from:
            criteria.append('(FROM "%s")' % self._safe_encoding(self.search_from))
        if self.search_to:
            criteria.append('(TO "%s")' % self._safe_encoding(self.search_to))
        if self.search_subject:
            criteria.append('(SUBJECT "%s")' % self._safe_encoding(self.search_subject))
        if self.search_body:
            criteria.append('(BODY "%s")' % self._safe_encoding(self.search_body))
        if self.search_since:
            criteria.append('(SINCE "%s")' % self._get_date_criteria(self.search_since))
        if self.search_before:
            criteria.append('(BEFORE "%s")' % self._get_date_criteria(self.search_before))
        self.logger.debug('Email criteria=%s' % criteria)
        result, data = self.m.search(None, *criteria)
        if data == [b'0']:
            return None
        id_list = data[0].split()
        if self.orderby == self.DESCENDING:
            id_list = id_list[::-1]
        for i, m_id in enumerate(id_list):
            if 0 < self.limit <= i:
                break
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
        # noinspection PyUnresolvedReferences
        return datetime.datetime.fromtimestamp(
            email.utils.mktime_tz(email.utils.parsedate_tz(dt))).strftime('%Y%m%d-%H%M%S')

    # ==========================================================================
    def _get_attach_filename(self, mail_id, fn):
        if not self.save_folder:
            os.makedirs(self.save_folder)
        if fn.startswith('=?') and fn.endswith('?='):
            fn = self._decode_header(fn)
        afn = os.path.join(self.save_folder, '%s_%s' % (mail_id.decode(), fn))
        while os.path.exists(afn):
            afn = os.path.join(self.save_folder,
                               '%s_%s_%s' % (mail_id.decode(), randint(10000, 99999), fn))
        return afn

    # ==========================================================================
    def read_mail_id(self, mail_id):
        try:
            b_seen = False
            self.logger.debug('read mail [%s]' % mail_id.decode())
            if self.after_unread:
                r, data = self.m.fetch(mail_id, '(FLAGS)')
                for d in data:
                    if d.decode("utf-8").endswith('(\\Seen))'):
                        b_seen = True
                        break

            result, data = self.m.fetch(mail_id, self.mail_protocol)
            if result != 'OK':
                raise Exception("Error reading email: {}".format(data))
            if self.delete:
                self.m.store(mail_id, '+FLAGS', '\\Deleted')
            message = self._message_from_string(data[0][1])
            # noinspection PyUnresolvedReferences
            res = {
                'from': email.utils.parseaddr(message['From'])[1],
                'from name':  self._decode_header(email.utils.parseaddr(message['From'])[0]),
                'time': self._get_time(message['Date']),
                'to': email.utils.parseaddr(message['To'])[1],
                'to name':  self._decode_header(email.utils.parseaddr(message['To'])[0]),
                'subject': self._decode_header(message["Subject"]),
                'body_file': None,
                'payload': None,
                'attachments': [],
                'msgid': message['Message-ID'],  # str(mail_id.decode()),
            }
            for part in message.walk():
                content_type = part.get_content_maintype()
                attach_filename = part.get_filename()
                if content_type == 'multipart':
                    continue

                # elif content_type == 'application' and attach_filename:
                if attach_filename:
                    fname = self._get_attach_filename(mail_id, part.get_filename())
                    if fnmatch(fname, self.attachment_match):
                        if not self.after_unread:
                            with open(fname, 'wb') as ofp:
                                ofp.write(part.get_payload(decode=True))
                        res['attachments'].append(fname)

                if content_type == 'text':
                    # reading as HTML (not plain text)
                    payload = part.get_payload(decode=True)
                    # body = self._message_from_string(payload)
                    body_fn = os.path.join(self.save_folder, '%s_body.txt' % mail_id.decode())

                    if isinstance(payload, str):
                        if len(payload) > 0 and payload[0] == '\n':
                            payload = payload[1:]
                        payload_str = str.encode(payload, 'utf-8')
                        res['payload'] = payload_str
                    elif isinstance(payload, bytes):
                        res['payload'] = payload.decode('utf-8', errors='ignore')
                    else:
                        raise RuntimeError(
                            'Invalid body type nore (str or bytes) but "%s"' % str(
                                type(payload)))

                    if not self.after_unread and self.store_body:
                        with open(body_fn, 'wb') as ofp:
                            # ofp.write(body.as_bytes())
                            if isinstance(payload, str):
                                if len(payload) > 0 and payload[0] == '\n':
                                    payload = payload[1:]
                                payload_str = str.encode(payload, 'utf-8')
                                ofp.write(payload_str)
                            elif isinstance(payload, bytes):
                                ofp.write(payload)
                        res['body_file'] = body_fn
                    # text = self.RE_W1.sub('', text)
                    # text = self.RE_W2.sub(' ', text)
                    # text = self.RE_W3.sub('\n', text)
                    # res['Text'] = text[:400]
            if self.after_unread:
                if not b_seen:
                    self.m.store(mail_id, '-FLAGS', '\\SEEN')
            self.logger.debug('read mail [%s] return %s' % (mail_id.decode(), res))
            return res
        except Exception as err:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('read_mail_id Error: %s: %s' % (str(err), ''.join(_out)))
            raise

    # ==========================================================================
    def get_list_from_res(self, res):
        rl = list()
        for h in self.HEADER:
            v = res[h]
            if h == 'time' and isinstance(v, datetime.datetime):
                v = v.strftime('%y%m%d-%H%M%S')
            elif h == 'attachments':
                v = ','.join(v)
            rl.append(v)
        return rl


################################################################################
def read_email(mcxt, args, after_unread=False):
    kwargs = {
        'server': args.server,
        'port': args.port,
        'user': args.user,
        'passwd': args.passwd,
        'use_ssl': not args.no_use_ssl,
        'mailbox': args.mailbox,
        'search_type': ImapMailClient.SEARCH_TYPE[args.search_type],
        'search_from': args.search_from,
        'search_to': args.search_to,
        'search_subject': args.search_subject,
        'search_body': args.search_body,
        'search_since': args.search_since,
        'search_before': args.search_before,
        'orderby': ImapMailClient.ASCENDING if args.orderby_old else ImapMailClient.DESCENDING,
        'save_folder': args.save_folder,
        'attachment_match': args.attachment_match,
        'delete': args.delete_after_read,
        'limit': args.limit,
        'store_body': args.store_body,
        'after_unread': after_unread,
        'logger': mcxt.logger,
    }
    mcxt.logger.debug('Try to read "%s" client: args=%s' % ('IMAP', args))
    rows = list()
    # if args.client == 'imap':
    with ImapMailClient(**kwargs) as mc:
        for m_id in mc.read_list():
            res = mc.read_mail_id(m_id)
            # Search BODY 결과가 생각처럼 나오지 않아 한번 더 체크
            if kwargs['search_body']:
                if res['payload'].find(kwargs['search_body']) < 0:
                    continue
            row = mc.get_list_from_res(res)
            rows.append(row)
    if not after_unread:
        cwr = csv.writer(sys.stdout, lineterminator='\n')
        if rows:
            cwr.writerow(ImapMailClient.HEADER)
            for row in rows:
                cwr.writerow(row)
    return len(rows)
    # else:
    #     raise RuntimeError('Not supported mail client protocol "%s"' % args.client)


################################################################################
def monitor_email(mcxt, args):
    cnt = 0
    tm = Timer()
    for i in range(3600 * 24 * 365 * 100):
        with tm:
            if i % args.mon_period == 0:
                cnt = read_email(mcxt, args, after_unread=True)
                if cnt > 0:
                    break
            if 0 < args.mon_timeout <= i:
                # raise TimeoutError('No email result during %s seconds' % args.mon_timeout)
                break
    print('%s' % cnt, end='')
    return cnt


################################################################################
# noinspection PyShadowingBuiltins
@func_log
def email_job(mcxt, args):
    # noinspection PyBroadException
    try:
        cnt = 0
        mcxt.logger.info('>>>starting...')
        if args.save_folder and not os.path.isdir(args.save_folder):
            os.makedirs(args.save_folder)
        if args.operation == 'read':
            cnt = read_email(mcxt, args)
        elif args.operation == 'monitor':
            cnt = monitor_email(mcxt, args)
        mcxt.logger.info('>>>end...')
        return 0
    except Exception as e:
        msg = 'Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='5',  # Email/Messenger
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Email IMAP Read/Mon',
        icon_path=get_icon_path(__file__),
        description='''Email operation for reading, monitoring, sending''',
        formatter_class=argparse.RawTextHelpFormatter
    ) as mcxt:
        # ######################################## for app dependent options
        # mcxt.add_argument('--client', '-c',
        #                   input_group='showwhen:operation=read,monitor',
        #                   display_name='Mail Protocol', show_default=True,
        #                   choices=["imap"], default='imap',
        #                   help='Set protocol of mail client to read or monitor, one of {"imap"}. In case of send use smtp protocol')
        mcxt.add_argument('--search-type',
                          display_name='Search Type', default='UNREAD',
                          choices=list(ImapMailClient.SEARCH_TYPE.keys()),
                          help='Search type for email ALL, UNSEEN, or SEEN, default is [[UNSEEN]].')
        mcxt.add_argument('--search-from',
                          display_name='Search Sender',
                          help='Set filter for email address or name who send. Note) Alphabet and digits only allowed.')
        mcxt.add_argument('--search-to',
                          display_name='Search To',
                          help='Set filter for email address or name who receive. Note) Alphabet and digits only allowed.')
        mcxt.add_argument('--search-subject',
                          display_name='Search Subject',
                          help='Set filter for subject match. Note) Alphabet and digits only allowed.')
        mcxt.add_argument('--search-body',
                          display_name='Search Body',
                          help='Set filter for subject match. Note) Alphabet and digits only allowed.')
        mcxt.add_argument('--search-since',
                          # input_method='dateselect',  # 변수사용 불가 오류
                          display_name='Search Since',
                          re_match=r'^\d{4}-\d{2}-\d{2}$',
                          help='Set filter for email address SINCE, example is [[2019-01-01]]. Note use UTC date!')
        mcxt.add_argument('--search-before',
                          # input_group='showwhen:operation=read,monitor',
                          display_name='Search Before',
                          re_match=r'^\d{4}-\d{2}-\d{2}$',
                          help='Set filter for email address BEFORE, example is [[2019-01-31]]. Note use UTC date!')
        mcxt.add_argument('--save-folder',
                          display_name='Save Folder',
                          input_method='folderread', show_default=True,
                          help='Save folder for mail contents and attachments, if not specified use system temprary directory')
        mcxt.add_argument('--attachment-match',
                          display_name='Attachment Match', show_default=True,
                          default='*',
                          help='Attachment filename match, default is [[*]] which means matching all')
        mcxt.add_argument('--delete-after-read', action="store_true",
                          display_name='Delete after Read',
                          help='If this flag is set, delete mail after read')
        mcxt.add_argument('--limit', type=int, default=50,
                          display_name='Limit of Res',
                          help='Set the number of results. 0 means no limit. Default is [[50]]')
        mcxt.add_argument('--store-body',
                          display_name='Store Body?',
                          action='store_true',
                          help='If this flag is set then store body as file')
        # ======================================================================
        # monitor options
        mcxt.add_argument('--mon-timeout', nargs='?', type=int,
                          display_name='Mon Timeout Sec',
                          default=0, const=0, min_value=0,
                          help='Timeout error when no filtered file during sec '
                               '(default is [[0]] sec which means no timeout)')
        mcxt.add_argument('--mon-period', nargs='?', type=int,
                          display_name='Mon Period Sec',
                          default=10, const=10, min_value=1,
                          help='Monitoring checking period of seconds, every checking after this seconds '
                               '(default is [[10]] sec, minimum value is 10)')
        # ======================================================================
        mcxt.add_argument('--port',
                          display_name='Mail Port',
                          type=int, default=0,
                          help='Default, IMAP is 143, IMAP with SSL is 993.')
        mcxt.add_argument('--no-use-ssl',
                          display_name='No Use SSL',
                          action='store_true',
                          help='If this flag is set then do not use SSL, default is using SSL')
        mcxt.add_argument('--mailbox',
                          input_group='showwhen:operation=read,monitor',
                          display_name='Mailbox', default='inbox',
                          help='Set mailbox for reading, default is [[inbox]]')
        mcxt.add_argument('--orderby-old',
                          input_group='showwhen:operation=read,monitor',
                          display_name='Order by Old',
                          action='store_true',
                          help='If this flag is set then order by from old to new, if not set order by from new to old')
        # mcxt.add_argument('--search-filter',
        #                   input_group='showwhen:operation=read,monitor',
        #                   display_name='Search Filter', default='UNSEEN',
        #                   help='Search filter for email, default is [[UNSEEN]]. '
        #                        'For example "ALL", "UNSEEN", "(FROM abc@any.com)", "(TO def@any.com)"')

        # ##################################### for app dependent parameters
        mcxt.add_argument('operation',
                          display_name='Mail Operation',
                          choices=["read", "monitor"], default='read',
                          help='mail operation, one of {"read", "monitor"}')
        mcxt.add_argument('server',
                          display_name='Mail Server',
                          help='EMail Server to send or receive')
        mcxt.add_argument('user',
                          display_name='Mail User',
                          help='EMail User')
        mcxt.add_argument('passwd',
                          display_name='Mail Password',
                          input_method='password',
                          help="EMail User's password")
        argspec = mcxt.parse_args(args)
        return email_job(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
