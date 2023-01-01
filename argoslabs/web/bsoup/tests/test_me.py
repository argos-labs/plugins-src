#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.web.bsoup`
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
#  * [2021/07/31]
#     - Change group "9: Utility Tools" => "10: Web Scraping"
#  * [2021/06/22]
#     - ClaimTech 규칙 테스트
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/05/26]
#     - find op에 name에서 td[3]과 같이 인덱스 추가 (1-based) for ASJ-480
#  * [2019/09/30]
#     - table > tbody > ... 등에서 tbody 넣거나 빼고 검색하도록 함
#  * [2019/05/31]
#     - --encoding 옵션 삭제(?) html 인코딩 상관없이 동작하도록
#  * [2019/05/22]
#     - --limit 옵션 추가
#  * [2019/05/15]
#     - re-replace 추가
#  * [2019/05/11]
#     - starting

################################################################################
import os
import sys
import csv
# from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.web.bsoup import _main as main
from tempfile import gettempdir
from alabs.common.util.vvencoding import get_file_encoding


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def setup(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        self.assertTrue(os.path.exists('1.html'))

    # ==========================================================================
    def test0000_init(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        self.assertTrue(os.path.exists('1.html'))

    # ==========================================================================
    def test0100_fail_html(self):
        try:
            _ = main('invalid.html')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_fail_spec(self):
        try:
            _ = main('1.html', '--spec-file', 'invalid.inv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0200_success_1_html_ext_01(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.grainger.com/	"3M T966130C"	1.html	ext-01.yaml
            r = main('1.html', '--spec-file', 'ext_01.yaml', '--outfile', of)
            self.assertTrue(r != 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.find('There is no Result') >= 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # # ==========================================================================
    # def test0205_success_1_5_html_ext_01_5(self):
    #     os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
    #     of = '%s/stdout.txt' % gettempdir()
    #     try:
    #         r = main('1.5.html', '--spec-file', 'ext_01.yaml', '--outfile', of)
    #         self.assertTrue(r == 0)
    #         with open(of) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #         rows = list()
    #         with open(of) as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (3,))
    #                 rows.append(row)
    #         self.assertTrue(len(rows) == 2)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)

    # ==========================================================================
    def test0210_success_2_html_ext_01(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        self.assertTrue(os.path.exists('1.html'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.grainger.com/	"SKF 6203 2RSJEM"	2.html	ext-01.yaml
            r = main('2.html', '--spec-file', 'ext_01.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0212_success_2_1_html_ext_01(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('2-1.html', '--spec-file', 'ext_01.yaml',
                     # '--encoding', 'cp949',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0214_success_2_2_html_ext_01(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('2-2.html', '--spec-file', 'ext_01.yaml',
                     #'--encoding', 'cp949',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0220_success_3_html_ext_01(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        self.assertTrue(os.path.exists('1.html'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.grainger.com/	"Ansell 92-675"	3.html	ext-01.yaml
            r = main('3.html', '--spec-file', 'ext_01.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 5)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0224_success_3_j_html_ext_01(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('3-j.html', '--spec-file', 'ext_01.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 5)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0230_success_4_html_ext_01(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.grainger.com/	"Baldor EM3615T"	4.html	ext-01.yaml
            r = main('4.html', '--spec-file', 'ext_01.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0240_success_5_html_ext_01(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.grainger.com/	"Milwaukee 0234-6"	5.html	ext-01.yaml
            r = main('5.html', '--spec-file', 'ext_01.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0250_success_6_html_ext_02(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        self.assertTrue(os.path.exists('1.html'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.mscdirect.com/	"3M T966130C"	6.html	ext-02.yaml
            r = main('6.html', '--spec-file', 'ext_02.yaml', '--outfile', of)
            self.assertTrue(r != 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.find('No Result') >= 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # # ==========================================================================
    # def test0255_success_6_5_html_ext_02(self):
    #     of = '%s/stdout.txt' % gettempdir()
    #     try:
    #         r = main('6.5.html', '--spec-file', 'ext_02.yaml', '--outfile', of)
    #         self.assertTrue(r == 0)
    #         with open(of) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #         rows = list()
    #         with open(of) as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (3,))
    #                 rows.append(row)
    #         self.assertTrue(len(rows) == 2)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)
    #
    # ==========================================================================
    def test0260_success_7_html_ext_02(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        self.assertTrue(os.path.exists('1.html'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.mscdirect.com/	"SKF 6203 2RSJEM"	7.html	ext-02.yaml
            r = main('7.html', '--spec-file', 'ext_02.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0262_success_7_1_html_ext_02(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('7-1.html', '--spec-file', 'ext_02.yaml',
                     # '--encoding', 'cp949',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0270_success_8_html_ext_02(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.mscdirect.com/	"Ansell 92-675"	8.html	ext-02.yaml
            r = main('8.html', '--spec-file', 'ext_02.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 5)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0272_success_8_1_html_ext_02(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('8-1.html', '--spec-file', 'ext_02.yaml',
                     # '--encoding', 'cp949',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 5)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0274_success_8_j_html_ext_02(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('8-j.html', '--spec-file', 'ext_02.yaml',
                     # '--encoding', 'cp949',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 5)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0280_success_9_html_ext_02(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.mscdirect.com/	"Baldor EM3615T"	9.html	ext-02.yaml
            r = main('9.html', '--spec-file', 'ext_02.yaml', '--outfile', of)
            self.assertTrue(r != 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.find('No Result') >= 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0290_success_10_html_ext_02(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.mscdirect.com/	"Milwaukee 0234-6"	10.html	ext-02.yaml
            r = main('10.html', '--spec-file', 'ext_02.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0292_success_10_1_html_ext_02(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('10-1.html', '--spec-file', 'ext_02.yaml',
                     # '--encoding', 'cp949',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0300_success_11_html_ext_03(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.motionindustries.com/	"3M T966130C"	11.html	ext-03.yaml
            r = main('11.html', '--spec-file', 'ext_03.yaml', '--outfile', of)
            self.assertTrue(r != 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.find('No Result') >= 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0310_success_12_html_ext_03(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.motionindustries.com/	"SKF 6203 2RSJEM"	12.html	ext-03.yaml
            r = main('12.html', '--spec-file', 'ext_03.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0320_success_13_html_ext_03(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.motionindustries.com/	"Ansell 92-675"	13.html	ext-03.yaml
            r = main('13.html', '--spec-file', 'ext_03.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 5)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # # ==========================================================================
    # def test0324_success_13_j_html_ext_03(self):
    #     of = '%s/stdout.txt' % gettempdir()
    #     try:
    #         r = main('13-j.html', '--spec-file', 'ext_03.yaml', '--outfile', of)
    #         self.assertTrue(r == 0)
    #         with open(of) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #         rows = list()
    #         with open(of) as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (3,))
    #                 rows.append(row)
    #         self.assertTrue(len(rows) == 5)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)
    #
    # ==========================================================================
    def test0330_success_14_html_ext_03(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.motionindustries.com/	"Baldor EM3615T"	14.html	ext-03.yaml
            r = main('14.html', '--spec-file', 'ext_03.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 8)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0340_success_15_html_ext_03(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.motionindustries.com/	"Milwaukee 0234-6"	15.html	ext-03.yaml
            r = main('15.html', '--spec-file', 'ext_03.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 3)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0350_success_16_html_ext_04(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        self.assertTrue(os.path.exists('1.html'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.amazon.com/	"3M T966130C"	16.html	ext-04.yaml
            r = main('16.html', '--spec-file', 'ext_04.yaml', '--outfile', of)
            self.assertTrue(r != 0)
            with open(of, encoding='utf8') as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.find('No Result') >= 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0360_success_17_html_ext_04(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.amazon.com/	"SKF 6203 2RSJEM"	17.html	ext-04.yaml
            r = main('17.html', '--spec-file', 'ext_04.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 9)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0370_success_18_html_ext_04(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.amazon.com/	"Ansell 92-675"	18.html	ext-04.yaml
            r = main('18.html', '--spec-file', 'ext_04.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 23)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # # ==========================================================================
    # def test0374_success_18_j_html_ext_04(self):
    #     of = '%s/stdout.txt' % gettempdir()
    #     try:
    #         r = main('18-j.html', '--spec-file', 'ext_04.yaml', '--outfile', of)
    #         self.assertTrue(r == 0)
    #         with open(of) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #         rows = list()
    #         with open(of) as ifp:
    #             cr = csv.reader(ifp)
    #             for ndx, row in enumerate(cr):
    #                 self.assertTrue(len(row) in (3,))
    #                 rows.append(row)
    #         self.assertTrue(len(rows) == 23)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)
    #
    # ==========================================================================
    def test0380_success_19_html_ext_04(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.amazon.com/	"Baldor EM3615T"	19.html	ext-04.yaml
            r = main('19.html', '--spec-file', 'ext_04.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 28)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0383_success_19_html_ext_04_with_limit(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('19.html', '--spec-file', 'ext_04.yaml',
                     '--limit', '10',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 11)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0390_success_20_html_ext_04(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.amazon.com/	"Milwaukee 0234-6"	20.html	ext-04.yaml
            r = main('20.html', '--spec-file', 'ext_04-c.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 10)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0392_success_20_1_html_ext_04(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('20-1.html', '--spec-file', 'ext_04-c.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 12)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0394_success_20_4_html_ext_04(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('20-4.html', '--spec-file', 'ext_04-c.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 10)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0396_success_20_c_html_ext_04(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            # r = main('20-c.html', '--spec-file', 'ext_04.yaml', '--outfile', of)
            r = main('20-c.html', '--spec-file', 'ext_04-c.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 49)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0400_success_gnt(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        self.assertTrue(os.path.exists('1.html'))
        of = '%s/stdout.txt' % gettempdir()
        test_set = [
            ('gnt-1.html', 'ext_gnt_01.yaml', 2, 2),
            ('gnt-2.html', 'ext_gnt_01.yaml', 2, 2),
            ('gnt-3.html', 'ext_gnt_01.yaml', 2, 2),
            ('gnt-4.html', 'ext_gnt_01.yaml', 2, 2),
            ('gnt-1.html', 'ext_gnt_02.yaml', 1, 2),
            ('gnt-2.html', 'ext_gnt_02.yaml', 1, 2),
            ('gnt-3.html', 'ext_gnt_02.yaml', 1, 2),
            ('gnt-4.html', 'ext_gnt_02.yaml', 1, 2),
            ('gnt-1.html', 'ext_gnt_03.yaml', 3, 2),
            ('gnt-2.html', 'ext_gnt_03.yaml', 3, 2),
            ('gnt-3.html', 'ext_gnt_03.yaml', 3, 2),
            ('gnt-4.html', 'ext_gnt_03.yaml', 3, 2),
            ('gnt-1.html', 'ext_gnt_04.yaml', 2, 14),
            ('gnt-2.html', 'ext_gnt_04.yaml', 2, 6),
            ('gnt-3.html', 'ext_gnt_04.yaml', 2, 12),
            ('gnt-4.html', 'ext_gnt_04.yaml', 2, 12),
            ('gnt-1.html', 'ext_gnt_05.yaml', 2, 9),
            ('gnt-2.html', 'ext_gnt_05.yaml', 2, 9),
            ('gnt-3.html', 'ext_gnt_05.yaml', 2, 9),
            ('gnt-4.html', 'ext_gnt_05.yaml', 2, 9),
            ('gnt-1.html', 'ext_gnt_06.yaml', 6, 2),
            ('gnt-2.html', 'ext_gnt_06.yaml', 6, 2),
            ('gnt-3.html', 'ext_gnt_06.yaml', 6, 2),
            ('gnt-4.html', 'ext_gnt_06.yaml', 6, 2),
            ('gnt-1.html', 'ext_gnt_07.yaml', 6, 2),
            ('gnt-2.html', 'ext_gnt_07.yaml', 6, 2),
            ('gnt-3.html', 'ext_gnt_07.yaml', 6, 2),
            ('gnt-4.html', 'ext_gnt_07.yaml', 6, 2),
            ('gnt-1.html', 'ext_gnt_08.yaml', 1, 2),
            ('gnt-2.html', 'ext_gnt_08.yaml', 1, 2),
            ('gnt-3.html', 'ext_gnt_08.yaml', 1, 2),
            ('gnt-4.html', 'ext_gnt_08.yaml', 1, 2),
            ('gnt-1.html', 'ext_gnt_09.yaml', 5, 2),
            ('gnt-2.html', 'ext_gnt_09.yaml', 5, 2),
            ('gnt-3.html', 'ext_gnt_09.yaml', 5, 2),
            ('gnt-4.html', 'ext_gnt_09.yaml', 5, 2),
            ('gnt-1.html', 'ext_gnt_10.yaml', 2, 9),
            ('gnt-2.html', 'ext_gnt_10.yaml', 2, 9),
            ('gnt-3.html', 'ext_gnt_10.yaml', 2, 8),
            ('gnt-4.html', 'ext_gnt_10.yaml', 2, 9),
        ]
        for html_f, rule_f, n_cols, n_rows in test_set:
            try:
                r = main(html_f, '--spec-file', rule_f, '--outfile', of)
                self.assertTrue(r == 0)
                encoding = get_file_encoding(of)
                # with open(of, encoding=encoding) as ifp:
                #     rs = ifp.read()
                #     print(rs)
                rows = list()
                with open(of, encoding=encoding) as ifp:
                    cr = csv.reader(ifp)
                    for ndx, row in enumerate(cr):
                        self.assertTrue(len(row) in (n_cols,))
                        rows.append(row)
                if len(rows) != n_rows:
                    print('Error at HTML="%s", rule="%s"' % (html_f, rule_f))
                self.assertTrue(len(rows) == n_rows)
            except Exception as e:
                sys.stderr.write('\n%s\n' % str(e))
                self.assertTrue(False)
            finally:
                if os.path.exists(of):
                    os.remove(of)

    # ==========================================================================
    def test0410_success_20_(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('gnt-2.html', '--spec-file', 'ext_gnt_04.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            encoding = get_file_encoding(of)
            with open(of, encoding=encoding) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of, encoding=encoding) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (2,))
                    rows.append(row)
            self.assertTrue(len(rows) == 6)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0420_success_20_(self):
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('gnt-3.html', '--spec-file', 'ext_gnt_04.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            encoding = get_file_encoding(of)
            with open(of, encoding=encoding) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of, encoding=encoding) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (2,))
                    rows.append(row)
            self.assertTrue(len(rows) == 12)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0430_success_takeshi_home(self):
        # os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        # self.assertTrue(os.path.exists('1.html'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            r = main('takeshi-HOMES.html', '--spec-file', 'takeshi-HOMES.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            # encoding = get_file_encoding(of)
            encoding = 'utf-8'
            # comment out: CP949 CMD error
            # with open(of, encoding=encoding) as ifp:
            #     rs = ifp.read()
            #     print(rs)
            rows = list()
            with open(of, encoding=encoding) as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (2,))
                    rows.append(row)
            self.assertTrue(len(rows) == 21)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0440_success_msc_15938_ext_02(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        self.assertTrue(os.path.exists('1.html'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.mscdirect.com/	"15938"	msc_15938.html	ext-02.yaml
            r = main('msc_15938.html', '--spec-file', 'ext_02.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    # todo : 왜 2개짜리가 마지막에 나온는지..
                    self.assertTrue(len(row) in (3,2))
                    rows.append(row)
            self.assertTrue(len(rows) == 7)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0450_success_msc_8287T24_ext_02(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        self.assertTrue(os.path.exists('1.html'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.mscdirect.com/	"8287T24"	msc_15938.html	ext-02.yaml
            r = main('msc_8287T24.html', '--spec-file', 'ext_02.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0460_success_amazon_520(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        self.assertTrue(os.path.exists('1.html'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.amazon.com/	"520"	16.html	ext-04.yaml
            r = main('amazon-520.html', '--spec-file', 'ext_04.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            encoding = get_file_encoding(of)
            # with open(of, encoding=encoding) as ifp:
            #     rs = ifp.read()
            #     print(rs)
            rows = list()
            with open(of, encoding=encoding) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 50)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0470_success_pwm_pk_1_html_ext_01_john_01(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            # https://www.grainger.com/	"PWM_PK_1"	5.html	ext-01-john.yaml
            r = main('grainger_pwm_pk_1.html', '--spec-file', 'ext_01_john.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (4,))
                    rows.append(row)
            self.assertTrue(len(rows) == 19)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

        try:
            # https://www.grainger.com/	"Milwaukee 0234-6"	5.html	ext-01.yaml
            r = main('2.html', '--spec-file', 'ext_01_john.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (4,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

        try:
            # https://www.grainger.com/	"Milwaukee 0234-6"	5.html	ext-01.yaml
            r = main('2-1.html', '--spec-file', 'ext_01_john.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (4,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

        try:
            # https://www.grainger.com/	"Milwaukee 0234-6"	5.html	ext-01.yaml
            r = main('1.5.html', '--spec-file', 'ext_01_john.yaml', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            rows = list()
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (4,))
                    rows.append(row)
            self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

        '''//*[@id="quote-header-zenity_info"]
        //*[@id="quote-header-zenity_info"]'''

    # ==========================================================================
    # def test0480_success_yahoo_finance_01(self):
    #     os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
    #     of = '%s/stdout.txt' % gettempdir()
    #     try:
    #         yf_list = (
    #             'yahoo-finance-01.html', 'yahoo-finance-02.html'
    #         )
    #         for yf in yf_list:
    #             r = main(yf, '--spec-file', 'yahoo-finance.yaml', '--outfile', of)
    #             self.assertTrue(r == 0)
    #             with open(of) as ifp:
    #                 rs = ifp.read()
    #                 print(rs)
    #             rows = list()
    #             with open(of) as ifp:
    #                 cr = csv.reader(ifp)
    #                 for row in cr:
    #                     self.assertTrue(len(row) in (4,))
    #                     rows.append(row)
    #             self.assertTrue(len(rows) == 2)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)

    # ==========================================================================
    def test0490_uspto(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            yf_list = (
                'uspto-table-7.html',
            )
            for yf in yf_list:
                r = main(yf, '--spec-file', 'uspto-table.yaml', '--outfile', of)
                self.assertTrue(r == 0)
                with open(of) as ifp:
                    rs = ifp.read()
                    print(rs)
                rows = list()
                with open(of) as ifp:
                    cr = csv.reader(ifp)
                    for row in cr:
                        self.assertTrue(len(row) in (11,))
                        rows.append(row)
                self.assertTrue(len(rows) == 64)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0500_us_capital(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            yf_list = (
                'us-alabama.html', 'us-ohio.html', 'us-utah.html', 'us-southdakota.html',
            )
            for yf in yf_list:
                r = main(yf, '--spec-file', 'us-capital.yaml', '--outfile', of)
                self.assertTrue(r == 0)
                with open(of) as ifp:
                    rs = ifp.read()
                    print(rs)
                rows = list()
                with open(of) as ifp:
                    cr = csv.reader(ifp)
                    for row in cr:
                        self.assertTrue(len(row) in (4,))
                        rows.append(row)
                self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0510_asj_homes(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            yf_list = (
                ('asj-homes-01.html', 14),
                ('asj-homes-02.html', 19),
                ('asj-homes-03.html', 10),
            )
            for yf, r_cnt in yf_list:
                r = main(yf, '--spec-file', 'asj-homes.yaml', '--outfile', of)
                self.assertTrue(r == 0)
                # with open(of, encoding='utf-8') as ifp:
                #     rs = ifp.read()
                #     print(rs)
                rows = list()
                with open(of, encoding='utf-8') as ifp:
                    cr = csv.reader(ifp)
                    for row in cr:
                        self.assertTrue(len(row) in (4,))
                        rows.append(row)
                self.assertTrue(len(rows) == r_cnt + 1)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0520_ibm_stock(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            yf_list = (
                'ibm-stock.html',
            )
            for yf in yf_list:
                r = main(yf, '--spec-file', 'ibm-stock.yaml', '--outfile', of)
                self.assertTrue(r == 0)
                with open(of, encoding='utf-8') as ifp:
                    rs = ifp.read()
                    print(rs)
                rows = list()
                with open(of, encoding='utf-8') as ifp:
                    cr = csv.reader(ifp)
                    for row in cr:
                        self.assertTrue(len(row) in (8,))
                        rows.append(row)
                self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # # ==========================================================================
    # def test0530_ibm_stock_table(self):
    #     os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
    #     of = '%s/stdout.txt' % gettempdir()
    #     try:
    #         yf_list = (
    #             'ibm-stock.html',
    #         )
    #         for yf in yf_list:
    #             r = main(yf, '--spec-file', 'ibm-stock-table.yaml', '--outfile', of)
    #             self.assertTrue(r == 0)
    #             with open(of, encoding='utf-8') as ifp:
    #                 rs = ifp.read()
    #                 print(rs)
    #             rows = list()
    #             with open(of, encoding='utf-8') as ifp:
    #                 cr = csv.reader(ifp)
    #                 for row in cr:
    #                     self.assertTrue(len(row) in (8,))
    #                     rows.append(row)
    #             self.assertTrue(len(rows) == 2)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)

    # ==========================================================================
    def test0540_football_team(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            yf_list = (
                'football-team.html',
            )
            for yf in yf_list:
                r = main(yf, '--spec-file', 'football-team.yaml', '--outfile', of)
                self.assertTrue(r == 0)
                with open(of, encoding='utf-8') as ifp:
                    rs = ifp.read()
                    # print(rs)
                rows = list()
                with open(of, encoding='utf-8') as ifp:
                    cr = csv.reader(ifp)
                    for row in cr:
                        self.assertTrue(len(row) in (3,))
                        rows.append(row)
                self.assertTrue(len(rows) == 27)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0550_unisys_table(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'HTML'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            yf_list = (
                'Unisys-table-01.html',
            )
            for yf in yf_list:
                r = main(yf, '--spec-file', 'Unisys-table.yaml', '--outfile', of)
                self.assertTrue(r == 0)
                with open(of, encoding='utf-8') as ifp:
                    rs = ifp.read()
                    print(rs)
                rows = list()
                with open(of, encoding='utf-8') as ifp:
                    cr = csv.reader(ifp)
                    for row in cr:
                        self.assertTrue(len(row) in (6,))
                        rows.append(row)
                self.assertTrue(len(rows) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0560_asj_480(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'ASJ'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            yf_list = (
                'ASJ-480-11-1-2.html',
            )
            for yf in yf_list:
                r = main(yf, '--spec-file', 'ASJ-480-11-1-2.yaml', '--outfile', of)
                self.assertTrue(r == 0)
                with open(of, encoding='utf-8') as ifp:
                    rs = ifp.read()
                    # print(rs)
                rows = list()
                with open(of, encoding='utf-8') as ifp:
                    cr = csv.reader(ifp)
                    for row in cr:
                        self.assertTrue(len(row) in (8,))
                        rows.append(row)
                self.assertTrue(len(rows) == 21)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0570_corrigo(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'WORK01'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            gsr_list = (
                ('corrigo_2_body.html', 'corrigo.yaml'),
                ('corrigo_3_body.html', 'corrigo.yaml'),
                ('corrigo_4_body.html', 'corrigo.yaml'),
            )
            for html, yaml in gsr_list:
                r = main(html, '--spec-file', yaml,
                         '--outfile', of)
                self.assertTrue(r == 0)
                print(f'{"*" * 80}')
                with open(of, encoding='utf-8') as ifp:
                    rs = ifp.read()
                    print(rs)
                rows = list()
                with open(of, encoding='utf-8') as ifp:
                    cr = csv.reader(ifp)
                    for row in cr:
                        self.assertTrue(len(row) in (1,))
                        rows.append(row)
                self.assertTrue(len(rows) in (7, 8))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0580_corrigo(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'WORK01'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            gsr_list = (
                ('corrigo_5_body.html', 'corrigo2.yaml'),
            )
            for html, yaml in gsr_list:
                r = main(html, '--spec-file', yaml,
                         '--outfile', of)
                self.assertTrue(r == 0)
                print(f'{"*" * 80}')
                with open(of, encoding='utf-8') as ifp:
                    rs = ifp.read()
                    print(rs)
                rows = list()
                with open(of, encoding='utf-8') as ifp:
                    cr = csv.reader(ifp)
                    for row in cr:
                        self.assertTrue(len(row) in (3,))
                        rows.append(row)
                self.assertTrue(len(rows) in (2,))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # # ==========================================================================
    # def test0590_google_search(self):
    #     os.chdir(os.path.join(os.path.dirname(__file__), 'WORK01'))
    #     of = '%s/stdout.txt' % gettempdir()
    #     try:
    #         gsr_list = (
    #             # 'google-search-result-01.html',
    #             'google-search-result-02.html',
    #         )
    #         for gsr in gsr_list:
    #             r = main(gsr, '--spec-file', 'google-search-result.yaml',
    #                      '--outfile', of)
    #             self.assertTrue(r == 0)
    #             with open(of, encoding='utf-8') as ifp:
    #                 rs = ifp.read()
    #                 # print(rs)
    #             rows = list()
    #             with open(of, encoding='utf-8') as ifp:
    #                 cr = csv.reader(ifp)
    #                 for row in cr:
    #                     self.assertTrue(len(row) in (8,))
    #                     rows.append(row)
    #             self.assertTrue(len(rows) == 21)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)

    # todo: next testing fail
    # ==========================================================================
    # def test0600_EAR_search(self):
    #     os.chdir(os.path.join(os.path.dirname(__file__), 'WORK01'))
    #     of = '%s/stdout.txt' % gettempdir()
    #     try:
    #         work_list = (
    #             # 'google-search-result-01.html',
    #             ('EAR-01.html', 'EAR-01.yaml', 1, 8),
    #         )
    #         for html, yaml, num_cols, num_rows in work_list:
    #             r = main(html, '--spec-file', yaml,
    #                      '--outfile', of)
    #             self.assertTrue(r == 0)
    #             with open(of, encoding='utf-8') as ifp:
    #                 rs = ifp.read()
    #                 # print(rs)
    #             rows = list()
    #             with open(of, encoding='utf-8') as ifp:
    #                 cr = csv.reader(ifp)
    #                 for row in cr:
    #                     self.assertTrue(len(row) in (8,))
    #                     rows.append(row)
    #             self.assertTrue(len(rows) == 21)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)

    # ==========================================================================
    def test0610_EXAMPLE_search(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'EXAMPLE'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            work_list = (
                ('exam.html', 'ext-exam-01.yaml', 2, 4, '$126.99 EA'),
                ('exam.html', 'ext-exam-02.yaml', 2, 4, '$94.99'),
                ('exam.html', 'ext-exam-03.yaml', 2, 4, '$512.99'),
            )
            for html, yaml, num_cols, num_rows, last_val in work_list:
                r = main(html, '--spec-file', yaml,
                         '--outfile', of)
                self.assertTrue(r == 0)
                with open(of, encoding='utf-8') as ifp:
                    rs = ifp.read()
                    print(rs)
                rows = list()
                with open(of, encoding='utf-8') as ifp:
                    cr = csv.reader(ifp)
                    for row in cr:
                        self.assertTrue(len(row) == num_cols)
                        rows.append(row)
                self.assertTrue(len(rows) == num_rows and
                                rows[-1][-1] == last_val)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0620_EXAMPLE_ecfr(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'WORK01'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            work_list = (
                ('ecfr-sample.html', 'ecfr-sample.yaml', 3, 248, '2019'),
            )
            for html, yaml, num_cols, num_rows, last_val in work_list:
                r = main(html, '--spec-file', yaml,
                         '--outfile', of)
                self.assertTrue(r == 0)
                with open(of, encoding='utf-8') as ifp:
                    rs = ifp.read()
                    print(rs)
                rows = list()
                with open(of, encoding='utf-8') as ifp:
                    cr = csv.reader(ifp)
                    for row in cr:
                        self.assertTrue(len(row) == num_cols)
                        rows.append(row)
                self.assertTrue(len(rows) == num_rows and
                                rows[-1][-1] == last_val)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0630_premier_league_table(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'UK'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            work_list = (
                ('skysports-premier.html', 'skysports-premier.yaml', 10, 21, '-1'),
            )
            for html, yaml, num_cols, num_rows, last_val in work_list:
                r = main(html, '--spec-file', yaml,
                         '--outfile', of)
                self.assertTrue(r == 0)
                with open(of, encoding='utf-8') as ifp:
                    rs = ifp.read()
                    print(rs)
                rows = list()
                with open(of, encoding='utf-8') as ifp:
                    cr = csv.reader(ifp)
                    for row in cr:
                        self.assertTrue(len(row) == num_cols)
                        rows.append(row)
                self.assertTrue(len(rows) == num_rows and rows[-1][-1])
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0640_premier_league_table(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'ClaimTech'))
        of = '%s/stdout.txt' % gettempdir()
        try:
            work_list = (
                ('claimtech_results.html', 'ext-claimtech.yaml', 13, 2, 'm503sq'),
            )
            for html, yaml, num_cols, num_rows, last_val in work_list:
                r = main(html, '--spec-file', yaml,
                         '--outfile', of)
                self.assertTrue(r == 0)
                with open(of, encoding='utf-8') as ifp:
                    rs = ifp.read()
                    print(rs)
                rows = list()
                with open(of, encoding='utf-8') as ifp:
                    cr = csv.reader(ifp)
                    for row in cr:
                        self.assertTrue(len(row) == num_cols)
                        rows.append(row)
                self.assertTrue(len(rows) == num_rows and rows[-1][-1])
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
