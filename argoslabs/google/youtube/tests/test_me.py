#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.google.youtube.tests.test_me`
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
#  * [2022/02/05]
#     - starting

################################################################################
import os
import sys
import csv
from unittest import TestCase
from argoslabs.google.youtube import _main as main
from contextlib import contextmanager
from io import StringIO


################################################################################
@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


################################################################################
class TU(TestCase):
    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_invalid_video(self):
        try:
            with captured_output() as (out, err):
                r = main('Get Info', 'invalid_video_id')
            self.assertTrue(r == 99)
            stderr = err.getvalue()
            self.assertTrue(stderr.strip() == 'Youtube error: invalid_vid is unavailable')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_video_get_info(self):
        try:
            vid = 'AsfC71SU7Jw'
            with captured_output() as (out, err):
                r = main('Get Info', vid)
            self.assertTrue(r == 0)
            out.seek(0)
            rows = list()
            cr = csv.reader(out)
            for ndx, row in enumerate(cr):
                self.assertTrue(len(row) in (12,))
                rows.append(row)
            self.assertTrue(len(rows) == 2 and rows[1][0] == vid)

            vid = 'f97mee-jofk'
            with captured_output() as (out, err):
                r = main('Get Info', vid)
            self.assertTrue(r == 0)
            out.seek(0)
            rows = list()
            cr = csv.reader(out)
            for ndx, row in enumerate(cr):
                self.assertTrue(len(row) in (12,))
                rows.append(row)
            self.assertTrue(len(rows) == 2 and rows[1][0] == vid)

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_video_stream_info(self):
        try:
            vid = 'AsfC71SU7Jw'
            with captured_output() as (out, err):
                r = main('Stream Info', vid)
            self.assertTrue(r == 0)
            out.seek(0)
            rows = list()
            cr = csv.reader(out)
            for ndx, row in enumerate(cr):
                self.assertTrue(len(row) in (13,))
                rows.append(row)
            self.assertTrue(len(rows) == 21 and rows[-1][0] == '20')
            out.seek(0)
            print(out.getvalue())
            setattr(TU, 'vid1_1_fsize', int(rows[1][-1]))

            vid = 'f97mee-jofk'
            with captured_output() as (out, err):
                r = main('Stream Info', vid)
            self.assertTrue(r == 0)
            out.seek(0)
            rows = list()
            cr = csv.reader(out)
            for ndx, row in enumerate(cr):
                self.assertTrue(len(row) in (13,))
                rows.append(row)
            self.assertTrue(len(rows) == 27 and rows[-1][0] == "26")
            out.seek(0)
            print(out.getvalue())
            setattr(TU, 'vid2_3_fsize', int(rows[3][-1]))

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_video_download(self):
        try:
            vid = 'AsfC71SU7Jw'
            with captured_output() as (out, err):
                r = main('Download', vid)
            self.assertTrue(r == 99)

            vid = 'AsfC71SU7Jw'
            save_file = f'{vid}-1.mp4'
            with captured_output() as (out, err):
                r = main('Download', vid,
                         '--save-file', save_file,
                         '--stream-index', '100')
            self.assertTrue(r == 99)

            vid = 'AsfC71SU7Jw'
            save_file = f'{vid}-1.mp4'
            with captured_output() as (out, err):
                r = main('Download', vid,
                         '--save-file', save_file,
                         '--stream-index', '1')
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            print(stdout)
            sf = os.path.abspath(save_file)
            self.assertTrue(stdout == sf and os.path.getsize(sf) == getattr(TU, 'vid1_1_fsize'))

            vid = 'f97mee-jofk'
            save_file = f'{vid}-3.mp4'
            with captured_output() as (out, err):
                r = main('Download', vid,
                         '--save-file', save_file,
                         '--stream-index', '3')
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            print(stdout)
            sf = os.path.abspath(save_file)
            self.assertTrue(stdout == sf and os.path.getsize(sf) == getattr(TU, 'vid2_3_fsize'))

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_video_caption_info(self):
        try:
            vid = 'AsfC71SU7Jw'
            with captured_output() as (out, err):
                r = main('Caption Info', vid)
            self.assertTrue(r == 0)
            out.seek(0)
            print(out.getvalue())
            out.seek(0)
            rows = list()
            cr = csv.reader(out)
            for ndx, row in enumerate(cr):
                self.assertTrue(len(row) in (4,))
                rows.append(row)
            self.assertTrue(len(rows) == 2 and rows[1][1] == 'a.ko')

            vid = '0Feuchkg5nM'
            with captured_output() as (out, err):
                r = main('Caption Info', vid)
            self.assertTrue(r == 0)
            out.seek(0)
            print(out.getvalue())
            out.seek(0)
            rows = list()
            cr = csv.reader(out)
            for ndx, row in enumerate(cr):
                self.assertTrue(len(row) in (4,))
                rows.append(row)
            self.assertTrue(len(rows) == 8 and rows[4][1] == "ja")

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_caption_get(self):
        try:
            vid = 'AsfC71SU7Jw'
            with captured_output() as (out, err):
                r = main('Caption Get', vid)
            self.assertTrue(r == 99)

            vid = 'AsfC71SU7Jw'
            caption_file = f'{vid}-1.mp4'
            with captured_output() as (out, err):
                r = main('Caption Get', vid,
                         '--caption-file', caption_file,
                         '--caption-index', '100')
            self.assertTrue(r == 99)

            vid = 'AsfC71SU7Jw'
            caption_file = f'{vid}-1.xml'
            with captured_output() as (out, err):
                r = main('Caption Get', vid,
                         '--caption-file', caption_file,
                         '--caption-index', '1')
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            print(stdout)
            sf = os.path.abspath(caption_file)
            self.assertTrue(stdout == sf)

            vid = '0Feuchkg5nM'
            caption_file = f'{vid}-4.txt'
            with captured_output() as (out, err):
                r = main('Caption Get', vid,
                         '--caption-file', caption_file,
                         '--caption-index', '4',
                         '--caption-text')
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            print(stdout)
            sf = os.path.abspath(caption_file)
            self.assertTrue(stdout == sf)

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
