"""
====================================
 :mod:`argoslabs.filesystem.subfolder`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module monitor file system
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/06/11]
#     - TS팀 요청으로 sort 옵션 추가
#  * [2021/04/07]
#     - 그룹에 "6-Files and Folders" 넣음
#  * [2020/12/10]
#     - 영준팀장의 요청으로 오류나는것 확인, 결과 없을 때 오류 문제
#  * [2020/10/06]
#     - 영준팀장의 요청으로 디폴트 출력에 target 폴더 이하만 출력하도록
#  * [2020/09/22]
#     - --depth-list, --basename, --exclude-empty
#  * [2020/09/08]
#     - change name 'Folder Structure'
#  * [2020/09/04]
#     - starting

################################################################################
import os
import sys
import csv
import argparse
import traceback
from alabs.common.util.vvargs import ModuleContext, func_log,  \
    ArgsError, ArgsExit, get_icon_path
from operator import itemgetter


################################################################################
HEADER = 'index', 'depth', 'subfolder', 'num_subfolders', 'num_files', \
         'total_subfolders', 'total_files'


################################################################################
def count_sub(rootfolder, maxdepth=0, depth_list=None, exclude_empty=False):
    t_folders, t_files = 0, 0
    for root, dirs, files in os.walk(rootfolder):
        t_folders += len(dirs)
        t_files += len(files)
        # if root == rootfolder:
        #     continue
        # subf = root[len(rootfolder) + 1:]
        # sepf = subf.split(os.path.sep)
        # depth = len(sepf)
        # if maxdepth == 0 or 0 < depth <= maxdepth:
        #     if depth_list and depth + 1 not in depth_list:
        #         continue
        #     if not (exclude_empty and len(dirs) <= 0 and len(files) <= 0):
        #         t_folders += len(dirs)
        #         t_files += len(files)
    return t_folders, t_files


################################################################################
# noinspection PyUnresolvedReferences
def traverse_subfolder(rootfolder, maxdepth=0,
                       depth_list=None, basename=False, exclude_empty=False,
                       sort=False, ord_desc=False):
    ndx = 1
    rows = list()
    for root, dirs, files in os.walk(rootfolder):
        if root == rootfolder:
            continue
        subf = root[len(rootfolder)+1:]
        sepf = subf.split(os.path.sep)
        depth = len(sepf)
        if maxdepth == 0 or 0 < depth <= maxdepth:
            pathname = os.path.basename(subf) if basename else subf
            row = [ndx, len(sepf), pathname, len(dirs), len(files)]
            if depth_list and depth not in depth_list:
                continue
            if not (exclude_empty and len(dirs) <= 0 and len(files) <= 0):
                row.extend(count_sub(root))
                rows.append(row)
                ndx += 1
    if depth_list and rows:
        p_row = rows[-1]
        sf_cnt = 0
        for i in range(len(rows)-2, -1, -1):
            c_row = rows[i]
            if c_row[1] == p_row[1]:
                sf_cnt += 1
            elif c_row[1] < p_row[1]:
                c_row[-2] = sf_cnt
                sf_cnt = 0
            else:
                sf_cnt = 0

    if sort:
        rows = sorted(rows, key=itemgetter(2))
        if ord_desc:
            rows = list(reversed(rows))
        for i, row in enumerate(rows):
            row[0] = i + 1
    c = csv.writer(sys.stdout, lineterminator='\n')
    c.writerow(HEADER)
    for row in rows:
        c.writerow(row)


################################################################################
# noinspection PyShadowingBuiltins
@func_log
def do_subf(mcxt, args):
    # noinspection PyBroadException
    try:
        mcxt.logger.info('>>>starting...')
        if not os.path.isdir(args.rootfolder):
            raise IOError('Root folder "%s" not found!' % args.rootfolder)
        traverse_subfolder(args.rootfolder, maxdepth=int(args.max_depth),
                           depth_list=args.depth_list,
                           basename=args.basename,
                           exclude_empty=args.exclude_empty,
                           sort=args.sort,
                           ord_desc=args.ord_desc)
        return 0
    except Exception as e:
        exc_info = sys.exc_info()
        out = traceback.format_exception(*exc_info)
        del exc_info
        msg_tb = "%s\n%s" % (''.join(out), str(e))
        msg = 'argoslabs.filesystem.monitor Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        mcxt.logger.error(msg_tb)
        sys.stderr.write('%s%s' % (msg_tb, os.linesep))
        return 1
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='6',  # Files and Folders
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Folder Structure',
        icon_path=get_icon_path(__file__),
        description='Sub folder traversing',
        formatter_class=argparse.RawTextHelpFormatter
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--max-depth', '-m', default=0, type=int,
                          display_name='Max Depth',
                          help='Maximum depth to show sub-folders')
        mcxt.add_argument('--depth-list', action='append', type=int,
                          display_name='Depth List',
                          help='Show only this depth')
        mcxt.add_argument('--basename', action='store_true',
                          display_name='FolderName Only',
                          help='Show only basename without full path')
        mcxt.add_argument('--exclude-empty', action='store_true',
                          display_name='Exclude Empty',
                          help='Show only folders which is not empty')
        mcxt.add_argument('--sort', action='store_true',
                          display_name='Sort Folder',
                          help='sort with sub-folder names')
        mcxt.add_argument('--ord-desc', action='store_true',
                          display_name='Desc Order',
                          help='sort with sub-folder names with descending order')

        # ##################################### for app dependent parameters
        mcxt.add_argument('rootfolder',
                          display_name='Root Folder',
                          input_method='folderread',
                          help='Root folder to read')
        argspec = mcxt.parse_args(args)
        return do_subf(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
