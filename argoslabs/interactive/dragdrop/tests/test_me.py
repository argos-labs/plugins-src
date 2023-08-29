
"""
====================================
 :mod:`argoslabs.google.vision`
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
#     - 그룹에 "7-Interactive" 넣음
#  * [2020/03/17]
#     - STU,PAM 에서 관리자 권한을 빼고 정상 Drag&Drop이 되므로 암호 등 뺌
#     - 해당 windnd.out 을 읽는 것을 확인
#  * [2019/11/12]
#     - starting

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.interactive.dragdrop import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        os.chdir(os.path.dirname(__file__))
        self.assertTrue(True)

    # ==========================================================================
    # def test0050_failure(self):
    #     outfile = 'stdout.txt'
    #     try:
    #         r = main('--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         self.assertTrue(False)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)
    #     finally:
    #         if os.path.exists(outfile):
    #             os.remove(outfile)

    # ==========================================================================
    # def test0100_text_success(self):
    #     outfile = 'stdout.txt'
    #     try:
    #         r = main('--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         print(out)
    #         # self.assertTrue(out.endswith('C:\\Users\\Administrator\\Documents\\DragAndDrop\\image.png'))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(outfile):
    #             os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
