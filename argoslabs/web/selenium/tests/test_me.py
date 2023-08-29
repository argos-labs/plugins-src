"""
====================================
 :mod:`argoslabs.web.selenium`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module to use Selenium
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
#  * [2020/12/20]
#     - get PySelenium class from alabs.selenium
#  * [2020/12/02]
#     - starting

################################################################################
import os
import sys
import csv
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.web.selenium import _main as main
from tempfile import gettempdir


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
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            _ = main('invalid.script')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test0110_success_naverstore(self):
    #     sg = sys.gettrace()
    #     if sg is None:  # Not in debug mode
    #         print('Skip testing at test/build time')
    #         return
    #     of = 'stdout.txt'
    #     try:
    #         r = main('Chrome',
    #                  'naverstore_test.py',
    #                  '--parameters', 'user_email::=kairoslab99@naver.com',
    #                  '--parameters', 'user_passwd::=momo369!',
    #                  '--parameters', r'target_folder::=V:\tmp\naverstore_out',
    #                  '--parameters', 'user_no::=USER_NO',
    #                  '--parameters', 'shop_id::=SHOP_ID',
    #                  '--parameters', 'product_no::=PRODUCT_NO',
    #                  '--outfile', of,
    #                  )
    #         self.assertTrue(r == 0)
    #         with open(of) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #         self.assertTrue(rs == r'V:\tmp\naverstore_out\sql.txt')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)
    #
    # # ==========================================================================
    # def test0120_success_gmarket(self):
    #     sg = sys.gettrace()
    #     if sg is None:  # Not in debug mode
    #         print('Skip testing at test/build time')
    #         return
    #     of = 'stdout.txt'
    #     try:
    #         r = main('Chrome',
    #                  'gmarket_test.py',
    #                  '--parameters', 'user_id::=inshowfac',
    #                  '--parameters', 'user_passwd::=in05020502@',
    #                  '--parameters', r'target_folder::=V:\tmp\GMarket\out_inshowfac',
    #                  # '--parameters', 'user_no::=USER_NO',
    #                  # '--parameters', 'shop_id::=SHOP_ID',
    #                  # '--parameters', 'product_no::=PRODUCT_NO',
    #                  '--outfile', of,
    #                  )
    #         self.assertTrue(r == 0)
    #         with open(of) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #         # self.assertTrue(rs == r'V:\tmp\GMarket\out_inshowfac\sql.txt')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)
    #
    # # ==========================================================================
    # def test0130_success_interpark(self):
    #     sg = sys.gettrace()
    #     if sg is None:  # Not in debug mode
    #         print('Skip testing at test/build time')
    #         return
    #     of = 'stdout.txt'
    #     try:
    #         r = main('Chrome',
    #                  'interpark_test.py',
    #                  '--parameters', 'user_id::=blueskai',
    #                  '--parameters', 'user_passwd::=viva2020@',
    #                  '--parameters', r'target_folder::=V:\tmp\InterPark\out_blueskai',
    #                  # '--parameters', 'user_no::=USER_NO',
    #                  # '--parameters', 'shop_id::=SHOP_ID',
    #                  # '--parameters', 'product_no::=PRODUCT_NO',
    #                  '--outfile', of,
    #                  )
    #         self.assertTrue(r == 0)
    #         with open(of) as ifp:
    #             rs = ifp.read()
    #             print(rs)
    #         # self.assertTrue(rs == r'V:\tmp\GMarket\out_inshowfac\sql.txt')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)

    # ==========================================================================
    def test0200_success_sample_01(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            r = main('Chrome',
                     'ss_sample_01.py',
                     '--parameters', 'name::=blueskai',
                     '--parameters', 'dob::=1999-11-22',
                     '--parameters', r'birth_place::=Tokyo, Japan',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            # self.assertTrue(rs == r'V:\tmp\GMarket\out_inshowfac\sql.txt')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0205_failure_sample_01(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        ef = 'stderr.txt'
        try:
            r = main('Chrome',
                     'ss_sample_01.py',
                     '--parameters', 'name::=blueskai',
                     # '--parameters', 'dob::=1999-11-22',
                     # '--parameters', r'birth_place::=Tokyo, Japan',
                     '--outfile', of,
                     '--errfile', ef,
                     )
            self.assertTrue(r != 0)
            with open(ef) as efp:
                rs = efp.read()
                #print(rs)
                self.assertTrue(rs.rstrip() == 'Invalid "name", "dob" or "birth_place" parameters')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0210_success_headless_yahoo_finance_top_most(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            r = main('Chrome',
                     'yahoo-finance-most-active.py',
                     # '--headless',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            rr = []
            with open(of) as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (10,))
                    rr.append(row)
                self.assertTrue(len(rr) == 26)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
