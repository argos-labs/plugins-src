#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.arun.text`
====================================
.. moduleauthor:: arun kumar <ak080495@gmail.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Jerry Chae <mcchae@argos-labs.com>
#
# Change Log
# --------
#
#  * [2021/04/06]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/12/11]
#     - add password : 표준 zipfile은 해지에만 암호를 넣을 수 있으나 생성은 안됨
#       pyzipper 이용, 윈도우 에서는 압축 해지 안됨, 맥에서는 정상적으로 암호 받고 해제 가능
#  * [2020/08/19]
#     - change option or parameter: files, folders
#     - if not set --unzip-folder for unzip then default is the dirname of zipfile
#  * [2020/08/02]
#     - starting

################################################################################
import os
import sys
import zipfile
import pyzipper
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
OP_LIST = ['Zip', 'Unzip', 'AddZip', 'List']
COMP_TYPE = {
    'STORED': zipfile.ZIP_STORED,
    'ZLIB': zipfile.ZIP_DEFLATED,
    'BZ2': zipfile.ZIP_BZIP2,
    'LZMA': zipfile.ZIP_LZMA,
}
COMP_LEVEL = [1, 2, 3, 4, 5, 6, 7, 8, 9]


################################################################################
@func_log
def zip_unzip(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if argspec.operation in ('UnZip', 'AddZip', 'List'):
            if not os.path.exists(argspec.zipfile):
                raise IOError(f'Cannot access zipfile "{argspec.zipfile}"')
        if argspec.operation not in OP_LIST:
            raise ValueError(f'Invalid operation not in "{OP_LIST}"')
        comp_type = COMP_TYPE.get(argspec.comp_type, zipfile.ZIP_STORED)
        comp_level = argspec.comp_level
        if argspec.operation in ('Zip', 'AddZip'):
            f_f = list()
            if argspec.folders:
                f_f.extend(argspec.folders)
            if argspec.files:
                f_f.extend(argspec.files)
            if not f_f:
                raise ValueError(f'Not specified for the files/folders to Zip/AddZip')
            mode = 'w' if argspec.operation == 'Zip' else 'a'

            pwd = os.getcwd()
            ffs = list()
            for ff in f_f:
                if not os.path.exists(ff):
                    continue  # ignore for non-existing file/folder
                if os.path.isdir(ff):
                    for folder, subfolders, files in os.walk(ff):
                        for file in files:
                            sf = os.path.join(folder, file)
                            ffs.append(os.path.abspath(sf).split(os.path.sep))
                else:
                    ffs.append(os.path.abspath(ff).split(os.path.sep))
            if not ffs:
                raise ValueError(f'Invalid files/folders to Zip/AddZip')
            if len(ffs) <= 1:
                lcp = ffs[0][:-1]
            else:
                # noinspection PyTypeChecker
                lcp = os.path.commonprefix(ffs)
            os.chdir(os.path.sep.join(lcp))
            if argspec.password:
                with pyzipper.AESZipFile(argspec.zipfile, mode,
                                         compression=comp_type,
                                         encryption=pyzipper.WZ_AES) as zfp:
                    zfp.setpassword(str.encode(argspec.password))
                    for ff in ffs:
                        zf = os.path.sep.join(ff[len(lcp):])
                        zfp.write(zf, compress_type=comp_type,
                                  compresslevel=comp_level)
            else:
                with zipfile.ZipFile(argspec.zipfile, mode) as zfp:
                    for ff in ffs:
                        zf = os.path.sep.join(ff[len(lcp):])
                        zfp.write(zf, compress_type=comp_type,
                                  compresslevel=comp_level)
            os.chdir(pwd)
            print(os.path.abspath(argspec.zipfile), end='')
        elif argspec.operation == 'Unzip':
            if not os.path.exists(argspec.zipfile):
                raise IOError(f'Invalid Zip file "{argspec.zipfile}"')
            zff = os.path.abspath(argspec.zipfile)
            zbn = os.path.basename(zff)
            zfn, _ = os.path.splitext(zbn)
            unzip_folder = os.path.join(os.path.dirname(zff), zfn)
            if argspec.unzip_folder:
                unzip_folder = argspec.unzip_folder
            if argspec.password:
                try:
                    with pyzipper.AESZipFile(argspec.zipfile) as zfp:
                        zfp.setpassword(str.encode(argspec.password))
                        zfp.extractall(path=unzip_folder)
                    print(os.path.abspath(unzip_folder), end='')
                    return 0
                except:
                    # fail but trying to use normal zipfile
                    ...
            with zipfile.ZipFile(argspec.zipfile) as zfp:
                if argspec.password:
                    zfp.setpassword(str.encode(argspec.password))
                if argspec.unzip_encoding:
                    zipInfo = zfp.infolist()
                    for member in zipInfo:
                        member.filename = member.filename.encode("cp437").decode('cp949')
                        zfp.extract(member, path=unzip_folder)
                else:
                    zfp.extractall(path=unzip_folder)
            print(os.path.abspath(unzip_folder), end='')
        elif argspec.operation == 'List':
            with zipfile.ZipFile(argspec.zipfile) as zfp:
                for i, file in enumerate(zfp.namelist()):
                    if i > 0:
                        print()
                    print(file, end='')
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
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
            owner='ARGOS-LABS',
            group='9',  # Utility Tools
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Zip/Unzip',
            icon_path=get_icon_path(__file__),
            description='zip unzip file',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('operation', choices=OP_LIST,
                          display_name='Operation', default=OP_LIST[-1],
                          help='choose zip or unzip or add-to-zip or list.')
        mcxt.add_argument('zipfile', input_method='fileread',
                          display_name='Zipfile',
                          help='zipfile to zip or unzip')
        mcxt.add_argument('files', input_method='fileread',  nargs='*',
                          display_name='Files',
                          help='Path of a file or a folder of files to zip')
        # ##################################### for app dependent options
        mcxt.add_argument('--password',
                          display_name='Password',
                          input_method='password',
                          help='Apply password for zip/unzip')
        mcxt.add_argument('--folders', input_method='folderread',  # nargs='*',
                          action='append', show_default=True,
                          display_name='Folders',
                          help='Path of a folder to zip')
        mcxt.add_argument('--unzip-folder', input_method='folderread',
                          display_name='Unzip Folder',
                          help='Target folder to unzip. '
                               'Default is current directory')
        mcxt.add_argument('--comp-type', choices=list(COMP_TYPE.keys()),
                          display_name='Comp Type',
                          default='STORED',
                          help='Set type of compress, default is STORED')
        mcxt.add_argument('--comp-level', choices=COMP_LEVEL,
                          display_name='Comp Level',
                          default=5, type=int,
                          help='Set level of compress, default is 5, '
                               'valid for ZLIB or BZ2')
        mcxt.add_argument('--unzip-encoding', action='store_true',
                          display_name='Unzip encoding',
                          help='filename encoding')
        argspec = mcxt.parse_args(args)
        return zip_unzip(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
