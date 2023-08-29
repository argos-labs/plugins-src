"""
====================================
 :mod:`argoslabs.data.sqlite`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
#
# Authors
# ===========
#
# * Kyobong An,
#
# Change Log
# --------
#
#  * [2021/07/06]
#

################################################################################
# import os
import sys
# import csv
# import shutil
import unittest
# from tempfile import gettempdir
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.data.sqlite import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    def test0000_execute(self):
        try:
            r = main("testdb.db",
                     "-e", "SELECT * FROM Artists")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0001_execute_select(self):
        try:
            r = main("testdb.db",
                     "-e", "SELECT * FROM Albums")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0002_execute_select(self):
        try:
            r = main("testdb.db",
                     "-e", "SELECT * FROM User")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0010_executescript(self):
        try:
            r = main("testdb.db",
                     "-f", "testcsv.sql")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0020_execute_csv(self):
        try:
            r = main("testdb.db",
                     "-f", "testcsv.sql",
                     "-c", "testdb.csv",
                     "--header-lines", "1")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0030_execute_insert(self):
        try:
            r = main("testdb.db",
                     "-e", """INSERT INTO Albums (AlbumName, Year, ArtistName)
                     VALUES ('Yummy Yummy', '1994', 'DK')""")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0040_execute_bulk_insert(self):
        try:
            r = main("testdb.db",
                     "-e", """INSERT INTO Albums (AlbumName, Year, ArtistName)
                     VALUES ('{0}', '{1}', '{2}')""",
                     "-c", "test_bulk.csv",
                     "--header-lines")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0050_execute_delete(self):
        try:
            r = main("testdb.db",
                     "-e", "DELETE FROM Albums WHERE AlbumId >5")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0055_execute_delete_Artists(self):
        try:
            r = main("testdb.db",
                     "-e", "DELETE FROM Artists WHERE ArtistId >5")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0060_sqlfile_bulk_csv(self):
        try:
            r = main("testdb.db",
                     "-f", "test_bulk.sql",
                     "-c", "test_bulk.csv",
                     "--header-lines", "1")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0070_sqlfile_bulk_csv(self):
        try:
            r = main("testdb.db",
                     "-e", """INSERT INTO User (name, sex, age, phone, email, birthday, job, address,mbti)
                           VALUES ('{0}', '{1}', {2}, '{3}', '{4}', {5}, '{6}', '{7}', '{8}')""",
                     "-c", "test_bulk.csv",
                     "--header-lines", "1")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0080_sqlfile_Ex(self):
        try:
            r = main("testdb.db",
                     "-f", "Example.sql",
                     '--outfile', 'output.txt')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
