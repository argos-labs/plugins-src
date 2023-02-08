#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.sqlite`
======0==============================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for sqlite
"""
#
# Authors
# ===========
#
# * Kyobong An
#
# Change Log
# --------
#  * [2023/01/05]
#  csv file 안에 따옴표(')가 들어갈 경우 에러 발생. Convert single quotes을 옵션으로 만듬. 기본값은 제거
#  * [2021/07/13]
#   sql file로 받을떄 executescript를 사용하고 싶었지만 sql file내에 SELECT문이 있을 경우 제대로 작동안할수있다./
#   기존 SQL의 방법을 가져옴
#  * [2021/07/05]
#   start


################################################################################
import os
import re
import sys
import csv
import sqlite3
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class SQLite(object):
    # ==========================================================================
    def __init__(self, argspec, logger, encoding='utf8', errors='strict'):
        self.dbfile = argspec.dbfile
        self.encoding = encoding
        self.logger = logger
        self.errors = errors
        # for internal
        self.is_opened = False
        self.conn = None

    def open(self):
        self.logger.debug('SQLite.open: trying to open')
        self.conn = sqlite3.connect(self.dbfile)
        self.is_opened = True
        self.logger.debug('SQLite.open: opened!')
        return self.is_opened

    # ==========================================================================
    def close(self):
        self.logger.debug('SQLite.open: trying to close')
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.is_opened = False
            self.logger.debug('SQLite.close: closed!')

    # # ==========================================================================
    # def sql_excutescript(self, sql):
    #     self.logger.debug('SQLite.sql_excutescript: sql=<%s>' % sql)
    #     cursor = self.conn.cursor()
    #     cursor.executescript(sql)
    #     print('affected_row_count\n%s' % cursor.rowcount)
    #     self.logger.debug('affected_row_count=%s' % cursor.rowcount)
    #     self.conn.commit()

    # ==========================================================================
    def sql_excute(self, sql):
        self.logger.debug('SQLite.sql_excute: sql=<%s>' % sql)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        print('affected_row_count\n %s' % cursor.rowcount)
        self.logger.debug('affected_row_count=%s' % cursor.rowcount)
        self.conn.commit()

    # ==========================================================================
    def sql_select(self, sql):
        self.logger.debug('SQLite.sql_select: sql=<%s>' % sql)
        cursor = self.conn.cursor()
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
    def sql_execute_with_csv(self, sql, csv_file, header_lines=0, single_quotes=''):
        self.logger.debug('SQLite.sql_execute_with_csv: sql=<%s>, csv_file=%s'
                          % (sql, csv_file))
        if not os.path.exists(csv_file):
            raise IOError('CSV file "%s" not found' % csv_file)
        with open(csv_file, 'r', encoding=self.encoding, errors=self.errors) as ifp:
            cooked = csv.reader(ifp)
            cursor = self.conn.cursor()
            cnt = 0
            for i, record in enumerate(cooked):
                if i < header_lines:
                    continue
                record = [i.replace("'", single_quotes) for i in record]
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
    return [x.strip() for x in s.split(';') if x.strip()]


################################################################################
@func_log
def do_sqlite(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    db = None
    try:
        if argspec.file:
            if not os.path.exists(argspec.file):
                raise IOError('sql file "%s" not found' % argspec.file)
            with open(argspec.file, encoding=argspec.encoding) as ifp:
                sql = ifp.read()
        else:
            sql = argspec.execute
        if not sql:
            raise IOError('Invalid sql')
        db = SQLite(argspec, logger=mcxt.logger)
        db.open()
        sqls = preprocess_sql(sql)
        for sql in sqls:
            if argspec.csv_file:
                db.sql_execute_with_csv(sql, argspec.csv_file, argspec.header_lines, argspec.single_quotes)
            else:
                if sql.lower().find('select') >= 0:
                    db.sql_select(sql)
                else:
                    db.sql_excute(sql)

        return 0
    except Exception as e:
        sys.stderr.write('[%s] Error: %s' % (argspec.dbtype, str(e)))
        return 9
    finally:
        if db is not None:
            db.close()


# ##########################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='8',  # Storage Solutions
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='SQLite',
        icon_path=get_icon_path(__file__),
        description='''SQLite plugin''',
    ) as mcxt:
        # ##################################### for app dependent options
        # ----------------------------------------------------------------------
        mcxt.add_argument('--file', '-f',
                          display_name='SQL file', show_default=True,
                          input_method='fileread',
                          input_group='radio=file_or_value;default',
                          help='sql file to execute')
        mcxt.add_argument('--execute', '-e',
                          display_name='SQL string', show_default=True,
                          input_group='radio=file_or_value',
                          help='sql string to excutescript')
        mcxt.add_argument('--csv-file', '-c',
                          display_name='CSV bulk input',
                          input_group='CSV option',
                          input_method='fileread',
                          help='''input csv file if needed for sql insert
        in case insert use the column like these:
          insert into table (col1, col2, col3) values ('{{0}}',{{3}},'{{2}}')
            {{0}} - first csv column reference in --execute or --file''')
        mcxt.add_argument('--header-lines', nargs='?', type=int,
                          display_name='Exc # headers',
                          input_group='CSV option',
                          default=0, const=0,
                          help='''exclude header lines for input csv file
          (defaut is 0 no header, and 1 means one header line to exclude)''')
        mcxt.add_argument('--single-quotes',
                          input_group='CSV option',
                          default='',
                          display_name='Convert single quotes',
                          help='Converting single quotes due to single quote recognition issue in SQLite. Default is Remove.')
        mcxt.add_argument('--encoding',
                          input_group='CSV option',
                          default='utf8',
                          display_name='Encoding for CSV-file or SQL file',
                          help='Set encoding for CSV file for bulk inserting. Default is [[utf8]].')
        # ##################################### for app dependent parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('dbfile', nargs='?',
                          display_name='DBfile',
                          input_method='fileread',
                          help='open db')
        argspec = mcxt.parse_args(args)
        return do_sqlite(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
