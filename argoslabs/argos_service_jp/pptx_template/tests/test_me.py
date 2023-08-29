#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.pptx_template`
====================================
.. moduleauthor:: Taiki Shimasaki <shimasaki@argos-service.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.argos_service_jp.pptx_template import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success(self):
        try:
            r = main('x10',
                     'C:/Users/Windows/Desktop/PowerPoint/Template-10.pptx',
                     'C:/Users/Windows/Desktop/PowerPoint/Template-10-edited.pptx',
                     '--file_exists',
                     'Overwrite')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_success_with_opt_x10(self):
        try:
            r = main('x10',
                     'C:/Users/Windows/Desktop/PowerPoint/Template-x10.pptx',
                     'C:/Users/Windows/Desktop/PowerPoint/Template-x10-edited_withopt.pptx',
                     '--text_01',
                     'ひとつめ',
                     '--text_02',
                     'second',
                     '--text_03',
                     '3番目',
                     '--text_04',
                     '4',
                     '--text_05',
                     '0505050505050505\n05050505050505',
                     '--text_06',
                     'test-06\ntest',
                     '--text_07',
                     '7777777777777777777777777777',
                     '--text_08',
                     '８８８８８８８８８８８８８８８８８８８８８８８８８８８８８８',
                     '--text_09',
                     '９　＿＿　テスト',
                     '--text_10',
                     'No.10_text',
                     '--img_01',
                     'C:/Users/Windows/Desktop/PowerPoint/img/10248-1.JPG',
                     '--img_02',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-01.png',
                     '--img_03',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-02.png',
                     '--img_04',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-03.png',
                     '--img_05',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-04.png',
                     '--img_06',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-05.png',
                     '--img_07',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-06.png',
                     '--img_08',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-07.png',
                     '--img_09',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-08.png',
                     '--img_10',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-09.png',
                     '--file_exists',
                     'Overwrite')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_success_with_opt_x6(self):
        try:
            r = main('x6',
                     'C:/Users/Windows/Desktop/PowerPoint/Template-x6.pptx',
                     'C:/Users/Windows/Desktop/PowerPoint/Template-x6-edited_withopt.pptx',
                     '--text_01',
                     'ひとつめ',
                     '--text_02',
                     'second',
                     '--text_03',
                     '3番目',
                     '--text_04',
                     '4',
                     '--text_05',
                     '0505050505050505\n05050505050505',
                     '--text_06',
                     'test-06\ntest',
                     '--img_01',
                     'C:/Users/Windows/Desktop/PowerPoint/img/10248-1.JPG',
                     '--img_02',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-01.png',
                     '--img_03',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-02.png',
                     '--img_04',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-03.png',
                     '--img_05',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-04.png',
                     '--img_06',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-05.png',
                     '--file_exists',
                     'Overwrite')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_success_with_opt_x3(self):
        try:
            r = main('x3',
                     'C:/Users/Windows/Desktop/PowerPoint/Template-x3.pptx',
                     'C:/Users/Windows/Desktop/PowerPoint/Template-x3-edited_withopt.pptx',
                     '--text_01',
                     'ひとつめ',
                     '--text_02',
                     'second',
                     '--text_03',
                     '3番目',
                     '--img_01',
                     'C:/Users/Windows/Desktop/PowerPoint/img/10248-1.JPG',
                     '--img_02',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-01.png',
                     '--img_03',
                     'C:/Users/Windows/Desktop/PowerPoint/img/image1-02.png',
                     '--file_exists',
                     'Overwrite')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
