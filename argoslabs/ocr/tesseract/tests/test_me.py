
"""
====================================
 :mod:`argoslabs.ocr.tesseract`
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
#  * [2021/04/09]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2020/03/21]
#     - install_tesseract.html 디자인 적용
#  * [2020/03/19]
#     - 최초 install_tesseract.html 설치 가이드 보여주기
#  * [2020/03/17]
#     - image, lang 을 옵션에서 제외하고 항상 넣도록, 아이콘 색상 조정
#  * [2020/03/10]
#     - download traineddata
#  * [2020/03/05]
#     - do main
#  * [2020/01/23]
#     - change call parameters
#  * [2019/08/11]
#     - finish
#  * [2019/08/10]
#     - starting

################################################################################
import os
import sys
# import shutil
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.ocr.tesseract import _main as main
# from argoslabs.ocr.tesseract import Tesseract


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        os.chdir(os.path.dirname(__file__))
        self.assertTrue(True)
        # if os.path.exists(Tesseract.DATADIRS[1]):
        #     shutil.rmtree(Tesseract.DATADIRS[1])
        # self.assertTrue(not os.path.exists(Tesseract.DATADIRS[1]))

    # ==========================================================================
    def test0010_failure(self):
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        try:
            r = main('invalid')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0030_failure_ocr_without_image(self):
        try:
            r = main('OCR')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success_version(self):
        outfile = 'stdout.txt'
        try:
            r = main('Get Version', "", "English",
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.startswith('4'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0110_success_list_lang(self):
        outfile = 'stdout.txt'
        try:
            r = main('List Languages', "", "English",
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(len(rs.split('\n')) == 124)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0120_success_list_lang_with_data_only(self):
        outfile = 'stdout.txt'
        try:
            r = main('List Languages', "", "English", '--trained-lang',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(len(rs.split('\n')) >= 2)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0130_success_ocr(self):
        outfile = 'stdout.txt'
        try:
            r = main('OCR', 'sample.png', 'English',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.startswith('Download the wheel file'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0140_success_ocr(self):
        outfile = 'stdout.txt'
        try:
            r = main('OCR', 'sample2.png', 'English',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.startswith('from tesserocr import PyTessBaseAPI'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0150_success_ocr(self):
        outfile = 'stdout.txt'
        try:
            r = main('OCR', 'sample3.png', 'English',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                print(rs)
                self.assertTrue(rs.startswith('Advanced API Examples'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0160_success_jpn_01(self):
        outfile = 'stdout.txt'
        try:
            r = main('OCR', 'jpn-01.png', 'Japanese',
                     '--lang', 'Japanese',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                rs = ifp.read()
                # print(rs)
                self.assertTrue(rs.startswith('サ ル も つ ら い よ'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0170_success_jpn_02(self):
        outfile = 'stdout.txt'
        try:
            r = main('OCR', 'jpn-02.png', 'Japanese',
                     '--lang', 'Japanese',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                rs = ifp.read()
                # print(rs)
                self.assertTrue(rs.rstrip().endswith('tvjapan.net'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0180_success_kor_02(self):
        outfile = 'stdout.txt'
        try:
            r = main('OCR', 'kor-02.png', 'Korean',
                     '--lang', 'Korean',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                rs = ifp.read()
                # print(rs)
                self.assertTrue(rs.startswith('( 지 디 넷 코 리 아'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0190_success_kor_01(self):
        outfile = 'stdout.txt'
        try:
            r = main('OCR', 'kor-01.png', 'Korean',
                     '--lang', 'Korean', '--lang2', 'English',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                rs = ifp.read()
                # print(rs)
                self.assertTrue(rs.rstrip().endswith('싶 어 졌 습 니 다 .'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0200_success_kor_03(self):
        outfile = 'stdout.txt'
        try:
            r = main('OCR', 'kor-03.png', 'Korean',
                     '--lang', 'Korean',
                     '--lang2', 'English',
                     '--psm', 'Treat the image as a single text line',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                rs = ifp.read()
                # print(rs)
                self.assertTrue(rs.rstrip().endswith('지 훈 현 서 아 빠'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
