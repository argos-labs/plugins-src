"""
====================================
 :mod:`argoslabs.microsoft.outlook`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Outlook
"""
#
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2021/07/21]
#     - build a plugin
#  * [2021/07/21]
#     - starting
#

################################################################################
import os
from datetime import datetime
import csv
import sys
import win32com.client
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit


################################################################################
def _get_safe_filename(fn):
    return "".join([c for c in fn if c.isalpha() or c.isdigit() or
                    c in (' ', '.', '-', '@')]).rstrip()


################################################################################
@func_log
def do_outlook(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        outlook = win32com.client.Dispatch('outlook.application')
        mapi = outlook.GetNamespace("MAPI")
        if argspec.account:
            inbox = mapi.Folders(argspec.account).Folders(argspec.emailfolder)
        else:
            inbox = mapi.GetDefaultFolder(argspec.foldertype)

        if argspec.subfolder:
            inbox = mapi.GetDefaultFolder(argspec.foldertype).Parent.Folders[
                argspec.subfolder]
        m = inbox.Items
        m.Sort("[ReceivedTime]", True)
        if argspec.conditions:
            m = m.restrict(argspec.conditions[0])
            for ent in argspec.conditions:
                m = m.restrict(ent)
        if argspec.mailsubject:
            m = m.restrict(f"[Subject]='{argspec.mailsubject}'")
        if argspec.sender:
            m = m.restrict(f"[SenderEmailAddress]='{argspec.sender}'")
        if argspec.received:
            m = m.restrict(f"[ReceivedTime]{argspec.received}")
        if argspec.findstr:
            m = list(m)
            new = []
            s = argspec.findstr.lower()
            for fn in m:
                body = fn.body.lower()
                if s in body:
                    new.append(fn)
            m = new

        if argspec.op == 'Mail Lists':
            s = csv.writer(sys.stdout, lineterminator='\n')
            s.writerow(['time', 'from', 'subject'])
            m = list(m)
            for i, ent in enumerate(m):
                try:
                    date = ent.ReceivedTime.strftime('%m-%d-%Y %H:%M:%S')
                    sender = ent.SenderEmailAddress
                    s.writerow([date, sender, ent.subject])
                except Exception:
                    s.writerow(['', '', ent.subject])
        elif argspec.op == 'Get Contents':
            if not os.path.exists(argspec.output):
                os.makedirs(argspec.output)
            s = csv.writer(sys.stdout, lineterminator='\n')
            s.writerow(['time', 'from', 'subject', 'body_file'])
            m = list(m)
            if len(m) > 0:
                for fn in m:
                    fsubject = fn.Subject
                    try:
                        date = fn.ReceivedTime.strftime('%m%d%Y%H%M%S')
                    except Exception:
                        now = datetime.now()
                        date = now.strftime('%m%d%Y%H%M%S')
                    if argspec.htmloutput:
                        if ':' in fsubject:
                            out = date + '-' + fsubject.split(':')[1] + '.html'
                        else:
                            out = date + '-' + fsubject + '.html'
                        out = os.path.join(argspec.output, _get_safe_filename(out))
                        with open(out, 'w', encoding='utf-8') as f:
                            f.write(fn.htmlbody)
                        f.close()
                    else:
                        if ':' in fsubject:
                            out = date + '-' + fsubject.split(':')[1] + '.txt'
                        else:
                            out = date + '-' + fsubject + '.txt'
                        out = os.path.join(argspec.output, _get_safe_filename(out))
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
        elif argspec.op == 'Save Attachment':
            output = os.path.abspath(argspec.output)
            for ent in m:
                try:
                    for attachment in ent.Attachments:
                        attachment.SaveASFile(
                            os.path.join(output, attachment.FileName))
                except Exception as e:
                    print("error when saving the attachment:" + str(e))
            print(output, end='')
        elif argspec.op == 'Move Emails':
            if argspec.msubfolder and argspec.maccount:
                move = mapi.Folders(argspec.maccount).Folders(argspec.msubfolder)
            elif argspec.msubfolder:
                move = mapi.GetDefaultFolder(argspec.mfoldertype).Parent.Folders[
                    argspec.msubfolder]
            else:
                move = mapi.GetDefaultFolder(argspec.mfoldertype)
            cnt = 0
            while len(m) > 0:
                m = list(m)
                # m = m.item[cnt]
                # m[0].UnRead = False
                m[0].Move(move)
                m = m[1:]
                cnt += 1
            print(f'Successfully moved {cnt} emails.')
        elif argspec.op == 'Send Mails':
            mail = outlook.CreateItem(0)
            mail.To = argspec.sender
            if argspec.body:
                mail.Body = argspec.body
            if argspec.htmlbody:
                mail.HTMLBody = argspec.htmlbody
            if argspec.mailsubject:
                mail.Subject = argspec.mailsubject
            if argspec.cc:
                mail.CC = argspec.cc
            if argspec.bcc:
                mail.BCC = argspec.bcc
            if argspec.attachment:
                for i in argspec.attachment:
                    f = os.path.abspath(i)
                    mail.Attachments.Add(f)
            mail.Send()
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
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
            display_name='Outlook',
            icon_path=get_icon_path(__file__),
            description='Outlook',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--foldertype', display_name='Folder Type',
                          default=6, type=int,
                          help='Specifies the folder type for a specified '
                               'folder. Default is 6 which is inbox. '
                               '(https://docs.microsoft.com/en-us/office/vba'
                               '/api/outlook.oldefaultfolders)')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--account', display_name='Account',
                          help='input your account')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--emailfolder', display_name='E-mail folder',
                          help='enter your E-mail folder')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--subfolder', display_name='Subfolder',
                          help='specify a subfolder')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--mailsubject', display_name='Subject',
                          help='specify a suject of the mail')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--sender', display_name='Sender/To Address',
                          help='specify the address of sender')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--received', display_name='Received Time',
                          help='specify the received time')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--findstr', display_name='Find String',
                          help='specify a string to find ')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--conditions', display_name='Mail Conditions',
                          action='append',
                          help='specify conditions of the mail')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--htmloutput', display_name='HTML Output',
                          help='specify the html output filepath',
                          action='store_true')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--output', display_name='Output Folder',
                          help='specify the output folder',
                          input_method='folderwrite', show_default=True)
        # ----------------------------------------------------------------------
        mcxt.add_argument('--mfoldertype', display_name='Move Folder Type',
                          default=6, type=int,
                          help='Specifies the folder type for a specified '
                               'folder. Default is 6 which is inbox. '
                               '(https://docs.microsoft.com/en-us/office/vba'
                               '/api/outlook.oldefaultfolders)')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--maccount', display_name='Move account',
                          help='Account with folder to move')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--msubfolder', display_name='Move Subfolder',
                          help='specify a subfolder')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--body', display_name='Mail Body',
                          input_group='Send Mails Conditions',
                          help='mail bodies to send')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--htmlbody', display_name='HTML Body',
                          input_group='Send Mails Conditions',
                          help='HTML bodies to send')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--cc', display_name='CC',
                          input_group='Send Mails Conditions',
                          help='CC')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--bcc', display_name='BCC',
                          input_group='Send Mails Conditions',
                          help='BCC')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--attachment', display_name='Attachments',
                          input_group='Send Mails Conditions',
                          help='Attachment', action='append',
                          input_method='fileread')
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='OP Type',
                          choices=['Mail Lists', 'Get Contents',
                                   'Save Attachment', 'Move Emails',
                                   'Send Mails'],
                          help='Choose an operation type')
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
