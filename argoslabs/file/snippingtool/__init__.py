"""
====================================
 :mod:`argoslabs.file.snippingtool`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for screen capture plugin
"""
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2020/10/21]
#    - build a plugin
#  * [2020/10/21]
#     - starting

################################################################################
import os
import sys
import time
import shutil
import subprocess
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
def do_screenshot(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    out_d = os.path.join(os.path.expanduser('~'), 'Documents', 'Screenshot')
    if not os.path.exists(out_d):
        os.makedirs(out_d)
    tempdir = None
    try:
        if sys.platform != 'win32':
            raise SystemError('Only Windows OS is supported!')
        if os.path.isdir(argspec.filepath):
            tempdir = os.path.join(argspec.filepath, 'Argos-capture.png')
            if os.path.exists(tempdir):
                fn, ext = os.path.splitext(tempdir)
                for n in range(1, 1000000):
                    nfn = f'{fn} ({n})' + ext
                    if not os.path.exists(nfn):
                        tempdir = nfn
                        break
            argspec.filepath = tempdir
        else:
            sps = os.path.splitext(argspec.filepath.lower())[-1]
            if not sps in ('.png', '.jpg', '.bmp'):
                raise RuntimeError('Only support file extension of ("*.png", "*.jpg", "*.bmp")')
        temptxt = os.path.join(out_d, 'screenshot.txt')
        with open(temptxt, 'w') as t:
            t.write(argspec.filepath)
            t.close()
        windnd = os.path.dirname(
            os.path.abspath(__file__)) + os.path.sep + 'Screenshot.exe'
        t = os.path.join(out_d, 'screenshot.out')
        po = subprocess.Popen(windnd)
        po.wait()
        time.sleep(0.1)
        with open(t, encoding='utf-8') as ifp:
            print(ifp.read().strip(), end='')
        sys.stdout.flush()
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        if os.path.exists(out_d) and not tempdir:
            shutil.rmtree(out_d)
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS',
            group='7',
            version='1.0',
            platform=['windows'],  # , 'darwin', 'linux'],
            output_type='text',
            display_name='Screen Snipping',
            icon_path=get_icon_path(__file__),
            description='take a screen capture',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('filepath',
                          display_name='Output Filepath',
                          input_method='filewrite',
                          help='An absolute file path to save an output')
        # ##################################### for app dependent parameters
        argspec = mcxt.parse_args(args)
        return do_screenshot(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
