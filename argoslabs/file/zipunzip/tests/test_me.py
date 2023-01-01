#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.myuti.text`
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
# * Jerry Chae <mcchae@argos-labs.com>
#
# Change Log
# --------
#
#  * [2021/04/06]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/08/19]
#     - change option or parameter: files, folders
#     - if not set --unzip-folder for unzip then default is the dirname of zipfile
#  * [2020/08/02]
#     - starting

################################################################################
import os
import sys
import shutil
# from alabs.common.util.vvargs import ArgsError
from tempfile import gettempdir
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.file.zipunzip import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.myuti.text
    """
    # ==========================================================================
    CF = os.path.dirname(__file__)
    ZF = os.path.join(gettempdir(), 'zipunzip-test')

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(self.CF)

    # ==========================================================================
    def test0000_init(self):
        zf = self.ZF
        if os.path.exists(zf):
            shutil.rmtree(zf)
        if not os.path.exists(zf):
            os.makedirs(zf)
            foo = os.path.join(zf, 'foo.txt')
            with open(foo, 'w') as ofp:
                ofp.write('This is a foo file\n')
            bar = os.path.join(zf, 'bar.txt')
            with open(bar, 'w') as ofp:
                ofp.write('This is a bar file\n')
                ofp.write('This is a bar file\n')
            foobar = os.path.join(zf, 'foobar')
            if not os.path.exists(foobar):
                os.makedirs(foobar)
            shutil.copy(foo, foobar)
            shutil.copy(bar, foobar)
        self.assertTrue(os.path.isdir(zf))

    # ==========================================================================
    def test0010_failure(self):
        try:
            _ = main('')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        try:
            _ = main('invalid-op', 'zipfile')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0030_failure(self):
        try:
            _ = main('Unzip', 'invalid-zipfile.zip')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0040_failure(self):
        try:
            r = main('Unzip', 'invalid-zipfile.zip')
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_success_zip(self):
        # run test0000_init before testing
        try:
            os.chdir(self.ZF)
            r = main(
                'Zip',
                os.path.join(self.CF, 'myzip.zip'),
                'foo.txt',
                'bar.txt',
                '--folders', 'foobar',
            )
            self.assertTrue(r == 0)
            os.chdir(self.CF)
            self.assertTrue(os.path.exists('myzip.zip'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success_unzip(self):
        # run test0000_init before testing
        try:
            r = main('Unzip', 'myzip.zip')
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(os.path.join('myzip', 'foobar', 'bar.txt')))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists('myzip'):
                shutil.rmtree('myzip')

    # ==========================================================================
    def test0120_success_unzip2(self):
        # run test0000_init before testing
        try:
            r = main('Unzip', 'myzip.zip',
                     '--unzip-folder', 'unzip-folder')
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(
                os.path.join('unzip-folder', 'foobar', 'bar.txt')))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists('unzip-folder'):
                shutil.rmtree('unzip-folder')

    # ==========================================================================
    def test0130_success_addzip(self):
        # run test0000_init before testing
        try:
            r = main('AddZip',
                     'myzip.zip',
                     'test_me.py')
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists('myzip.zip'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_success_unzip3(self):
        # run test0000_init before testing
        try:
            r = main('Unzip', 'myzip.zip',
                     '--unzip-folder', 'unzip-folder')
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(
                os.path.join('unzip-folder', 'test_me.py')))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists('unzip-folder'):
                shutil.rmtree('unzip-folder')

    # ==========================================================================
    def test0150_success_list(self):
        # run test0000_init before testing
        stdout = 'stdout.txt'
        try:
            r = main('List', 'myzip.zip',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                out = ifp.read()
            flist = out.split('\n')
            self.assertTrue('foobar/foo.txt' in flist)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        # finally:
        #     if os.path.exists('unzip-folder'):
        #         shutil.rmtree('unzip-folder')

    # ==========================================================================
    def test0160_success_all_options(self):
        try:
            stdout = 'stdout.txt'
            c_types = ('STORED', 'ZLIB', 'BZ2', 'LZMA')
            c_levels = (1, 5, 9)
            for c_type in c_types:
                for c_level in c_levels:
                    os.chdir(self.ZF)
                    r = main('Zip',
                             os.path.join(self.CF, 'myzip.zip'),
                             'foo.txt',
                             'bar.txt',
                             '--folders', 'foobar',
                             '--comp-type', c_type,
                             '--comp-level', str(c_level),
                             '--outfile', stdout)
                    self.assertTrue(r == 0)
                    os.chdir(self.CF)
                    self.assertTrue(os.path.exists('myzip.zip'))
                    fsize = os.path.getsize('myzip.zip')
                    print(f'zip({c_type},{c_level}) size is {fsize} Bytes')

                    r = main('Unzip', 'myzip.zip',
                             '--unzip-folder', 'unzip-folder',
                             '--outfile', stdout)
                    self.assertTrue(r == 0)
                    bar_txt = os.path.join('unzip-folder', 'foobar', 'bar.txt')
                    self.assertTrue(os.path.exists(bar_txt) and
                                    os.path.getsize(bar_txt) == 40)
                    shutil.rmtree('unzip-folder')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_success_zip_password(self):
        # run test0000_init before testing
        try:
            os.chdir(self.ZF)
            r = main(
                'Zip',
                os.path.join(self.CF, 'myzip2.zip'),
                'foo.txt',
                'bar.txt',
                '--folders', 'foobar',
                '--password', '12345',
            )
            self.assertTrue(r == 0)
            os.chdir(self.CF)
            self.assertTrue(os.path.exists('myzip2.zip'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0180_success_list_password(self):
        # run test0000_init before testing
        stdout = 'stdout.txt'
        try:
            r = main('List', 'myzip2.zip',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout, encoding='utf-8') as ifp:
                out = ifp.read()
            flist = out.split('\n')
            self.assertTrue('foobar/foo.txt' in flist)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0190_success_unzip_password(self):
        # run test0000_init before testing
        try:
            r = main('Unzip', 'myzip2.zip')
            self.assertTrue(r != 0)
            r = main('Unzip', 'myzip2.zip',
                     '--password', '12345',)
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(os.path.join('myzip2', 'foobar', 'bar.txt')))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists('myzip2'):
                shutil.rmtree('myzip2')

    # ==========================================================================
    def test0200_success_unzip_password(self):
        # run test0000_init before testing
        try:
            r = main('Unzip', 'myzip-passwd.zip')
            self.assertTrue(r != 0)
            r = main('Unzip', 'myzip-passwd.zip',
                     '--password', '12345',)
            self.assertTrue(r == 0)
            self.assertTrue(os.path.exists(os.path.join('myzip-passwd', 'build.bat')))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists('myzip-passwd'):
                shutil.rmtree('myzip-passwd')

    # ==========================================================================
    def test9999_quit(self):
        zf = self.ZF
        if os.path.exists(zf):
            shutil.rmtree(zf)
        self.assertTrue(not os.path.exists(zf))
