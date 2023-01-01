"""
====================================
 :mod:`argoslabs.search.sphinx`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module to use Sphinx
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/10/07]
#     - starting

################################################################################
import os
import sys
import csv
import pymysql
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class SphinxSearch(object):
    # ==========================================================================
    def __init__(self, host, port, query, index, columns, limit=10):
        self.host = host
        self.port = port
        self.query = query
        self.index = index
        self.columns = columns
        self.limit = limit
        # for internal
        self.db = None
        self.cursor = None
        self.cw = csv.writer(sys.stdout, lineterminator='\n')

    # ==========================================================================
    def open(self):
        try:
            self.db = pymysql.connect(
                host=self.host,
                port=self.port,
                user='', passwd='', charset='utf8', db=''
            )
            self.cursor = self.db.cursor()
        except Exception as err:
            raise ConnectionError(f'Cannot connect to Sphinx Search Engin with "{self.host}:{self.port}"')

    # ==========================================================================
    def close(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.db is not None:
            self.db.close()
            self.db = None

    # ==========================================================================
    def do_query(self):
        if self.db is None or self.cursor is None:
            raise RuntimeError(f'Engine is not opened')
        qry = f'SELECT {",".join(self.columns)} from {self.index} ' \
              f'WHERE MATCH(\'{self.query}\') limit {self.limit};'
        self.cursor.execute(qry)
        rows = self.cursor.fetchall()
        if rows:
            self.cw.writerow(self.columns)
        for row in rows:
            self.cw.writerow(row)

    # ==========================================================================
    def __enter__(self):
        self.open()
        return self

    # ==========================================================================
    def __exit__(self, *args):
        self.close()


################################################################################
@func_log
def do_search(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if not argspec.host:
            raise ValueError('Invalid Host')
        if not argspec.query:
            raise ValueError('Invalid Query')
        if not argspec.index:
            raise ValueError('Invalid Index')
        if not argspec.columns:
            raise ValueError('Invalid Column')
        with SphinxSearch(
            argspec.host,
            argspec.port,
            argspec.query,
            argspec.index,
            argspec.columns,
            argspec.limit
        ) as ss:
            ss.do_query()
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        if isinstance(err, ValueError):
            return 9
        return 99
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='8',  # Storage Solutions
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Sphinx Search',
        icon_path=get_icon_path(__file__),
        description='''Get search from Sphinx Search Engine''',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('host',
                          display_name='Host',
                          help='Host address or IP address')
        mcxt.add_argument('port',
                          display_name='Port',
                          type=int,
                          default=9312,
                          help='Host address or IP address, default is [[9312]]')
        mcxt.add_argument('query',
                          display_name='Query',
                          help='Search Query')
        mcxt.add_argument('index',
                          display_name='Index',
                          help='Index(table) name')
        mcxt.add_argument('columns',
                          display_name='Column',
                          nargs='+',
                          help='Column names to get')

        # ##################################### for app dependent options
        mcxt.add_argument('--limit',
                          display_name='Limit',
                          type=int,
                          default=10,
                          help='Number of results, default is [[10]]')
        argspec = mcxt.parse_args(args)
        return do_search(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
