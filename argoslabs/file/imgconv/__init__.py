#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.file.imgconv`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for converting encoding
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/06]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2021/01/11]
#     - starting

################################################################################
import os
import sys
import PIL.features
from io import StringIO
from PIL import Image
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from alabs.common.util.vvencoding import get_file_encoding


################################################################################
IMGTYPE = {
    'open': {},
    'save': {}
}


################################################################################
def get_img_type():
    ofp = StringIO()
    PIL.features.pilinfo(ofp)
    imginfo = {'name': None, 'exts': None, 'feat': None}
    for line in ofp.getvalue().split('\n'):
        line = line.rstrip()
        if line.startswith('----'):
            if imginfo['name'] and imginfo['exts'] and imginfo['feat']:
                if 'open' in imginfo['feat']:
                    IMGTYPE['open'][imginfo['name']] = imginfo
                if 'save' in imginfo['feat']:
                    IMGTYPE['save'][imginfo['name']] = imginfo
            imginfo = {'name': None, 'exts': None, 'feat': None}
            continue
        if line.startswith('Extensions: '):
            imginfo['exts'] = line[12:].split(', ')
        elif line.startswith('Features: '):
            imginfo['feat'] = line[10:].split(', ')
        else:
            imginfo['name'] = line


################################################################################
def get_img_type_from_ext(sv):
    for k, v in IMGTYPE['open'].items():
        if ', '.join(v['exts']) == sv:
            return k
    raise ValueError(f'Inavlid extension {sv}')


################################################################################
def get_safe_tf(tf):
    cnt = 1
    ntf = tf
    while os.path.exists(ntf):
        fn, ext = os.path.splitext(tf)
        ntf = fn + f' ({cnt})' + ext
        cnt += 1
    return ntf


################################################################################
def conv_img(f, src_type, target_type, tlist):
    _, ext = os.path.splitext(f)
    s_ii = IMGTYPE['open'][src_type]
    if ext.lower() not in s_ii['exts']:
        return tlist
    tf = os.path.splitext(f)[0] + IMGTYPE['save'][target_type]['exts'][-1]
    tf = get_safe_tf(tf)
    img = Image.open(f)
    out = img.convert("RGB")
    ttype = target_type.split()[0]
    out.save(tf, ttype)  # , quality=90)
    tlist.append(os.path.abspath(tf))
    return tlist


################################################################################
def conv_tree(f, src_type, target_type, tlist, recursive=False):
    if os.path.isfile(f):
        return conv_img(f, src_type, target_type, tlist)
    if not os.path.isdir(f):
        return tlist
    for root, dirs, files in os.walk(f):
        for file_ in files:
            sf = os.path.join(root, file_)
            conv_img(sf, src_type, target_type, tlist)
        if not recursive:
            break
    return tlist


################################################################################
@func_log
def img_convert(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        if not argspec.src_ext:
            raise RuntimeError('Invalid Srouce extension')
        src_type = get_img_type_from_ext(argspec.src_ext)
        if not argspec.target_type:
            raise RuntimeError('Invalid Target Image Type')
        if src_type == argspec.target_type:
            raise ValueError(f'Cannot convert same image type of "{src_type}"')
        tlist = list()
        conv_tree(argspec.src, src_type, argspec.target_type, tlist,
                  recursive=argspec.recursive)
        print('\n'.join(tlist), end='')
        return 0
    except Exception as e:
        msg = 'argoslabs.file.encoding Error: %s' % str(e)
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
    get_img_type()
    with ModuleContext(
        owner='ARGOS-LABS',
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Convert Image',
        icon_path=get_icon_path(__file__),
        description='Convert Image type',
    ) as mcxt:
        src_ext_choices = [', '.join(x['exts']) for x in IMGTYPE['open'].values()]
        target_type_choices = list(IMGTYPE['save'].keys())
        # ##################################### for app dependent parameters
        mcxt.add_argument('src_ext',
                          display_name='Src Img Ext',
                          choices=src_ext_choices,
                          help='Source Image Extension')
        mcxt.add_argument('src',
                          display_name='Source File/Folder',
                          input_method='fileread',
                          help='Source file name')
        mcxt.add_argument('target_type',
                          display_name='Target Image Type',
                          choices=target_type_choices,
                          help='Target Image Type')
        # ##################################### for app dependent options
        mcxt.add_argument('--recursive',
                          display_name='Apply SubFolders',
                          action='store_true',
                          help='If this flag is set')

        argspec = mcxt.parse_args(args)
        return img_convert(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
