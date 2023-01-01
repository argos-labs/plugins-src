#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.xmlmanage`
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
#  * [2021/08/25]
#     - starting

################################################################################
import os
import sys
import csv
# from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.data.xmlmanage import _main as main
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
    TestCase for argoslabs.demo.xmlextract
    """
    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0040_failure(self):
        try:
            with captured_output() as (out, err):
                r = main('Get', 'invalid.xml', '/')
            self.assertTrue(r == 1)
            stderr = err.getvalue()
            self.assertTrue(stderr.find('Cannot get XML file') >= 0)

            with captured_output() as (out, err):
                r = main('Get', '', '')
            self.assertTrue(r == 1)
            stderr = err.getvalue()
            self.assertTrue(stderr.find('Cannot get XML file') >= 0)

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_success(self):
        try:
            with captured_output() as (out, err):
                r = main('Get',
                         'foo.xml',
                         '/world/people[1]/name',
                         '--strip')
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == 'Earth')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success(self):
        try:
            with captured_output() as (out, err):
                r = main('Get',
                         'bar.xml',
                         '/food[1]/item',
                         '--strip')
            self.assertTrue(r == 2)     # invalid xpath

            with captured_output() as (out, err):
                r = main('Get',
                         'bar.xml',
                         '/metadata/food[2]/item',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == 'Paper Dosa')

            with captured_output() as (out, err):
                r = main('Get',
                         'bar.xml',
                         '//food[4]/item',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == 'Bisi Bele Bath')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_success_attr(self):
        try:
            with captured_output() as (out, err):
                r = main('Get',
                         'bar.xml',
                         '//food[2]/item/@name',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == 'lunch')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_success_length(self):
        try:
            with captured_output() as (out, err):
                r = main('Length',
                         'bar.xml',
                         '//food',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == '5')

            with captured_output() as (out, err):
                r = main('Length',
                         'bar.xml',
                         '/metadata/food/price',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == '5')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_success_delete(self):
        try:
            res_xml = 'res140.xml'
            with captured_output() as (out, err):
                r = main('Delete',
                         'bar.xml',
                         '//food[2]',
                         )
            self.assertTrue(r == 1)

            with captured_output() as (out, err):
                r = main('Delete',
                         'bar.xml',
                         '//food[2]',
                         '--out-xml', res_xml,
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout.endswith(res_xml))

            with captured_output() as (out, err):
                r = main('Length',
                         res_xml,
                         '//food',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == '4')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_success_delete_attr(self):
        try:
            res_xml = 'res150.xml'
            with captured_output() as (out, err):
                r = main('Delete',
                         'bar.xml',
                         '//food[5]/item/@name',
                         '--out-xml', res_xml,
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout.endswith(res_xml))

            with captured_output() as (out, err):
                r = main('Length',
                         res_xml,
                         '//food/item/@name',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == '4')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_success_set(self):
        try:
            res_xml = 'res160.xml'
            with captured_output() as (out, err):
                r = main('Set',
                         'bar.xml',
                         '//food[1]/calories',
                         '--value', '999',
                         '--out-xml', res_xml,
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout.endswith(res_xml))

            with captured_output() as (out, err):
                r = main('Get',
                         res_xml,
                         '//food[1]/calories',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == '999')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_success_set_attr_exists(self):
        try:
            res_xml = 'res170.xml'
            with captured_output() as (out, err):
                r = main('Set',
                         'bar.xml',
                         '//food[1]/item/@name',
                         '--value', 'Hello',
                         '--out-xml', res_xml,
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout.endswith(res_xml))

            with captured_output() as (out, err):
                r = main('Get',
                         res_xml,
                         '//food[1]/item/@name',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == 'Hello')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0180_success_set_attr_non_exists(self):
        try:
            res_xml = 'res180.xml'
            with captured_output() as (out, err):
                r = main('Set',
                         'bar.xml',
                         '//food[1]/item/@newatt1',
                         '--value', 'World',
                         '--out-xml', res_xml,
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout.endswith(res_xml))

            with captured_output() as (out, err):
                r = main('Get',
                         res_xml,
                         '//food[1]/item/@newatt1',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == 'World')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0190_success_append_next(self):
        try:
            res_xml = 'res190.xml'

            # value 는 XML 형식이어야 합니다
            with captured_output() as (out, err):
                r = main('AppendNext',
                         'bar.xml',
                         '//food[1]/price',
                         '--value', '34',
                         '--out-xml', res_xml,
                         )
            self.assertTrue(r == 1)

            with captured_output() as (out, err):
                r = main('AppendNext',
                         'bar.xml',
                         '//food[1]/price',
                         '--value', '<age>34</age>',
                         '--out-xml', res_xml,
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout.endswith(res_xml))

            with captured_output() as (out, err):
                r = main('Get',
                         res_xml,
                         '//food[1]/age',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == '34')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_success_append_next_attr(self):
        try:
            res_xml = 'res200.xml'

            with captured_output() as (out, err):
                r = main('AppendNext',
                         'bar.xml',
                         '//food[3]/item/@name',
                         '--value', '<age>23</age>',
                         '--out-xml', res_xml,
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout.endswith(res_xml))

            with captured_output() as (out, err):
                r = main('Get',
                         res_xml,
                         '//food[3]/age',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == '23')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_success_append_child(self):
        try:
            res_xml = 'res210.xml'

            # value 는 XML 형식이어야 합니다
            with captured_output() as (out, err):
                r = main('AppendChild',
                         'bar.xml',
                         '//food[1]/price',
                         '--value', '34',
                         '--out-xml', res_xml,
                         )
            self.assertTrue(r == 1)
            stderr = err.getvalue()
            self.assertTrue(stderr.find('but "34"') > 0)

            with captured_output() as (out, err):
                r = main('AppendChild',
                         'bar.xml',
                         '//food[1]/price',
                         '--value', '<child>First Son</child>',
                         '--out-xml', res_xml,
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout.endswith(res_xml))

            with captured_output() as (out, err):
                r = main('Get',
                         res_xml,
                         '//food[1]/price/child',
                         )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == 'First Son')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
