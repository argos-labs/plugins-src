"""
====================================
 :mod:`argoslabs.web.scrapy`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module web bsoup using BeautifulSoup
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/07/31]
#     - Change group "9: Utility Tools" => "10: Web Scraping"
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/10/09]
#     - add --parameters
#  * [2020/10/07]
#     - starting

################################################################################
import os
import sys
import csv
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.web.scrapy import _main as main
from tempfile import gettempdir
# from alabs.common.util.vvencoding import get_file_encoding


################################################################################
class TU(TestCase):
    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        ...

    # ==========================================================================
    def test0010_fail_empty(self):
        try:
            _ = main('invalid.script')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_fail_script(self):
        try:
            r = main('invalid.script')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0030_fail_url(self):
        try:
            r = main('myspider.py')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # scrapy 특성 상 동일 Process 내에서 여러 번 start 할 경우,
    #   ReactorNotRestartable 오류 발생, STU에서 매번 별도 프로세스로 돌리면 이상 없음
    # ==========================================================================
    # def test0100_success_1(self):
    #     of = 'stdout.txt'
    #     try:
    #         r = main('myspider.py',
    #                  '--urls', 'https://finance.yahoo.com/most-active',
    #                  '--outfile', of
    #                  )
    #         self.assertTrue(r == 0)
    #         with open(of) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #         rows = list()
    #         with open(of) as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (9,))
    #                 rows.append(row)
    #         self.assertTrue(len(rows) == 26)
    #
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)

    # ==========================================================================
    def test0110_success_with_parameters(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            r = main('myspider2.py',
                     '--urls', 'https://finance.yahoo.com/{urlparam}',
                     '--parameters', 'symbol::=symbol_h',
                     '--parameters', 'name::=name_h',
                     '--parameters', 'urlparam::=most-active',
                     '--outfile', of
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (9,))
                    rows.append(row)
            self.assertTrue(len(rows) == 26)

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
