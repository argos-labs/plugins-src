"""
====================================
 :mod:`argoslabs.data.json.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
#
# Authors
# ===========
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/01]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2021/01/22]
#     - Irene, Venkatesh JSON 가져오는 것을 약간 수정
#       fields 라는 것 동일 반복 데이터를 가지고 있는 것 처리
#  * [2020/10/26]
#     - --encoding 옵션 추가
#  * [2019/12/10]
#     - 기존 성공이면 1을 리턴하는 대신 결과가 있으면 0, 없거나 실패하면 1 또는 2로 수정
#  * [2019/04/18]
#     - 일본어 등의 출력이 unicode로 되는 것을 utf8로 수정
#  * [2019/03/22]
#     - --rows, --cells, --cell-key 옵션 추가
#  * [2019/03/13]
#     - --errfile 용 수정 및 테스트 추가
#  * [2019/03/08]
#     - add icon
#  * [2019/03/07]
#     - starting, testing

################################################################################
import os
import sys
import csv
import json
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
from argoslabs.data.json import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    jsf = 'mytest.json'

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.assertTrue(True)

    # ==========================================================================
    def test0100_help(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('--help')
            self.assertTrue(False)
        except ArgsExit as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_dumpspec(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('--dumpspec', 'yaml')
            self.assertTrue(False)
        except ArgsExit as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0200_save_json(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            d = {
                "page": 1,
                "per_page": 3,
                "total": 12,
                "total_pages": 4,
                "pagedata": {
                    "data": [
                        {
                            "id": 1,
                            "name": "cerulean",
                            "year": 2000,
                            "color": "#98B2D1",
                            "pantone_value": "우리는"
                        },
                        {
                            "id": 2,
                            "name": "fuchsia rose",
                            "year": 2001,
                            "color": "#C74375",
                            "pantone_value": "자유"
                        },
                        {
                            "id": 3,
                            "name": "true red",
                            "year": 2002,
                            "color": "#BF1932",
                            "pantone_value": "영혼"
                        }
                    ]
                },
                'jpn': {
                    "data": {
                        "shippingDay": "2019-04-02",
                        "mansionName": "新宿ビル"
                    },
                    "status": 200
                }

            }
            with open(TU.jsf, 'w') as ofp:
                json.dump(d, ofp)
            self.assertTrue(d['total'] == 12)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_get_xpath_without_outfile(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(TU.jsf, 'total')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_get_xpath_with_outfile(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'foo.txt'
        try:
            r = main(TU.jsf, 'total', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                ofr = ifp.read().rstrip()
            self.assertTrue(ofr == '12')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0230_get_xpath_depth_two(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'foo.txt'
        try:
            r = main(TU.jsf, 'pagedata/data[2]/id', '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                ofr = ifp.read().rstrip()
            self.assertTrue(ofr == '3')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0240_get_xpath_invalid_key(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'foo.txt'
        try:
            r = main(TU.jsf, 'pagedata_invalid', '--outfile', of)
            self.assertTrue(r != 0)
            with open(of) as ifp:
                ofr = ifp.read().rstrip()
            self.assertTrue(not ofr)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0250_get_xpath_csv_out_success(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'foo.txt'
        try:
            r = main(TU.jsf, 'pagedata/data',
                     '--format', 'csv',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            rr = list()
            with open(of, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 5)
                    rr.append(row)
            self.assertTrue(len(rr) == 4 and rr[-1][-1] == '영혼')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0260_get_xpath_csv_out_failure(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'foo.txt'
        try:
            r = main(TU.jsf, 'pagedata',
                     '--format', 'csv',
                     '--outfile', of,
                     )
            self.assertTrue(r != 0)
            with open(of) as ifp:
                ofr = ifp.read().rstrip()
            self.assertTrue(not ofr)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0270_get_xpath_csv_out_failure_exception(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(TU.jsf, 'pagedata/invalid', '--raise-exception',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r != 0)
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(os.path.getsize(ef) > 0)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0300_get_330_csv(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', '330.pdf.json')
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(jf, '/fields',  '--format', 'csv',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            lr = []
            with open(of) as ifp:
                print(ifp.read())
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 9)
                    lr.append(row)
                self.assertTrue(len(lr) == 15)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0310_get_330_and_two(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', '330.pdf.json')
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(jf, '/fields',  '--format', 'csv',
                     '--and-filter', 'name=recipient_addrline',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            lr = []
            with open(of) as ifp:
                print(ifp.read())
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 9)
                    lr.append(row)
                self.assertTrue(len(lr) == 3)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0320_get_330_and_one(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', '330.pdf.json')
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(jf, '/fields',  '--format', 'csv',
                     '--and-filter', 'name=amount_due',
                     '--and-filter', 'value=2000.00',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            lr = []
            with open(of) as ifp:
                print(ifp.read())
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 9)
                    lr.append(row)
                self.assertTrue(len(lr) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0330_get_330_and_no(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', '330.pdf.json')
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(jf, '/fields',  '--format', 'csv',
                     '--and-filter', 'name=amount_due',
                     '--and-filter', 'value=999',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r != 0)
            lr = []
            with open(of) as ifp:
                print(ifp.read())
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 9)
                    lr.append(row)
                self.assertTrue(len(lr) == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0340_get_330_or_three(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', '330.pdf.json')
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(jf, '/fields',  '--format', 'csv',
                     '--or-filter', 'name=recipient_addrline',
                     '--or-filter', 'name=amount_due',
                     '--or-filter', 'name=date_due',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            lr = []
            with open(of) as ifp:
                print(ifp.read())
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 9)
                    lr.append(row)
                self.assertTrue(len(lr) == 4)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0350_get_097_or_two(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', 'INV-000097.pdf.json')
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(jf, '/fields',  '--format', 'csv',
                     '--or-filter', 'name=recipient_addrline',
                     '--or-filter', 'name=amount_due',
                     '--or-filter', 'name=date_due',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            lr = []
            with open(of) as ifp:
                print(ifp.read())
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 9)
                    lr.append(row)
                self.assertTrue(len(lr) == 3)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0360_get_table_300(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', '330.pdf.json')
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(jf, '/',
                     '--find-all', 'cells',
                     '--cell-key', 'content',
                     '--format', 'csv',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            lr = []
            with open(of, encoding='utf-8') as ifp:
                print(ifp.read())
            with open(of, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 4)
                    lr.append(row)
                self.assertTrue(len(lr) == 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0370_get_table_726346(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', 'Invoice_726346_1550562703686.pdf.json')
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(jf, '/',
                     '--find-all', 'cells',
                     '--cell-key', 'content',
                     '--format', 'csv',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            lr = []
            with open(of, encoding='utf-8') as ifp:
                print(ifp.read())
            with open(of, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (5, 6, 7))
                    lr.append(row)
                self.assertTrue(len(lr) == 34)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0380_get_table_726346_exclude(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', 'Invoice_726346_1550562703686.pdf.json')
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(jf, '/',
                     '--find-all', 'cells',
                     '--cell-key', 'content',
                     '--exclude-index', '1',
                     '--exclude-value', 'Item',
                     '--format', 'csv',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            lr = []
            with open(of, encoding='utf-8') as ifp:
                print(ifp.read())
            with open(of, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (5, 6, 7))
                    lr.append(row)
                self.assertTrue(len(lr) == 30)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0390_get_len_tables(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', 'Invoice_726346_1550562703686.pdf.json')
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(jf, 'tables',
                     '--len',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            with open(of, encoding='utf-8') as ifp:
                self.assertTrue(int(ifp.read()) == 4)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0400_get_first_table_726346_exclude(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', 'Invoice_726346_1550562703686.pdf.json')
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(jf, 'tables[0]',
                     '--find-all', 'cells',
                     '--cell-key', 'content',
                     '--format', 'csv',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            lr = []
            with open(of, encoding='utf-8') as ifp:
                print(ifp.read())
            with open(of, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 5)
                    lr.append(row)
                self.assertTrue(len(lr) == 5)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0410_get_second_table_726346_exclude(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', 'Invoice_726346_1550562703686.pdf.json')
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(jf, 'tables[1]',
                     '--find-all', 'cells',
                     '--cell-key', 'content',
                     '--format', 'csv',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            lr = []
            with open(of, encoding='utf-8') as ifp:
                print(ifp.read())
            with open(of, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 5)
                    lr.append(row)
                self.assertTrue(len(lr) == 9)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0420_get_jpn_data(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(TU.jsf, '/jpn/data/mansionName',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            with open(of, encoding='utf-8') as ifp:
                print(ifp.read())
            with open(of, encoding='utf-8') as ifp:
                d = ifp.read()
                self.assertTrue(d == '新宿ビル')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0430_get_user2(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', 'REST API-get-user2.json')
        of = 'foo.txt'
        ef = 'bar.txt'
        try:
            r = main(jf, '/data/email',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            with open(of, encoding='utf-8') as ifp:
                print(ifp.read())
            with open(of, encoding='utf-8') as ifp:
                d = ifp.read()
                self.assertTrue(d == 'janet.weaver@reqres.in')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    # def test0440_get_rooman_his(self):
    #     jf = os.path.join('json', '2020-09-01.json')
    #     of = 'out.txt'
    #     ef = 'err.txt'
    #     try:
    #         r = main(jf, '/',
    #                  '--outfile', of, '--errfile', ef)
    #         self.assertTrue(r == 0)
    #         with open(of, encoding='utf-8') as ifp:
    #             print(ifp.read())
    #         with open(of, encoding='utf-8') as ifp:
    #             d = ifp.read()
    #             self.assertTrue(d == 'janet.weaver@reqres.in')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)
    #         if os.path.exists(ef):
    #             os.remove(ef)

    # ==========================================================================
    def test0450_get_baemin(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', 'api-out.json')
        of = 'out450.txt'
        ef = 'err.txt'
        try:
            r = main(jf, '/data/shops',
                     '--find-all', 'shopName',
                     '--format', 'csv',
                     # '--encoding', '',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            with open(of, encoding='utf-8') as ifp:
                rstr = ifp.read()
                # print(rstr)
                self.assertTrue(rstr.find('명주') > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0460_get_baemin(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', 'test-restaurants.json')
        # jf = os.path.join('json', 'test3.json')
        of = 'out469.txt'
        ef = 'err.txt'
        try:
            r = main(jf, '/data/shops',
                     '--find-all', 'shopInfo',
                     '--format', 'csv',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            # with open(of, encoding='utf-8') as ifp:
            #     rstr = ifp.read()
            #     # print(rstr)
            #     self.assertTrue(rstr.find('불깐쇼새우') > 0)
            rr = list()
            with open(of, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 13)
                    rr.append(row)
            self.assertTrue(len(rr) == 13 and rr[-1][-1] == '짜장면, 짬뽕')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0470_irene_vankatesh(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', 'irene-apple.json')
        # jf = os.path.join('json', 'test3.json')
        of = 'out.txt'
        ef = 'err.txt'
        try:
            r = main(jf, '/documents_response',
                     '--find-all', 'field',
                     '--format', 'csv',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            rr = list()
            with open(of, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 4)
                    rr.append(row)
            self.assertTrue(len(rr) == 29)

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test0480_shige_debug(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        jf = os.path.join('json', '163081225(1)-apple(1).json')
        # jf = os.path.join('json', 'test3.json')
        of = 'out.txt'
        ef = 'err.txt'
        try:
            r = main(jf, 'documents_response/document/field_data',
                     '--find-all', 'field',
                     '--format', 'csv',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            rr = list()
            with open(of, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 4)
                    rr.append(row)
            self.assertTrue(len(rr) == 29)

            r = main(jf, 'documents_response/document/field_data/field',
                     '--format', 'csv',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            rr = list()
            with open(of, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 4)
                    rr.append(row)
            self.assertTrue(len(rr) == 13)

            r = main(jf, 'documents_response/document/field_data/field_set/row[2]/field',
                     '--format', 'csv',
                     '--outfile', of, '--errfile', ef)
            self.assertTrue(r == 0)
            rr = list()
            with open(of, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) == 4)
                    rr.append(row)
            self.assertTrue(len(rr) == 5)

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(ef):
                os.remove(ef)

    # ==========================================================================
    def test9999_quit(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        if os.path.exists(TU.jsf):
            os.remove(TU.jsf)
        self.assertTrue(True)
