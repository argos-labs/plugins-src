#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.office.emailsend`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2020/08/27]
#     - starting

################################################################################
import os
import sys
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.office.o365send import _main as main
from contextlib import contextmanager
from io import StringIO


################################################################################
@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


################################################################################
# noinspection PyUnresolvedReferences
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    ARGS = {
        'gmail': [
            'imap.gmail.com',
            'mcchae@gmail.com',
            '..',
        ],
        'vivans': [
            'mail2.vivans.net',
            'mcchae@vivans.net',
            '..',
        ],
        'plugin': [
            'imap.gmail.com',
            'plugin@argos-labs.com',
            '..',
        ],
        'office365': [
            'smtp.office365.com',
            'a7733@myoffice.site',
            '..',
        ],
    }

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_invalid(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_invalid(self):
        try:
            _ = main(*TU.ARGS['vivans'])
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0030_invalid(self):
        try:
            _ = main(*TU.ARGS['gmail'], 'Test subject')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0040_invalid(self):
        try:
            _ = main(*TU.ARGS['gmail'], 'Test subject',
                     '--to', '채문창<mcchaehm@gmail.com>')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_valid(self):
        try:
            r = main(*TU.ARGS['gmail'], 'First Test subject',
                     '--to', 'Jerry HM<mcchaehm@gmail.com>',
                     '--body-text', 'Hello world? This is a test!!!\nsecond line')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_invalid_mail_address(self):
        try:
            _ = main(*TU.ARGS['gmail'], 'First Test subject',
                     '--to', 'mcchaehm-gmail.com',
                     '--body-text', 'Hello world? This is a test!!!\nsecond line')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0120_invalid_mail_address(self):
        try:
            r = main(*TU.ARGS['gmail'], 'First Test subject',
                     '--to', 'one@one.org',
                     '--body-text', 'Hello world? This is a test!!!\nsecond line')
            # gmail은 해당 도메인이 없다는 것이 메일로 옴
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0130_valid(self):
        try:
            r = main(*TU.ARGS['gmail'], 'Second Test subject, multi-line ok? 여러줄 안됨',
                     '--to', '채문창<mcchaehm@gmail.com>',
                     '--body-text', '안녕? 이것은 테스트야!!!\nsecond line')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_valid_multi_to(self):
        try:
            r = main(*TU.ARGS['gmail'], 'Thrid Test subject',
                     '--to', '채문창<mcchaehm@gmail.com>',
                     '--to', '채문창<mcchae@vivans.net>',
                     '--to', 'Jerry Chae<mcchae@argos-labs.com>',
                     '--body-text', '안녕? 이것은 테스트야!!!\nsecond line')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_valid_multi_cc_bcc(self):
        try:
            r = main(*TU.ARGS['gmail'], 'Forth Test subject',
                     '--to', '채문창<mcchaehm@gmail.com>',
                     '--cc', '채문창<mcchae@vivans.net>',
                     '--cc', '채문창<mcchae@argos-labs.com>',
                     '--bcc', '마우스 Chae<mousechae@gmail.com>',
                     '--bcc', '쥐메일 Chae<mcchae@gmail.com>',
                     '--body-text', '안녕? 이것은 테스트야!!!\nsecond line')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_valid_file(self):
        try:
            os.chdir(os.path.dirname(__file__))
            r = main(*TU.ARGS['gmail'], 'Fifth Test subject',
                     '--to', '채문창<mcchaehm@gmail.com>',
                     '--body-file', 'body.html')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_valid_file_html(self):
        try:
            os.chdir(os.path.dirname(__file__))
            r = main(*TU.ARGS['gmail'], 'Sixth Test subject',
                     '--to', '채문창<mcchaehm@gmail.com>',
                     '--body-file', 'body.html',
                     '--body-type', 'html')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0180_valid_file_html_attach_1(self):
        try:
            os.chdir(os.path.dirname(__file__))
            r = main(*TU.ARGS['gmail'], 'Seventh Test subject',
                     '--to', '채문창<mcchaehm@gmail.com>',
                     '--body-file', 'body.html',
                     '--attachments', 'Python Plugin ARGOSLABS EWP 06122019.pdf'
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0190_valid_file_html_attach_3(self):
        try:
            os.chdir(os.path.dirname(__file__))
            r = main(*TU.ARGS['gmail'], 'Seventh Test subject',
                     '--to', '채문창<mcchaehm@gmail.com>',
                     '--body-file', 'body.html',
                     '--body-type', 'html',
                     '--attachments', 'Email_Send-1.png',
                     '--attachments', 'Email_Send-2.png',
                     '--attachments', 'Email_Send-3.png',
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_valid(self):
        try:
            r = main(*TU.ARGS['plugin'], 'Second Test subject, multi-line ok? 여러줄 안됨',
                     '--to', '플러그인<plugin@argos-labs.com>',
                     '--body-text', '안녕? 이것은 테스트야!!!\nsecond line')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_valid(self):
        try:
            os.chdir(os.path.dirname(__file__))
            r = main(*TU.ARGS['plugin'], 'Seventh Test subject',
                     '--to', '플러그인<plugin@argos-labs.com>',
                     '--body-file', 'body.html',
                     '--body-type', 'html',
                     '--attachments', 'Email_Send-1.png',
                     '--attachments', 'Email_Send-2.png',
                     '--attachments', 'Email_Send-3.png',
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_valid_office365(self):
        try:
            r = main(*TU.ARGS['office365'],
                     'Second Test subject, multi-line ok? 여러줄 안됨',
                     '--use-tls',
                     '--to', 'mcchae@gmail.com',
                     '--body-text', '안녕? 이것은 테스트야!!!\nsecond line')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0230_valid_reply_to(self):
        try:
            r = main(*TU.ARGS['vivans'],
                     'RE> reply???',
                     '--to', 'mcchae@gmail.com',
                     '--body-text', 'This is your reply email!!!\nsecond line',
                     '--reply-msgid', '<5f42341d.1c69fb81.d38cf.3131@mx.google.com>',
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
