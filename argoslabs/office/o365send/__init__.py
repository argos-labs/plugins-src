"""
====================================
 :mod:`argoslabs.office.o365send`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for sending email
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2020/08/28]
#     - starting

################################################################################

import os
import sys
import ssl
import smtplib
import argparse
from email.utils import make_msgid
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# noinspection PyProtectedMember,PyUnresolvedReferences
from email.utils import formatdate, COMMASPACE
from alabs.common.util.vvargs import ModuleContext, func_log,  \
    ArgsError, ArgsExit, get_icon_path
from alabs.common.util.vvencoding import get_file_encoding


################################################################################
class EMailSend(object):
    # ==========================================================================
    def __init__(self, server, user, passwd,
                 to, subject,
                 cc=None, bcc=None,
                 reply_msgid=None,
                 body_text=None, body_file=None, body_type=None,
                 attachments=None,
                 port=0, use_ssl=True, use_tls=False,
                 logger=None):
        self.server = server
        self.user = user
        self.passwd = passwd
        self.to = to if to else []
        self.subject = subject
        self.cc = cc if cc else []
        self.bcc = bcc if bcc else []
        self.reply_msgid = reply_msgid
        self.body_text = body_text
        self.body_file = body_file
        self.body_type = body_type
        self.attachments = attachments if attachments else []
        self.port = port
        self.use_ssl = use_ssl
        self.use_tls = use_tls
        self.logger = logger
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
            if self.use_tls:
                if not self.port:
                    self.port = 587
                self.sm = smtplib.SMTP(self.server, self.port)
                # self.sm.starttls()
                # context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
                self.sm.ehlo()
                self.sm.starttls(context=context)
                self.sm.ehlo()
            else:
                if not self.port:
                    self.port = 25
                self.sm = smtplib.SMTP(self.server, self.port)
        self.sm.login(self.user, self.passwd)

    # ==========================================================================
    def close(self):
        if self.sm is not None:
            self.sm.close()
            # self.sm.quit()
            self.sm = None

    # ==========================================================================
    def check_valid(self):
        if not self.to:
            raise RuntimeError('One or more recepient needed with --to option!')
        if self.body_type not in ('text', 'html'):
            raise RuntimeError('Invalid type of Email body "%s"' % self.body_type)
        if not self.logger:
            raise RuntimeError('Invalid logger')

    # ==========================================================================
    def send(self):
        self.check_valid()
        # necessary mimey stuff
        msg = MIMEMultipart()
        msg.preamble = 'This is a multi-part message in MIME format.\n'
        msg.epilogue = ''
        msg['From'] = self.user
        if self.reply_msgid:
            # new_msgid = make_msgid()
            # msg['Message-ID'] = new_msgid
            msg['In-Reply-To'] = self.reply_msgid
            msg['References'] = self.reply_msgid
            msg['Reply-To'] = COMMASPACE.join(self.to)
        msg['To'] = COMMASPACE.join(self.to)
        msg['Cc'] = COMMASPACE.join(self.cc)
        msg['Bcc'] = COMMASPACE.join(self.bcc)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = self.subject
        msg_body = MIMEMultipart('alternative')
        body_type = 'html' if self.body_type == 'html' else 'plain'
        body = self.body_text
        if body:
            msg_body.attach(MIMEText(body, body_type))
        if self.body_file:
            if not os.path.exists(self.body_file):
                raise RuntimeError('Cannot find --body-file "%s"' % self.body_file)
            encoding = get_file_encoding(self.body_file)
            with open(self.body_file, encoding=encoding) as ifp:
                body = ifp.read()
        if not body:
            raise RuntimeError('Invalid body, please set --body-text or --body-file')
        msg_body.attach(MIMEText(body, body_type))
        msg.attach(msg_body)
        receiver = self.to + self.cc + self.bcc
        for f in self.attachments:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=os.path.basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
            msg.attach(part)
        # self.sm.set_debuglevel(1)
        r = self.sm.sendmail(self.user, receiver, msg.as_string())
        if r:
            self.logger.error('Email send error: %s' % r)
        else:
            print('OK')
        return not bool(r)


################################################################################
def send_email(mcxt, args):
    use_ssl = not args.no_use_ssl
    if args.use_tls:
        use_ssl = False
    kwargs = {
        'server': args.server,
        'user': args.user,
        'passwd': args.passwd,
        'to': args.to,
        'cc': args.cc,
        'bcc': args.bcc,
        'reply_msgid': args.reply_msgid,
        'subject': args.subject,
        'body_text': args.body_text,
        'body_file': args.body_file,
        'body_type': args.body_type,
        'attachments': args.attachments,
        'port': args.port,
        'use_ssl': use_ssl,
        'use_tls': args.use_tls,
        'logger': mcxt.logger,
    }
    with EMailSend(**kwargs) as sm:
        r = sm.send()
    return 0 if r else 1


################################################################################
# noinspection PyShadowingBuiltins
@func_log
def email_job(mcxt, args):
    # noinspection PyBroadException
    try:
        mcxt.logger.info('>>>starting...')
        return send_email(mcxt, args)
    except Exception as e:
        msg = 'Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        raise
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='office',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Adv Email Send',
        icon_path=get_icon_path(__file__),
        description='''Email operation for reading, monitoring, sending''',
        formatter_class=argparse.RawTextHelpFormatter
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--use-tls',
                          input_group='showwhen:operation=send',
                          display_name='Use TLS',
                          action='store_true',
                          help='If this flag is set then use TLS in sending email')
        mcxt.add_argument('--no-use-ssl',
                          display_name='No Use SSL',
                          action='store_true',
                          help='If this flag is set then do not use SSL, default is using SSL')
        mcxt.add_argument('--port',
                          display_name='Mail Port',
                          type=int, default=0,
                          help='Default, SMTP is 25, SMTP with SSL is 465, SMTP with TLS is 587.')
        mcxt.add_argument('--to', action='append',
                          display_name='Mail To', show_default=True,
                          help='One or more email recipient, "John X. Doe <jxd@example.com>"')
        mcxt.add_argument('--cc', action='append',
                          display_name='Mail CC',
                          help='Optional One or more email recipient, "John X. Doe <jxd@example.com>"')
        mcxt.add_argument('--bcc', action='append',
                          display_name='Mail BCC',
                          help='Hidden Optional One or more email recipient, "John X. Doe <jxd@example.com>"')
        mcxt.add_argument('--body-text', input_group='radio=Body',
                          display_name='Mail Body text', show_default=True,
                          help='Email Body text')
        mcxt.add_argument('--body-file', input_group='radio=Body',
                          display_name='Mail Body file', show_default=True,
                          input_method='fileread',
                          help='Email Body text')
        mcxt.add_argument('--body-type', choices=['text', 'html'], default='text',
                          display_name='Mail Body type', show_default=True,
                          input_method='Email Body type',
                          help='Email Body type one of {"text", "html"}, default is "text"')
        mcxt.add_argument('--attachments', action='append',
                          display_name='Attachments', show_default=True,
                          input_method='fileread',
                          help='Email file attachments')
        mcxt.add_argument('--reply-msgid',
                          display_name='Rep Msg Id',
                          help='Message Id to reaply to')

        # ##################################### for app dependent parameters
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
        mcxt.add_argument('subject',
                          display_name='Subject',
                          help="EMail Subject")
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
