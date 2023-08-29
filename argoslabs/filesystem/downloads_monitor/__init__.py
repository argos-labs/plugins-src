#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.filesystem.downloads_monitor`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Downloads Monitor
"""
# Authors
# ===========
#
# * Kyobong An
#
# --------
#
#  * [2023/04/27]
#     - starting

################################################################################
import os
import csv
import sys
import time
from alabs.common.util.vvencoding import get_file_encoding
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
# noinspection PyBroadException
class Download_Monitor(object):
    def __init__(self, argspec):
        self.argspec = argspec
        self.downloads_path = os.path.expanduser(os.path.join('~', 'downloads'))

        self.downloads_list = self.argspec.csv_path
        # csv_path를 지정하지 않을 경우 바탕화면에 폴더 생성 하는건데
        # if not self.downloads_list:
        #     self.downloads_list = os.path.expanduser(os.path.join('~', 'Desktop', 'download_check', 'downloads.csv'))

        if not os.path.exists(os.path.dirname(self.downloads_list)):
            os.makedirs(os.path.dirname(self.downloads_list))

        self.encoding = argspec.encoding

        if not argspec.encoding:
            self.encoding = get_file_encoding(self.downloads_list)

    # ==========================================================================
    def get_file_list(self):
        with open(self.downloads_list, 'w', encoding=self.encoding) as p:
            wirter = csv.writer(p)
            wirter.writerow(os.listdir(os.path.join(os.path.expanduser('~'), 'downloads')))

    # ==========================================================================
    def d_monitoring(self):
        try:
            before_list = list()
            with open(self.downloads_list, 'r', encoding=self.encoding) as p:
                reader = csv.reader(p)
                for row in reader:
                    before_list += row

            dl_wait = True
            downloads = list()
            while dl_wait:
                time.sleep(1)
                dl_wait = False
                after_list = os.listdir(os.path.join(os.path.expanduser('~'), 'downloads'))
                downloads = list(set(before_list) ^ set(after_list))
                for file_name in after_list:
                    # web downloading check
                    if file_name.endswith('.crdownload'):
                        dl_wait = True
                if len(downloads) == 0:
                    dl_wait = True

            for file in downloads:
                print(self.downloads_path + '\\' + file)

        except Exception as err:
            sys.stderr.write(str(err))


################################################################################
@func_log
def func(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        dm = Download_Monitor(argspec)
        if argspec.operation == 'Before download':
            dm.get_file_list()
        elif argspec.operation == 'Monitoring':
            dm.d_monitoring()
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS',
            group='6',  # Files and Folders
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Downloads Monitor',
            icon_path=get_icon_path(__file__),
            description='It monitors downloads of files to a folder.',
    ) as mcxt:
        # #####################################  for app dependent parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('operation',
                          display_name='Operation',
                          choices=['Before download', 'Monitoring'],
                          help='Check the files in the folder before downloading.')
        # ----------------------------------------------------------------------
        mcxt.add_argument('csv_path', display_name='CSV Path',
                          show_default=True,
                          input_method='filewrite',
                          help='The path of the csv file contained or containing the file list in the download folder')
        # ######################################  for app optional parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('--encoding',
                          display_name='Encoding',
                          help='Encoding for CSV file')

        argspec = mcxt.parse_args(args)
        return func(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
