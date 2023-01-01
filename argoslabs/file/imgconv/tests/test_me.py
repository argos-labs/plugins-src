#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.file.imgconv`
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
#  * [2021/04/06]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2021/01/11]
#     - starting

################################################################################
import os
import sys
import chardet
from unittest import TestCase
from argoslabs.file.imgconv import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # # ==========================================================================
    # def test0010_invalid_operation(self):
    #     try:
    #         _ = main('invalid_env', '', '', '')
    #         self.assertTrue(False)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)

    # ==========================================================================
    def test0100_tiff_jpeg(self):
        stdout = 'stdout.txt'
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return

            src_ext = '.tif, .tiff'
            src = os.path.join('imgdir', 'autumn.tif')
            target_type = 'JPEG image/jpeg'
            r = main(src_ext, src, target_type,
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.find(src[:-4]) > 0)
            self.assertTrue(os.path.exists(rs))

            r = main(src_ext, src, target_type,
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                rs2 = ifp.read()
                print(rs2)
                self.assertTrue(rs2.find(src[:-4]) > 0)
            self.assertTrue(os.path.exists(rs2))

            os.remove(rs)
            os.remove(rs2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0110_tiff_jpeg_folder(self):
        stdout = 'stdout.txt'
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            src_ext = '.tif, .tiff'
            src = 'imgdir'
            target_type = 'JPEG image/jpeg'
            r = main(src_ext, src, target_type,
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(len(rs.split('\n')) == 2)
            for tf in rs.split('\n'):
                self.assertTrue(os.path.exists(tf))
                os.remove(tf)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0120_tiff_jpeg_folder_recursive(self):
        stdout = 'stdout.txt'
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            src_ext = '.tif, .tiff'
            src = 'imgdir'
            target_type = 'JPEG image/jpeg'
            r = main(src_ext, src, target_type, '--recursive',
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(len(rs.split('\n')) == 3)
            for tf in rs.split('\n'):
                self.assertTrue(os.path.exists(tf))
                os.remove(tf)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test0130_GIF_png(self):
        stdout = 'stdout.txt'
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return

            src_ext = '.gif'
            src = os.path.join('imgdir', 'MARBLES.GIF')
            target_type = 'PNG image/png'
            r = main(src_ext, src, target_type,
                     '--outfile', stdout)
            self.assertTrue(r == 0)
            with open(stdout) as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.find(src[:-4]) > 0)
            self.assertTrue(os.path.exists(rs))

            os.remove(rs)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(stdout):
                os.remove(stdout)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
