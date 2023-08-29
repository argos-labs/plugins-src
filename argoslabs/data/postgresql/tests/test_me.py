"""
====================================
 :mod:argoslabs.data.rdb
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS
"""
# 관련 작업자
# ===========
#
# 본 모듈은 다음과 같은 사람들이 관여했습니다:
#  * 채문창
#
# 작업일지
# --------
#
# 다음과 같은 작업 사항이 있었습니다:
#
#  * [2022/02/11]
#     - CSV Insert 에 ' 가 들어 있는 경우 처리
#  * [2021/11/29]
#     - 본 모듈 작업 시작

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.data.postgresql import _main as main
from alabs.common.util.vvnet import is_svc_opeded


################################################################################
class TU(TestCase):
    # ==========================================================================
    tut = None

    # ==========================================================================
    @classmethod
    def _up(cls):
        cls.tut = [
            '192.168.35.241',
            '5432',
            # 'pguser',
            # 'pguser1!',
            'postgres',
            'postgres123',
            'testdb',
        ]
        return cls.tut

    # ==========================================================================
    @staticmethod
    def _gp(f):
        dp = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(dp, 'sql', f)

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0090_invalid_sql(self):
        try:
            args = ['', '', '', '', '']
            _ = main(*args)
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test1000_prepare(self):
        # https://judo0179.tistory.com/96
        ...

    # ==========================================================================
    def test2010_create_table(self):
        # ----------------------------------------------------------------------
        try:
            args = self._up()
            sql_f = self._gp('2010-create-table.sql')
            r = main(*args, '--file', sql_f)
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test2020_static_insert(self):
        # ----------------------------------------------------------------------
        try:
            r = main(*self._up(),
                     '--file', self._gp('2020-static-insert.sql'))
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test2030_template_insert(self):
        # ----------------------------------------------------------------------
        try:
            r = main(*self._up(),
                     '--file', self._gp('2030-template-insert.sql'),
                     '--csv-file', self._gp('foo.csv'),
                     '--header-lines', '1')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test2040_select(self):
        outfile = 'out.txt'
        try:
            r = main(*self._up(),
                     '--file', self._gp('2040-select.sql'),
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for ndx, row in enumerate(cr):
                    self.assertTrue(len(row) in (3,))
                    rows.append(row)
            self.assertTrue(len(rows) == 6)

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test2050_select_error(self):
        # ----------------------------------------------------------------------
        stderr_file = 'stderr.txt'
        try:
            r = main(*self._up(),
                     '--execute', 'select AAA',
                     '--errfile', stderr_file)
            self.assertTrue(r == 1)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(os.path.exists(stderr_file) and
                            os.path.getsize(stderr_file) > 0)
        finally:
            if os.path.exists(stderr_file):
                os.remove(stderr_file)

    # ==========================================================================
    def test2060_drop_table(self):
        # ----------------------------------------------------------------------
        try:
            r = main(*self._up(),
                     '--file', self._gp('2050-drop-table.sql'))
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9000_clear(self):
        # dbms = 'mysql'
        # self.assertTrue(self._rp(dbms))
        # try:
        #     r = main(*self._rp(dbms),
        #              '--file', self._gp('9000-drop-database.sql', dbms))
        #     self.assertTrue(r == 0)
        # except ArgsError as e:
        #     sys.stderr.write('\n%s\n' % str(e))
        #     self.assertTrue(False)
        ...

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
