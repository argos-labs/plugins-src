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
#  * [2021/07/28]
#     - clone from rdb into oracle
#  * [2021/07/26]
#     - GMarket Debugging
#  * [2021/07/15]
#     - CBCI 'div ..' 오류 디버깅: 입력 문자열 안에 ';' 가 들어가 있는 경우 있음
#       preprocess_sql 에서 라인 마지막에 ';' 으로 끝나는 경우만 나눔
#  * [2021/04/01]
#     - 그룹에 "8-Storage Solutions" 넣음
#  * [2020/02/27]
#     - --suppress-warning
#  * [2019/12/12]
#     - set pre-compiled for pymssql
#  * [2019/10/25]
#     - csv.writer에 개행문자가 하나 더 포함되는 문제 해결
#  * [2019/10/23]
#     - -- csv-file 옵션에 input_method를 fileread 로 수정
#  * [2019/06/24]
#     - --file 옵션에 fileread input_method 추가
#  * [2019/05/09]
#     - --charset 옵션 추가
#  * [2019/03/13]
#     - --errfile 용 수정 및 테스트 추가
#     - dbpass의 input_method에 password 추가
#  * [2019/03/05]
#     - add icon
#  * [2019/03/05]
#     - oracle 작업
#  * [2019/03/02]
#     - oracle 작업 시작
#  * [2019/03/01]
#     - mssql 작업 및 테스트
#  * [2019/01/02]
#     - ppm SDK로 전환 및 테스트
#  * [2018/09/30]
#     - 본 모듈 작업 시작

################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.data.oracle import _main as main
from alabs.common.util.vvnet import is_svc_opeded


################################################################################
class TU(TestCase):
    # ==========================================================================
    tut = None

    # ==========================================================================
    # noinspection PyMethodParameters,PyMethodOverriding,PyTypeChecker
    @classmethod
    def setUpClass(cls):
        cls.tut = {
            'oracle': {
                'svclist': [
                    {
                        'host': '192.168.35.241',
                        'port': 1521,
                    },
                    {
                        'host': '192.168.99.248',
                        'port': 1521,
                    },
                    {
                        'host': 'localhost',
                        'port': 11521,
                    },
                    {
                        'host': '10.211.55.2',
                        'port': 11521,
                    },
                ],
                'root_params': None,
                'user_params': None,
            }
        }
        for dbms, tut in cls.tut.items():
            has_svc = False
            for svc in tut['svclist']:
                print('Try to connecing [%s] %s:%s'
                      % (dbms, svc['host'], svc['port']), end=' ... ')
                if is_svc_opeded(svc['host'], svc['port']):
                    tut['user_params'] = \
                        (svc['host'], str(svc['port']),
                         'sys', 'MyOrcl_01', 'orcl')
#                         'orcl', 'orcl_01', 'orcl')
                    has_svc = True
                    print('connected!')
                    break
                print('NOT connected!')

            # if not has_svc:
            #     raise IOError('Cannot find %s Service' % dbms)

    # ==========================================================================
    @classmethod
    def _rp(cls, db):
        return cls.tut[db]['root_params']

    # ==========================================================================
    @classmethod
    def _up(cls, db):
        return cls.tut[db]['user_params']

    # ==========================================================================
    @staticmethod
    def _gp(f, db=None):
        dp = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(dp, db, f) if db else os.path.join(dp, f)

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0100_invalid_sql(self):
        dbms = 'mysql'
        try:
            # _ = main(*self._rp(dbms))
            # self.assertTrue(False)
            ...
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test1000_prepare(self):
    #     dbms = 'mysql'
    #     self.assertTrue(self._rp(dbms))
    #     # noinspection PyBroadException
    #     try:
    #         _ = main(*self._rp(dbms),
    #                  '--file', self._gp('9000-drop-database.sql', dbms))
    #     except Exception:
    #         pass
    #     try:
    #         r = main(*self._rp(dbms),
    #                  '--file', self._gp('1000-create-database.sql', dbms))
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test2010_create_table(self):
        # ----------------------------------------------------------------------
        dbms = 'oracle'
        if dbms in self.tut:
            print('%s%s' % (dbms, '*'*80))
            self.assertTrue(self._up(dbms))
            # noinspection PyBroadException
            try:
                _ = main(*self._up(dbms),
                         '--file', self._gp('2050-drop-table.sql', dbms))
            except Exception:
                pass
            try:
                r = main(*self._up(dbms),
                         '--file', self._gp('2010-create-table.sql', dbms))
                self.assertTrue(r == 0)
            except ArgsError as e:
                sys.stderr.write('\n%s\n' % str(e))
                self.assertTrue(False)

    # ==========================================================================
    def test2020_static_insert(self):
        # ----------------------------------------------------------------------
        dbms = 'oracle'
        if dbms in self.tut:
            print('%s%s' % (dbms, '*'*80))
            self.assertTrue(self._up(dbms))
            try:
                r = main(*self._up(dbms),
                         '--file', self._gp('2020-static-insert.sql', dbms))
                self.assertTrue(r == 0)
            except ArgsError as e:
                sys.stderr.write('\n%s\n' % str(e))
                self.assertTrue(False)

    # ==========================================================================
    def test2030_template_insert(self):
        # ----------------------------------------------------------------------
        dbms = 'oracle'
        if dbms in self.tut:
            print('%s%s' % (dbms, '*'*80))
            self.assertTrue(self._up(dbms))
            try:
                r = main(*self._up(dbms),
                         '--file', self._gp('2030-template-insert.sql', dbms),
                         '--csv-file', self._gp('foo.csv'),
                         '--header-lines', '1')
                self.assertTrue(r == 0)
            except ArgsError as e:
                sys.stderr.write('\n%s\n' % str(e))
                self.assertTrue(False)

    # ==========================================================================
    def test2035_template_insert_with_encoding(self):
        bar_f = None
        encoding = 'euckr'
        try:
            bar_f = os.path.join(os.path.dirname(self._gp('foo.csv')),
                                 'bar.csv')
            with open(self._gp('foo.csv'), encoding='utf8') as ifp:
                bar = ifp.read()
            with open(bar_f, 'w', encoding=encoding) as ofp:
                ofp.write(bar.encode(encoding).decode(encoding))
            # ----------------------------------------------------------------------
            dbms = 'oracle'
            if dbms in self.tut:
                print('%s%s' % (dbms, '*'*80))
                self.assertTrue(self._up(dbms))
                try:
                    r = main(*self._up(dbms),
                             '--file', self._gp('2030-template-insert.sql', dbms),
                             '--csv-file', self._gp('bar.csv'),
                             '--header-lines', '1',
                             '--encoding', encoding)
                    self.assertTrue(r == 0)
                except ArgsError as e:
                    sys.stderr.write('\n%s\n' % str(e))
                    self.assertTrue(False)
        finally:
            if bar_f and os.path.exists(bar_f):
                os.remove(bar_f)

    # ==========================================================================
    def test2040_select(self):
        # ----------------------------------------------------------------------
        outfile = 'stdout.txt'
        # ----------------------------------------------------------------------
        dbms = 'oracle'
        if dbms in self.tut:
            print('%s%s' % (dbms, '*'*80))
            self.assertTrue(self._up(dbms))
            try:
                r = main(*self._up(dbms),
                         '--file', self._gp('2040-select.sql', dbms))
                self.assertTrue(r == 0)
            except ArgsError as e:
                sys.stderr.write('\n%s\n' % str(e))
                self.assertTrue(False)

    # ==========================================================================
    def test2045_select_with_charset(self):
        # ----------------------------------------------------------------------
        charset = 'invalid'
        dbms = 'oracle'
        if dbms in self.tut:
            print('%s%s' % (dbms, '*'*80))
            self.assertTrue(self._up(dbms))
            try:
                r = main(*self._up(dbms),
                         '--file', self._gp('2040-select.sql', dbms),
                         '--charset', charset)
                self.assertTrue(r == 0)
            except ArgsError as e:
                sys.stderr.write('\n%s\n' % str(e))
                self.assertTrue(False)

    # ==========================================================================
    def test2050_select_error(self):
        # ----------------------------------------------------------------------
        stderr_file = 'stderr.txt'
        # ----------------------------------------------------------------------
        dbms = 'oracle'
        if dbms in self.tut:
            print('%s%s' % (dbms, '*'*80))
            self.assertTrue(self._up(dbms))
            try:
                _ = main(*self._up(dbms),
                         '--execute', 'select AAA',
                         '--errfile', stderr_file)
                self.assertTrue(False)
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
        dbms = 'oracle'
        if dbms in self.tut:
            print('%s%s' % (dbms, '*'*80))
            self.assertTrue(self._up(dbms))
            try:
                r = main(*self._up(dbms),
                         '--file', self._gp('2050-drop-table.sql', dbms))
                self.assertTrue(r == 0)
            except ArgsError as e:
                sys.stderr.write('\n%s\n' % str(e))
                self.assertTrue(False)

    # # ==========================================================================
    # def test9000_clear(self):
    #     dbms = 'mysql'
    #     self.assertTrue(self._rp(dbms))
    #     try:
    #         r = main(*self._rp(dbms),
    #                  '--file', self._gp('9000-drop-database.sql', dbms))
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
