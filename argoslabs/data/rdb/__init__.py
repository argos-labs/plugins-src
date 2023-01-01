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
#  * [2021/12/10] => need test and build
#     - csv insert 시 예외 발생하면 return 5
#  * [2021/07/26]
#     - GMarket Debugging
#     - instead find 'select' use startswith in sql to detect
#  * [2021/07/20]
#     - on-premise 에서 설치 문제가 있다하여 pymssql
#  * [2021/07/17]
#     - dll 등 문제로 Oracle 제외
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
import re
import sys
import csv
import argparse
import warnings
import pymysql
import pymssql
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class MySQL(object):
    field_type = {
        0: 'DECIMAL',
        1: 'TINY',
        2: 'SHORT',
        3: 'LONG',
        4: 'FLOAT',
        5: 'DOUBLE',
        6: 'NULL',
        7: 'TIMESTAMP',
        8: 'LONGLONG',
        9: 'INT24',
        10: 'DATE',
        11: 'TIME',
        12: 'DATETIME',
        13: 'YEAR',
        14: 'NEWDATE',
        15: 'VARCHAR',
        16: 'BIT',
        246: 'NEWDECIMAL',
        247: 'INTERVAL',
        248: 'SET',
        249: 'TINY_BLOB',
        250: 'MEDIUM_BLOB',
        251: 'LONG_BLOB',
        252: 'BLOB',
        253: 'VAR_STRING',
        254: 'STRING',
        255: 'GEOMETRY'}

    # ==========================================================================
    def __init__(self, dbhost, dbport, dbuser, dbpass, dbname, logger,
                 charset='utf8mb4', encoding='utf8', errors='strict'):
        self.host, self.port, self.user, self.passwd, self.db, self.charset, \
        self.encoding, self.errors \
            = dbhost, dbport, dbuser, dbpass, dbname, charset, encoding, errors
        self.logger = logger
        # for internal
        self.is_opened = False
        self.conn = None

    # ==========================================================================
    def open(self):
        self.logger.debug('MySQL.open: trying to open')
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.passwd,
            port=int(self.port),
            db=self.db,
            charset=self.charset,
            # charset='utf8mb4',
        )
        self.is_opened = True
        self.logger.debug('MySQL.open: opened!')
        return self.is_opened

    # ==========================================================================
    def close(self):
        self.logger.debug('MySQL.open: trying to close')
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.is_opened = False
            self.logger.debug('MySQL.close: closed!')

    # ==========================================================================
    def sql_execute(self, sql):
        self.logger.debug('MySQL.sql_execute: sql=<%s>' % sql)
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            print('affected_row_count\n%s' % cursor.rowcount)
            self.logger.debug('affected_row_count=%s' % cursor.rowcount)
        self.conn.commit()

    # ==========================================================================
    def sql_select(self, sql):
        self.logger.debug('MySQL.sql_select: sql=<%s>' % sql)
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            # num_fields = len(cursor.description)
            field_names = [x[0] for x in cursor.description]
            # noinspection PyUnusedLocal
            field_types = [x[1] for x in cursor.description]
            print('%s' % ','.join(field_names))
            cwr = csv.writer(sys.stdout, lineterminator='\n')
            rows = cursor.fetchall()
            for row in rows:
                cwr.writerow(row)

    # ==========================================================================
    def sql_execute_with_csv(self, sql, csv_file, header_lines=0):
        self.logger.debug('MySQL.sql_execute_with_csv: sql=<%s>, csv_file=%s'
                          % (sql, csv_file))
        if not os.path.exists(csv_file):
            raise IOError('CSV file "%s" not found' % csv_file)
        with open(csv_file, 'r', encoding=self.encoding, errors=self.errors) as ifp:
            cooked = csv.reader(ifp)
            with self.conn.cursor() as cursor:
                cnt = 0
                for i, record in enumerate(cooked):
                    if i < header_lines:
                        continue
                    try:
                        esql = sql.format(*record)
                        esql = esql.replace("''", "NULL")
                        cursor.execute(esql)
                        cnt += 1
                    except Exception as err:
                        msg = f'CSV[{cnt+1}] esql="{esql}"\nError={str(err)}'
                        self.logger.error(msg)
                        raise
                self.conn.commit()
                print('affected_row_count\n%s' % cnt)
                self.logger.debug('affected_row_count=%s' % cnt)
        warnings.resetwarnings()


################################################################################
class MSSQL(object):
    # ==========================================================================
    def __init__(self, dbhost, dbport, dbuser, dbpass, dbname,
                 logger, charset='utf8', encoding='utf8', errors='strict'):
        self.host, self.port, self.user, self.passwd, self.db, self.charset, \
        self.encoding, self.errors \
            = dbhost, dbport, dbuser, dbpass, dbname, charset, encoding, errors
        self.logger = logger
        # for internal
        self.is_opened = False
        self.conn = None

    # ==========================================================================
    def open(self):
        self.logger.debug('MSSQL.open: trying to open')
        self.conn = pymssql.connect(
            host=self.host,
            user=self.user,
            password=self.passwd,
            port=int(self.port),
            database=self.db,
            charset=self.charset,
            # charset='utf8',
        )
        self.is_opened = True
        self.logger.debug('MSSQL.open: opened!')
        return self.is_opened

    # ==========================================================================
    def close(self):
        self.logger.debug('MSSQL.open: trying to close')
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.is_opened = False
            self.logger.debug('MSSQL.close: closed!')

    # ==========================================================================
    def sql_execute(self, sql):
        self.logger.debug('MSSQL.sql_execute: sql=<%s>' % sql)
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            print('affected_row_count\n%s' % cursor.rowcount)
            self.logger.debug('affected_row_count=%s' % cursor.rowcount)
        self.conn.commit()

    # ==========================================================================
    def sql_select(self, sql):
        self.logger.debug('MSSQL.sql_select: sql=<%s>' % sql)
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            # num_fields = len(cursor.description)
            field_names = [x[0] for x in cursor.description]
            # noinspection PyUnusedLocal
            field_types = [x[1] for x in cursor.description]
            print('%s' % ','.join(field_names))
            cwr = csv.writer(sys.stdout, lineterminator='\n')
            rows = cursor.fetchall()
            for row in rows:
                cwr.writerow(row)

    # ==========================================================================
    def sql_execute_with_csv(self, sql, csv_file, header_lines=0):
        self.logger.debug('MSSQL.sql_execute_with_csv: sql=<%s>, csv_file=%s'
                          % (sql, csv_file))
        if not os.path.exists(csv_file):
            raise IOError('CSV file "%s" not found' % csv_file)
        with open(csv_file, 'r', encoding=self.encoding, errors=self.errors) as ifp:
            cooked = csv.reader(ifp)
            with self.conn.cursor() as cursor:
                cnt = 0
                for i, record in enumerate(cooked):
                    if i < header_lines:
                        continue
                    esql = sql.format(*record)
                    cursor.execute(esql)
                    cnt += 1
                self.conn.commit()
                print('affected_row_count\n%s' % cnt)
                self.logger.debug('affected_row_count=%s' % cnt)


################################################################################
def preprocess_sql(s):
    s = s.strip()
    # '-- ... $' comment is not work
    s = re.sub(re.compile('^--.*$', re.MULTILINE), '', s)
    # return [x.strip() for x in s.split(';') if x.strip()]
    sqls = list()
    sql_lines = list()
    for line in s.split('\n'):
        line = line.strip()
        if not line:
            continue
        sql_lines.append(line)
        if line.endswith(';') and sql_lines:
            sqls.append('\n'.join(sql_lines))
            sql_lines = list()
    if sql_lines:
        sqls.append('\n'.join(sql_lines))
    return sqls


################################################################################
# noinspection PyShadowingBuiltins
@func_log
def do_job(mcxt, argspec):
    db = None
    try:
        sql = None
        if argspec.file:
            if not os.path.exists(argspec.file):
                raise IOError('sql file "%s" not found' % argspec.file)
            with open(argspec.file, encoding=argspec.encoding) as ifp:
                sql = ifp.read()
        else:
            sql = argspec.execute
        if not sql:
            raise IOError('Invalid sql')

        conn_eles = (argspec.dbhost, argspec.dbport,
                     argspec.dbuser, argspec.dbpass, argspec.dbname)
        kwargs = {
            'logger': mcxt.logger,
            'encoding': argspec.encoding,
            'errors': 'strict',
        }
        if argspec.charset:
            kwargs['charset'] = argspec.charset

        if argspec.suppress_warning:
            warnings.simplefilter("ignore")
            kwargs['errors'] = 'ignore'

        if argspec.dbtype == 'mysql':
            db = MySQL(*conn_eles, **kwargs)
        elif argspec.dbtype == 'mssql':
            db = MSSQL(*conn_eles, **kwargs)
        # elif argspec.dbtype == 'oracle':
        #     db = Oracle(*conn_eles, **kwargs)
        else:
            raise NotImplementedError('RDB "%s" is not implemented yet'
                                      % argspec.dbtype)
        db.open()
        sqls = preprocess_sql(sql)
        for i, sql in enumerate(sqls):
            sql = sql.strip()
            try:
                if argspec.csv_file:
                    db.sql_execute_with_csv(sql, argspec.csv_file,
                                            argspec.header_lines)
                else:
                    if sql.lower().startswith('select'):
                        db.sql_select(sql)
                    else:
                        db.sql_execute(sql)
            except Exception as err:
                msg = f'[{i+1}] sql="{sql}"\nError: {str(err)}\n'
                sys.stderr.write(msg)
                return 5
        return 0
    except Exception as e:
        sys.stderr.write('[%s] Error: %s' % (argspec.dbtype, str(e)))
        return 9
    finally:
        if db is not None:
            db.close()


################################################################################
def _main(*args):
    try:
        with ModuleContext(
            owner='ARGOS-LABS',
            group='8',  # Storage Solutions
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='SQL',
            icon_path=get_icon_path(__file__),
            description='''SQL operation for RDB''',
            formatter_class=argparse.RawTextHelpFormatter
        ) as mcxt:
            # ######################################## for app dependent options
            # TODO: 현재 add_mutually_exclusive_group은 display_name 을 지원하지 않음
            # ag = mcxt.add_mutually_exclusive_group(required=True)
            mcxt.add_argument('--execute', '-e',
                              display_name='SQL string', show_default=True,
                              input_group='radio=SQL;default',
                              help='sql string to execute')
            mcxt.add_argument('--file', '-f',
                              display_name='SQL file', show_default=True,
                              input_method='fileread',
                              input_group='radio=SQL',
                              help='sql file to execute')
            mcxt.add_argument('--csv-file', '-c',
                              display_name='CSV bulk input',
                              input_method='fileread',
                              help='''input csv file if needed for sql insert
    in case insert use the column like these:
      insert into table (col1, col2, col3) values ('{{0}}',{{3}},'{{2}}')
        {{0}} - first csv column reference in --execute or --file''')
            mcxt.add_argument('--header-lines', nargs='?', type=int,
                              display_name='Exc # headers',
                              default=0, const=0,
                              help='''exclude header lines for input csv file
      (defaut is 0 no header, and 1 means one header line to exclude)''')
            mcxt.add_argument('--charset',
                              display_name='Character set',
                              help='Set Character set for DB Connection. If not set "utf8mb4" for MySQL and [[utf8]] for MSSQL. Oracle does not take charset.')
            mcxt.add_argument('--encoding',
                              default='utf8',
                              display_name='Encoding for CSV-file or SQL file',
                              help='Set encoding for CSV file for bulk inserting. Default is [[utf8]].')
            mcxt.add_argument('--suppress-warning', action='store_true',
                              display_name='Suppress Warning',
                              help='Suppress warnings for example data truncated for column.')
            # ##################################### for app dependent parameters
            # mcxt.add_argument('dbtype', choices=['mysql', 'mssql', 'oracle'],
            #                   display_name='RDB type',
            #                   help='database type. One of {"mysql", "mssql", "oracle"}')
            mcxt.add_argument('dbtype', choices=['mysql', 'mssql'],
                              display_name='RDB type',
                              help='database type. One of {"mysql", "mssql"}')
            mcxt.add_argument('dbhost',
                              display_name='DB Host',
                              help='DB host name or address')
            mcxt.add_argument('dbport', type=int,
                              display_name='DB Port',
                              help='DB host port')
            mcxt.add_argument('dbuser',
                              display_name='DB User',
                              help='DB user id')
            mcxt.add_argument('dbpass', input_method='password',
                              display_name='DB Password',
                              help='DB user password')
            mcxt.add_argument('dbname', help='DB name to use')
            argspec = mcxt.parse_args(args)
            return do_job(mcxt, argspec)
    except Exception as e:
        sys.stderr.write('[%s] Error: %s' % (argspec.dbtype, str(e)))
        return 98


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
