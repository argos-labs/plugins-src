"""
====================================
 :mod:`argoslabs.office.wordeditor`
====================================
.. moduleauthor:: Arun Kumar <ak080495@gmail.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS-LABS RPA Word Editor module
"""
# Authors
# ===========
#
# * Arun Kumar
#
# Change Log
# --------
#
#  * [2022/02/02]
#     - starting

################################################################################
import os
import sys
# import warnings
from unittest import TestCase
from argoslabs.office.wordeditor import _main as main
# warnings.simplefilter("ignore", ResourceWarning)

################################################################################
class TU(TestCase):

    # ==========================================================================
    def setUp(self) -> None:

        os.chdir(os.path.dirname(__file__))
        self.docx_file = r'C:\Users\Administrator\Desktop\docx operation\sample.docx'
        # r'C:\Users\Administrator\Desktop\docx operation\fax_renrakuhyo01.docx'

    # ==========================================================================
    def test0010_fail_empty(self):

        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test00101_paragraph_read(self):

        try:
            r = main(self.docx_file, 'Read Paragraphs',
                     '--run',
                     # '--plot',
                     '--nplot'
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test00101_paragraph_read_with_paragrap_id(self):

        try:
            r = main(self.docx_file, 'Read Paragraphs', '--paragrap_id', 6)
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test00101_paragraph_read_with_run(self):

        try:
            r = main(self.docx_file, 'Read Paragraphs', '--run')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test00101_paragraph_read_with_paragrap_id_and_run(self):

        try:
            r = main(self.docx_file, 'Read Paragraphs',
                     # '--paragrap_id', 6,
                     # '--run',
                     # '--plot',
                     # '--nplot'

                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test00101_table_update_Paragraphs(self):
    #
    #     try:
    #         r = main(self.docx_file, 'Update Paragraphs',
    #                  '--paragrap_id', 15,
    #                  # '--run_id', 0,
    #                  # '--output_path', self.output_path,
    #                  '--update_value', 'Changed Terms and conditions'
    #                  )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)

    # ==========================================================================
    def test00101_table_read(self):

        try:
            r = main(self.docx_file, 'Read Table', '--table_id', 1,
                     # '--row_id', 0,
                     # '--cell_id', 1,
                     '--run',
                     # '--plot',
                     # '--nplot'
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test00101_table_update_table(self):
    #
    #     try:
    #         r = main(self.docx_file, 'Update Table Rows',
    #                  '--table_id', 1,
    #                  '--row_id', 1,
    #                  # '--row_id', 1,
    #                  '--cell_id', 0,
    #                  # '--cell_id', 0,
    #                  '--paragrap_id', 2,
    #                  # '--paragrap_id', 2,
    #                  '--run_id', 0,
    #                  # '--run_id', 0,
    #                  '--update_value', "04",
    #                  # '--update_value', "05",
    #                  )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)

    # ==========================================================================
    def test00101_header_paragraph_read(self):

        try:
            r = main(self.docx_file, 'Read Header',
                     '--run'
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test00101_header_paragraph_update(self):
    #
    #     # , '--table_id', 1, '--row_id', 1, '--cell_id', 1
    #     try:
    #         _ = main(self.docx_file,'Update Header',
    #                     '--paragrap_id', 0,
    #                     '--run_id', 0,
    #                     # '--output_path', self.output_path,
    #                     '--update_value','August'
    #                  )
    #         self.assertTrue(False)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)
    #
    # # ==========================================================================
    def test00101_footer_paragraph_read(self):
        try:
            r = main(self.docx_file, 'Read Footer',
                     '--run'
                     )
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test00101_footer_paragraph_update(self):
    #     try:
    #         r = main(self.docx_file,'Update Footer',
    #                     '--paragrap_id', 0,
    #                     '--run_id', 2,
    #                     '--update_value','change'
    #                  )
    #         self.assertTrue(r==0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)

    # ==========================================================================

    def test9999_quit(self):
        self.assertTrue(True)
