"""
====================================
 :mod:`argoslabs.comm.redis`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/03/27]
#     - 그룹에 "8-Storage Solutions" 넣음
#  * [2019/08/13]
#     - starting

################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.comm.redis import _main as main
from alabs.common.util.vvnet import is_svc_opeded


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    svclist = [
        ('redis.argos-labs.com', 6379, '..'),
        ('127.0.0.1', 6379, None),
        ('10.211.55.2', 6379, None),
        ('192.168.1.249', 6379, None),
    ]
    host = None
    port = None
    passwd = None

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        for h, p, w in cls.svclist:
            if is_svc_opeded(h, p):
                cls.host = h
                cls.port = p
                cls.passwd = w
                break

    # ==========================================================================
    def test0010_failure(self):
        try:
            r = main('invalid_ip')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        try:
            r = main('127.0.0.1', 'invalid_op')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0030_failure(self):
        try:
            r = main('127.0.0.1', 'SET', 'global_var')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success_exists(self):
        outfile = 'stdout.txt'
        try:
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'EXIST', 'global_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'false')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0110_success_set(self):
        outfile = 'stdout.txt'
        try:
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'SET', 'global_var', 'my value',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'my value')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0120_success_get(self):
        outfile = 'stdout.txt'
        try:
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'GET', 'global_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'my value')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0130_success_exists(self):
        outfile = 'stdout.txt'
        try:
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'EXIST', 'global_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'true')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0140_success_exists(self):
        outfile = 'stdout.txt'
        try:
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'DELETE', 'global_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'true')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0150_success_exists(self):
        outfile = 'stdout.txt'
        try:
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'EXIST', 'global_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'false')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0200_success_list(self):
        outfile = 'stdout.txt'
        try:
            # DELETE list
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'DELETE', 'list_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            # list exists?
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'EXIST', 'list_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'false')
            # list get which does not exists?
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'LIST-Get', 'list_var', 'invalid_index',
                     '--outfile', outfile)
            self.assertTrue(r != 0)
            # list get which does not exists?
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'LIST-Get', 'list_var', '0',
                     '--outfile', outfile)
            self.assertTrue(r != 0)
            # list append? fail
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'LIST-Append', 'list_var',
                     '--outfile', outfile)
            self.assertTrue(r != 0)
            # list append
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'LIST-Append', 'list_var', 'one', 'two', 'three',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(int(out) == 3)
            # get one item
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'LIST-Get', 'list_var', '0',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'one')
            # get two items
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'LIST-Get', 'list_var', '1', '2',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'two\nthree')
            # set item
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'LIST-Set', 'list_var', '1', 'four',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'true')
            # get one item
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'LIST-Get', 'list_var', '1',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'four')
            # get length
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'LIST-Length', 'list_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(int(out) == 3)
            # list append
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'LIST-Append', 'list_var', 'four', 'five', 'four',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(int(out) == 6)
            # remove item in list
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'LIST-Remove', 'list_var', '-2', 'four',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(int(out) == 4)
            # get one item
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'LIST-Get', 'list_var', '1',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'four')
            # get length
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'LIST-Length', 'list_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(int(out) == 4)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0300_success_set(self):
        outfile = 'stdout.txt'
        try:
            # DELETE set
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'DELETE', 'set_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            # set exists?
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'EXIST', 'set_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'false')
            # set append? fail
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'SET-Add', 'set_var',
                     '--outfile', outfile)
            self.assertTrue(r != 0)
            # set append
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'SET-Add', 'set_var', 'one', 'two', 'three', 'two',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(int(out) == 3)
            # is exists item
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'SET-IsMember', 'set_var', 'two',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'true')
            # is exists item
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'SET-IsMember', 'set_var', 'nine',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'false')
            # get length
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'SET-Length', 'set_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(int(out) == 3)
            # set append
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'SET-Add', 'set_var', 'four', 'five', 'four',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(int(out) == 5)
            # remove item in set
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'SET-Remove', 'set_var', 'two', 'four',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(int(out) == 3)
            # is exists item
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'SET-IsMember', 'set_var', 'four',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'false')
            # get length
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'SET-Length', 'set_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(int(out) == 3)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0400_success_hash(self):
        outfile = 'stdout.txt'
        try:
            # DELETE hash
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'DELETE', 'hash_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            # hash exists?
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'EXIST', 'hash_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'false')
            # hash append? fail
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'HASH-Get', 'hash_var', 'invalid-key',
                     '--outfile', outfile)
            self.assertTrue(r != 0)
            # hash set
            for i in range(4):
                r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                         'HASH-Set', 'hash_var', 'key%s' % i, 'value%s' % i,
                         '--outfile', outfile)
                self.assertTrue(r == 0)
                with open(outfile) as ifp:
                    out = ifp.read()
                    print(out)
                    self.assertTrue(out == 'true')
            # hash get?
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'HASH-Get', 'hash_var', 'key2',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'value2')
            # hash exists?
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'HASH-Exists', 'hash_var', 'key2',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'true')
            # get length
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'HASH-Length', 'hash_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(int(out) == 4)
            # hash delete
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'HASH-Delete', 'hash_var', 'key1', 'key3',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'true')
            # hash exists?
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'HASH-Exists', 'hash_var', 'key1',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'false')
            # get length
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'HASH-Length', 'hash_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(int(out) == 2)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0500_success_queue(self):
        outfile = 'stdout.txt'
        try:
            # DELETE queue
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'DELETE', 'queue_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            # queue exists?
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'EXIST', 'queue_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(out == 'false')
            # queue length
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'QUEUE-Length', 'queue_var',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                out = ifp.read()
                print(out)
                self.assertTrue(int(out) == 0)
            # queue get which does not exists?
            r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                     'QUEUE-Pop', 'queue_var', '--timeout', '2',
                     '--outfile', outfile)
            self.assertTrue(r != 0)
            # queue push
            for i in range(3):
                r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                         'QUEUE-Push', 'queue_var', 'Queue-%s' % i,
                         '--outfile', outfile)
                self.assertTrue(r == 0)
                with open(outfile) as ifp:
                    out = ifp.read()
                    print(out)
                    self.assertTrue(int(out) == i + 1)
            # queue pop
            for i in range(4):
                r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                         'QUEUE-Pop', 'queue_var', '--timeout', '2',
                         '--outfile', outfile)
                if i < 3:
                    self.assertTrue(r == 0)
                    with open(outfile) as ifp:
                        out = ifp.read()
                        print(out)
                        self.assertTrue(out == 'Queue-%s' % i)
                else:
                    self.assertTrue(r != 0)
                # queue length
                qcnt = 2 - i
                if qcnt < 0:
                    qcnt = 0
                r = main(TU.host, '--port', TU.port, '--passwd', TU.passwd,
                         'QUEUE-Length', 'queue_var',
                         '--outfile', outfile)
                self.assertTrue(r == 0)
                with open(outfile) as ifp:
                    out = ifp.read()
                    print(out)
                    self.assertTrue(int(out) == qcnt)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
