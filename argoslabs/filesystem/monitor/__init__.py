"""
====================================
:mod:`argoslabs.filesystem.monitor`
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
#  * [2022/08/12]
#     - 윈도우에서 폴더이름에 [] 대괄호 있으면 안되는 문제 [허상민]
#  * [2021/04/07]
#     - 그룹에 "6-Files and Folders" 넣음
#  * [2020/11/19]
#     - default 필터를 *.txt 에서 *.* 으로
#  * [2020/11/18]
#     - Irene이 데모할 때 매 빈줄이 추가되는것 수정
#  * [2020/11/18]
#     - Irene이 데모할 때 매 빈줄이 추가되는것 수정
#  * [2020/11/15]
#     - File Monitor ==> Folder Monitor
#  * [2020/09/01]
#     - 매칭되는 csv 결과가 없을 때는 기존 멈춤 대신 헤더만 출력하도록
#     - csv_out이 False이고 basename이 True인 경우에는 이를 False로 수정
#  * [2020/08/24]
#     - --order-by, --desc 옵션 추가
#     - 모니터링에서 해당 폴더가 아예 없으면 오류가 나오는데 이를 0 으로 나오게
#  * [2020/04/13]
#     - Make sure the label os "--csv-out" : "Details in CSV" and show_default
#     - in case of "--basename": set "--csv-out"
#     - "--basename"의 레이블을 "File name only"로 변경
#  * [2019/04/25]
#     - default result is # of files, --
#  * [2019/04/08]
#     - add --basename option
#  * [2019/04/04]
#     - starting

################################################################################
import os
import sys
import glob
import shutil
import argparse
from alabs.common.util.vvargs import ModuleContext, func_log,  \
    ArgsError, ArgsExit, get_icon_path
from alabs.common.util.timer import Timer


################################################################################
ORDER_BY = {
    'Filename': os.path.basename,
    'Size': os.path.getsize,
    'Create Time': os.path.getctime,
    'Modify Time': os.path.getmtime,
}


################################################################################
def _glob_dir(d, f, flist, is_recursive=True, order_by='Filename', desc=False):
    for _f in f:
        gg = sorted(glob.glob('%s%s%s' % (glob.escape(d), os.path.sep, _f)),
                    key=ORDER_BY[order_by], reverse=desc)
        for fi in gg:
            if os.path.isfile(fi) and fi not in flist:
                flist.append(fi)
    if is_recursive:
        gg = sorted(glob.glob('%s%s%s' % (d, os.path.sep, '*')),
                    key=ORDER_BY[order_by], reverse=desc)
        for fi in gg:
            if os.path.isdir(fi):
                _glob_dir(fi, f, flist, is_recursive)


################################################################################
# noinspection PyShadowingBuiltins
@func_log
def mon_dir(mcxt, args):
    # noinspection PyBroadException
    try:
        mcxt.logger.info('>>>starting...')
        if args.move and not os.path.isdir(args.move):
            raise IOError('Moving monitor "%s" not found!' % args.move)
        if not args.csv_out and args.basename:
            args.basename = False

        flist = list()
        tm = Timer()
        for i in range(3600*24*365):
            with tm:
                for folder in args.folder:
                    if not os.path.isdir(folder):
                        # 모니터링에서 해당 폴더가 아예 없으면 오류가 나오는데 이를 0 으로 나오게
                        # raise IOError('Directory "%s" not found!' % folder)
                        continue
                    _glob_dir(folder, args.filter, flist,
                                is_recursive=args.recursive,
                                order_by=args.order_by,
                                desc=args.desc)
                if flist:
                    break
            if 0 < args.timeout <= i:
                if args.csv_out:
                    # raise TimeoutError('Cannot find files (%s) in %s with timeout(%d)'
                    #                    % (args.filter, folder, args.timeout))
                    print('index,filepath,filesize', end='')
                else:
                    print('0', end='')
                return 0
            mcxt.logger.debug('cannot find files(%s) in %s' % (args.filter, folder))
        ppl = list()
        mvl = list()
        if flist:
            mcxt.logger.info('#%d files(%s) found at (%s)'
                                % (len(flist), filter, folder))
            # ppl.append('index,filepath,filesize')
            for i, f in enumerate(flist):
                fsize = os.path.getsize(f)
                fn = f
                if args.basename:
                    fn = os.path.basename(fn)
                    setattr(args, "csv_out", True)
                msg = '%d,"%s",%d' % (i+1, fn, fsize)
                mcxt.logger.debug('added file item: %s' % msg)
                if args.move:
                    try:
                        mf = os.path.join(args.move, os.path.basename(f))
                        shutil.move(f, mf)
                        if mf not in mvl:
                            mvl.append(mf)
                        fsize = os.path.getsize(mf)
                        # noinspection PyUnusedLocal
                        msg = '%d,"%s",%d' % (i + 1, mf, fsize)
                        mcxt.logger.debug('moved item: %s => %s\\%s'
                                            % (f, args.move, os.path.basename(f)))
                    except Exception as err:
                        mcxt.logger.error('moved item: %s => %s\\%s Error: %s'
                                            % (f, args.move, os.path.basename(f),
                                                str(err)))
                else:
                    ppl.append(msg)
            if args.move:
                for i, f in enumerate(mvl):
                    fsize = os.path.getsize(f)
                    fn = f
                    if args.basename:
                        fn = os.path.basename(fn)
                    msg = '%d,"%s",%d' % (i+1, fn, fsize)
                    ppl.append(msg)

        if args.csv_out:
            ppl.insert(0, 'index,filepath,filesize')
            if ppl:
                print('\n'.join(ppl))
        else:
            print(len(ppl))
        return 0
    except Exception as e:
        msg = 'argoslabs.filesystem.monitor Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
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
        display_name='Folder Monitor',
        icon_path=get_icon_path(__file__),
        description='''Monitor with filter/matching and write the list of filtered files
    eg) {prog} -f *.pfx -f *.log -t 10 -r -m C:\\Temp\\tmp2 C:\\Temp

    output)
3
    If set --csv-out option then,
index,filepath,filesize
1, "C:\\Temp\\a.txt", 234
2, "C:\\Temp\\b.txt", 27
3, "C:\\Temp\\c.txt", 27845
''',
        formatter_class=argparse.RawTextHelpFormatter
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--filter', '-f', action='append',
                            display_name='Search for', show_default=True,
                            help='Set file matching filter like *.* '
                                '(multiple setting is possible, default is [[*.*]])')
        mcxt.add_argument('--timeout', '-t', nargs='?', type=int,
                            display_name='Timeout',
                            default=3, const=3, min_value=0,
                            help='Timeout error when no filtered file during sec '
                                '(default is [[3]] sec, 0 means not timeout)')
        mcxt.add_argument('--basename', action='store_true',
                            display_name='File name only',
                            help='If set this flag only basename instead full pathname.')
        mcxt.add_argument('--move', '-m', nargs="?",
                            display_name='Move-to folder',
                            help='Set moving monitor when filtered file matched')
        mcxt.add_argument('--recursive', '-r', action='store_true',
                            display_name='Inc subfolders',
                            default=False,
                            help='If set then matching recursively')
        mcxt.add_argument('--csv-out', action='store_true',
                            display_name='Details in CSV', show_default=True,
                            default=False,
                            help='If set then CSV output for "index,filepath,filesize"')
        mcxt.add_argument('--order-by',
                            choices=list(ORDER_BY.keys()),
                            display_name='Order By',
                            default='Filename',
                            help='Choose which criteria for Ordering by')
        mcxt.add_argument('--desc', action='store_true',
                            display_name='Descending',
                            help='Choose which criteria for Ordering by')

        # ##################################### for app dependent parameters
        mcxt.add_argument('folder', nargs='+',
                            display_name='Folders to monitor',
                            input_method='folderread',
                            help='monitor')
        argspec = mcxt.parse_args(args)
        if not argspec.filter:
            argspec.filter = ['*.*']
        return mon_dir(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
