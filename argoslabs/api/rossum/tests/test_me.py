"""
====================================
 :mod:`argoslabs.api.rossum`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Rossum API unittest module
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/03/26]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2020/03/19]
#     - test csv output
#  * [2019/12/05]
#     - second testing
#  * [2019/03/21]
#     - starting

################################################################################
import os
import sys
import csv
import json
# from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from alabs.common.util.vvtest import captured_output
from argoslabs.api.rossum import _main as main
from pprint import pprint


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True
    userid = 'mcchae@vivans.net'
    passwd = '..'

    # ==========================================================================
    def test0000_init(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.assertTrue(True)

    # ==========================================================================
    def test0010_invalid_pdf(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_invalid_pdf(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main(self.userid, 'invalid-passwd', 'invalid.pdf', 'json')
            self.assertTrue(r != 0)
            err = err.getvalue()
            self.assertTrue(err.startswith('Invalid user or password'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0030_invalid_pdf(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main(self.userid, self.passwd, 'invalid.pdf', 'json')
            self.assertTrue(r != 0)
            err = err.getvalue()
            self.assertTrue(err.strip().endswith('Image file "invalid.pdf" not found'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_valid_default_json(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        os.chdir(os.path.dirname(__file__))
        try:
            with captured_output() as (out, err):
                r = main(self.userid, self.passwd, 'INV-000097.pdf', 'json')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            # print(_out)
            rd = json.loads(_out)
            pprint(rd)
            self.assertTrue(rd['results'] and
                            len(rd['results'][0]['content']) > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_valid_default_csv(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        os.chdir(os.path.dirname(__file__))
        outfile = 'myout.txt'
        try:
            r = main(self.userid, self.passwd, 'INV-000097.pdf', 'csv',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                print(ifp.read(), end='')
            rr = []
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (25,))
                    rr.append(row)
            self.assertTrue(len(rr) == 3)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0120_valid_default_xml(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        os.chdir(os.path.dirname(__file__))
        outfile = 'myout.txt'
        try:
            r = main(self.userid, self.passwd, 'INV-000097.pdf', 'xml',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs, end='')
                self.assertTrue(rs.find('<export><results>') > 0)

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0200_valid_with_option(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        os.chdir(os.path.dirname(__file__))
        try:
            with captured_output() as (out, err):
                r = main(self.userid, self.passwd, 'INV-000097.pdf', 'json',
                         '--qname', 'Multipage Test',
                         '--keep-doc',
                         )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            # print(_out)
            rd = json.loads(_out)
            pprint(rd)
            self.assertTrue(rd['results'] and
                            len(rd['results'][0]['content']) > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_invalid_with_timeout(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        os.chdir(os.path.dirname(__file__))
        try:
            with captured_output() as (out, err):
                r = main(self.userid, self.passwd, 'INV-000097.pdf', 'json',
                         '--qname', 'Multipage Test',
                         '--timeout', '10',
                         )
            self.assertTrue(r != 0)
            err = err.getvalue()
            self.assertTrue(err.strip().endswith('Processing timeout exceed 10 seconds'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
