#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.word2pdf`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.data.word2pdf import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    key_id = None
    key = None

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        cls.tdir = os.path.dirname(__file__)

    # # ==========================================================================
    # def test0100_success(self):
    #     try:
    #         r = main('HASLC01211009758 UWS联丰格式单.doc',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0110_success(self):
    #     try:
    #         r = main('test.docx',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)



