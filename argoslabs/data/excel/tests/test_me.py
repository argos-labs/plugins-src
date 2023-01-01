"""
====================================
 :mod:`argoslabs.data.excel`
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
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/06/17]
#     - Data-Only로 읽어오는데 문제 디버깅 [by Shige]
#  * [2021/05/26]
#     - A{{rp.index}} 에 repeat를 돌면서 CSV에 넣는데 무조건 덮어 씀
#  * [2021/03/29]
#     - 그룹에 "2-Business Apps" 넣음
#  * [2021/01/14]
#     - --keep-blank의 표시이름 "Keep Ext Blanks" => "Keep Blanks"
#  * [2020/10/12]
#     - test0680_debug_TS_all4home 영준 팀장이 하는데 30초 이상 걸리는 문제
#  * [2020/08/19]
#     - 만약 특정 파일명으로 출력하도록 되어 있는 경우, 출력을 이 파일명으로 지정
#     - --overwrite 옵션 추가하여 --data-only 여도 덮어쓰도록 함
#  * [2020/08/14]
#     - --set-cell, --set-value 이고 --data-only 인 경우 "파일명 (n).xlsx" 적용
#  * [2020/08/13]
#     - 다시 --with-formula 대신 --data-only 넣음
#     - 만약 --data-only 이고 출력을 동일 파일로 할 경우 저장된 formula가
#     -   모두 사라질 수 있으므로 "파일명 (n).xlsx" 식으로 변경
#  * [2020/08/05]
#     - add --with-formula instead of --data-only
#  * [2020/03/19]
#     - Change order of parameters
#  * [2020/02/02]
#     - add --encoding
#  * [2019/12/18]
#     - csv를 --big 으로 읽고 나중에 close, remove tempfile에 예외 발생 너머감
#     - --big인 경우, 100개만 처리하는 것 막고 모든 레코드 출력
#  * [2019/11/20]
#     - add new --find-string and --find-partial
#  * [2019/11/13]
#     - suppress warning which cause error from PAM
#  * [2019/08/19]
#     - "Copy of Bot Queue Demo.xlsx" 과 같이 헤더 또는 내용에 ,,,,,,, 가 포함되는 것을
#       제외 시킴
#     - --keep-blank 가 설정되어 있으면 위의 규칙을 안 따름
#     - add --set-cell, --set-value 로 입력 엑셀에 특정 셀 값 설정
#  * [2019/09/10]
#     - 결과의 앞뒤로 strip() 시켜서 출력
#  * [2019/07/19]
#     - add --dimensions
#  * [2019/07/18]
#     - add --clear-cell option
#  * [2019/04/25]
#     - set argument's displayname
#  * [2019/04/17]
#     - add csv read
#  * [2019/03/15]
#     - lineterminator='\n' # in windows twice newline
#  * [2018/11/28]
#     - starting
#

################################################################################
import os
import sys
import csv
import glob
import shutil
from tempfile import gettempdir
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.data.excel import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    @staticmethod
    def _get_safe_next_filename(fn):
        fn, ext = os.path.splitext(fn)
        for n in range(1, 1000000):
            nfn = f'{fn} ({n})' + ext
            if not os.path.exists(nfn):
                return nfn

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        self.xlf = 'sample.xlsx'
        self.csv = 'foo.csv'
        self.wxl = os.path.join(gettempdir(), 'foo.xlsx')
        self.wcsv = os.path.join(gettempdir(), 'foo.csv')
        self.out = 'stdout.txt'
        self.err = 'stderr.txt'

    # ==========================================================================
    def test0000_init(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        tf = os.path.join(gettempdir(), self.xlf)
        if os.path.exists(tf):
            os.remove(tf)
        shutil.copy(self.xlf, tf)
        for foo_f in glob.glob(os.path.join(gettempdir(), 'foo*.*')):
            os.remove(foo_f)
        self.__class__.xlf = tf
        self.assertTrue(os.path.exists(self.xlf))

    # ==========================================================================
    def test0100_failure_empty(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_list_sheet(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.xlf, '--list-sheet')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_list_sheet(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.xlf, '--list-sheet',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                r = ifp.read().rstrip()
                self.assertTrue(r == 'hanbin,Sheet1')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_cannot_read(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            _ = main('not-existed.xlsx', '--list-sheet',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            with open(self.err) as ifp:
                r = ifp.read().rstrip()
                self.assertTrue(r == 'Cannot read excel file "not-existed.xlsx"')

    # comment out : for CP949 build.bat Error
    # # ==========================================================================
    # def test0200_read_all(self):
    #     try:
    #         r = main(self.xlf, '--sheet', 'hanbin',
    #                  '--errfile', self.err)
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0210_read_all(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.xlf, '--sheet', 'hanbin',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(len(rr) in (52,))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_read_range(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.xlf, '--sheet', 'hanbin',
                     '--range', 'A4:C13',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(len(rr) == 10
                            and int(rr[0][-1]) == 2157630
                            and int(rr[-1][-1]) == 295388)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0230_read_range_big(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.xlf, '--sheet', 'hanbin',
                     '--range', 'A4:C13',
                     '--big',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(len(rr) == 10
                            and int(rr[0][-1]) == 2157630
                            and int(rr[-1][-1]) == 295388)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0240_read_range_big_reverse(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            _ = main(self.xlf, '--sheet', 'hanbin',
                     '--range', 'A4:C13',
                     '--big', '--reverse',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0250_read_range_reverse(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.xlf, '--sheet', 'hanbin',
                     '--range', 'A4:C13',
                     '--reverse',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (10,))
                    rr.append(row)
            self.assertTrue(len(rr) == 3
                            and int(rr[-1][0]) == 2157630
                            and int(rr[-1][-1]) == 295388)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0260_formula(self):
    #     # TODO: formula를 설정하는 것을 테스트 하는데,
    #     #     openpyxl 을 이용하여 formula를 설정하는 것은 가능하지만
    #     #     엑셀에서 다시 열어서 저장해야만 해당 값이 별도로 반영되는 문제
    #     #     formulas 등등의 모듈을 확인해 봤는데도 문제 있었음. 해결 결과의
    #     #     formula를 가져오는 것은 가능
    #     try:
    #         r = main(self.xlf, '--sheet', 'hanbin',
    #                  '--formula', 'A54=SUM($A$4:$A$53)',
    #                  '--formula', 'C54=AVERAGE($C$4:$C$53)',
    #                  '--range', 'A54:C54',
    #                  '--outfile', self.out,
    #                  '--errfile', self.err)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         with open(self.out, 'r', encoding='utf8') as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (3,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) == 3
    #                         and int(rr[0][-1]) == 257454)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0270_formula(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.xlf, '--sheet', 'Sheet1',
                     '--range', 'G1:I70',
                     '--data-only',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(
                len(rr) == 70
                and int(rr[-1][0]) == 32450750
                and int(rr[-1][-1]) == 1731842000
            )
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0300_write_overwrite(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            # 복사해서 덮어쓰는지 확인
            if os.path.exists(self.wxl):
                os.remove(self.wxl)
            shutil.copy(self.xlf, self.wxl)
            wxl_n = self._get_safe_next_filename(self.wxl)

            r = main(self.xlf, '--sheet', 'Sheet1',
                     '--range', 'G1:I70',
                     '--write', self.wxl,
                     '--data-only',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out, 'r', encoding='utf8') as ifp:
                rstr = ifp.read()
                self.assertTrue(rstr == os.path.abspath(wxl_n))
            # rr = []
            # with open(self.out, 'r', encoding='utf8') as ifp:
            #     cr = csv.reader(ifp)
            #     for row in cr:
            #         self.assertTrue(len(row) in (3,))
            #         rr.append(row)
            # self.assertTrue(
            #     len(rr) == 70
            #     and int(rr[-1][0]) == 32450750
            #     and int(rr[-1][-1]) == 1731842000
            # )

            # 덮어쓴 엑셀 읽어 확인
            # 이전에 --data-only 때문에 파일명 (n).xlsx 형식으로 씀
            # r = main(self.wxl, '--sheet', 'Sheet1',
            r = main(wxl_n, '--sheet', 'Sheet1',
                     '--range', 'A1:C70',
                     '--data-only',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(
                len(rr) == 70
                and int(rr[-1][0]) == 32450750
                and int(rr[-1][-1]) == 1731842000
            )
            if os.path.exists(wxl_n):
                os.remove(wxl_n)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0310_write_overwrite_new_sheet(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            # 복사해서 덮어쓰는지 확인
            if os.path.exists(self.wxl):
                os.remove(self.wxl)
            shutil.copy(self.xlf, self.wxl)
            wxl_n = self._get_safe_next_filename(self.wxl)

            r = main(self.xlf, '--sheet', 'Sheet1',
                     '--range', 'G1:I70',
                     '--write', self.wxl,
                     '--write-sheet', 'Sheet2',
                     '--write-cell', 'C3',
                     '--data-only',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out, 'r', encoding='utf8') as ifp:
                self.assertTrue(ifp.read() == wxl_n)
            # rr = []
            # with open(self.out, 'r', encoding='utf8') as ifp:
            #     cr = csv.reader(ifp)
            #     for row in cr:
            #         self.assertTrue(len(row) in (3,))
            #         rr.append(row)
            # self.assertTrue(
            #     len(rr) == 70
            #     and int(rr[-1][0]) == 32450750
            #     and int(rr[-1][-1]) == 1731842000
            # )

            # 덮어쓴 엑셀 읽어 확인
            # 이전에 --data-only 때문에 파일명 (n).xlsx 형식으로 씀
            # r = main(self.wxl, '--sheet', 'Sheet2',
            r = main(wxl_n, '--sheet', 'Sheet2',
                     '--range', 'C3:E72',
                     '--data-only',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(
                len(rr) == 70
                and int(rr[-1][0]) == 32450750
                and int(rr[-1][-1]) == 1731842000
            )
            if os.path.exists(wxl_n):
                os.remove(wxl_n)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0320_write_overwrite_new_book(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            # 복사해서 덮어쓰는지 확인
            if os.path.exists(self.wxl):
                os.remove(self.wxl)

            r = main(self.xlf, '--sheet', 'Sheet1',
                     '--range', 'G1:I70',
                     '--write', self.wxl,
                     '--write-sheet', 'NewSheet',
                     '--write-cell', 'C3',
                     '--data-only',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out, 'r', encoding='utf8') as ifp:
                self.assertTrue(ifp.read() == self.wxl)
            # rr = []
            # with open(self.out, 'r', encoding='utf8') as ifp:
            #     cr = csv.reader(ifp)
            #     for row in cr:
            #         self.assertTrue(len(row) in (3,))
            #         rr.append(row)
            # self.assertTrue(
            #     len(rr) == 70
            #     and int(rr[-1][0]) == 32450750
            #     and int(rr[-1][-1]) == 1731842000
            # )

            # 덮어쓴 엑셀 읽어 확인
            r = main(self.wxl, '--sheet', 'NewSheet',
                     '--range', 'C3:E72',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(
                len(rr) == 70
                and int(rr[-1][0]) == 32450750
                and int(rr[-1][-1]) == 1731842000
            )
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0330_write_csv(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            # 복사해서 덮어쓰는지 확인
            if os.path.exists(self.wcsv):
                os.remove(self.wcsv)

            r = main(self.xlf, '--sheet', 'Sheet1',
                     '--range', 'G1:I70',
                     '--write', self.wcsv,
                     '--data-only',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out, 'r', encoding='utf8') as ifp:
                self.assertTrue(ifp.read() == self.wcsv)
            # rr = []
            # with open(self.out, 'r', encoding='utf8') as ifp:
            #     cr = csv.reader(ifp)
            #     for row in cr:
            #         self.assertTrue(len(row) in (3,))
            #         rr.append(row)
            # self.assertTrue(
            #     len(rr) == 70
            #     and int(rr[-1][0]) == 32450750
            #     and int(rr[-1][-1]) == 1731842000
            # )

            # CSV 읽어 확인
            rr = []
            with open(self.wcsv, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(
                len(rr) == 70
                and int(rr[-1][0]) == 32450750
                and int(rr[-1][-1]) == 1731842000
            )
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0410_read_all(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.csv,
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (10,))
                    rr.append(row)
            self.assertTrue(len(rr) == 300)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0420_read_range(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.csv,
                     '--range', 'F4:H13',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(len(rr) == 10
                            and rr[0][0] == 'H05' and rr[-1][0] == 'H19')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0423_read_one_cell(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.csv,
                     '--range', 'F4:F4',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out, 'r', encoding='utf8') as ifp:
                rs = ifp.read()
            self.assertTrue(rs == 'H05')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0430_write_overwrite_new_book(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            # 복사해서 덮어쓰는지 확인
            if os.path.exists(self.wxl):
                os.remove(self.wxl)

            r = main(self.csv,
                     '--range', 'F4:H13',
                     '--write', self.wxl,
                     '--write-sheet', 'NewSheet',
                     '--write-cell', 'C3',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out, 'r', encoding='utf8') as ifp:
                rstr = ifp.read()
                self.assertTrue(rstr == self.wxl)
            # rr = []
            # with open(self.out, 'r', encoding='utf8') as ifp:
            #     cr = csv.reader(ifp)
            #     for row in cr:
            #         self.assertTrue(len(row) in (3,))
            #         rr.append(row)
            # self.assertTrue(len(rr) == 10
            #                 and rr[0][0] == 'H05' and rr[-1][0] == 'H19')
            # self.assertTrue(os.path.exists(self.wxl))

            # 덮어쓴 엑셀 읽어 확인
            r = main(self.wxl, '--sheet', 'NewSheet',
                     '--range', 'C3:E8',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            # self.assertTrue(len(rr) == 6
            #                 and rr[0][0] == 'H05' and rr[-1][0] == 'H11')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0440_write_csv(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            # 복사해서 덮어쓰는지 확인
            if os.path.exists(self.wcsv):
                os.remove(self.wcsv)

            r = main(self.csv,
                     '--range', 'F4:H13',
                     '--write', self.wcsv,
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out, 'r', encoding='utf8') as ifp:
                self.assertTrue(ifp.read() == self.wcsv)
            # rr = []
            # with open(self.out, 'r', encoding='utf8') as ifp:
            #     cr = csv.reader(ifp)
            #     for row in cr:
            #         self.assertTrue(len(row) in (3,))
            #         rr.append(row)
            # self.assertTrue(len(rr) == 10
            #                 and rr[0][0] == 'H05' and rr[-1][0] == 'H19')

            # CSV 읽어 확인
            rr = []
            with open(self.wcsv, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            # self.assertTrue(len(rr) == 10
            #                 and rr[0][0] == 'H05' and rr[-1][0] == 'H19')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0450_clear_sheet(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            # 복사해서 덮어쓰는지 확인
            shutil.copy(self.xlf, 'sample2.xlsx')
            r = main('sample2.xlsx',
                     '--sheet', 'hanbin',
                     '--clear-cell',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            # get dimensions
            r = main(self.xlf, '--dimensions',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                r = ifp.read().rstrip()
                self.assertTrue(r == 'A1:C53')
            # get dimensions
            r = main('sample2.xlsx', '--dimensions',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                r = ifp.read().rstrip()
                self.assertTrue(r == 'A1:A1')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0460_clear_csv(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            # 복사해서 덮어쓰는지 확인
            shutil.copy(self.csv, 'bar2.csv')
            r = main('bar2.csv',
                     '--clear-cell',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            # get dimensions
            r = main(self.csv, '--dimensions',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                r = ifp.read().rstrip()
                self.assertTrue(r == 'A1:J300')
            # get dimensions
            r = main('bar2.csv', '--dimensions',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                r = ifp.read().rstrip()
                self.assertTrue(r == 'A1:A1')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0470_clear_sheet_range(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            # 복사해서 덮어쓰는지 확인
            shutil.copy(self.xlf, 'sample3.xlsx')
            r = main('sample3.xlsx',
                     '--sheet', 'hanbin',
                     '--range', 'B6:C10',
                     '--clear-cell',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            # check results
            r = main('sample3.xlsx',
                     '--range', 'B6:C10',
                     '--write', self.wcsv,
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                # for row in cr:
                #     self.assertTrue(len(row) in (2,))
                #     self.assertFalse(any(row))
                #     rr.append(row)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0480_clear_sheet_range_csv(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            # 복사해서 덮어쓰는지 확인
            shutil.copy(self.csv, 'bar3.csv')
            r = main('bar3.csv',
                     '--range', 'B6:C10',
                     '--clear-cell',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            # check results
            r = main('bar3.csv',
                     '--range', 'B6:C10',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (2,))
                    self.assertFalse(any(row))
                    rr.append(row)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0490_sheet_tailing_empty_commas_csv(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('Copy of Bot Queue Demo.xlsx',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(len(rr) == 6)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0500_sheet_tailing_empty_commas_csv_keep_blank(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('Copy of Bot Queue Demo.xlsx',
                     '--keep-blank',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (21,))
                    rr.append(row)
            self.assertTrue(len(rr) == 13)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0510_sheet_set_cell(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('Copy of Bot Queue Demo.xlsx',
                     '--set-cell', 'B3',
                     '--set-value', '5274',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(len(rr) == 6)

            r = main('Copy of Bot Queue Demo.xlsx',
                     '--set-cell', 'B3',
                     # '--set-value', '',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(len(rr) == 6 and rr[2][1] == '5274')

            r = main('Copy of Bot Queue Demo.xlsx',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    rr.append(row)
            self.assertTrue(len(rr) == 6 and not rr[2][1])
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0520_slg_read(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('09-2019.xlsx',
                     '--sheet', 'Transactions Summary',
                     '--range', 'a1:f100',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (6,))
                    rr.append(row)
            self.assertTrue(len(rr) == 46)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0530_slg_find_exact(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('09-2019.xlsx',
                     '--sheet', 'Transactions Summary',
                     # '--range', 'a1:f100',
                     '--find-string', '15447358',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (1,))
                    rr.append(row)
            self.assertTrue(len(rr) == 2)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0540_slg_find_partial(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('09-2019.xlsx',
                     '--sheet', 'Transactions Summary',
                     # '--range', 'a1:f100',
                     '--find-string', '154',
                     '--find-partial',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (1,))
                    rr.append(row)
            self.assertTrue(len(rr) == 5)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0550_slg_find_partial(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('09-2019.xlsx',
                     '--sheet', 'Transactions Summary',
                     # '--range', 'a1:f100',
                     '--find-string', '786',
                     '--find-partial',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (1,))
                    rr.append(row)
            self.assertTrue(len(rr) == 2)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0570_asj_find_partial(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('find-1901.xlsx',
                     '--sheet', '日本',
                     # '--find-string', '株式会社オレガ',
                     '--find-string', 'しょーけ',
                     # r = main('sample.xlsx',
                     # '--sheet', 'Sheet1',
                     # '--find-string', '주변기기',
                     # '--find-partial',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (1,))
                    rr.append(row)
            self.assertTrue(len(rr) == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0580_csv_big(self):
    #     try:
    #         r = main('names demo 001.csv',
    #                  '--big',
    #                  '--outfile', self.out,
    #                  '--errfile', self.err,
    #                  )
    #         self.assertTrue(r == 0)
    #         with open(self.out) as ifp:
    #             print(ifp.read())
    #         rr = []
    #         with open(self.out, 'r', encoding='utf8') as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (7,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) == 351)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0590_csv_debug(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('newconnections.csv',
                     '--sheet', 'mysheet',
                     '--range', 'A1:F3000',
                     '--encoding', 'cp932',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            # with open(self.out, encoding='utf8') as ifp:
            #     print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (5,))
                    rr.append(row)
            self.assertTrue(len(rr) == 2401)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0600_csv_debug(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            # xlsx = 'foo_body.xlsx'
            # xlsx2 = 'foo_body2.xlsx'
            # xlsx3 = 'foo_body3.xlsx'
            # shutil.copy(xlsx,xlsx2)
            for i in range(1, 10, 3):
                r = main('foo_body.xlsx',
                         '--set-cell', f'm{i}',
                         '--set-value', f'= SUM($H${i}:$L${i})',
                         '--outfile', self.out,
                         '--errfile', self.err,
                         )
                self.assertTrue(r == 0)
                # with open(self.out, encoding='utf8') as ifp:
                #     print(ifp.read())
                print(f'testing... [{i}]')
                # time.sleep(1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0610_csv_debug_ASJ_492(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('data_sheet_01.xlsx',
                     '--sheet', 'calc',
                     '--range', 'I12:K12',
                     '--write', 'data_sheet_02.xlsx',
                     '--write-sheet', 'cp_sheet1',
                     '--write-cell', 'D1400',
                     '--keep-blank',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            # check results
            r = main('data_sheet_02.xlsx',
                     '--sheet', 'cp_sheet1',
                     '--range', 'D1400:F1400',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3, 2))
                    rr.append(row)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0620_write_overwrite_new_sheet(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            xls4 = "sample4.xlsx"
            if os.path.exists(xls4):
                os.remove(xls4)
            shutil.copy(self.xlf, xls4)
            r = main(xls4,
                     '--range', 'B4:C20',
                     '--write', xls4,
                     '--write-sheet', 'NewSheet',
                     '--write-cell', 'B2',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            self.assertTrue(xls4)
            # 덮어쓴 엑셀 읽어 확인
            r = main(xls4, '--sheet', 'NewSheet',
                     '--range', 'B2:C18',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (2,))
                    rr.append(row)
            self.assertTrue(len(rr) == 17 and rr[-1][-1] == '100100')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0630_write_overwrite_new_sheet_data_only(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        xls4_1 = "sample4 (1).xlsx"
        if os.path.exists(xls4_1):
            os.remove(xls4_1)
        try:
            xls4 = "sample4.xlsx"
            if os.path.exists(xls4):
                os.remove(xls4)
            shutil.copy(self.xlf, xls4)
            r = main(xls4,
                     '--range', 'B4:C20',
                     '--write', xls4,
                     '--write-sheet', 'NewSheet',
                     '--write-cell', 'B2',
                     '--data-only',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(xls4_1))
            # 덮어쓴 엑셀 읽어 확인
            r = main(xls4_1, '--sheet', 'NewSheet',
                     '--range', 'B2:C18',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (2,))
                    rr.append(row)
            self.assertTrue(len(rr) == 17 and rr[-1][-1] == '100100')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(xls4_1):
                os.remove(xls4_1)

    # ==========================================================================
    def test0640_write_overwrite_new_sheet_data_only_overwrite(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        xls4_1 = "sample4 (1).xlsx"
        if os.path.exists(xls4_1):
            os.remove(xls4_1)
        try:
            xls4 = "sample4.xlsx"
            if os.path.exists(xls4):
                os.remove(xls4)
            shutil.copy(self.xlf, xls4)
            r = main(xls4,
                     '--range', 'B4:C20',
                     '--write', xls4,
                     '--write-sheet', 'NewSheet',
                     '--write-cell', 'B2',
                     '--data-only',
                     '--overwrite',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(xls4) and not os.path.exists(xls4_1))
            # 덮어쓴 엑셀 읽어 확인
            r = main(xls4, '--sheet', 'NewSheet',
                     '--range', 'B2:C18',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (2,))
                    rr.append(row)
            self.assertTrue(len(rr) == 17 and rr[-1][-1] == '100100')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(xls4_1):
                os.remove(xls4_1)

    # ==========================================================================
    def test0650_sheet_set_cell_data_only(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        xls4_1 = "sample4 (1).xlsx"
        if os.path.exists(xls4_1):
            os.remove(xls4_1)
        try:
            xls4 = "sample4.xlsx"
            if os.path.exists(xls4):
                os.remove(xls4)
            shutil.copy(self.xlf, xls4)
            r = main(xls4,
                     '--set-cell', 'A1',
                     '--set-value', 'OK-OK',
                     '--data-only',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(xls4_1))
            r = main(xls4_1,
                     '--range', 'A1:A1',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                self.assertTrue(ifp.read() == 'OK-OK')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0660_sheet_set_cell_data_only_overwrite(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        xls4_1 = "sample4 (1).xlsx"
        if os.path.exists(xls4_1):
            os.remove(xls4_1)
        try:
            xls4 = "sample4.xlsx"
            if os.path.exists(xls4):
                os.remove(xls4)
            shutil.copy(self.xlf, xls4)
            r = main(xls4,
                     '--set-cell', 'A1',
                     '--set-value', 'OK-OK',
                     '--data-only',
                     '--overwrite',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(xls4) and not os.path.exists(xls4_1))
            r = main(xls4,
                     '--range', 'A1:A1',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                self.assertTrue(ifp.read() == 'OK-OK')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0670_debug_TS(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            xls = "killprocess.xlsx"
            r = main(xls,
                     '--sheet', 'Sheet1',
                     '--range', 'A1:A1',
                     # '--range', 'A1',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out, 'r', encoding='utf8') as ifp:
                rs = ifp.read()
                # print(rs)
                self.assertTrue(rs == 'chromedriver;chrome;EXCEL;')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0680_debug_TS_all4home(self):
    #     try:
    #         xls = "0. ARGOS(09.09).xlsx"
    #         r = main(xls,
    #                  '--sheet', 'Sheet1',
    #                  '--range', 'A2:AK4',
    #                  '--write', '(정산)2020.09.10 ARGOS.xlsx',
    #                  '--write-sheet', '내역서',
    #                  '--write-cell', 'Z7',
    #                  '--outfile', self.out,
    #                  '--errfile', self.err,
    #                  )
    #         self.assertTrue(r == 0)
    #         with open(self.out, 'r', encoding='utf8') as ifp:
    #             rs = ifp.read()
    #             # print(rs)
    #             self.assertTrue(rs == 'chromedriver;chrome;EXCEL;')
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0690_debug_TS_all4home(self):
    #     try:
    #         _csv = "p2.csv"
    #         r = main(_csv,
    #                  '--sheet', 'p2',
    #                  '--range', 'A1:E63',
    #                  '--write', 'conv.xlsx',
    #                  '--write-sheet', 'p2',
    #                  '--write-cell', 'A1',
    #                  '--outfile', self.out,
    #                  '--errfile', self.err,
    #                  )
    #         self.assertTrue(r == 0)
    #         with open(self.out, 'r', encoding='utf8') as ifp:
    #             rs = ifp.read()
    #             # print(rs)
    #             self.assertTrue(rs == 'chromedriver;chrome;EXCEL;')
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0700_JIRA_501(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            xls = "test-empty-rows.xlsx"
            r = main(xls,
                     '--data-only',
                     '--keep-blank',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out, 'r', encoding='utf8') as ifp:
                rs = ifp.read()
                # print(rs)
                self.assertTrue(len(rs.split('\n')) == 7)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0710_Irene_Debug(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            xls = "1.xlsx"
            r = main(xls,
                     '--sheet', 'Sheet1',
                     '--range', 'A1:B1',
                     '--write', '123.csv',
                     '--write-sheet', 'Sheet1',
                     '--write-cell', 'A1',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)

            xls = "2.xlsx"
            r = main(xls,
                     '--sheet', 'Sheet1',
                     '--range', 'A1:B1',
                     '--write', '123.csv',
                     '--write-sheet', 'Sheet1',
                     '--write-cell', 'A2',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)

            xls = "3.xlsx"
            r = main(xls,
                     '--sheet', 'Sheet1',
                     '--range', 'A1:B1',
                     '--write', '123.csv',
                     '--write-sheet', 'Sheet1',
                     '--write-cell', 'A3',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0720_Shige_Debug(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            xls = r"C:\work\Bots\ExcelAdv\TestXLXS_0613.xlsx"
            r = main(xls,
                     '--sheet', 'Sheet1',
                     '--range', 'c1:d5',
                     '--data-only',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (2,))
                    rr.append(row)
            self.assertTrue(len(rr) == 5 and rr[-1][0] == '5')

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0730_password_read(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('Credentials.xlsx',
                     '--password', 'argos0520',
                     '--range', 'a1:b5',
                     '--outfile', self.out,
                     '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            with open(self.out) as ifp:
                print(ifp.read())
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (2,))
                    rr.append(row)
            self.assertTrue(len(rr) == 5 and rr[-1][-1] == 'user')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        if os.path.exists(self.out):
            os.remove(self.out)
        if os.path.exists(self.err):
            os.remove(self.err)
        if os.path.exists(self.wxl):
            os.remove(self.wxl)
        if os.path.exists(self.wcsv):
            os.remove(self.wcsv)
        self.assertTrue(True)
