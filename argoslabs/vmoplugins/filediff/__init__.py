#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.vmoplugins.filediff`
====================================
.. moduleauthor:: Phuong Nguyen <phuong.nguyen@vmodev.com>
.. note:: ARGOS-LABS License
Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Phuong Nguyen
#
# Change Log
# --------
#
#  * [2019/03/08]
#     - starting

################################################################################
import os
import sys
from filecmp import cmp, dircmp
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from os import path


################################################################################
arr_diff = []


################################################################################
@func_log
def file_diff(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        abs_first_path = os.path.abspath(argspec.first_input)
        abs_second_path = os.path.abspath(argspec.second_input)

        # ##################################### check exits file or folder
        if not path.exists(abs_first_path) or not path.exists(abs_second_path):
            raise Exception("File/folder input is not exists")

        is_first_path_file = path.isfile(abs_first_path)
        is_second_path_file = path.isfile(abs_second_path)

        # ##################################### check and compare files or folders
        if is_first_path_file != is_second_path_file:
            raise Exception("Can not compare file and folder")

        if is_first_path_file:
            is_diff = cmp(argspec.first_input, argspec.second_input)
            if not is_diff:
                diff = "{file_1} and {file_2} are differences".format(
                    file_1=argspec.first_input, file_2=argspec.second_input)
                arr_diff.append(diff)
        else:
            print_diff_folder(abs_first_path, abs_second_path)

        return 0 if len(arr_diff) > 0 else 1
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 9
    finally:
        sys.stdout.flush()
        print(arr_diff, end='')
        mcxt.logger.info('>>>end...')


################################################################################
def print_diff_folder(left_file_path, right_file_path):
    dcmp = dircmp(left_file_path, right_file_path)

    for name in dcmp.diff_files:
        diff = " Diff file {name} found in {left} and {right}".format(name=name,left=dcmp.left,right=dcmp.right)
        arr_diff.append(diff)

    for name in dcmp.left_only:
        diff = "{name} only in {left}".format(name=name, left=dcmp.left)
        arr_diff.append(diff)

    for name in dcmp.right_only:
        diff = "{name} only in {right}".format(name=name, right=dcmp.right)
        arr_diff.append(diff)

    for name in dcmp.funny_files:
        diff = "Found {name} could not be compared".format(name=name)
        arr_diff.append(diff)

    for subdir in dcmp.common_dirs:
        print_diff_folder(os.path.join(dcmp.left, subdir), os.path.join(dcmp.right, subdir))


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
            owner='ARGOS-LABS',
            group='filediff',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='file diff',
            icon_path=get_icon_path(__file__),
            description='difference between two files or folder',
    ) as mcxt:
        try:
            mcxt.add_argument('first_input',
                              display_name='First File/Folder',
                              input_method='fileread',
                              help="input first file/folder")
            mcxt.add_argument('second_input',
                              display_name='Second File/Folder',
                              input_method='fileread',
                              help='input second file/folder')
            argspec = mcxt.parse_args(args)
            return file_diff(mcxt, argspec)
        except Exception as ex:
            print(ex)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
