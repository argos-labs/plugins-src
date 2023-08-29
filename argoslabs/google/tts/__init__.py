#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.google.tts`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module ai tts
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/07]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2020/04/29]
#     - add --file, --encoding options
#  * [2020/03/05]
#     - just change group display name
#     - remove engine parameter
#     - move argoslabs.ai.tts => argoslabs.google.tts
#  * [2019/10/09]
#     - chagne --lang choices into real language name
#  * [2019/04/25]
#     - add arguments' display_name
#  * [2019/03/08]
#     - starting

################################################################################
import os
import sys
import time
import shutil
from random import randint
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
# noinspection PyPackageRequirements
from gtts import gTTS
from tempfile import gettempdir
# noinspection PyPackageRequirements
from playsound import playsound


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
    'English (Australia)': 'en-au',
    'English (Canada)': 'en-ca',
    # 'English (UK)': 'en-gb',
    'English (Ghana)': 'en-gh',
    'English (Ireland)': 'en-ie',
    'English (India)': 'en-in',
    'English (Nigeria)': 'en-ng',
    'English (New Zealand)': 'en-nz',
    'English (Philippines)': 'en-ph',
    'English (Tanzania)': 'en-tz',
    'English (UK)': 'en-uk',
    'English (US)': 'en-us',
    'English (South Africa)': 'en-za',
    'English': 'en',
    'Esperanto': 'eo',
    'Spanish (Spain)': 'es-es',
    'Spanish (United States)': 'es-us',
    'Spanish': 'es',
    'Estonian': 'et',
    'Finnish': 'fi',
    'French (Canada)': 'fr-ca',
    'French (France)': 'fr-fr',
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
    'Portuguese (Brazil)': 'pt-br',
    'Portuguese (Portugal)': 'pt-pt',
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
def get_lang_code(la):
    if la in lang_dict:
        return lang_dict[la]


################################################################################
@func_log
def do_tts(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    mp3file = None
    try:
        if argspec.file:
            if not os.path.exists(argspec.file):
                raise IOError('Invalid message or text file')
            with open(argspec.file, encoding=argspec.encoding) as ifp:
                argspec.msg = ifp.read()
        if not argspec.msg:
            raise ValueError('Invalid or empty message or text file')
        lang = get_lang_code(argspec.lang)
        tts = gTTS(argspec.msg, lang=lang, slow=argspec.slow)
        mp3file = os.path.join(gettempdir(),
                               'gtts_%06d.mp3' % randint(1, 999999))
        if os.path.exists(mp3file):
            os.remove(mp3file)
        tts.save(mp3file)
        if not os.path.exists(mp3file):
            raise IOError('Result mp3 file "%s" does not exists.' % mp3file)
        playsound(mp3file)
        return 0
    except Exception as e:
        msg = 'TTS error: %s' % str(e)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        mcxt.logger.error(msg)
        return 1
    finally:
        time.sleep(1)
        if os.path.exists(mp3file):
            if argspec.save_mp3:
                shutil.move(mp3file, argspec.save_mp3, )
            else:
                os.remove(mp3file)
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
        group='1',  # AI Solutions
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Google TTS',
        icon_path=get_icon_path(__file__),
        description='Google Text-to-Speech',
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
        mcxt.add_argument('--save-mp3', '-o',
                          display_name='Save to mp3 file',
                          input_method='filewrite',
                          help='mp3 file to save the result of tts')
        mcxt.add_argument('--lang', '-l', default='English',
                          display_name='Language', show_default=True,
                          choices=list(lang_dict.keys()),
                          help='language to use '
                               'default is [[English]]')
        mcxt.add_argument('--slow', '-s', action='store_true',
                          display_name='Say slowly',
                          help='if set say slow TTS')
        # ##################################### for app dependent parameters
        # mcxt.add_argument('engine',
        #                   display_name='TTS Engine',
        #                   default='google',
        #                   choices=['google'],
        #                   help='TTS engine to use [[google]]')
        mcxt.add_argument('msg', help='message to TTS')
        argspec = mcxt.parse_args(args)
        return do_tts(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
