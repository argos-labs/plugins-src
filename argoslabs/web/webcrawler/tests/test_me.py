"""
====================================
 :mod:`argoslabs.web.webcrawler.tests.test_me`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Kyobong An
#
# Change Log
# --------
#
#  * [2023/06/21]
#     - start

################################################################################
import os
import sys
import json
import requests
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.web.webcrawler import _main as main
from alabs.common.util.vvencoding import get_file_encoding


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    # cwd = os.getcwd()

    # # ==========================================================================
    # def test0000_save_txt(self):
    #     try:
    #         r = main('https://github.com/flet-dev/examples/blob/main/python/apps/todo/todo.py',
    #                  '--domain-name', 'https://github.com',
    #                  '--save-file', r'C:\plugins-src\argoslabs\web\webcrawler\tests\html.txt',
    #                  '--parser', 'html.parser')
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0001_save_html(self):
    #     try:
    #         r = main('https://github.com/flet-dev/examples/blob/main/python/apps/todo/todo.py',
    #                  '--domain-name', 'https://github.com',
    #                  '--save-file', r'C:\plugins-src\argoslabs\web\webcrawler\tests\html.html',
    #                  '--connection-attempt', 3
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0002_depth(self):
    #     try:
    #         r = main('https://www.bobaedream.co.kr/list?code=best',
    #                  '--domain-name', 'https://www.bobaedream.co.kr',
    #                  '--depth-url', 'https://www.bobaedream.co.kr/view?code=best&No=',
    #                  '--depth', 5,
    #                  '--save-file', r'C:\plugins-src\argoslabs\web\webcrawler\tests\bobadream.html',
    #                  '--connection-attempt', 3
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0002_width(self):
    #     try:
    #         r = main('https://www.bobaedream.co.kr/list?code=best&s_cate=&maker_no=&model_no=&or_gu=10&or_se=desc&s_selday=&pagescale=30&info3=&noticeShow=&s_select=&s_key=&level_no=&bestCode=&bestDays=&bestbbs=&vdate=&type=list&page=1#',
    #                  '--domain-name', 'https://www.bobaedream.co.kr',
    #                  '--depth-url', 'https://www.bobaedream.co.kr/list?code=best&s_cate=&maker_no=&model_no=&or_gu=10&or_se=desc&s_selday=&pagescale=30&info3=&noticeShow=&s_select=&s_key=&level_no=&bestCode=&bestDays=&bestbbs=&vdate=&type=list&page=',
    #                  '--depth', 5,
    #                  '--width-url', 'https://www.bobaedream.co.kr/view?code=best&No=',
    #                  '--width', 5,
    #                  '--save-file', r'C:\plugins-src\argoslabs\web\webcrawler\tests\boba.html',
    #                  '--connection-attempt', 4
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0002_width(self):
    #     try:
    #         r = main('https://wiki.argos-labs.com/display/RPARELNOTE/YouTube+Operation#YoutubeOperation-4.305.1730',
    #                  '--domain-name', 'https://wiki.argos-labs.com',
    #                  # '--depth-url', 'https://www.bobaedream.co.kr/list?code=best&s_cate=&maker_no=&model_no=&or_gu=10&or_se=desc&s_selday=&pagescale=30&info3=&noticeShow=&s_select=&s_key=&level_no=&bestCode=&bestDays=&bestbbs=&vdate=&type=list&page=',
    #                  # '--depth', 5,
    #                  '--width-url', 'https://wiki.argos-labs.com/display/RPARELNOTE/Dialog',
    #                  '--width', 5,
    #                  '--save-file', r'C:\Users\argos\Desktop\bongsplugin\plug-in-test\web crawler\test\wiki-dialog.text',
    #                  '--connection-attempt', 4
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
