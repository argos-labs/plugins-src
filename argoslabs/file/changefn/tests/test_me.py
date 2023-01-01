"""
====================================
 :mod:`argoslabs.file.changefn`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module: unittest
"""

################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.file.changefn import _main as main


################################################################################
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))


    # # ==========================================================================
    # def test100_success(self):
    #     try:
    #         r = main('C:/Users/MyGuide/Desktop/image.png', 'image.png',
    #                  '--choice', 'Overwrite')
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test200_success(self):
    #     try:
    #         r = main('sample2.csv', 'sample2.csv')
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)