"""
====================================
 :mod:`argoslabs.interactive.dragdrop`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for google vision API
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/02/18]
#     - Image Drop Only => Online Image Drop
#  * [2021/04/09]
#     - 그룹에 "7-Interactive" 넣음
#  * [2020/03/17]
#     - STU,PAM 에서 관리자 권한을 빼고 정상 Drag&Drop이 되므로 암호 등 뺌
#     - 해당 windnd.out 을 읽는 것을 확인
#  * [2019/11/12]
#     - starting

################################################################################
import os
import sys
import time
import glob
import shutil
import subprocess
from tempfile import mkdtemp
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from random import randint


################################################################################
def get_tmp_fn(f):
    dn = os.path.dirname(f)
    bn = os.path.basename(f)
    fn, ext = os.path.splitext(bn)
    while True:
        rn = randint(10000000, 99999999)
        tf = os.path.join(dn, f'{fn}_{rn}{ext}')
        if not os.path.exists(tf):
            return tf


################################################################################
@func_log
def do_dragdrop(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    out_d = os.path.join(os.path.expanduser('~'), 'Documents', 'DragAndDrop')
    if not os.path.exists(out_d):
        os.makedirs(out_d)
    tmpdir = mkdtemp(prefix='windnd_')
    try:
        if sys.platform != 'win32':
            raise SystemError('Only Windows OS is supported!')
        windnd = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + 'windnd.exe'
        # windnd_t = gettempdir() + os.path.sep + 'windnd.exe'
        # if not os.path.exists(windnd_t):
        # shutil.copy(windnd, windnd_t)
        cmd = [
            windnd
        ]
        if argspec.filedrop_only:
            cmd.append('-f')
        if argspec.image_only:
            cmd.append('-i')
        cmd.append(tmpdir)
        po = subprocess.Popen(cmd)  # , stdout=subprocess.PIPE)
        po.wait()
        time.sleep(0.1)

        f_cnt = 0
        is_image = False
        for f in glob.glob(f'{tmpdir}{os.path.sep}image*'):
            bn = os.path.basename(f)
            tf = os.path.join(out_d, bn)
            tif = get_tmp_fn(tf)
            shutil.move(f, tif)
            print(tif, end='')
            is_image = True
            f_cnt += 1

        if not is_image:
            for f in glob.glob(f'{tmpdir}{os.path.sep}windnd.out'):
                with open(f, encoding='utf-8') as ifp:
                    print(ifp.read().strip(), end='')
                f_cnt += 1
        # if not is_found:
        #     raise IOError(f'Cannot read file "{out_f}"')
        sys.stdout.flush()
        if f_cnt <= 0:
            return 1    # 그냥 닫으면
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 9
    finally:
        # if os.path.exists(out_f):
        #     os.remove(out_f)
        shutil.rmtree(tmpdir)
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
        group='7',  # Interactive
        version='1.0',
        platform=['windows'],  # , 'darwin', 'linux'],
        output_type='text',
        display_name='Drag and Drop',
        icon_path=get_icon_path(__file__),
        description='Drag and drop object',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--filedrop-only',
                          display_name='File Drop Only', action='store_true',
                          help='If this flag is set, only file drop allowed')
        mcxt.add_argument('--image-only',
                          display_name='Online Image Drop', action='store_true',
                          help='If this flag is set, only image data drop allowed')
        # ##################################### for app dependent parameters
        argspec = mcxt.parse_args(args)
        return do_dragdrop(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
