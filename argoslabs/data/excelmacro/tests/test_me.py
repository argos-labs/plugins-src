"""
====================================
 :mod:`argoslabs.data.excelmacro`
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
#  * [2021/03/29]
#     - 그룹에 "2-Business Apps" 넣음
#  * [2020/04/28]
#     - only accept '.xlsm', 'xls'
#     - return abspath for filename
#  * [2019/07/17]
#     - starting
#

################################################################################
import os
import sys
import csv
import shutil
from tempfile import gettempdir
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.data.excelmacro import _main as main
from argoslabs.data.excel import _main as excel_main


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    # xlf = 'sample.xlsx'
    # wxl = os.path.join(gettempdir(), 'foo.xlsx')
    xlsms = (  # tests/*.xlsm must be copyed
        'C:/work/excelmacro/stoptime.xlsm',
        'C:/work/excelmacro/macro_test01.xlsm',
    )
    out = 'stdout.txt'
    err = 'stderr.txt'

    # ==========================================================================
    def test0000_init(self):
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        for xlsm in self.xlsms:
            if os.path.exists(xlsm):
                os.remove(xlsm)
            xlsm_dir = os.path.dirname(xlsm)
            if not os.path.exists(xlsm_dir):
                os.makedirs(xlsm_dir)
            shutil.copy(os.path.basename(xlsm), xlsm)
            self.assertTrue(os.path.exists(xlsm))

    # ==========================================================================
    def test0100_failure_empty(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_cannot_read(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            _ = main('not-existed.xlsx',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(str(e) == 'the following arguments are required: funcname')

    # ==========================================================================
    def test0200_before_clear(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        r = excel_main(self.xlsms[0],
                       '--sheet', 'Ark2',
                       '--range', 'A1:C13',
                       '--clear-cell',
                       '--outfile', self.out,
                       '--errfile', self.err,
                       )
        self.assertTrue(r == 0)
        # check results
        r = excel_main(self.xlsms[0],
                       '--sheet', 'Ark2',
                       '--range', 'A1:C13',
                       '--outfile', self.out,
                       '--errfile', self.err)
        self.assertTrue(r == 0)
        with open(self.out, 'r', encoding='utf8') as ifp:
            rs = ifp.read()
            print(rs)
        rr = []
        with open(self.out, 'r', encoding='utf8') as ifp:
            cr = csv.reader(ifp)
            for row in cr:
                self.assertTrue(len(row) in (3,))
                self.assertFalse(any(row))
                rr.append(row)

    # ==========================================================================
    def test0210_macro_run(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.xlsms[0], 'Calculate',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out, 'r', encoding='utf8') as ifp:
                rs = ifp.read()
                self.assertTrue(rs == os.path.abspath(self.xlsms[0]))
            # check results
            r = excel_main(self.xlsms[0],
                           '--sheet', 'Ark2',
                           '--range', 'A1:C13',
                           '--outfile', self.out,
                           '--errfile', self.err)
            self.assertTrue(r == 0)
            vr_cnt = 0
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (3,))
                    if any(row):
                        vr_cnt += 1
                    rr.append(row)
            self.assertTrue(vr_cnt == 12)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_before_clear(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        r = excel_main(self.xlsms[1],
                       '--sheet', 'Sheet1',
                       '--range', 'A1:A1',
                       '--clear-cell',
                       '--outfile', self.out,
                       '--errfile', self.err,
                       )
        self.assertTrue(r == 0)
        # check results
        r = excel_main(self.xlsms[1],
                       '--sheet', 'Sheet1',
                       '--range', 'A1:A1',
                       '--outfile', self.out,
                       '--errfile', self.err)
        self.assertTrue(r == 0)
        with open(self.out, 'r', encoding='utf8') as ifp:
            print(ifp.read())
        rr = []
        with open(self.out, 'r', encoding='utf8') as ifp:
            cr = csv.reader(ifp)
            for row in cr:
                self.assertTrue(len(row) in (1,))
                self.assertFalse(any(row))
                rr.append(row)

    # ==========================================================================
    def test0230_macro_run(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(self.xlsms[1], 'StartMe',
                     '--params', '1',
                     '--params', 'From Unittest Hello?',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r == 0)
            with open(self.out, 'r', encoding='utf8') as ifp:
                rs = ifp.read()
                self.assertTrue(rs == os.path.abspath(self.xlsms[1]))
            # check results
            r = excel_main(self.xlsms[1],
                           '--sheet', 'Sheet1',
                           '--range', 'A1:A1',
                           '--outfile', self.out,
                           '--errfile', self.err)
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (1,))
                    self.assertTrue(row[0] == 'From Unittest Hello?')
                    break
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0240_macro_run(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main('foo.xlsx', 'StartMe',
                     '--params', '1',
                     '--params', 'From Unittest Hello?',
                     '--outfile', self.out,
                     '--errfile', self.err)
            self.assertTrue(r != 0)
            with open(self.err, 'r', encoding='utf8') as ifp:
                self.assertTrue(ifp.read().startswith('Cannot run macro for the extension'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        if os.path.exists(self.out):
            os.remove(self.out)
        if os.path.exists(self.err):
            os.remove(self.err)
        self.assertTrue(True)
