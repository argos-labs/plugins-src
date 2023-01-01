"""
====================================
 :mod:`argoslabs.filesystem.op`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for operations of filesystem
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/03/10] Kyobong An
#     - remove할때 wildcard 사용시 해당 되는 것들만삭제 폴더가 비더라도 유지 하도록 변경
#  * [2022/03/10] Kyobong An
#     - remove에 recursive 기능 추가
#  * [2022/03/08] Kyobong An
#     - 파일이동후 소스폴더에 파일이 없을 경우 삭제됨. move일 경우 회피하도록 수정
#  * [2021/10/27] Kyobong An
#     - fnmatch() 함수에 기존 fullpath로 입력 -> filename만 입력되도록 변경
#  * [2021/04/08]
#     - 그룹에 "6-Files and Folders" 넣음
#  * [2021/02/17]
#     - create 때 이미 있으면 (1) 번호 붙이던가 overwirte 체크면 덮어쓰기
#     - already exists 문구 삭제
#  * [2020/12/17]
#     - copy 시 Target 파일 경로를 출력하도록 수정
#  * [2020/11/12]
#     - create 시 생성한 파일 경로를 출력하도록 수정
#  * [2020/08/26]
#     - 없는 파일/폴더를 삭제할 때 예외 말고 .. 리턴
#     - 있는 파일/폴더를 생성하려고 할 때 예외 말고 .. 리턴
#  * [2020/04/29]
#     - 기존 os.walk 대신 glob.glob로 변경
#     - --recursive 욥션 추가
#  * [2020/04/23]
#     - foo/*.txt 를 bar 폴더에 옮기는데 foo 자체가 지워지는 문제 밸생 문제
#  * [2020/04/21]
#     - 경우에 따라 결과에 계속해서 복사하는 문제 해결
#  * [2019/10/29]
#     - move 또는 remove 에서 와일드카드 작동하도록
#  * [2019/06/20]
#     - 와일드카드 추가
#     - 이동/복사 시 동일 이름의 target이 존재하면 (1), (2) ... 등을 붙임
#  * [2019/05/20]
#     - create 기능 추가
#  * [2019/04/26]
#     - target이 비어있지 않으면 지우는 로직 변경
#  * [2019/04/18]
#     - 이동하거나 복사할 목적지 폴더가 없으면 생성하려고 해 봄
#     - 이동하거나 복사할 대상 파일의 폴더가 없으면 생성하려고 해 봄
#     - src가 폴더이고 \로 끝나면 (윈도우에서) 오류 발생
#       - PAM에서
#         argoslabs.filesystem.op.exe -vvv copy "C:\tmp\1\" "C:\tmp\2"
#         라고 호출하면 src가 'C:\\tmp\\1" C:\\tmp\\2' 가 되는 문제점 발생
#       ==> PAM에서 수정하기로 함 (개별 args 목록에 넣는 것으로)
#  * [2019/03/08]
#     - add icon
#  * [2018/11/28]
#     - starting

################################################################################
import os
import sys
import shutil
from pathlib import Path
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from fnmatch import fnmatch


################################################################################
OUT_LINE = None


################################################################################
def is_empty(s):
    _is_empty = True
    for root, dirs, files in os.walk(s):
        if dirs or files:
            _is_empty = False
            break
    return _is_empty


################################################################################
def get_next_filedir(t):
    tdir = os.path.dirname(t)
    tbase = os.path.basename(t)
    tfile, text = os.path.splitext(tbase)
    cnt = 1
    while True:
        tt = os.path.join(tdir, '%s (%d)%s' % (tfile, cnt, text))
        if not os.path.exists(tt):
            t = tt
            break
        cnt += 1
    return t


################################################################################
def copy_file(s, t,
              preserve=False,
              symlinks=False,
              overwrite=False,
              wildcard='*',
              is_delete_src=False):
    if not os.path.isfile(s):
        raise RuntimeError('Cannot get file for source "%s" file' % s)
    if s == t:
        raise RuntimeError('Cannot copy same source or target file "%s"' % s)
    # if not fnmatch(s, wildcard): # fullpath로 적용됨
    if not fnmatch(os.path.basename(s), wildcard):
        return 0
    tdir = os.path.dirname(t)
    if not os.path.exists(tdir):
        os.makedirs(tdir)
    if os.path.exists(t) and not overwrite:
        t = get_next_filedir(t)
    copy_f = shutil.copy2 if preserve else shutil.copy
    copy_f(s, t, follow_symlinks=symlinks)
    OUT_LINE.append(os.path.abspath(t))
    if is_delete_src:
        os.remove(s)
        # if not os.path.isdir(os.path.dirname(s)):
        #     os.makedirs(os.path.dirname(s))

    return 1


################################################################################
def copy_tree(s, t,
              preserve=False,
              symlinks=False,
              overwrite=False,
              wildcard='*',
              is_delete_src=False,
              recursive=False,
              operation=None):
    if os.path.isfile(s):
        return copy_file(s, t, preserve=preserve,
                         symlinks=symlinks, overwrite=overwrite)
    if s == t:
        raise RuntimeError('Cannot copy same source or target dir "%s"' % s)
    cnt = 0
    for root, dirs, files in os.walk(s):
        if root.startswith(t):
            continue  # 경우에 따라 결과에 계속해서 복사하는 문제 해결
        for file_ in files:
            fs = os.path.join(root, file_)
            # ft = os.path.join(t, fs[len(s):]) : 어떤 경우에 t가 사라지는 현상
            tfn = fs[len(s):]
            ft = t
            if t[-1] not in ('\\', '/') and tfn[0] not in ('\\', '/'):
                ft += os.path.sep
            ft += tfn
            r = copy_file(fs, ft, preserve=preserve, symlinks=symlinks,
                          overwrite=overwrite, wildcard=wildcard,
                          is_delete_src=is_delete_src)
            cnt += r
        if is_delete_src:
            if is_empty(root) and root != s:
                shutil.rmtree(root)
        if not recursive:
            break
    if is_delete_src:
        if is_empty(s) and operation != 'move':
            shutil.rmtree(s)
    return cnt


################################################################################
def remove_file(t, wildcard='*'):
    if not os.path.isfile(t):
        # raise RuntimeError('Cannot get file for removing "%s" file' % t)
        # 2020/08/26 later change this return above 0 with plugin ResultHandler
        return 0
    if not fnmatch(t, wildcard):
        return 0
    os.remove(t)
    OUT_LINE.append(os.path.abspath(t))
    return 1


################################################################################
def remove_tree(t, wildcard='*', recursive=False):
    if os.path.isfile(t):
        return remove_file(t, wildcard=wildcard)
    cnt = 0
    for root, dirs, files in os.walk(t):
        for file_ in files:
            ft = os.path.join(root, file_)
            r = remove_file(ft, wildcard=wildcard)
            cnt += r

        if not recursive:
            break
    if wildcard == '*':
        shutil.rmtree(t)
    return cnt


################################################################################
@func_log
def do_op(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: 0
    """
    try:
        global OUT_LINE
        OUT_LINE = list()
        mcxt.logger.info('>>>starting...')
        if argspec.operation == 'create':
            if not argspec.src:
                raise ValueError(f'Enter new file path/name at Source File/Folder, not Target')
            if os.path.exists(argspec.src):
                if not argspec.overwrite:
                    argspec.src = get_next_filedir(argspec.src)
                else:  # overwrite
                    if os.path.isdir(argspec.src):
                        print(os.path.abspath(argspec.src), end='')
                        return 0
                    # for creation in case of file overwrite
                    os.remove(argspec.src)
            if argspec.src[-1] in ('/', '\\'):
                # 이동하거나 복사할 목적지 폴더가 없으면 생성하려고 해 봄
                os.makedirs(argspec.src)
            else:
                Path(argspec.src).touch()
            print(os.path.abspath(argspec.src), end='')
            return 0

        if not os.path.exists(argspec.src):
            # raise IOError('Cannot find source file or folder')
            print(f'Cannot find source file or folder "{argspec.src}"')
            # 2020/08/26 later change this return above 0 with plugin ResultHandler
            return 0
        src_is_dir = os.path.isdir(argspec.src)
        if argspec.operation not in ('remove', 'create'):
            if not argspec.target:
                raise ValueError('Invalid target')
        target_is_dir = os.path.isdir(argspec.target) if argspec.target else False
        if argspec.operation in ('copy', 'move'):
            if argspec.src == argspec.target:
                raise RuntimeError('Cannot %s for same src and target "%s"'
                                   % (argspec.operation, argspec.src))
            if not os.path.exists(argspec.target):
                if src_is_dir or argspec.target[-1] in ('/' or '\\'):
                    # 이동하거나 복사할 목적지 폴더가 없으면 생성하려고 해 봄
                    os.makedirs(argspec.target)
                    target_is_dir = True
                else:
                    dn = os.path.dirname(os.path.abspath(argspec.target))
                    # 이동하거나 복사할 대상 파일의 폴더가 없으면 생성하려고 해 봄
                    if not os.path.exists(dn):
                        os.makedirs(dn)
            is_delete_src = True if argspec.operation == 'move' else False
            if src_is_dir:
                if not target_is_dir:
                    raise RuntimeError('Cannot %s for "%s" src folder into target "%s" file'
                                       % (argspec.operation, argspec.src, argspec.target))
                copy_tree(argspec.src, argspec.target,
                          preserve=argspec.preserve,
                          symlinks=argspec.symlink,
                          overwrite=argspec.overwrite,
                          wildcard=argspec.wildcard,
                          is_delete_src=is_delete_src,
                          recursive=argspec.recursive,
                          operation=argspec.operation)
            else:
                target = argspec.target
                if os.path.isdir(argspec.target):
                    target = os.path.join(argspec.target, os.path.basename(argspec.src))
                copy_file(argspec.src, target,
                          preserve=argspec.preserve,
                          symlinks=argspec.symlink,
                          overwrite=argspec.overwrite,
                          wildcard=argspec.wildcard,
                          is_delete_src=is_delete_src)
        elif argspec.operation == 'remove':
            if not src_is_dir:
                remove_file(argspec.src, wildcard=argspec.wildcard)
            else:
                remove_tree(argspec.src, wildcard=argspec.wildcard, recursive=argspec.recursive,)
        print('\n'.join(OUT_LINE), end='')
        mcxt.logger.info('>>>end...')
        return 0
    except Exception as e:
        msg = 'argoslabs.filesystem.op Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        raise


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='6',  # Files and Folders
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='File/Folder Op',
        icon_path=get_icon_path(__file__),
        description='filesystem operation. file/folder move/copy/create etc',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--wildcard',
                          display_name='Src file wildcard', show_default=True,
                          default='*',
                          help='In folder opeartion use matching wildcard, default is [[*]]')
        mcxt.add_argument('--preserve', '-p', action='store_true',
                          display_name='Preserve time,mode',
                          help='If this flag is set preserve meta information of filesystem. Time and mode are preserved.')
        mcxt.add_argument('--symlink', '-s', action='store_true',
                          display_name='Follow symlink',
                          help='If this flag is set and src is symbolic link then target preserve symlink. '
                               'This option is not applicable at Windows system.')
        mcxt.add_argument('--overwrite', action='store_true',
                          display_name='Overwrite',
                          help='Is this flag is set and target file already exists then overwrite,'
                               ' otherwise target filename is appended "(number)"')
        mcxt.add_argument('--recursive', action='store_true',
                          display_name='Recursive Op',
                          help='If this flag is set copy or move recursively.')

        # 옵션과 상관없이 target에 동일한 파일이 없으면 복사
        # target이 있었으면 update 옵션이 없으면 무조건 덮어씀, update option이
        # 있으면 target이 src보다 오래된 경우에만 덮어씀
        # mcxt.add_argument('--update', action='store_true',
        #                   display_name='Update mode',
        #                   help='If this flag is set, "src" will only be copied if "dst" does not exist, '
        #                        'or if "dst" does exist but is older than "src". If not set alwarys overwrite.')
        # ##################################### for app dependent parameters
        mcxt.add_argument('operation',
                          display_name='File/Folder op',
                          choices=['copy', 'move', 'remove', 'create'],
                          help='type of operation for filesystem.')
        mcxt.add_argument('src',
                          display_name='Source File/Folder',
                          input_method='fileread',
                          help='source file or folder')
        mcxt.add_argument('target', nargs='?', const=None,
                          display_name='Target File/Folder',
                          input_method='filewrite',
                          help='target file or folder. Note that if target is folder then first target folder is REMOVED. So be CAREFUL!')
        argspec = mcxt.parse_args(args)
        return do_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
