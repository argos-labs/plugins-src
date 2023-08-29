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
#  * [2021/12/06]
#     - Erase oracle testing
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
from argoslabs.data.rdb import _main as main
from alabs.common.util.vvnet import is_svc_opeded


################################################################################
class TU(TestCase):
    # ==========================================================================
    tut = None

    # ==========================================================================
    def setUp(self) -> None:
        self.tut = {
            'mysql': {
                'svclist': [
                    {
                        'host': '192.168.35.241',
                        'port': 3306,
                    },
                    {
                        'host': '192.168.99.249',
                        'port': 3306,
                    },
                    {
                        'host': 'localhost',
                        'port': 13306,
                    },
                    {
                        'host': '10.211.55.2',
                        'port': 13306,
                    },
                ],
                'root_params': None,
                'user_params': None,
            },
            'mssql': {
                'svclist': [
                    {
                        'host': '192.168.35.241',
                        'port': 1433,
                    },
                    {
                        'host': '192.168.99.247',
                        'port': 1433,
                    },
                    {
                        'host': 'localhost',
                        'port': 11433,
                    },
                    {
                        'host': '10.211.55.2',
                        'port': 11433,
                    },
                ],
                'root_params': None,
                'user_params': None,
            },
        }
        for dbms, tut in self.tut.items():
            has_svc = False
            for svc in tut['svclist']:
                print('Try to connecing [%s] %s:%s'
                      % (dbms, svc['host'], svc['port']), end=' ... ')
                if is_svc_opeded(svc['host'], svc['port']):
                    if dbms == 'mysql':
                        tut['root_params'] = \
                            (dbms, svc['host'], str(svc['port']),
                             'root', 'r', 'mysql')
                        tut['user_params'] = \
                            (dbms, svc['host'], str(svc['port']),
                             'myuser', 'myuser123!@#', 'mytest')
                    elif dbms == 'mssql':
                        tut['user_params'] = \
                            (dbms, svc['host'], str(svc['port']),
                             'sa', 'test-oracle123', 'tempdb')
                    has_svc = True
                    print('connected!')
                    break
                print('NOT connected!')

            # if not has_svc:
            #     raise IOError('Cannot find %s Service' % dbms)

    # ==========================================================================
    def _rp(self, db):
        return self.tut[db]['root_params']

    # ==========================================================================
    def _up(self, db):
        return self.tut[db]['user_params']

    # ==========================================================================
    @staticmethod
    def _gp(f, db=None):
        dp = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(dp, db, f) if db else os.path.join(dp, f)

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0090_invalid_sql(self):
        dbms = 'mysql'
        try:
            args = [dbms, '', '', '', '', '']
            _ = main(*args)
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_invalid_sql(self):
        dbms = 'mysql'
        try:
            args = self._rp(dbms)
            _ = main(*args)
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test1000_prepare(self):
        dbms = 'mysql'
        rp = self._rp(dbms)
        self.assertTrue(self._rp(dbms))
        # noinspection PyBroadException
        try:
            _ = main(*self._rp(dbms),
                     '--file', self._gp('9000-drop-database.sql', dbms))
        except Exception:
            pass
        try:
            r = main(*self._rp(dbms),
                     '--file', self._gp('1000-create-database.sql', dbms))
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test2010_create_table(self):
        # ----------------------------------------------------------------------
        dbms = 'mysql'
        if dbms in self.tut:
            print('%s%s' % (dbms, '*'*80))
            self.assertTrue(self._up(dbms))
            try:
                r = main(*self._up(dbms),
                         '--file', self._gp('2010-create-table.sql', dbms))
                self.assertTrue(r == 0)
            except ArgsError as e:
                sys.stderr.write('\n%s\n' % str(e))
                self.assertTrue(False)
        # ----------------------------------------------------------------------
        dbms = 'mssql'
        if dbms in self.tut:
            print('%s%s' % (dbms, '*'*80))
            self.assertTrue(self._up(dbms))
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
        dbms = 'mysql'
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
        # ----------------------------------------------------------------------
        dbms = 'mssql'
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
        dbms = 'mysql'
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
        # ----------------------------------------------------------------------
        dbms = 'mssql'
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
            dbms = 'mysql'
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
            # ----------------------------------------------------------------------
            dbms = 'mssql'
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
        dbms = 'mysql'
        if dbms in self.tut:
            print('%s%s' % (dbms, '*'*80))
            self.assertTrue(self._up(dbms))
            try:
                r = main(*self._up(dbms),
                         '--file', self._gp('2040-select.sql', dbms),
                         '--outfile', outfile)
                self.assertTrue(r == 0)
            except ArgsError as e:
                sys.stderr.write('\n%s\n' % str(e))
                self.assertTrue(False)
        # ----------------------------------------------------------------------
        dbms = 'mssql'
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
        charset = 'euckr'
        dbms = 'mysql'
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
        # ----------------------------------------------------------------------
        charset = 'EUC-KR'
        dbms = 'mssql'
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
        dbms = 'mysql'
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
        # ----------------------------------------------------------------------
        dbms = 'mssql'
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
        dbms = 'mysql'
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
        # ----------------------------------------------------------------------
        dbms = 'mssql'
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
    # def test3000_problem_newline(self):
    #     # ----------------------------------------------------------------------
    #     # DB 접속정보 보내 드립니다.
    #     # DB : Mysql
    #     # Host : mail.vivans.net
    #     # Userid : kingnik
    #     # PW : 한려**1
    #     # Port : 3306
    #     # DB : viva_op
    #     # 쿼리 : SELECT * FROM test1
    #
    #     dbms = 'mysql'
    #     if dbms in self.tut:
    #         print('%s%s' % (dbms, '*'*80))
    #         try:
    #             r = main('mysql', 'mail.vivans.net', 3306, 'kingnik', 'gksfutneh1', 'viva_op',
    #                      '-e', 'SELECT * FROM test1')
    #             self.assertTrue(r == 0)
    #         except ArgsError as e:
    #             sys.stderr.write('\n%s\n' % str(e))
    #             self.assertTrue(False)

    # ==========================================================================
    # def test3010_problem_csv_insert(self):
    #     # ----------------------------------------------------------------------
    #     # DB 접속정보 보내 드립니다.
    #     # DB : Mysql
    #     # Host : 1.251.164.100
    #     # Userid : osdm
    #     # PW : !@43osdm^^
    #     # Port : 3306
    #     # DB : test
    #     # 쿼리 : REPLACE INTO qc VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}');
    #
    #     errfile = 'stderr.txt'
    #     dbms = 'mysql'
    #     if dbms in self.tut:
    #         print('%s%s' % (dbms, '*'*80))
    #         try:
    #             dp = os.path.abspath(os.path.dirname(__file__))
    #             csv_file = os.path.join(dp, 'debug', 'filter.csv')
    #             r = main('mysql', '1.251.164.100', '3306', 'osdm', '!@43osdm^^', 'test',
    #                      '-e', "REPLACE INTO qc VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}');",
    #                      '--csv-file', csv_file, '--header-lines', '1',
    #                      '--encoding', 'euckr',
    #                      '--errfile', errfile
    #                      )
    #             self.assertTrue(r == 0)
    #             with open(errfile, encoding='utf-8') as ifp:
    #                 print(ifp.read())
    #             self.assertTrue(os.path.getsize(errfile) > 0)
    #
    #             r = main('mysql', '1.251.164.100', '3306', 'osdm', '!@43osdm^^', 'test',
    #                      '-e', "REPLACE INTO qc VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}');",
    #                      '--csv-file', csv_file, '--header-lines', '1',
    #                      '--encoding', 'euckr',
    #                      '--suppress-warning',
    #                      '--errfile', errfile
    #                      )
    #             self.assertTrue(r == 0)
    #             self.assertTrue(os.path.getsize(errfile) <= 0)
    #         except ArgsError as e:
    #             sys.stderr.write('\n%s\n' % str(e))
    #             self.assertTrue(False)
    #         finally:
    #             if os.path.exists(errfile):
    #                 os.remove(errfile)

    # ==========================================================================
    # def test3020_problem_csv_insert(self):
    #     # ----------------------------------------------------------------------
    #     # DB 접속정보 보내 드립니다.
    #     # DB : Mysql
    #     # Host : 1.251.164.100
    #     # Userid : osdm
    #     # PW : !@43osdm^^
    #     # Port : 3306
    #     # DB : test
    #     # 쿼리 : REPLACE INTO qc VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}');
    #
    #     errfile = 'stderr.txt'
    #     dbms = 'mysql'
    #     if dbms in self.tut:
    #         print('%s%s' % (dbms, '*'*80))
    #         try:
    #             dp = os.path.abspath(os.path.dirname(__file__))
    #             csv_file = os.path.join(dp, 'debug', 'filter-7K.csv')
    #             r = main('mysql', '1.251.164.100', '3306', 'osdm', '!@43osdm^^', 'test',
    #                      '-e', "REPLACE INTO qc VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}');",
    #                      '--csv-file', csv_file, '--header-lines', '1',
    #                      '--encoding', 'euckr',
    #                      '--suppress-warning',
    #                      '--errfile', errfile
    #                      )
    #             self.assertTrue(r == 0)
    #             self.assertTrue(os.path.getsize(errfile) <= 0)
    #         except ArgsError as e:
    #             sys.stderr.write('\n%s\n' % str(e))
    #             self.assertTrue(False)
    #         finally:
    #             if os.path.exists(errfile):
    #                 os.remove(errfile)

    # ==========================================================================
    # def test3030_problem_csv_insert(self):
    #     # ----------------------------------------------------------------------
    #     # 한솔씨가 디버깅 요청
    #     # DB : Mysql
    #     # Host : 218.145.31.34
    #     # Userid : viva
    #     # PW : viva6373
    #     # Port : 3306
    #     # DB : azon
    #     # 쿼리 : REPLACE INTO qc VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}');
    #
    #     errfile = 'stderr.txt'
    #     dbms = 'mysql'
    #     if dbms in self.tut:
    #         print('%s%s' % (dbms, '*'*80))
    #         sql = '''REPLACE INTO CBCI_11ST_SALEACCNT VALUES ('kari','{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}','{23}','{24}','{25}','{26}','{27}','{28}','{29}','{30}','{31}','{32}','{33}','{34}','{35}','{36}','{37}',REPLACE('{38}',',',''),'{39}','{40}','{41}','{42}','{43}','{44}','{45}','{46}','{47}','{48}','{49}','{50}','{51}','{52}','{53}','{54}',NOW());'''
    #         try:
    #             dp = os.path.abspath(os.path.dirname(__file__))
    #             csv_file = os.path.join(dp, 'debug', '정산_확정건__20200322_20200323_kairoslab.csv')
    #             r = main('mysql', '218.145.31.34', '3306', 'viva', 'viva6373', 'azon',
    #                      '-e', sql,
    #                      '--csv-file', csv_file,
    #                      '--header-lines', '5',
    #                      '--encoding', 'euckr',
    #                      '--suppress-warning',
    #                      '--errfile', errfile
    #                      )
    #             self.assertTrue(r == 0)
    #             self.assertTrue(os.path.getsize(errfile) <= 0)
    #         except ArgsError as e:
    #             sys.stderr.write('\n%s\n' % str(e))
    #             self.assertTrue(False)
    #         finally:
    #             if os.path.exists(errfile):
    #                 os.remove(errfile)

    # ==========================================================================
    # def test3040_problem_csv_insert(self):
    #     # ----------------------------------------------------------------------
    #     # 한솔씨가 디버깅 요청
    #     # DB : Mysql
    #     # Host : server.noonbesoft.com
    #     # Userid : nbmes
    #     # PW : noonbe12345!
    #     # Port : 13300
    #     # DB : isc
    #     # 쿼리 : REPLACE INTO measure_result VALUES ('0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48',NOW());
    #
    #     errfile = 'stderr.txt'
    #     dbms = 'mysql'
    #     if dbms in self.tut:
    #         print('%s%s' % (dbms, '*'*80))
    #         sql = '''REPLACE INTO measure_result VALUES ('0','1','2','3','4','5','6','7','8','9','0','1','2','3','4','5','6','7','8','9','0','1','2','3','4','5','6','7','8','9','0','1','2','3','4','5','6','7','8','9','0','1','2','3','4','5','6','7','8',NOW());'''
    #         try:
    #             dp = os.path.abspath(os.path.dirname(__file__))
    #             # csv_file = os.path.join(dp, 'debug', '정산_확정건__20200322_20200323_kairoslab.csv')
    #             r = main('mysql', 'server.noonbesoft.com', '13300', 'nbmes', 'noonbe12345!', 'isc',
    #                      '-e', sql,
    #                      # '--csv-file', csv_file,
    #                      # '--header-lines', '5',
    #                      # '--encoding', 'euckr',
    #                      # '--suppress-warning',
    #                      '--errfile', errfile
    #                      )
    #             self.assertTrue(r == 0)
    #             self.assertTrue(os.path.getsize(errfile) <= 0)
    #         except ArgsError as e:
    #             sys.stderr.write('\n%s\n' % str(e))
    #             self.assertTrue(False)
    #         finally:
    #             if os.path.exists(errfile):
    #                 os.remove(errfile)

    # ==========================================================================
    # def test3050_CBCI_COUPANG_problem_csv_insert(self):
    #     # ----------------------------------------------------------------------
    #     # TS팀 박준형씨가 디버깅 요청
    #
    #     errfile = 'stderr.txt'
    #     dbms = 'mysql'
    #
    #     sql_f = self._gp('CBCI_COUPANG-failure-01.txt', dbms)
    #     # with open(sql_f, encoding='utf-8') as ifp:
    #     #     sql = ifp.read()
    #     try:
    #         dp = os.path.abspath(os.path.dirname(__file__))
    #         r = main(dbms, '211.218.126.175', '3306', 'cubici', '~~', 'cubici',
    #                  '--file', sql_f,
    #                  '--errfile', errfile
    #                  )
    #         self.assertTrue(r == 0)
    #         self.assertTrue(os.path.getsize(errfile) <= 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(errfile):
    #             os.remove(errfile)

    # ==========================================================================
    # def test3050_CBCI_COUPANG_problem_csv_insert(self):
    #     # ----------------------------------------------------------------------
    #     # TS팀 박준형씨가 디버깅 요청
    #
    #     errfile = 'stderr.txt'
    #     dbms = 'mysql'
    #
    #     sql_f = self._gp('gmarket_sql_sending.txt', 'CBCI')
    #     # with open(sql_f, encoding='utf-8') as ifp:
    #     #     sql = ifp.read()
    #     try:
    #         dp = os.path.abspath(os.path.dirname(__file__))
    #         r = main(dbms, '211.218.126.175', '3306', 'cubici', '..', 'cubici',
    #                  '--file', sql_f,
    #                  '--errfile', errfile
    #                  )
    #         self.assertTrue(r == 0)
    #         self.assertTrue(os.path.getsize(errfile) <= 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(errfile):
    #             os.remove(errfile)

    # ==========================================================================
    def test9000_clear(self):
        dbms = 'mysql'
        self.assertTrue(self._rp(dbms))
        try:
            r = main(*self._rp(dbms),
                     '--file', self._gp('9000-drop-database.sql', dbms))
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
