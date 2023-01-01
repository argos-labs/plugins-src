"""
====================================
 :mod:`argoslabs.data.mongodb.tests.test_me`
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
#  * [2021/04/01]
#     - 그룹에 "4-Data Science" 넣음
#  * [2021/02/15]
#     - find with ObjectId
#  * [2021/02/12]
#     - return list of id for insert op
#  * [2020/12/02]
#     - starting

################################################################################
import os
import sys
import json
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.data.mongodb import _main as main


################################################################################
class TU(TestCase):
    host = '192.168.35.241'
    port = '27017'
    user = ''       # 'devroot'
    passwd = ''     # 'devroot'

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        ...

    # ==========================================================================
    def test0010_fail_empty(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            _ = main('invalid.script')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success_drop_db(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            r = main('drop_database',
                     TU.host, TU.port, 'argos', '',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == '1')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0110_success_dbs(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            r = main('list_database_names',
                     TU.host, TU.port, '', '',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs.find('admin') >= 0 and rs.find('argos') < 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0120_success_find_0(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            r = main('list_database_names',
                     TU.host, TU.port, '', '',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs.find('admin') >= 0 and rs.find('config') >= 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0130_success_count(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            r = main('count',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == '0')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0140_success_insert(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            r = main('insert',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--outfile', of,
                     )
            self.assertTrue(r == 99)

            r = main('insert',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--input-json', 'input_one.json',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                TU.inserted_id = rs
            self.assertTrue(rs and len(rs.split('\n')) == 1)

            r = main('count',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == '1')

            r = main('insert',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--input-json', 'input_many.json',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs and len(rs.split('\n')) == 2)

            r = main('count',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == '3')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0150_success_find(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            # find all
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(len(rj) == 3)

            # find one record
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"author": "Jerry"}',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(len(rj) == 1 and rj[0]['author'] == 'Jerry')

            # find two record
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"author": {"$gt": "Jerry"}}',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(len(rj) == 2)

            # multi criteria
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter',
                     '{"author": {"$gt": "Jerry"}, "text": {"$regex": "second.*post"}}',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(len(rj) == 1 and rj[0]['author'] == 'Tom')

            # find with projection
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"author": {"$gt": "Jerry"}}',
                     '--find-projection', '{"text":1, "author":1}',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(len(rj) == 2 and 'tags' not in rj[0])

            # find with sort
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--find-sort', '[("author", -1)]',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(len(rj) == 3 and rj[0]['author'] == 'Tom')

            # find with skip
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--find-sort', '[("author", -1)]',
                     '--find-skip', '1',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(len(rj) == 2 and rj[0]['author'] == 'Mike')

            # find with skip and limit
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--find-sort', '[("author", -1)]',
                     '--find-skip', '1',
                     '--find-limit', '1',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(len(rj) == 1 and rj[0]['author'] == 'Mike')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0155_success_find_id(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            # find one record
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"_id": ObjectId("%s")}' % TU.inserted_id,
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(len(rj) == 1 and rj[0]['author'] == 'Mike')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0160_success_find_one(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            # find_one with projection
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--one-document',
                     '--filter', '{"author": {"$gt": "Jerry"}}',
                     '--find-projection', '{"text":1, "author":1}',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(rj['author'] == 'Mike')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0170_success_update(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            # update many
            r = main('update',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"date": {"$gte": "2020/01/09"}}',
                     '--input-json', 'update_date.json',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == '2')

            # find for validation
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"date": {"$gte": "2020/01/09"}}',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(len(rj) == 2 and rj[0]['date'] == '2020/02/22' and
                            rj[0]['update'] == 'update_test')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0180_success_update_one(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            # update one
            r = main('update',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"author": {"$gte": "M"}}',
                     '--input-json', 'update_one.json',
                     '--one-document',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == '1')

            # find for validation
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"author": {"$gte": "M"}}',
                     '--find-sort', '[("author", 1)]',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(len(rj) == 2 and rj[0]['date'] == '2020/02/23' and
                            rj[0]['author'] == 'Mike')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0190_success_update_upsert(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            # update without upsert
            r = main('update',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"author": {"$gte": "X"}}',
                     '--input-json', 'update_new.json',
                     '--one-document',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == '0')

            # find for validation
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"author": {"$gte": "Z"}}',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(not rj)

            # update with upsert
            r = main('update',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"author": {"$gte": "X"}}',
                     '--input-json', 'update_new.json',
                     '--is-upsert',
                     '--one-document',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == '1')

            # find for validation
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"author": {"$gte": "Z"}}',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(len(rj) == 1 and rj[0]['author'] == 'Zebra')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0200_success_delete(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            # delete many
            r = main('delete',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"author": {"$gte": "T"}}',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == '2')

            # find for validation
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"author": {"$gte": "T"}}',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(not rj)

            # delete one
            r = main('delete',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"author": {"$gte": "A"}}',
                     '--one-document',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == '1')

            # find for validation
            r = main('find',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--filter', '{"author": {"$gte": "A"}}',
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
                rj = json.loads(rs)
            self.assertTrue(len(rj) == 1 and rj[0]['author'] in ('Jerry', 'Mike'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0950_success_drop_collection(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        of = 'stdout.txt'
        try:
            r = main('collection_names',
                     TU.host, TU.port, 'invaliddb', '',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(not rs)

            r = main('collection_names',
                     TU.host, TU.port, 'argos', '',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs.find('blogs') >= 0)

            r = main('drop_collection',
                     TU.host, TU.port, 'argos', 'blogs',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == '1')

            r = main('collection_names',
                     TU.host, TU.port, 'argos', '',
                     '--user', TU.user, '--passwd', TU.passwd,
                     '--outfile', of,
                     )
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs.find('blogs') < 0)

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
