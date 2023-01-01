"""
====================================
 :mod:argoslabs.data.oracle
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
import cx_Oracle
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
def oracle_dll_path():
    md = os.path.abspath(os.path.dirname(__file__))
    os.environ['PATH'] = md + os.pathsep + os.environ['PATH']
    os.putenv('NLS_LANG', '.UTF8')
    return True


################################################################################
class Oracle(object):
    # ==========================================================================
    def __init__(self, dbhost, dbport, dbuser, dbpass, dbname,
                 logger, charset='urf8', encoding='utf8', errors='strict'):
        self.host, self.port, self.user, self.passwd, self.db, self.charset, \
        self.encoding, self.errors \
            = dbhost, dbport, dbuser, dbpass, dbname, charset, encoding, errors
        self.logger = logger
        # for internal
        self.is_opened = False
        self.conn = None
        oracle_dll_path()

    # ==========================================================================
    def open(self):
        self.logger.debug('Oracle.open: trying to open')
        self.conn = cx_Oracle.connect(
            '{user}/{password}@//{host}:{port}/{database}'.format(
                host=self.host,
                user=self.user,
                password=self.passwd,
                port=int(self.port),
                database=self.db,
            ) )  # , mode=cx_Oracle.SYSDBA)
        # TODO : how to set charset in Oracle
        self.is_opened = True
        self.logger.debug('Oracle.open: opened!')
        return self.is_opened

    # ==========================================================================
    def close(self):
        self.logger.debug('Oracle.open: trying to close')
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.is_opened = False
            self.logger.debug('Oracle.close: closed!')

    # ==========================================================================
    def sql_execute(self, sql):
        self.logger.debug('Oracle.sql_execute: sql=<%s>' % sql)
        with self.conn.cursor() as cursor:
            cursor.execute(sql.encode('utf8'))
            print('affected_row_count\n%s' % cursor.rowcount)
            self.logger.debug('affected_row_count=%s' % cursor.rowcount)
        self.conn.commit()

    # ==========================================================================
    def sql_select(self, sql):
        self.logger.debug('Oracle.sql_select: sql=<%s>' % sql)
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
        self.logger.debug('Oracle.sql_execute_with_csv: sql=<%s>, csv_file=%s'
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
                    cursor.execute(esql.encode('utf8'))
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

        db = Oracle(*conn_eles, **kwargs)
        db.open()
        sqls = preprocess_sql(sql)
        for i, sql in enumerate(sqls):
            sql = sql.strip()
            sql = sql.rstrip(';')
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
                msg = f'[{i+1}] sql="{sql}" Error: {str(err)}\n'
                sys.stderr.write(msg)
        return 0
    except Exception as e:
        sys.stderr.write('[%s] Error: %s' % ('Oracle', str(e)))
        return 9
    finally:
        if db is not None:
            db.close()


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='8',  # Storage Solutions
        version='1.0',
        platform=['windows',],
        output_type='text',
        display_name='Oracle SQL',
        icon_path=get_icon_path(__file__),
        description='''SQL operation for Oracle RDB''',
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
                          input_group='radio=SQL',
                          input_method='fileread',
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


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
