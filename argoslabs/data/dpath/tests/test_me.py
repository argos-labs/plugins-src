"""
====================================
 :mod:`argoslabs.data.dpath.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
import csv
import json
import yaml
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
from argoslabs.data.dpath import _main as main

from contextlib import contextmanager
from io import StringIO


################################################################################
@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    def setUp(self) -> None:
        mdir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(mdir)
        # odir = os.path.join(mdir, 'output')
        # if not os.path.exists(odir):
        #     os.makedirs(odir)

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_help(self):
        try:
            _ = main('--help')
            self.assertTrue(False)
        except ArgsExit as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_dpath_ex01_get(self):
        try:
            inf = 'input/dpath-ex01.json'
            with captured_output() as (out, err):
                r = main('get', inf, '/a/b/43')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            out.seek(0)
            d = json.load(out)
            self.assertTrue(d == 30)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_dpath_ex01_fail(self):
        try:
            inf = 'input/dpath-ex01.json'
            with captured_output() as (out, err):
                r = main('get', inf, '/a/b/zzz')
            self.assertTrue(r == 1)
            _err = err.getvalue()
            self.assertTrue(_err.find('Invalid key') >= 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_dpath_ex01_search(self):
        try:
            inf = 'input/dpath-ex01.json'
            with captured_output() as (out, err):
                r = main('search', inf, '/a/b/[cd]')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            out.seek(0)
            d = json.load(out)
            self.assertTrue('c' in d['a']['b'] and 'd' in d['a']['b'])
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_dpath_ex01_values(self):
        try:
            inf = 'input/dpath-ex01.json'
            with captured_output() as (out, err):
                r = main('values', inf, '/a/b/d/*')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            out.seek(0)
            d = json.load(out)
            self.assertTrue('bumpers' in d)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_dpath_ex01_set(self):
        try:
            inf = 'input/dpath-ex01.json'
            with captured_output() as (out, err):
                r = main('set', inf, '/a/b/[cd]', '--set-value', 'Waffles')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            out.seek(0)
            d = json.load(out)
            self.assertTrue(d['a']['b']['c'] == 'Waffles' and
                            d['a']['b']['d'] == 'Waffles')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_dpath_ex01_set(self):
        try:
            inf = 'input/dpath-ex01.json'
            with captured_output() as (out, err):
                r = main('set', inf, '/a/b/[cd]',
                         '--set-value', '{"k1":"v1", "k2":22}',
                         '--output-format', 'YAML')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            out.seek(0)
            # d = json.load(out)
            d = yaml.load(out)
            self.assertTrue(d['a']['b']['c']['k1'] == 'v1' and
                            d['a']['b']['d']['k2'] == 22)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_dpath_ex01_new(self):
        try:
            inf = 'input/dpath-ex01.json'
            with captured_output() as (out, err):
                r = main('new', inf, 'a/b/e/f/g', '--set-value', 'Roffle')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            out.seek(0)
            d = json.load(out)
            self.assertTrue(d['a']['b']['e']['f']['g'] == 'Roffle')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_ex_01(self):
        try:
            inf = 'input/ex-01.json'
            with captured_output() as (out, err):
                r = main('get', inf, '/1')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            out.seek(0)
            d = json.load(out)
            self.assertTrue(d == 500)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_ex_02(self):
        try:
            inf = 'input/ex-02.json'
            with captured_output() as (out, err):
                r = main('get', inf, '/topping')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            out.seek(0)
            d = json.load(out)
            self.assertTrue(len(d) == 7 and d[-1]['id'] == '5004')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_ex_02_yaml(self):
        try:
            inf = 'input/ex-02.json'
            with captured_output() as (out, err):
                r = main('get', inf, '/topping', '--output-format', 'YAML')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            out.seek(0)
            d = yaml.load(out)
            self.assertTrue(len(d) == 7 and d[-1]['id'] == '5004')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0230_ex_02_csv(self):
        try:
            inf = 'input/ex-02.json'
            with captured_output() as (out, err):
                r = main('get', inf, '/topping', '--output-format', 'CSV')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            out.seek(0)

            rr = []
            cr = csv.reader(out)
            for row in cr:
                self.assertTrue(len(row) in (2,))
                rr.append(row)
            self.assertTrue(len(rr) == 8 and rr[-1][0] == '5004')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
