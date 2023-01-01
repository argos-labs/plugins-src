"""
====================================
 :mod:`argoslabs.microsoft.sharepoint`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for SharePoint: unittest
"""
#
# Authors
# ===========
#
# * Kyobong An
#
# Change Log
# --------
#
#  * [2021/10/27]
#     - starting
#


################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.microsoft.sharepoint import _main as main
from alabs.common.util.vvargs import vv_base64_encode

################################################################################
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test50_missing(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # # ==========================================================================
    # def test100_Create_Folder(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents',
    #                  '--folder-op', 'Create Folder',
    #                  '--sub-folder', 'move'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test200_Upload_Folder(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents/sub folder',
    #                  '--folder-op', 'Upload Folder',
    #                  '--out-folder', r'C:\plugins\argoslabs\microsoft\sharepoint\tests\file',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test210_Upload_Folder_wildcard(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents/sub folder',
    #                  '--folder-op', 'Upload Folder',
    #                  '--out-folder', r'C:\plugins\argoslabs\microsoft\sharepoint\tests\file',
    #                  '--wildcard', vv_base64_encode('im*')
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test300_Download_Folder(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents/sub folder',
    #                  '--folder-op', 'Download Folder',
    #                  '--out-folder', r'C:\plugins\argoslabs\microsoft\sharepoint\tests\output',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test310_Download_Folder_wildcard(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents/sub folder',
    #                  '--folder-op', 'Download Folder',
    #                  '--out-folder', r'C:\plugins\argoslabs\microsoft\sharepoint\tests\output',
    #                  '--wildcard', vv_base64_encode('im*')
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test400_Copy_Folder(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents/sub folder',
    #                  '--folder-op', 'Copy Folder',
    #                  '--target-folder', 'Shared Documents/move'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test410_Copy_Folder_wildcard(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents/sub folder',
    #                  '--folder-op', 'Copy Folder',
    #                  '--wildcard', 'im*',
    #                  '--target-folder', 'Shared Documents/move'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test450_Copy_File(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents/sub folder',
    #                  '--file-op', 'Copy File',
    #                  '--file-list-name', 'output.txt',
    #                  '--file-list-name', 'text_file.txt',
    #                  '--target-folder', 'Shared Documents/move'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test460_Copy_File_copyname(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents/sub folder',
    #                  '--file-op', 'Copy File',
    #                  '--file-list-name', 'output.txt',
    #                  '--file-list-name', 'text_file.txt',
    #                  '--file-list-copyname', 'test1.txt',
    #                  '--file-list-copyname', 'test2.txt',
    #                  '--target-folder', 'Shared Documents/move'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test500_Upload_File(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents/sub folder',
    #                  '--file-op', 'Upload File',
    #                  '--out-folder', r'C:\plugins\argoslabs\microsoft\sharepoint\tests\output',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test600_Download_File(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents/sub folder',
    #                  '--file-op', 'Download File',
    #                  '--out-folder', r'C:\plugins\argoslabs\microsoft\sharepoint\tests\output',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test700_Delete_Folder(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents/move',
    #                  '--delete-op', 'Delete Folder',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test800_Delete_File(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents/move',
    #                  '--delete-op', 'Delete File',
    #                  '--file-list-name', 'output.txt',
    #                  '--file-list-name', 'text_file.txt',
    #                  '--file-list-name', 'excel_file.xlsx',
    #                  '--file-list-name', 'image001.png',
    #                  '--file-list-name', 'img_file.png',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test810_Delete_File_wildcard(self):
    #     try:
    #         r = main('https://vivans94.sharepoint.com/', 'akb0930@vivans94.onmicrosoft.com', 'shalth13!',
    #                  'https://vivans94.sharepoint.com/sites/vivans', 'Shared Documents/move',
    #                  '--delete-op', 'Delete File',
    #                  '--wildcard', '^im*'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

