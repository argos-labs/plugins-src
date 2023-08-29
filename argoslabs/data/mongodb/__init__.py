"""
====================================
 :mod:`argoslabs.data.mongodb`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module to use Selenium
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/07/30]
#     - Change group to 8 : "Storage Solution"
#  * [2021/04/01]
#     - 그룹에 "4-Data Science" 넣음
#  * [2021/02/15]
#     - find with ObjectId
#  * [2021/02/12]
#     - return list of id for insert op
#  * [2021/02/08]
#     - starting

################################################################################
import os
import sys
import traceback
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId


################################################################################
class MongoDB(object):
    # ==========================================================================
    OPS = [
        'find',
        'insert',
        'update',
        'delete',
        'count',
        'collection_names',
        'list_database_names',
        'drop_database',
        'drop_collection',
    ]

    # ==========================================================================
    def __init__(self, host, port, dbname, collection, user=None, passwd=None):
        self.host = host
        self.port = int(port)
        self.dbname = dbname
        self.collection = collection
        self.user = user
        self.passwd = passwd
        # for internal
        self.mc = None
        self.mdb = None
        self.is_opened = False
        self.dbs = []
        self.db = None
        self.tbl = None
        self.result = None

    # ==========================================================================
    def open(self):
        if self.user or self.passwd:
            connstr = f'mongodb://{self.user}:{self.passwd}@{self.host}:{self.port}'
        else:
            connstr = f'mongodb://{self.host}:{self.port}'
        self.mc = MongoClient(connstr)
        self.dbs = self.mc.list_database_names()
        if self.dbname:
            self.db = self.mc[self.dbname]
        if self.collection:
            self.tbl = self.db[self.collection]
        self.is_opened = True

    # ==========================================================================
    def close(self):
        if not self.is_opened:
            return
        self.mc.close()
        self.is_opened = False

    # ==========================================================================
    def __enter__(self):
        self.open()
        return self

    # ==========================================================================
    def __exit__(self, *args):
        self.close()

    # ==========================================================================
    def drop_database(self):
        self.result = self.mc.drop_database(self.dbname)
        # return self.result  # None even at successful case
        return 1

    # ==========================================================================
    def insert(self, doc_or_docs):
        if self.tbl is None:
            raise ReferenceError('Invalid Collection')
        self.result = self.tbl.insert(doc_or_docs)
        if not self.result:
            return ''
        if not isinstance(self.result, (list, tuple)):
            return str(self.result)
        return '\n'.join([str(x) for x in self.result])

    # ==========================================================================
    def update(self, _filter, _update, _upsert=False, one_document=False):
        if self.tbl is None:
            raise ReferenceError('Invalid Collection')
        if not one_document:
            r = self.tbl.update_many(_filter, _update, upsert=_upsert)
        else:
            r = self.tbl.update_one(_filter, _update, upsert=_upsert)
        rc = r.modified_count
        if r.upserted_id is not None:
            rc += 1
        self.result = rc
        return rc

    # ==========================================================================
    def delete(self, _filter, one_document=False):
        if self.tbl is None:
            raise ReferenceError('Invalid Collection')
        if not one_document:
            self.result = self.tbl.delete_many(_filter)
        else:
            self.result = self.tbl.delete_one(_filter)
        return self.result.deleted_count

    # ==========================================================================
    def find(self, _filter=None, _projection=None, _skip=0, _limit=0, _sort=None,
             one_document=False):
        if self.tbl is None:
            raise ReferenceError('Invalid Collection')
        if not one_document:
            self.result = []
            for c in self.tbl.find(_filter, _projection, _skip, _limit, sort=_sort):
                self.result.append(c)
            return dumps(self.result, indent=2)
        else:
            self.result = self.tbl.find_one(_filter, _projection)
            return dumps(self.result, indent=2)

    # ==========================================================================
    def count(self):
        if self.tbl is None:
            raise ReferenceError('Invalid Collection')
        return self.tbl.count()

    # ==========================================================================
    def collection_names(self):
        return [col_name for col_name in self.db.collection_names()]

    # ==========================================================================
    def drop_collection(self):
        if self.tbl is None:
            raise ReferenceError('Invalid Collection')
        self.tbl.drop()
        return 1


################################################################################
@func_log
def do_mongo(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        with MongoDB(argspec.host, argspec.port, argspec.dbname,
                     argspec.collection,
                     user=argspec.user, passwd=argspec.passwd) as mdb:
            _filter = argspec.filter
            if _filter:
                try:
                    _filter = loads(_filter)
                except:
                    _filter = eval(_filter)

            if argspec.op == 'list_database_names':
                print('\n'.join(mdb.dbs), end='')
            elif argspec.op == 'count':
                print(mdb.count(), end='')
            elif argspec.op in ('insert', 'update'):
                if not argspec.input_json:
                    raise IOError(f'Need "Input JSON file"')
                if not os.path.exists(argspec.input_json):
                    raise IOError(f'Invalid "Input JSON file" "{argspec.input_json}"')
                with open(argspec.input_json, encoding=argspec.encoding) as ifp:
                    jstr = ifp.read()
                    js = loads(jstr)
                if argspec.op == 'insert':
                    r = mdb.insert(js)
                else:
                    r = mdb.update(_filter, js, argspec.is_upsert,
                                   one_document=argspec.one_document)
                print(r, end='')
            elif argspec.op == 'drop_database':
                print(mdb.drop_database(), end='')
            elif argspec.op == 'find':
                _projection = argspec.find_projection
                if _projection:
                    _projection = loads(_projection)
                _sort = argspec.find_sort
                if _sort:
                    _sort = eval(_sort)
                _skip = argspec.find_skip
                _skip = int(_skip) if _skip else 0
                _limit = argspec.find_limit
                _limit = int(_limit) if _limit else 0

                rjstr = mdb.find(_filter=_filter, _projection=_projection,
                                 _skip=_skip, _limit=_limit,
                                 _sort=_sort,
                                 one_document=argspec.one_document)
                print(rjstr, end='')
            elif argspec.op == 'delete':
                r = mdb.delete(_filter, one_document=argspec.one_document)
                print(r, end='')
            elif argspec.op == 'collection_names':
                r = mdb.collection_names()
                print('\n'.join(r), end='')
            elif argspec.op == 'drop_collection':
                r = mdb.drop_collection()
                print(r, end='')

            else:
                raise ValueError(f'Invalid operation "{argspec.op}"')

        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='8',  # Storage Solution
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='MongoDB',
        icon_path=get_icon_path(__file__),
        description='''MongoDB plugin''',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          choices=MongoDB.OPS,
                          default=MongoDB.OPS[0],
                          display_name='Operation',
                          help='Operation for MongoDB')
        mcxt.add_argument('host',
                          display_name='Host',
                          help='Host name or IP Address for MongoDB')
        mcxt.add_argument('port',
                          display_name='Port',
                          default=27017, type=int,
                          help='Port number for MongoDB, default is [[27017]]')
        mcxt.add_argument('dbname',
                          display_name='DB Name',
                          help='Database Name for MongoDB')
        mcxt.add_argument('collection',
                          display_name='Collection Name',
                          help='Collection Name for MongoDB')

        # ##################################### for app dependent options
        mcxt.add_argument('--user',
                          display_name='User',
                          show_default=True,
                          help='User for MongoDB Authentication')
        mcxt.add_argument('--passwd',
                          display_name='Password',
                          show_default=True, input_method='password',
                          help='Password for MongoDB Authentication')
        mcxt.add_argument('--input-json',
                          display_name='Input JSON file',
                          input_method='fileread',
                          help='JSON file for inserting')
        mcxt.add_argument('--encoding',
                          display_name='Encoding',
                          default='utf-8',
                          help='Encoding for JSON file, default is [[utf-8]]')
        mcxt.add_argument('--one-document', action='store_true',
                          display_name='One Doc',
                          help='Apply only one document for find, update, delete')
        mcxt.add_argument('--filter',
                          display_name='Filter',
                          help='Filter for find, update, delete')
        mcxt.add_argument('--find-projection',
                          display_name='Find Projection',
                          help='Projection for find')
        mcxt.add_argument('--find-sort',
                          display_name='Find Sort',
                          help='Sort for find')
        mcxt.add_argument('--find-skip',
                          display_name='Find Skip',
                          type=int,
                          help='Skip for find, default is [[0]]')
        mcxt.add_argument('--find-limit',
                          display_name='Find Limit',
                          type=int,
                          help='Limit for find, default is [[0]]')
        mcxt.add_argument('--is-upsert', action='store_true',
                          display_name='Is Upsert',
                          help='When this flag is set upsert flag is true for update')

        argspec = mcxt.parse_args(args)
        return do_mongo(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
