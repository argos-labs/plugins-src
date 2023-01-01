"""
====================================
 :mod:`argoslabs.microsoft.outlook`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Outlook: unittest
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
#  * [2021/07/13]
#     - unittest
#  * [2021/07/13]
#     - starting
#


################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.microsoft.outlook import _main as main


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
    #                  '--account', 'akb0930@mail2.argos-labs.com',
    #                  '--emailfolder', '받은 편지함',
    #                  # '--findstr', '보낸 날짜:	7/28/2021 2:42 PM'
    #                  # '--foldertype', '6',
    #                  '--outfile', stdout
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    # def test150_diffcol(self):
    #     try:
    #         r = main('Get Contents',
    #                  '--foldertype', '6',
    #                  # '--subfolder', 'subfolder',
    #                  # '--mailsubject', 'Updates to our terms of use',
    #                  # '--sender', 'msa@communication.microsoft.com',
    #                  '--received', ">= '09/03/2021 15:00'",
    #                  '--output', 'output',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    # def test200_get(self):
    #     stdout = 'output.txt'
    #     try:
    #         r = main('Get Contents',
    #         # '--outfile', stdout,
    #                  # '--conditions', "[SentOn] > '5/30/2017 08:00 AM'",
    #                  # '--mailsubject', 'Microsoft 계정 암호 ',
    #                  '--htmloutput',
    #                  '--output', 'output'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    # def test250_save_attachment(self):
    #     try:
    #         r = main('Save Attachment',
    #                  '--mailsubject', '받은 편지함',
    #                  '--received', ">= '2021-8'",
    #                  '--output', 'output.txt'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test300_move_folder(self):
        try:
            r = main('Move Emails',
                     '--received', ">= '09/03/2021 15:00'",
                     # '--subfolder', 'newfolder'
                     '--account', 'akb0930@mail2.argos-labs.com',
                     '--emailfolder', 'newfolder',
                     '--maccount', 'akb0930@mail2.argos-labs.com',
                     '--msubfolder', '받은 편지함'
                     )
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test350_move_folder(self):
    #     try:
    #         r = main('Move Emails',
    #                  '--received', ">= '2020-12'",
    #                  '--subfolder', 'newfolder'
    #                  )
    #         self.assertTrue(r == 1)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test400_move_folder(self):
    #     try:
    #         r = main('Move Emails',
    #                  '--received', ">= '2020-12'",
    #                  '--msubfolder', 'newfolder'
    #                  )
    #         self.assertTrue(r == 1)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test450_send_mails(self):
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