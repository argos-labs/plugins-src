"""
====================================
 :mod:`argoslabs.microsoft.outlookemail`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Outlook
"""
#
# Authors
# ===========
#
# * Kyobong An
#
# Change Log
# --------
#
#  * [2023/05/17]
#     - html file, image to html body 기능 추가(본문이미지 추가는 outlook에서만 확
#     )
#  * [2023/03/15]
#     - Unread Only 기능 추가
#  * [2021/11/17]
#     - 메일을 저장할때 초까지 같은 경우가 발생해서 완전 같은 경우 filename뒤에 (1)을 추가
#  * [2021/09/10]
#     - Mark as Read를 읽지않은 메일만 가져올때와 동시에 사용할때 오류가 생김 메일을 가져온뒤에 Mark as Read를 사용하도록 변경
#  * [2021/09/07]
#     - starting
#

################################################################################
import os
from datetime import datetime
import csv
import sys
import win32com.client
from alabs.common.util.vvencoding import get_file_encoding
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit

################################################################################
def _get_safe_filename(fn):
    return "".join([c for c in fn if c.isalpha() or c.isdigit() or
                    c in (' ', '.', '-', '@')]).rstrip()


def _get_safe_next_filename(fn):
    fn, ext = os.path.splitext(fn)
    for n in range(1, 1000000):
        nfn = f'{fn} ({n})' + ext
        if not os.path.exists(nfn):
            return nfn


class OutLook(object):
    def __init__(self, argspec):
        self.argspec = argspec
        self.op = self.argspec.op
        if self.op == 'Send Mails':
            self.outlook = win32com.client.Dispatch('outlook.application')
        elif self.op == 'Save Mails':
            self.outlook = win32com.client.Dispatch('outlook.application')
        else:
            self.outlook = win32com.client.Dispatch('outlook.application').GetNamespace("MAPI")
            self.account = self.argspec.account
            self.emailfolder = self.argspec.emailfolder

            self.mailbox = self.openoutlook_mailbox()    # 사용할 아웃룩 계정의 폴더를 가져옴
            self.mail = self.get_mail()    # 메일 가져오는 부분

        if self.op == 'Mail Lists':
            self.maillist()
        elif self.op == 'Get Contents':
            self.get_contents()
        elif self.op == 'Save Attachment':
            self.save_attachment()
        elif self.op == 'Move Emails':
            self.move_emails()
        elif self.op == 'Send Mails':
            self.sendmail()
        elif self.op == 'Save Mails':
            self.savemail()

        if self.argspec.unread:     # 다른작업을 모두하고 읽음으로 표시하도록 변경함.
            for mail in self.mail:
                if mail.Unread:
                    mail.Unread = False

    def openoutlook_mailbox(self):
        # 파라미터로 계정과 폴더를 받아야함.
        mailbox = self.outlook.Folders(self.account).Folders(self.emailfolder)

        if self.argspec.subfolder:     # 계정 - 폴더 - 하위폴더  이부분은 하위폴더의 경우 사용
            mailbox = mailbox.Folders(self.argspec.subfolder)
        return mailbox

    def get_mail(self):
        mails = self.mailbox.Items
        if self.argspec.conditions:
            mails = mails.restrict(self.argspec.conditions[0])
            for ent in self.argspec.conditions:
                mails = mails.restrict(ent)
        if self.argspec.search_subject:
            mails = mails.restrict(f"[Subject]='{self.argspec.search_subject}'")
        if self.argspec.search_sender:
            mails = mails.restrict(f"[SenderEmailAddress]='{self.argspec.search_sender}'")
        if self.argspec.search_to:
            mails = mails.restrict(f"[To]='{self.argspec.search_to}'")
        if self.argspec.since:
            mails = mails.restrict(f"[ReceivedTime]>='{self.argspec.since}'")
        if self.argspec.before:
            mails = mails.restrict(f"[ReceivedTime]<'{self.argspec.before}'")
        if self.argspec.get_unread:
            mails = list(mails)
            new = []
            for mail in mails:
                if mail.Unread:
                    new.append(mail)
            mails = new
        if self.argspec.search_body:
            mails = list(mails)
            new = []
            s = self.argspec.search_body.lower()
            for mail in mails:
                body = mail.body.lower()
                if s in body:
                    new.append(mail)
            mails = new

        if self.argspec.sort == 'Descending':
            mails.Sort("[ReceivedTime]", True)
        elif self.argspec.sort == 'Ascending':
            mails.Sort("[ReceivedTime]", False)

        if self.argspec.mails_number != 0:      # 메일의 수를 지정하는 부분 0일경우 모든 이메일
            mails = list(mails)
            mails = mails[:self.argspec.mails_number]
        return mails

    def maillist(self):
        s = csv.writer(sys.stdout, lineterminator='\n')
        s.writerow(['time', 'from', 'subject'])
        m = list(self.mail)
        for i, ent in enumerate(m):
            try:
                date = ent.ReceivedTime.strftime('%m-%d-%Y %H:%M:%S')
                sender = ent.SenderEmailAddress
                s.writerow([date, sender, ent.subject])
            except Exception:
                s.writerow(['', '', ent.subject])

    def get_contents(self):
        if not os.path.exists(self.argspec.output):
            raise Exception('The output folder is not entered.')
        s = csv.writer(sys.stdout, lineterminator='\n')
        s.writerow(['time', 'from', 'subject', 'body_file'])
        mails = list(self.mail)
        if len(mails) > 0:
            for fn in mails:
                fsubject = fn.Subject
                try:
                    date = fn.ReceivedTime.strftime('%m%d%Y%H%M%S')
                except Exception:
                    now = datetime.now()
                    date = now.strftime('%m%d%Y%H%M%S')
                if self.argspec.htmloutput:
                    if ':' in fsubject:
                        out = date + '-' + fsubject.split(':')[1] + '.html'
                    else:
                        out = date + '-' + fsubject + '.html'
                    out = os.path.join(self.argspec.output, _get_safe_filename(out))
                    with open(out, 'w', encoding='utf-8') as f:
                        f.write(fn.htmlbody)
                    f.close()
                else:
                    if ':' in fsubject:
                        out = date + '-' + fsubject.split(':')[1] + '.txt'
                    else:
                        out = date + '-' + fsubject + '.txt'
                    out = os.path.join(self.argspec.output, _get_safe_filename(out))
                    if os.path.exists(out):
                        out = _get_safe_next_filename(out)
                    with open(out, 'w', encoding='utf-8') as f:
                        f.write(fn.body)
                    f.close()
                try:
                    time = fn.ReceivedTime.strftime('%m-%d-%Y %H:%M:%S')
                    sender = fn.SenderEmailAddress
                    s.writerow([time, sender, fn, out])
                except Exception:
                    s.writerow(['', '', out])
        else:
            raise IOError('Cannot find any email')

    def save_attachment(self):
        if not self.argspec.output:
            raise Exception('The output folder is not entered.')
        output = os.path.abspath(self.argspec.output)
        for ent in self.mail:
            try:
                for attachment in ent.Attachments:
                    if os.path.exists(os.path.join(output, attachment.FileName)):   # 파일이름이 같은 경우
                        attachment.SaveASFile(
                            _get_safe_next_filename(os.path.join(output, attachment.FileName)))
                    else:
                        attachment.SaveASFile(os.path.join(output, attachment.FileName))
            except Exception as e:
                print("error when saving the attachment:" + str(e))
        print(output, end='')

    def move_emails(self):
        if self.argspec.mfolder and self.argspec.maccount:   # 이동시킬 폴더의 계정과 폴더
            move = self.outlook.Folders(self.argspec.maccount).Folders(self.argspec.mfolder)
        else:   # 이동할 폴더의 계정을 지정하지않는다면 이동시킬 폴더의 계정을 사용함
            move = self.outlook.Folders(self.account).Folders(self.argspec.mfolder)
        if self.argspec.msubfolder:     # 계정 - 폴더 - 하위폴더  이부분은 하위폴더의 경우 사용
            move = move.Folders(self.argspec.msubfolder)

        cnt = 0
        mails = list(self.mail)
        for mail in mails:  # 메일 이동시키는 부분
            mail.Move(move)
            cnt += 1

        print(f'Successfully moved {cnt} emails.')

    def sendmail(self):
        mail = self.outlook.CreateItem(0)
        mail.To = ';'.join(self.argspec.to)+';'
        if self.argspec.send_body:      # 본문 부분이 한줄로만 작성이 되어서 리스트형식으로 받아서 조인시킴
            mail.Body = "\n".join(self.argspec.send_body)
            # mail.Body = self.argspec.send_body
        if self.argspec.htmlbody or self.argspec.htmlbody_file:
            if self.argspec.htmlbody_file:
                if not os.path.exists(self.argspec.htmlbody_file):
                    raise RuntimeError('Cannot find --body-file "%s"' % self.argspec.htmlbody_file)
                encoding = get_file_encoding(self.argspec.htmlbody_file)
                with open(self.argspec.htmlbody_file, encoding=encoding) as ifp:
                    htmlbody = ifp.read()
            else:
                htmlbody = self.argspec.htmlbody

            for n, key in enumerate(self.argspec.key):
                image_attachment = mail.Attachments.Add(self.argspec.value[n], 1, 0, key)
                image_cid = image_attachment.FileName
                htmlbody = htmlbody.replace(key, f"cid:{image_cid}")

            mail.HTMLBody = htmlbody
        if self.argspec.send_subjact:
            mail.Subject = self.argspec.send_subjact
        if self.argspec.cc:
            mail.CC = ';'.join(self.argspec.cc)+';'
        if self.argspec.bcc:
            mail.BCC = ';'.join(self.argspec.bcc)+';'
        if self.argspec.attachment:
            for attach in self.argspec.attachment:
                mail.Attachments.Add(os.path.abspath(attach))
        mail.Send()
        print("Successfully sending emails.")

    def savemail(self):
        mail = self.outlook.CreateItem(0)
        mail.To = ';'.join(self.argspec.to)+';'
        if self.argspec.send_body:      # 본문 부분이 한줄로만 작성이 되어서 리스트형식으로 받아서 조인시킴
            mail.Body = "\n".join(self.argspec.send_body)
            # mail.Body = self.argspec.send_body
        if self.argspec.htmlbody:
            mail.HTMLBody = self.argspec.htmlbody
        if self.argspec.send_subjact:
            mail.Subject = self.argspec.send_subjact
        if self.argspec.cc:
            mail.CC = ';'.join(self.argspec.cc)+';'
        if self.argspec.bcc:
            mail.BCC = ';'.join(self.argspec.bcc)+';'
        if self.argspec.attachment:
            for attach in self.argspec.attachment:
                mail.Attachments.Add(os.path.abspath(attach))
        mail.Save()
        print("Successfully saving emails.")

################################################################################
@func_log
def do_outlook(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        OutLook(argspec)
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
            owner='ARGOS-LABS',
            group='5',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Outlook E-mail',
            icon_path=get_icon_path(__file__),
            description='Outlook',
    ) as mcxt:
        # ######################################## for app dependent options
        # ----------------------------------------------------------------------
        mcxt.add_argument('--subfolder', show_default=True,
                          display_name='Mail Subfolder',
                          help='specify a subfolder')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--output', show_default=True,
                          display_name='Save Folder',
                          help='specify the output folder',
                          input_method='folderwrite')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--search-subject', display_name='Search Subject',
                          help='specify a suject of the mail')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--search-sender', display_name='Search Sender',
                          help='specify the address of sender')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--search-to', display_name='Search To',
                          help='specify the address of to')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--search-body', display_name='Search Body',
                          help='specify a string to find')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--since', display_name='Search Since',
                          help='Set filter for email address SINCE, example is [[09/01/2021 15:00]]')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--before', display_name='Search Before',
                          help='Set filter for email address BEFORE, example is [[09/07/2021 15:00]]')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--conditions', display_name='Mail Conditions',
                          action='append',
                          help="specify conditions of the mail, example is[[[ReceivedTime]>='09/06/2021 15:00']]")
        # ----------------------------------------------------------------------
        mcxt.add_argument('--mails-number', type=int,
                          default=0,
                          display_name='Number of mails',
                          help='specify the number of emails.')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--get-unread', action="store_true",
                          display_name='Unread Only',
                          help='unread mails')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--unread',  action="store_true",
                          display_name='Mark as Read',
                          help='mails mark as read')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--sort',  choices=['Descending', 'Ascending'],
                          display_name='Sorted by Date',
                          help='get descending or ascending order by date')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--htmloutput', display_name='HTML Output',
                          input_group='Get Contents Option',
                          help='specify the html output filepath',
                          action='store_true')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--maccount', display_name='Target Account',
                          input_group='Move Emails Option',
                          help='Account with folder to move')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--mfolder', display_name='Target Folder',
                          input_group='Move Emails Option',
                          help='specify a subfolder')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--msubfolder', display_name='Target Subfolder',
                          input_group='Move Emails Option',
                          help='specify a subfolder')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--to', action='append',
                          display_name='Mail To',
                          input_group='Send Mails Conditions',
                          help='One or more email recipient')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--send-subjact', display_name='Mail Subjact',
                          input_group='Send Mails Conditions',
                          help='mail subjact to send')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--send-body', action='append',
                          display_name='Mail Body',
                          input_group='Send Mails Conditions',
                          help='mail bodies to send')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--htmlbody', display_name='HTML Body',
                          input_group='Send Mails Conditions',
                          help='HTML bodies to send')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--htmlbody-file', input_group='Send Mails Conditions',
                          display_name='HTML Body file',
                          input_method='fileread',
                          help='HTML bodies to send')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--cc', action='append',
                          display_name='CC',
                          input_group='Send Mails Conditions',
                          help='CC')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--bcc', action='append',
                          display_name='BCC',
                          input_group='Send Mails Conditions',
                          help='BCC')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--attachment', display_name='Attachments',
                          input_group='Send Mails Conditions',
                          help='Attachment', action='append',
                          input_method='fileread')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--key',
                          display_name='Key', action='append',
                          input_group='Image to htmlbody',
                          help='The parameter name to use for the HTML Body. (eg, "my.a")')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--value', display_name='Value', action='append',
                          input_group='Image to htmlbody',
                          input_method='fileread',
                          help='Image to convert to base64')
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Mail Operation',
                          choices=['Mail Lists', 'Get Contents',
                                   'Save Attachment', 'Move Emails',
                                   'Send Mails', 'Save Mails'],
                          help='Choose an operation type')
        # ----------------------------------------------------------------------
        mcxt.add_argument('account', display_name='Mail Account',
                          help='input your account')
        # ----------------------------------------------------------------------
        mcxt.add_argument('emailfolder', display_name='Mail Folder',
                          help='enter your E-mail folder')
        argspec = mcxt.parse_args(args)
        return do_outlook(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
