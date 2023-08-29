"""
====================================
 :mod:`argoslabs.office.emailread`
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
import sys
import csv
import time
import glob
import shutil
import datetime
# import subprocess
# from alabs.common.util.vvargs import ArgsError
from tempfile import gettempdir
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.office.emailread import _main as main
# if sys.gettrace() is not None:
from argoslabs.office.emailsend import _main as main_send
from contextlib import contextmanager
from io import StringIO
from alabs.common.util.vvencoding import get_file_encoding
# from threading import Thread
from multiprocessing import Process


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
    ARGS = {
        'gmail': [
            # gmail do not accept weak credentials so I changed into vivans
            'imap.gmail.com',
            'mcchae@gmail.com',
            '..',     # 2-pass password
        ],
        'vivans': [
            'mail2.vivans.net',
            'mcchae@vivans.net',
            '..',
        ],
        'hotmail': [
            'imap.gmail.com',
            'mcchaehm@gmail.com',
            '..',
        ],
        'outlook': [                # exchange server
            'outlook.office365.com',
            'jerrychae@outlook.com',
            '..',
        ],
    }
    stdout = '%s%sout.txt' % (gettempdir(), os.path.sep)

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))
        for ed in glob.glob('%s%semail_save*' % (gettempdir(), os.path.sep)):
            shutil.rmtree(ed)
        for _ in glob.glob('%s%semail_save*' % (gettempdir(), os.path.sep)):
            self.assertTrue(False)
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

    # # ==========================================================================
    # def test0090_valid_read_delete_all(self):
    #     sf = '%s%stest_save_folder' % (gettempdir(), os.path.sep)
    #     try:
    #         if os.path.exists(sf):
    #             shutil.rmtree(sf)
    #         os.makedirs(sf)
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--search-type', 'ALL',
    #                  '--delete-after-read',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0100_valid_send(self):
    #     try:
    #         TU.subject = 'First Test subject'
    #         TU.body = 'Hello world? This is a test!!!\nsecond line'
    #         r = main_send(*TU.ARGS['gmail'], TU.subject,
    #                       '--to', 'Jerry HM<jerrychae@outlook.com>',
    #                       '--body-text', TU.body)
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0110_valid_read(self):
    #     try:
    #         time.sleep(5)
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) == 2 and rr[1][5] == TU.subject)
    #         # with open(rr[1][6]) as ifp:
    #         #     bs = ifp.read()
    #         # self.assertTrue(bs == TU.body)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0120_valid_send(self):
    #     try:
    #         TU.subject = '두 번째 Test subject'
    #         TU.body = 'Hello world? 이것은 테스트임!!!\nsecond line'
    #         r = main_send(*TU.ARGS['gmail'], TU.subject,
    #                       '--to', 'Jerry HM<jerrychae@outlook.com>',
    #                       '--body-text', TU.body)
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0130_valid_read_all(self):
    #     try:
    #         time.sleep(5)
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--search-type', 'ALL',
    #                  '--store-body',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) >= 2 and rr[1][5] == TU.subject)
    #
    #         encoding = get_file_encoding(rr[1][6])
    #         with open(rr[1][6], encoding=encoding) as ifp:
    #             bs = ifp.read()
    #         self.assertTrue(bs == TU.body)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0140_valid_read_all_since(self):
    #     try:
    #         dt_since = datetime.date.today() + datetime.timedelta(days=1)
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--search-type', 'ALL',
    #                  '--search-since', dt_since.strftime('%Y-%m-%d'),
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r != 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0150_valid_read_all_since_before(self):
    #     try:
    #         # 검색 날짜는 실제로 UTC 검색으로 해야 함
    #         un = datetime.datetime.utcnow()
    #         un_dt = datetime.date(un.year, un.month, un.day)
    #         un_dt_1 = un_dt + datetime.timedelta(days=1)
    #         dt = datetime.date.today()
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--search-type', 'ALL',
    #                  '--search-since', un_dt.strftime('%Y-%m-%d'),
    #                  '--search-before', un_dt_1.strftime('%Y-%m-%d'),
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         dt_p = dt_c = None
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for i, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #                 if i > 0:
    #                     dt_row = datetime.datetime.strptime(row[0][:8], "%Y%m%d").date()
    #                     self.assertTrue(dt_row == dt)  # 검색은 UTC Date로, 저장된 내용은 local로
    #                     dt_c = datetime.datetime.strptime(row[0], "%Y%m%d-%H%M%S")
    #                     if dt_p is not None:
    #                         self.assertTrue(dt_c <= dt_p)
    #                     dt_p = dt_c
    #         self.assertTrue(len(rr) > 1)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0160_valid_read_all_since_before_orderby(self):
    #     try:
    #         un = datetime.datetime.utcnow()
    #         un_dt = datetime.date(un.year, un.month, un.day)
    #         un_dt_1 = un_dt + datetime.timedelta(days=1)
    #         dt = datetime.date.today()
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--search-type', 'ALL',
    #                  '--search-since', un_dt.strftime('%Y-%m-%d'),
    #                  '--search-before', un_dt_1.strftime('%Y-%m-%d'),
    #                  '--orderby-old',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         dt_p = dt_c = None
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for i, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #                 if i > 0:
    #                     dt_row = datetime.datetime.strptime(row[0][:8], "%Y%m%d").date()
    #                     self.assertTrue(dt_row == dt)  # 검색은 UTC Date로, 저장된 내용은 local로
    #                     dt_c = datetime.datetime.strptime(row[0], "%Y%m%d-%H%M%S")
    #                     if dt_p is not None:
    #                         self.assertTrue(dt_c >= dt_p)
    #                     dt_p = dt_c
    #         self.assertTrue(len(rr) > 1)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0200_valid_send_attach(self):
    #     try:
    #         TU.subject = '첫 번째 첨부테스트'
    #         TU.body = 'Hello world? 이것은 테스트임!!!\nsecond line'
    #         r = main_send(*TU.ARGS['gmail'], TU.subject,
    #                       '--to', 'Jerry HM<jerrychae@outlook.com>',
    #                       '--body-text', TU.body,
    #                       '--body-file', 'body.html',
    #                       '--body-type', 'html',
    #                       '--attachments', 'Email_Send-1.png',
    #                       '--attachments', 'body.html',
    #                       )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0210_valid_read(self):
    #     sf = '%s%stest_save_folder' % (gettempdir(), os.path.sep)
    #     try:
    #         time.sleep(5)
    #         if os.path.exists(sf):
    #             shutil.rmtree(sf)
    #         os.makedirs(sf)
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--save-folder', sf,
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for i, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) > 1)
    #         attachments = rr[1][7].split(',')
    #         for attachment in attachments:
    #             if attachment.endswith('.png'):
    #                 self.assertTrue(os.path.getsize(attachment) ==
    #                                 os.path.getsize('Email_Send-1.png'))
    #             elif attachment.endswith('.html'):
    #                 self.assertTrue(os.path.getsize(attachment) ==
    #                                 os.path.getsize('body.html'))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(sf):
    #             shutil.rmtree(sf)
    #
    # # ==========================================================================
    # def test0220_valid_send_attach(self):
    #     try:
    #         TU.subject = '두 번째 첨부테스트'
    #         TU.body = 'Hello world? 이것은 테스트임!!!\nsecond line'
    #         r = main_send(*TU.ARGS['gmail'], TU.subject,
    #                       '--to', 'Jerry HM<jerrychae@outlook.com>',
    #                       '--body-text', TU.body,
    #                       '--body-file', 'body.html',
    #                       '--body-type', 'html',
    #                       '--attachments', 'Email_Send-2.png',
    #                       '--attachments', 'Email_Send-3.png',
    #                       '--attachments', 'body.html',
    #                       )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0230_valid_read(self):
    #     sf = '%s%stest_save_folder' % (gettempdir(), os.path.sep)
    #     try:
    #         time.sleep(5)
    #         if os.path.exists(sf):
    #             shutil.rmtree(sf)
    #         os.makedirs(sf)
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--save-folder', sf,
    #                  '--attachment-match', '*.png',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for i, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) > 1)
    #         attachments = rr[1][7].split(',')
    #         pngs = ('Email_Send-2.png', 'Email_Send-3.png')
    #         for png in pngs:
    #             b_found = False
    #             for attachment in attachments:
    #                 if png in attachment:
    #                     b_found = True
    #                     break
    #             self.assertTrue(b_found)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(sf):
    #             shutil.rmtree(sf)
    #
    # # ==========================================================================
    # def test0240_valid_read_criteria(self):
    #     try:
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--search-type', 'READ',
    #                  '--search-subject', 'First Test',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for i, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #                 if i > 0:
    #                     fndx = row[5].find('First Test')
    #                     self.assertTrue(fndx >= 0)
    #         self.assertTrue(len(rr) > 1)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # # ==========================================================================
    # # def test0250_valid_read_criteria(self):
    # #     try:
    # #         r = main('read', *TU.ARGS['outlook'],
    # #                  '--search-type', 'ALL',
    # #                  '--search-subject', '두 번째',
    # #                  '--outfile', TU.stdout)
    # #         self.assertTrue(r == 0)
    # #         rr = []
    # #         encoding = get_file_encoding(TU.stdout)
    # #         with open(TU.stdout, encoding=encoding) as ifp:
    # #             print(ifp.read())
    # #         with open(TU.stdout, encoding=encoding) as ifp:
    # #             cr = csv.reader(ifp)
    # #             for i, row in enumerate(cr):
    # #                 self.assertTrue(len(row) in (9,))
    # #                 rr.append(row)
    # #                 if i > 0:
    # #                     fndx = row[5].find('두 번째')
    # #                     self.assertTrue(fndx >= 0)
    # #         self.assertTrue(len(rr) > 1)
    # #     except Exception as e:
    # #         sys.stderr.write('\n%s\n' % str(e))
    # #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0260_valid_read_criteria(self):
    #     try:
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--search-type', 'READ',
    #                  '--search-from', 'mcchae',
    #                  '--search-subject', 'First Test',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for i, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #                 if i > 0:
    #                     self.assertTrue(row[1].find('mcchae') >= 0 or row[2].find('mcchae') >= 0)
    #                     self.assertTrue(row[5].find('First Test') >= 0)
    #         self.assertTrue(len(rr) > 1)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0270_invalid_read_criteria(self):
    #     try:
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--search-type', 'READ',
    #                  '--search-from', 'foobar',
    #                  '--search-subject', 'First Test',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r != 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0280_valid_read_criteria(self):
    #     try:
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--search-type', 'READ',
    #                  '--search-to', 'jerrychae',
    #                  '--search-subject', 'First Test',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for i, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #                 if i > 0:
    #                     self.assertTrue(row[3].find('jerrychae') >= 0 or row[4].find('jerrychae') >= 0)
    #                     self.assertTrue(row[5].find('First Test') >= 0)
    #         self.assertTrue(len(rr) > 1)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0290_valid_read_criteria(self):
    #     try:
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--search-type', 'READ',
    #                  '--search-body', 'Hello world',
    #                  '--store-body',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for i, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #                 if i > 0:
    #                     encoding = get_file_encoding(row[6])
    #                     with open(row[6], encoding=encoding) as ifp:
    #                         bs = ifp.read()
    #                         self.assertTrue(bs.find('Hello world') >= 0)
    #         self.assertTrue(len(rr) > 1)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0300_valid_read_criteria(self):
    #     try:
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--search-type', 'READ',
    #                  '--search-body', 'This is mail test',
    #                  '--store-body',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for i, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #                 if i > 0:
    #                     encoding = get_file_encoding(row[6])
    #                     with open(row[6], encoding=encoding) as ifp:
    #                         bs = ifp.read()
    #                         self.assertTrue(bs.find('This is mail test') >= 0)
    #         self.assertTrue(len(rr) > 1)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0310_valid_send_attach(self):
    #     try:
    #         TU.subject = 'delete mail test'
    #         TU.body = 'Hello world?\nThis mail is auto deleted after read!'
    #         r = main_send(*TU.ARGS['gmail'], TU.subject,
    #                       '--to', 'Jerry HM<jerrychae@outlook.com>',
    #                       '--body-text', TU.body,
    #                       '--attachments', 'Email_Send-3.png',
    #                       )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0320_valid_read(self):
    #     sf = '%s%stest_save_folder' % (gettempdir(), os.path.sep)
    #     try:
    #         time.sleep(5)
    #         if os.path.exists(sf):
    #             shutil.rmtree(sf)
    #         os.makedirs(sf)
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--save-folder', sf,
    #                  '--delete-after-read',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for i, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #                 if i == 1:
    #                     self.assertTrue(row[5] == TU.subject)
    #         self.assertTrue(len(rr) == 2)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(sf):
    #             shutil.rmtree(sf)
    #
    # # ==========================================================================
    # def test0330_invalid_read_criteria(self):
    #     try:
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--search-type', 'READ',
    #                  '--search-subject', TU.subject,
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r != 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0340_valid_monitor_criteria_limit(self):
    #     try:
    #         r = main('monitor', *TU.ARGS['outlook'],
    #                  '--search-type', 'READ',
    #                  '--limit', '2',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #             self.assertTrue(rs == '2')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0350_valid_send_attach(self):
    #     try:
    #         TU.subject = '세 번째 : 모니터 테스트'
    #         TU.body = 'Hmm... Monitor test! 이것은 테스트임!!!\nsecond line'
    #         r = main_send(*TU.ARGS['gmail'], TU.subject,
    #                       '--to', 'Jerry HM<jerrychae@outlook.com>',
    #                       '--body-text', TU.body,
    #                       # '--body-file', 'body.html',  # html 로 메시지 덮어쓰게됨
    #                       # '--body-type', 'html',
    #                       '--attachments', 'Email_Send-2.png',
    #                       '--attachments', 'Email_Send-3.png',
    #                       '--attachments', 'body.html',
    #                       )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0360_valid_monitor_timeout(self):
    #     try:
    #         r = main('monitor', *TU.ARGS['outlook'],
    #                  '--search-type', 'UNREAD',
    #                  '--attachment-match', '*.png',
    #                  '--mon-period', '5',
    #                  '--mon-timeout', '10',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #             self.assertTrue(rs == '1')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)
    #
    # # ==========================================================================
    # def test0370_valid_read_criteria(self):
    #     try:
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--search-type', 'UNREAD',
    #                  '--attachment-match', '*.png',
    #                  '--store-body',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for i, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #                 if i > 0:
    #                     encoding = get_file_encoding(row[6])
    #                     with open(row[6], encoding=encoding) as ifp:
    #                         bs = ifp.read()
    #                         self.assertTrue(bs.find('Monitor test') >= 0)
    #         self.assertTrue(len(rr) == 2)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0380_valid_monitor_timeout(self):
    #     try:
    #         r = main('monitor', *TU.ARGS['outlook'],
    #                  '--search-type', 'UNREAD',
    #                  '--attachment-match', '*.png',
    #                  '--mon-period', '3',
    #                  '--mon-timeout', '7',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #             self.assertTrue(rs == '0')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)
    #
    # # # ==========================================================================
    # # def test0410_valid_monitor(self):
    # #     try:
    # #         t = Process(target=test0410_send)
    # #         t.start()
    # #         r = main('monitor', *TU.ARGS['outlook'],
    # #                  '--search-type', 'UNREAD',
    # #                  '--mon-period', '10',
    # #                  '--outfile', TU.stdout)
    # #         self.assertTrue(r == 0)
    # #         rr = []
    # #         encoding = get_file_encoding(TU.stdout)
    # #         with open(TU.stdout, encoding=encoding) as ifp:
    # #             print(ifp.read())
    # #         with open(TU.stdout, encoding=encoding) as ifp:
    # #             cr = csv.reader(ifp)
    # #             for i, row in enumerate(cr):
    # #                 self.assertTrue(len(row) in (8,))
    # #                 rr.append(row)
    # #         self.assertTrue(len(rr) == 2)
    # #         t.join()
    # #     except Exception as e:
    # #         sys.stderr.write('\n%s\n' % str(e))
    # #         self.assertTrue(False)
    #
    # # ==========================================================================
    # # def test0390_read_attachment_txt(self):
    # #     try:
    # #         sf = os.path.join(os.path.dirname(__file__), 'sf')
    # #         r = main('read', *TU.ARGS['outlook'],
    # #                  '--save-folder', sf,
    # #                  '--search-type', 'ALL',
    # #                  '--attachment-match', '*.txt',
    # #                  '--outfile', TU.stdout)
    # #         self.assertTrue(r == 0)
    # #         encoding = get_file_encoding(TU.stdout)
    # #         with open(TU.stdout, encoding=encoding) as ifp:
    # #             rs = ifp.read()
    # #             print(rs)
    # #             self.assertTrue(rs == '1')
    # #     except Exception as e:
    # #         sys.stderr.write('\n%s\n' % str(e))
    # #         self.assertTrue(True)
    #
    # # ==========================================================================
    # def test0390_valid_send_attach_txt(self):
    #     try:
    #         TU.subject = 'txt 첨부테스트'
    #         TU.body = 'Hello world? 이것은 테스트임!!!\nsecond line'
    #         r = main_send(*TU.ARGS['gmail'], TU.subject,
    #                       '--to', 'Jerry HM<jerrychae@outlook.com>',
    #                       '--body-text', TU.body,
    #                       '--body-file', 'body.html',
    #                       '--body-type', 'html',
    #                       '--attachments', 'attach.txt',
    #                       )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0400_valid_read_attachment_txt(self):
    #     # sf = '%s%stest_save_folder' % (gettempdir(), os.path.sep)
    #     sf = os.path.join(os.path.dirname(__file__), 'sf')
    #     try:
    #         time.sleep(5)
    #         if os.path.exists(sf):
    #             shutil.rmtree(sf)
    #         os.makedirs(sf)
    #         r = main('read', *TU.ARGS['outlook'],
    #                  '--save-folder', sf,
    #                  '--attachment-match', '*.txt',
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for i, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) > 1)
    #         attachments = rr[1][7].split(',')
    #         for attachment in attachments:
    #             if attachment.endswith('.txt'):
    #                 self.assertTrue(os.path.getsize(attachment) ==
    #                                 os.path.getsize('attach.txt'))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(sf):
    #             shutil.rmtree(sf)

    # # ==========================================================================
    # def test0410_valid_read_vvmail(self):
    #     try:
    #         r = main('read', *TU.ARGS['vivans'],
    #                  '--outfile', TU.stdout)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         encoding = get_file_encoding(TU.stdout)
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             print(ifp.read())
    #         with open(TU.stdout, encoding=encoding) as ifp:
    #             cr = csv.reader(ifp)
    #             for i, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (9,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) > 1)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         ...

    # ==========================================================================
    def test9999_quit(self):
        for ed in glob.glob('%s%semail_save*' % (gettempdir(), os.path.sep)):
            shutil.rmtree(ed)
        self.assertTrue(True)
