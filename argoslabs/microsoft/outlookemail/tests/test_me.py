"""
====================================
 :mod:`argoslabs.microsoft.outlookemeil`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Outlook: unittest
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
#  * [2021/09/07]
#     - starting
#


################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.microsoft.outlookemail import _main as main


################################################################################
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test50_missing(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    # def test100_maillists(self):
    #     stdout = 'output.txt'
    #     try:
    #         r = main('Mail Lists',
    #                  'akb0930@vivans.net', '받은 편지함',
    #                  # '--subfolder', 'test',
    #                  # '--sender', 'akb0930@naver.com',
    #                  # '--to', 'akb0930@vivans.net',
    #                  # '--to', 'argos',
    #                  '--search-body', '안녕하세요',
    #                  # '--sort', 'Descending',
    #                  # '--sort', 'Ascending',
    #                  # '--unread',
    #                  '--since', '09/01/2021 09:52',
    #                  # '--since', '09/08/2021 09:52',
    #                  # '--before', '09/08/2021 09:55',
    #                  '--outfile', stdout
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    # def test200_get_contents(self):
    #     try:
    #         r = main('Get Contents', 'akb0930@vivans.net', '받은 편지함',
    #                  # '--subfolder', 'test',
    #                  '--search-body', '안녕하세요',
    #                  # '--mailsubject', '9월 6일 RPA Sprint 회의 내용',
    #                  # '--received', ">= '09/03/2021 15:00'",
    #                  '--mails-number', '3',
    #                  '--output', 'output',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test300_save_attachment(self):
    #     try:
    #         r = main('Save Attachment',
    #                  'akb0930@vivans.net', '받은 편지함',
    #                  '--subfolder', 'test',
    #                  '--output', 'output'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test400_move_folder(self):
    #     try:
    #         r = main('Move Emails', 'akb0930@vivans.net', '받은 편지함',
    #                  '--subfolder', 'test',
    #                  '--maccount', 'akb0930@mail2.argos-labs.com',
    #                  '--mfolder', 'Drafts',
    #                  # '--msubfolder', 'test',
    #                  '--since', '09/06/2021 15:00',
    #                  '--mails-number', '3',
    #                  '--sort', 'Descending'
    #                  # '--msubfolder', 'test',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    # # ==========================================================================
    # def test410_move_folder(self):
    #     try:
    #         r = main('Move Emails', 'akb0930@vivans.net', '받은 편지함',
    #                  '--subfolder', 'test',
    #                  '--mfolder', '받은 편지함'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test500_test500_send_mailsr(self):
    #     try:
    #         r = main('Send Mails', 'akb0930@vivans.net', '보낸 편지함',
    #                  '--send-subjact', 'send-test',
    #                  '--to', 'akb0930@naver.com',
    #                  # '--to', 'akb0930@argos-labs.com',
    #                  # '--to', 'ankyobong@gmail.com',
    #                  '--cc', 'akb0930@argos-labs.com',
    #                  '--bcc', 'akb0930@naver.com',
    #                  '--send-body', 'test boby!!!',
    #                  '--send-body', 'test boby!!!',
    #                  '--attachment', 'output.txt'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)


    # # ==========================================================================
    # def test500_send_mails(self):
    #     file = 'output/072120211332 test.html'
    #     fn = open(file, 'rb')
    #     str = '<div dir="ltr"><br>test<br><div class="gmail_quote"><div dir="ltr" class="gmail_attr">---------- Forwarded message ---------<br>From: <strong class="gmail_sendername" dir="auto">Irene Cho</strong> <span dir="auto">&lt;<a href="mailto:irene@argos-labs.com">irene@argos-labs.com</a>&gt;</span><br>Date: Wed, Jul 21, 2021 at 1:32 PM<br>Subject: Re: test<br>To: Cho Irene &lt;<a href="mailto:irene1014@outlook.kr">irene1014@outlook.kr</a>&gt;<br></div><br><br><div dir="ltr"><br></div><br><div class="gmail_quote"><div dir="ltr" class="gmail_attr">On Wed, Jul 21, 2021 at 12:58 PM Cho Irene &lt;<a href="mailto:irene1014@outlook.kr" target="_blank">irene1014@outlook.kr</a>&gt; wrote:<br></div><blockquote class="gmail_quote" style="margin:0px 0px 0px 0.8ex;border-left:1px solid rgb(204,204,204);padding-left:1ex">\r\r\n\r\r\n\r\r\n\r\r\n\r\r\n\r\r\n<div lang="EN-US">\r\r\n<div>\r\r\n<p class="MsoNormal">test<u></u><u></u></p>\r\r\n</div>\r\r\n</div>\r\r\n\r\r\n</blockquote></div>\r\r\n</div></div>\r\r\n'
    #
    #     try:
    #         r = main('Send Mails',
    #                  '--htmlbody', str,
    #                  '--sender', 'irene@argos-labs.com',
    #                  # '--cc', 'irene@argos-labs.com',
    #                  # '--bcc', 'irene25621@gmail.com',
    #                  # '--attachment', 'output/072120211332 test.txt',
    #                  '--mailsubject','notitle'
    #                  )
    #         self.assertTrue(r == 0)
    #         fn.close()
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)