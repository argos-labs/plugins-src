
"""
====================================
 :mod:`argoslabs.datanalysis.pandasprofiling`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS data analysis using PANDAS profiling
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
#  * [2020/05/07]
#     - title, html_style 추가
#  * [2020/04/30]
#     - profiling에서 중간 프로세싱 결과가 stderr로 출력되는 것을 별도 처리
#  * [2020/04/27]
#     - pandas_safe_eval 함수 추가
#  * [2020/04/26]
#     - starting

################################################################################
import os
import sys
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.datanalysis.pandasprofiling import _main as main


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
        errfile = 'stderr.txt'
        try:
            r = main('bar.csv', 'bar.html',
                     '--header', '0',
                     '--title', 'Example Bar CSV data',
                     '--outfile', outfile,
                     '--errfile', errfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                self.assertTrue(rs.endswith('bar.html'))
            with open(errfile, encoding='utf-8') as ifp:
                rs = ifp.read()
                self.assertTrue(not rs)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
