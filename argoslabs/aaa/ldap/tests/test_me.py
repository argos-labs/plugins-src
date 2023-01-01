#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.aaa.ldap.tests.test_me`
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
#  * [2021/03/25]
#     - 그룹에 "9-Utility Tools" 넣음
#     - comment out for "server down"
#  * [2019/11/24]
#     - starting

################################################################################
import os
import sys
import csv
from unittest import TestCase
from argoslabs.aaa.ldap import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0020_empty_parameter(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0030_incomleted_parameter(self):
        try:
            _ = main('unknown', 'param2', 'user')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0040_invalid_op(self):
        try:
            _ = main('unknown', 'router.vivans.net', 'invalid@ad.vivans.net', 'pass')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0050_invalid_server(self):
        stdout = 'stdout.txt'
        try:
            r = main('Get', '10.211.55.99', 'invalid@ad.vivans.net', 'pass',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                out = ifp.read()
            self.assertTrue(out == 'server down')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # # ==========================================================================
    # def test0060_invalid_user(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('Get', 'router.vivans.net', 'invalid@ad.vivans.net', 'pass',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout) as ifp:
    #             out = ifp.read()
    #         self.assertTrue(out == 'invalid credential')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #
    # # ==========================================================================
    # def test0070_invalid_domain(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('Get', 'router.vivans.net', 'administrator@invalid.example.net', 'pass',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout) as ifp:
    #             out = ifp.read()
    #         self.assertTrue(out == 'invalid credential')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #
    # # ==========================================================================
    # def test0080_invalid_pass(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('Get', 'router.vivans.net', 'administrator@ad.vivans.net', 'pass',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout) as ifp:
    #             out = ifp.read()
    #         self.assertTrue(out == 'invalid credential')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #
    # # ==========================================================================
    # def test0100_success_get(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('Get', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         rr = []
    #         with open(stdout, 'r', encoding='utf8') as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (29,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) == 2)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #
    # # ==========================================================================
    # def test0110_error_search(self):
    #     stdout = 'stdout.txt'
    #     stderr = 'stderr.txt'
    #     try:
    #         r = main('Search', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--outfile', stdout, '--errfile', stderr)
    #         self.assertTrue(r != 0)
    #         with open(stderr) as ifp:
    #             out = ifp.read()
    #         self.assertTrue(out.strip() == '"Attributes to search" must be provided')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #         if os.path.exists(stderr):
    #             os.remove(stderr)
    #
    # # ==========================================================================
    # def test0120_success_search(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('Search', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--search-attributes', 'name=test*',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         rr = []
    #         with open(stdout, 'r', encoding='utf8') as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (29,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) == 2)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #
    # # ==========================================================================
    # def test0130_success_search_no_result(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('Search', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--search-attributes', 'name=mytest*',
    #                  # '--search-attributes', 'displayname=*',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         # print(out)
    #         self.assertTrue('no result')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #
    # # ==========================================================================
    # def test0140_error_create(self):
    #     stdout = 'stdout.txt'
    #     stderr = 'stderr.txt'
    #     try:
    #         r = main('Create', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--search-attributes', 'name=mytest*',
    #                  '--outfile', stdout, '--errfile', stderr)
    #         self.assertTrue(r != 0)
    #         with open(stderr) as ifp:
    #             out = ifp.read()
    #         self.assertTrue(out.strip() == '"User to create" must be provided')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #         if os.path.exists(stderr):
    #             os.remove(stderr)
    #
    # # ==========================================================================
    # def test0150_error_create(self):
    #     stdout = 'stdout.txt'
    #     stderr = 'stderr.txt'
    #     try:
    #         r = main('Create', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--create-user', 'mytestuser01',
    #                  '--outfile', stdout, '--errfile', stderr)
    #         self.assertTrue(r != 0)
    #         with open(stderr) as ifp:
    #             out = ifp.read()
    #         self.assertTrue(out.strip() == '"Password to create" must be provided')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #         if os.path.exists(stderr):
    #             os.remove(stderr)
    #
    # # ==========================================================================
    # def test0160_success_create(self):
    #     stdout = 'stdout.txt'
    #     stderr = 'stderr.txt'
    #     try:
    #         user = 'mytestuser01'
    #         r = main('Create', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--create-user', user,
    #                  '--create-pass', 'mytestuser!@',
    #                  '--outfile', stdout, '--errfile', stderr)
    #         self.assertTrue(r == 0)
    #         with open(stdout, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         rr = []
    #         with open(stdout, 'r', encoding='utf8') as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (30,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) == 2)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #         if os.path.exists(stderr):
    #             os.remove(stderr)
    #
    # # ==========================================================================
    # def test0170_failure_create_already_exists(self):
    #     stdout = 'stdout.txt'
    #     stderr = 'stderr.txt'
    #     try:
    #         user = 'mytestuser01'
    #         r = main('Create', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--create-user', user,
    #                  '--create-pass', 'mytestuser!@',
    #                  '--outfile', stdout, '--errfile', stderr)
    #         self.assertTrue(r != 0)
    #         with open(stderr, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         self.assertTrue(out.find('Already exists') >= 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #         if os.path.exists(stderr):
    #             os.remove(stderr)
    #
    # # ==========================================================================
    # def test0180_success_create2(self):
    #     stdout = 'stdout.txt'
    #     stderr = 'stderr.txt'
    #     try:
    #         user = 'mytestuser02'
    #         r = main('Create', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--create-user', user,
    #                  '--create-pass', 'mytestuser!#',
    #                  '--outfile', stdout, '--errfile', stderr)
    #         self.assertTrue(r == 0)
    #         with open(stdout, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         rr = []
    #         with open(stdout, 'r', encoding='utf8') as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (30,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) == 2)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #         if os.path.exists(stderr):
    #             os.remove(stderr)
    #
    # # ==========================================================================
    # def test0190_success_search_2(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('Search', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--search-attributes', 'name=mytest*',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         rr = []
    #         with open(stdout, 'r', encoding='utf8') as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (30,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) == 3)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #
    # # # ==========================================================================
    # # def test0200_invalid_modify(self):
    # #     stdout = 'stdout.txt'
    # #     stderr = 'stderr.txt'
    # #     try:
    # #         user = 'mytestuser02'
    # #         r = main('Modify', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    # #                  '--modify-user', user,
    # #                  '--outfile', stdout, '--errfile', stderr)
    # #         self.assertTrue(r != 0)
    # #         with open(stderr, encoding='utf-8') as ifp:
    # #             out = ifp.read()
    # #         self.assertTrue(out.strip() == '"Old Attr to modify" must be provided')
    # #     except Exception as e:
    # #         sys.stderr.write('\n%s\n' % str(e))
    # #         self.assertTrue(False)
    # #     finally:
    # #         if os.path.exists(stdout):
    # #             os.remove(stdout)
    # #         if os.path.exists(stderr):
    # #             os.remove(stderr)
    #
    # # ==========================================================================
    # def test0210_invalid_modify(self):
    #     stdout = 'stdout.txt'
    #     stderr = 'stderr.txt'
    #     try:
    #         user = 'mytestuser02'
    #         r = main('Modify', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--modify-user', user,
    #                  '--outfile', stdout, '--errfile', stderr)
    #         self.assertTrue(r != 0)
    #         with open(stderr, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         self.assertTrue(out.strip() == '"New Attr to modify" must be provided')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #         if os.path.exists(stderr):
    #             os.remove(stderr)
    #
    # # ==========================================================================
    # def test0220_success_modify(self):
    #     stdout = 'stdout.txt'
    #     stderr = 'stderr.txt'
    #     try:
    #         user = 'mytestuser02'
    #         r = main('Modify', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--modify-user', user,
    #                  '--modify-to', 'description=my new description = this!',
    #                  '--outfile', stdout, '--errfile', stderr)
    #         self.assertTrue(r == 0)
    #         rr = []
    #         with open(stdout, 'r', encoding='utf8') as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (30,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) == 2)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #         if os.path.exists(stderr):
    #             os.remove(stderr)
    #
    # # ==========================================================================
    # def test0230_invalid_delete(self):
    #     stdout = 'stdout.txt'
    #     stderr = 'stderr.txt'
    #     try:
    #         user = 'mytestuser02'
    #         r = main('Delete', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--outfile', stdout, '--errfile', stderr)
    #         self.assertTrue(r != 0)
    #         with open(stderr, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         self.assertTrue(out.strip() == '"User to delete" must be provided')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #         if os.path.exists(stderr):
    #             os.remove(stderr)
    #
    # # ==========================================================================
    # def test0240_invalid_delete_user(self):
    #     stdout = 'stdout.txt'
    #     stderr = 'stderr.txt'
    #     try:
    #         user = 'mytestuser0999'
    #         r = main('Delete', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--delete-user', user,
    #                  '--outfile', stdout, '--errfile', stderr)
    #         self.assertTrue(r != 0)
    #         with open(stderr, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         self.assertTrue(out.find('No such object') >= 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #         if os.path.exists(stderr):
    #             os.remove(stderr)
    #
    # # ==========================================================================
    # def test0250_success_delete_user(self):
    #     stdout = 'stdout.txt'
    #     stderr = 'stderr.txt'
    #     try:
    #         user = 'mytestuser01'
    #         r = main('Delete', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--delete-user', user,
    #                  '--outfile', stdout, '--errfile', stderr)
    #         self.assertTrue(r == 0)
    #         with open(stdout, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         self.assertTrue(out == 'deleted')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #         if os.path.exists(stderr):
    #             os.remove(stderr)
    #
    # # ==========================================================================
    # def test0260_success_search_1(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('Search', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--search-attributes', 'name=mytest*',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         rr = []
    #         with open(stdout, 'r', encoding='utf8') as ifp:
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 self.assertTrue(len(row) in (30,))
    #                 rr.append(row)
    #         self.assertTrue(len(rr) == 2)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #
    # # ==========================================================================
    # def test0270_success_delete_user(self):
    #     stdout = 'stdout.txt'
    #     stderr = 'stderr.txt'
    #     try:
    #         user = 'mytestuser02'
    #         r = main('Delete', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--delete-user', user,
    #                  '--outfile', stdout, '--errfile', stderr)
    #         self.assertTrue(r == 0)
    #         with open(stdout, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         self.assertTrue(out == 'deleted')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)
    #         if os.path.exists(stderr):
    #             os.remove(stderr)
    #
    # # ==========================================================================
    # def test0280_success_search_no_result(self):
    #     stdout = 'stdout.txt'
    #     try:
    #         r = main('Search', 'router.vivans.net', 'administrator@ad.vivans.net', 'argos0520!',
    #                  '--search-attributes', 'name=mytest*',
    #                  '--outfile', stdout)
    #         self.assertTrue(r == 0)
    #         with open(stdout, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         # print(out)
    #         self.assertTrue('no result')
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(stdout):
    #             os.remove(stdout)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
