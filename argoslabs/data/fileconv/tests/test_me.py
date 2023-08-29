"""
====================================
 :mod:`argoslabs.data.fileconv.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
#  * [2021/04/01]
#     - 그룹에 "6-Files and Folders" 넣음
#  * [2021/01/20]
#     - xrld 버전을 1.2.0 으로 고정해야 했음
#  * [2020/07/27]
#     - xlsx2csv, xlsx2xls 기능 추가 (장소장님 요청; 남동발전소)
#  * [2020/03/25]
#     - xls2csv 기능 추가 (한솔씨 요청)
#  * [2020/03/07]
#     - xls2xlsx 기능 추가 (Shige 요청, SAP 관련 작업에서 필요)
#     - display_name: "Data Conv" => "File Conv"
#     - stdout 에는 target 파일명 출력 (Shige 요청)
#  * [2019/12/18]
#     - csv2_sv 에서 "delimiter" must be a 1-character string 오류 수정
#  * [2019/09/16]
#     - check error of same src and target is not allowed
#  * [2019/06/03]
#     - add get_file_encoding for detect encoding
#  * [2019/05/10]
#     - add json2xml, xml2json
#  * [2019/05/02]
#     - starting


################################################################################
import os
import sys
import csv
import json
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from tempfile import gettempdir
# noinspection PyProtectedMember
from argoslabs.data.fileconv import _main as main
from alabs.common.util.vvencoding import get_file_encoding


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True
    src = os.path.join(gettempdir(), 'argoslabs.data.csv2tsv.csv')
    target = os.path.join(gettempdir(), 'argoslabs.data.csv2tsv.tsv')

    # ==========================================================================
    def test0000_init(self):
        if os.path.exists(TU.src):
            os.remove(TU.src)
        with open(TU.src, 'w') as ofp:
            ofp.write('''1, tom, 13
2, jerry, 16
3, "foo, foo", 23''')
        self.assertTrue(os.path.exists(TU.src))
        if os.path.exists(TU.target):
            os.remove(TU.target)
        self.assertTrue(not os.path.exists(TU.target))

    # ==========================================================================
    def test0100_invalid_operation(self):
        try:
            _ = main('invalid', 'tom', 'jerry')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_csv2tsv(self):
        try:
            r = main('csv2tsv', TU.src, TU.target)
            self.assertTrue(r == 0)
            with open(TU.target) as ifp:
                t = ifp.read()
            self.assertTrue(t == '1{cs}tom{cs}13\n2{cs}jerry{cs}16\n3{cs}foo, foo{cs}23\n'.format(cs='\t'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0114_csv2tsv_same_src_tgt(self):
        try:
            r = main('csv2tsv', TU.src, TU.src)
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_csv2tsv_without_target_sep(self):
        try:
            _ = main('csv2_sv', TU.src, TU.target)
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0130_csv2_sv(self):
        try:
            r = main('csv2_sv', TU.src, TU.target, '--target-sep', '|')
            self.assertTrue(r == 0)
            with open(TU.target) as ifp:
                t = ifp.read()
            self.assertTrue(t == '1{cs}tom{cs}13\n2{cs}jerry{cs}16\n3{cs}foo, foo{cs}23\n'.format(cs='|'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_xml2json(self):
        src = os.path.join(os.path.dirname(__file__), 'foo.xml')
        src2 = os.path.join(os.path.dirname(__file__), 'foo.json')
        target = os.path.join(gettempdir(), 'foo.json')
        try:
            r = main('xml2json', src, target)
            self.assertTrue(r == 0)
            with open(target) as ifp:
                t = ifp.read()
            print(t)
            with open(target, encoding=get_file_encoding(target)) as ifp:
                jd_t = json.load(ifp)

            with open(src2, encoding=get_file_encoding(src2)) as ifp:
                jd_s = json.load(ifp)
            self.assertTrue(jd_t == jd_s)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(target):
                os.remove(target)

    # ==========================================================================
    def test0210_json2xml_xml2json(self):
        src = os.path.join(os.path.dirname(__file__), 'foo.json')
        target = os.path.join(gettempdir(), 'foo.xml')
        target2 = os.path.join(gettempdir(), 'bar2.json')
        try:
            r = main('json2xml', src, target)
            self.assertTrue(r == 0)
            with open(target) as ifp:
                t = ifp.read()
            print(t)
            r = main('xml2json', target, target2)
            self.assertTrue(r == 0)
            with open(target2) as ifp:
                t = ifp.read()
            print(t)
            with open(src, encoding=get_file_encoding(src)) as ifp:
                jd_src = json.load(ifp)
            with open(target2, encoding=get_file_encoding(target2)) as ifp:
                jd_t2 = json.load(ifp)
            self.assertTrue(jd_src == jd_t2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(target):
                os.remove(target)
            if os.path.exists(target2):
                os.remove(target2)

    # ==========================================================================
    def test0220_xml2json_kr(self):
        src = os.path.join(os.path.dirname(__file__), 'foo_kr.xml')
        src2 = os.path.join(os.path.dirname(__file__), 'bar_kr.json')
        target = os.path.join(gettempdir(), 'foo.json')
        try:
            r = main('xml2json', src, target)
            self.assertTrue(r == 0)
            with open(target) as ifp:
                t = ifp.read()
            print(t)
            with open(target, encoding=get_file_encoding(target)) as ifp:
                jd_t = json.load(ifp)

            with open(src2, encoding=get_file_encoding(src2)) as ifp:
                jd_s = json.load(ifp)
            self.assertTrue(jd_t == jd_s)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(target):
                os.remove(target)

    # ==========================================================================
    def test0230_json2xml_xml2json_kr(self):
        src = os.path.join(os.path.dirname(__file__), 'bar_kr.json')
        target = os.path.join(gettempdir(), 'bar_kr.xml')
        target2 = os.path.join(gettempdir(), 'bar2_kr.json')
        try:
            r = main('json2xml', src, target)
            self.assertTrue(r == 0)
            with open(target) as ifp:
                t = ifp.read()
            print(t)
            r = main('xml2json', target, target2)
            self.assertTrue(r == 0)
            with open(target2) as ifp:
                t = ifp.read()
            print(t)
            with open(src, encoding=get_file_encoding(src)) as ifp:
                jd_src = json.load(ifp)
            with open(target2, encoding=get_file_encoding(target2)) as ifp:
                jd_t2 = json.load(ifp)
            self.assertTrue(jd_src == jd_t2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(target):
                os.remove(target)
            if os.path.exists(target2):
                os.remove(target2)

    # ==========================================================================
    def test0240_csv_tsv(self):
        stdout = 'stdout.txt'
        src = os.path.join(os.path.dirname(__file__), 'names demo 001.csv')
        target = os.path.join(gettempdir(), 'names demo 001._sv')
        try:
            r = main('csv2_sv', src, target,
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(target) as ifp:
                t = ifp.read()
            print(t)
            with open(stdout) as ifp:
                rs = ifp.read()
                self.assertTrue(rs == target)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(target):
                os.remove(target)
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0250_xls_xlsx(self):
        tdir = os.path.dirname(__file__)
        src = os.path.join(tdir, 'Commercial_Invoice_List.xls')
        target = os.path.join(tdir, 'Commercial_Invoice_List.xlsx')
        try:
            r = main('xls2xlsx', src, target)
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            # if os.path.exists(target):
            #     os.remove(target)
            ...

    # ==========================================================================
    def test0260_xls_xlsx(self):
        tdir = os.path.dirname(__file__)
        src = os.path.join(tdir, 'Attachment 2 3rd Party Summary-current.xls')
        target = os.path.join(tdir, 'Attachment 2 3rd Party Summary-current.xlsx')
        try:
            r = main('xls2xlsx', src, target)
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            # if os.path.exists(target):
            #     os.remove(target)
            ...

    # ==========================================================================
    def test0270_xls_csv(self):
        tdir = os.path.dirname(__file__)
        src = os.path.join(tdir, 'kairoslab.xls')
        target = os.path.join(tdir, 'kairoslab.csv')
        try:
            r = main('xls2csv', src, target)
            self.assertTrue(r == 0)
            rr = []
            with open(target, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (55,))
                    rr.append(row)
            self.assertTrue(len(rr) in (8,))

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            # if os.path.exists(target):
            #     os.remove(target)
            ...

    # ==========================================================================
    def test0280_xlsx_xls(self):
        tdir = os.path.dirname(__file__)
        src = os.path.join(tdir, 'Commercial_Invoice_List.xlsx')
        target = os.path.join(tdir, 'foobar.xls')
        try:
            r = main('xlsx2xls', src, target)
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            # if os.path.exists(target):
            #     os.remove(target)
            ...

    # ==========================================================================
    # def test0290_xlsx_xls_conditional_formatting(self):
    #     tdir = os.path.dirname(__file__)
    #     src = os.path.join(tdir, 'excel Simple write test.xlsx')
    #     target = os.path.join(tdir, 'excel Simple write test.xls')
    #     try:
    #         r = main('xlsx2xls', src, target,
    #                  '--conditional-formatting')
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         # if os.path.exists(target):
    #         #     os.remove(target)
    #         ...

    # ==========================================================================
    def test0290_xlsx_csv(self):
        tdir = os.path.dirname(__file__)
        src = os.path.join(tdir, 'Commercial_Invoice_List.xlsx')
        target = os.path.join(tdir, 'foobar.csv')
        try:
            r = main('xlsx2csv', src, target)
            self.assertTrue(r == 0)
            rr = []
            with open(target, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (10,))
                    rr.append(row)
            self.assertTrue(len(rr) in (20,))

            src = os.path.join(tdir, 'foobar.xls')
            target = os.path.join(tdir, 'foobar2.csv')
            r = main('xls2csv', src, target)
            self.assertTrue(r == 0)
            rr = []
            with open(target, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (10,))
                    rr.append(row)
            self.assertTrue(len(rr) in (20,))

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            # if os.path.exists(target):
            #     os.remove(target)
            ...

    # ==========================================================================
    def test0300_xlsx_csv(self):
        tdir = os.path.dirname(__file__)
        src = os.path.join(tdir, 'issue', 'sql-test01.xlsx')
        target = os.path.join(tdir, 'issue', 'sql-test01.csv')
        try:
            r = main('xlsx2csv', src, target)
            self.assertTrue(r == 0)
            rr = []
            with open(target, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (38,))
                    rr.append(row)
            self.assertTrue(len(rr) in (2,))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            # if os.path.exists(target):
            #     os.remove(target)
            ...

    # ==========================================================================
    def test9999_quit(self):
        if os.path.exists(TU.src):
            os.remove(TU.src)
        self.assertTrue(not os.path.exists(TU.src))
        if os.path.exists(TU.target):
            os.remove(TU.target)
        self.assertTrue(not os.path.exists(TU.target))
