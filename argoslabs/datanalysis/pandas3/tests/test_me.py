
"""
====================================
 :mod:`argoslabs.datanalysis.pandas3`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS data analysis using PANDAS basic
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/06]
#     - 그룹에 "4-Data Science" 넣음
#  * [2020/09/15]
#     - --in-csv-seps, --in-encodings
#     - --out-header, --out-index, --out-csv-sep, --out-encoding 분리
#  * [2020/09/11]
#     - "Header" => "Header Row", "Out Index" => "Show Index"
#  * [2020/09/10]
#     - suppress output for exec
#  * [2020/09/07]
#     - starting

################################################################################
import os
import sys
import csv
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.datanalysis.pandas3 import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_failure(self):
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        try:
            r = main('invalid')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success_csv(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main('result.csv', 'new.xls', 'original.xlsm', 'complete.xlsx',
                     '--dtypes', "{'LH담당자연락처': str, '하자접수일': str, '보수지시일': str, '처리기한': str}",
                     '--headers', '0',
                     '--headers', '1',
                     '--headers', '1',
                     '--stats', r"section = '경북2권역' if argspec.in_files[0].find('세음') > 0 else '경북3권역'",
                     '--stats', r"merge_1 = (pd.concat([dfs[1], dfs[0]], ignore_index=False, sort=False).drop_duplicates(['접수일련번호'], keep='first'))",
                     '--stats', r"drop_1 = (pd.concat([merge_1, dfs[1]], ignore_index=False, sort=False).drop_duplicates(['접수일련번호'], keep=False))",
                     '--stats', r"merge_2 = (pd.concat([dfs[2], drop_1], ignore_index=False, sort=False).drop_duplicates(['접수일련번호'], keep='first'))",
                     '--stats', r"df = (pd.concat([merge_2, dfs[2]], ignore_index=False, sort=False).drop_duplicates(['접수일련번호'], keep=False))",
                     '--stats', r"df['현장담당'] = '김정'",
                     '--stats', r"df['권역구분'] = np.nan",
                     '--stats', r"section2_arr0 = ['경북혁신2', '경북혁신3', '고령다산1', '고령다산2', '고령다산3', '구미구평', '구미도량2-3', '구미도산', '구미옥계1', '구미옥계2', '구미인의', '구미황상3', '군위서부', '김천대신', '김천덕곡', '김천부곡2', '의성상리', '경북혁신']",
                     '--stats', r"section2_arr1 = ['고령덕경인터빌', '구미고아에덴', '김천일천푸른마을']",
                     '--stats', r"section2_arr2 = ['구미화성파크드림', '고령디오팰리스']",
                     '--stats', r"section3_arr0 = ['경산백천', '경산사동휴먼시아1', '경산사동휴먼시아2', '경산상방', '경산진량휴먼시아', '경주건천', '경주금장', '경주안강', '경주외동', '경주용강', '영천망정5', '영천문내', '영천야사4', '청도범곡휴먼시아']",
                     '--stats', r"section3_arr1 = ['경산삼주봉황1차', '경산삼주봉황2차', '경산초원장미', '경주안강에덴', '경주안강장미마을', '경주우성한빛1차', '경주우성한빛2차', '경주위덕삼성', '경주일천푸른마을', '경주전원홈그린', '한동그린타운', '한동화성타운']",
                     '--stats', r"section3_arr2 = ['경산진량우림필유', '영천해피포유']",
                     '--stats', r"df = df[['접수일련번호', '하자접수일', '하자진행상태', '하자구분', '하자상세구분', '단지 및 동주소', '임대유형', '대분류', '동', '호', '공간', '대표공종', '중분류', '소분류', '세분류', '하자내용', '계약번호', '견적금액', '공사금액', '민원인', '연락처', '연락처2', 'LH담당자', 'LH담당자연락처', '처리내용', '완료보고일', '보수완료일', '반려자명', '반려일', '반려사유', '보수지시일', '처리기한', '경과일', '비고', '작업자', '현장담당', '권역구분']]",
                     '--stats', r"if section == '경북2권역':",
                     '--stats', r"    df.loc[df['단지 및 동주소'].isin(section2_arr0), ['권역구분']] = '2건설'",
                     '--stats', r"    df.loc[df['단지 및 동주소'].isin(section2_arr1), ['권역구분']] = '2부도'",
                     '--stats', r"    df.loc[df['단지 및 동주소'].isin(section2_arr2), ['권역구분']] = '2리츠'",
                     '--stats', r"    df.loc[df['권역구분'].isnull(), ['권역구분']] = '2다가구'",
                     '--stats', r"    df['비고'] = '㈜세음건설'",
                     '--stats', r"elif section == '경북3권역':",
                     '--stats', r"    df.loc[df['단지 및 동주소'].isin(section3_arr0), ['권역구분']] = '3건설'",
                     '--stats', r"    df.loc[df['단지 및 동주소'].isin(section3_arr1), ['권역구분']] = '3부도'",
                     '--stats', r"    df.loc[df['단지 및 동주소'].isin(section3_arr2), ['권역구분']] = '3리츠'",
                     '--stats', r"    df.loc[df['권역구분'].isnull(), ['권역구분']] = '3다가구'",
                     '--stats', r"    df['비고'] = '㈜이두건설'",
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            rows = list()
            with open('result.csv', encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (37,))
                    rows.append(row)
            self.assertTrue(len(rows) in (178, 179) and
                            rows[-1][-1] == '3다가구')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0110_success_stat_file(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main('result.csv', 'new.xls', 'original.xlsm', 'complete.xlsx',
                     '--dtypes', "{'LH담당자연락처': str, '하자접수일': str, '보수지시일': str, '처리기한': str}",
                     '--headers', '0',
                     '--headers', '1',
                     '--headers', '1',
                     '--stat-file', "pandas3-body.py",
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            rows = list()
            with open('result.csv', encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (37,))
                    rows.append(row)
            self.assertTrue(len(rows) in (178, 179) and
                            rows[-1][-1] == '3다가구')
            with open(outfile, encoding='utf-8') as ifp:
                rstr = ifp.read()
                self.assertTrue(rstr == os.path.abspath('result.csv'))
                # print(rstr)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
