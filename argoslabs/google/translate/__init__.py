#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.google.translate`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module ai translate
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/08/29]
#     - "九百十二万二千三百四十一", Japanese ==> English 의 결과가 922,22,441 이 나옴, 
#       구글 홈페이지에서는 9,222,341 나오는 문제 파악요 [Shige]
#  * [2021/07/05]
#     - 안된다고 보고됨 by Young
#     - googletrans==3.1.0a0 이용하여 해결
#  * [2021/04/07]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2020/12/04]
#     - Google API changed so new module using google_trans_new
#  * [2020/04/29]
#     - add --file, --encoding options
#  * [2020/03/05]
#     - just change group display name
#     - remove engine parameter
#     - move argoslabs.ai.translate => argoslabs.google.translate
#  * [2019/04/25]
#     - add arguments' display_name
#  * [2019/04/10]
#     - some en-us lang does not working
#  * [2019/03/08]
#     - starting

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
# noinspection PyPackageRequirements
from googletrans import Translator
# from google_trans_new import google_translator


################################################################################
lang_dict = {
    'Afrikaans': 'af',
    'Arabic': 'ar',
    'Bengali': 'bn',
    'Bosnian': 'bs',
    'Catalan': 'ca',
    'Czech': 'cs',
    'Welsh': 'cy',
    'Danish': 'da',
    'German': 'de',
    'Greek': 'el',
    'English': 'en',
    'Esperanto': 'eo',
    'Spanish': 'es',
    'Estonian': 'et',
    'Finnish': 'fi',
    'French': 'fr',
    'Hindi': 'hi',
    'Croatian': 'hr',
    'Hungarian': 'hu',
    'Armenian': 'hy',
    'Indonesian': 'id',
    'Icelandic': 'is',
    'Italian': 'it',
    'Japanese': 'ja',
    'Javanese': 'jw',
    'Khmer': 'km',
    'Korean': 'ko',
    'Latin': 'la',
    'Latvian': 'lv',
    'Macedonian': 'mk',
    'Malayalam': 'ml',
    'Marathi': 'mr',
    'Myanmar (Burmese)': 'my',
    'Nepali': 'ne',
    'Dutch': 'nl',
    'Norwegian': 'no',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Sinhala': 'si',
    'Slovak': 'sk',
    'Albanian': 'sq',
    'Serbian': 'sr',
    'Sundanese': 'su',
    'Swedish': 'sv',
    'Swahili': 'sw',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Thai': 'th',
    'Filipino': 'tl',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Vietnamese': 'vi',
    'Chinese (Mandarin/China)': 'zh-cn',
    'Chinese (Mandarin/Taiwan)': 'zh-tw',
}


################################################################################
def get_lang_code(lang):
    if lang == 'auto':
        return lang
    if lang in lang_dict:
        return lang_dict[lang]
    for k, v in lang_dict.items():
        if lang == v:
            return v
    raise LookupError('Cannot find language code from "%s"' % lang)


################################################################################
@func_log
def do_translate(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if argspec.file:
            if not os.path.exists(argspec.file):
                raise IOError('Invalid message or text file')
            with open(argspec.file, encoding=argspec.encoding) as ifp:
                argspec.msg = ifp.read()
        if not argspec.msg:
            raise ValueError('Invalid or empty message or text file')
        tr = Translator()
        # tr = google_translator(timeout=5)
        if argspec.detect:
            dl = tr.detect(argspec.msg)
            print('lang, confidence')
            print('%s, %s' % (dl.lang, dl.confidence), end='')
            # New google_trans_new does not get the confidence
            # print('%s, %s' % (dl[0], 'N/A'))
        else:
            dest = get_lang_code(argspec.dest)
            src = get_lang_code(argspec.src)
            # r_tr = tr.translate(argspec.msg,
            #                     lang_tgt=dest, lang_src=src)
            r_tr = tr.translate(argspec.msg,
                                dest=dest, src=src)
            print(r_tr.text, end='', flush=True)
        return 0
    except Exception as e:
        msg = 'Translation error: %s' % str(e)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        mcxt.logger.error(msg)
        return 1
    finally:
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
        group='1',   # AI Solutions
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Google Translate',
        icon_path=get_icon_path(__file__),
        description='Translate using Google Translate engine',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--file',
                          display_name='Text file', show_default=True,
                          input_method='fileread',
                          help='Text file to read message')
        mcxt.add_argument('--encoding',
                          display_name='File Encoding',
                          default='utf8',
                          help='File encoding for text file, default is [[utf8]].')
        src_list = list(lang_dict.keys())
        mcxt.add_argument('--dest', '-d', default='English',
                          display_name='Target lang', show_default=True,
                          choices=src_list,
                          help='Destination language to use, default is [[English]]')
        src_list.insert(0, 'auto')
        mcxt.add_argument('--src', '-s', default='auto',
                          display_name='Source lang',
                          choices=src_list,
                          help='Source language to use, default is "auto" means '
                               'automatic detection of language [[auto]]')
        mcxt.add_argument('--detect', action='store_true',
                          display_name='Detect lang',
                          help='If set this flag just guessing the language of message and confidence. '
                               'The result looks like "ko, 0.778"')
        # ##################################### for app dependent parameters
        # mcxt.add_argument('engine',
        #                   default='google',
        #                   choices=['google'],
        #                   help='Translating engine to use')
        mcxt.add_argument('msg', help='message to translate')
        argspec = mcxt.parse_args(args)
        return do_translate(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
