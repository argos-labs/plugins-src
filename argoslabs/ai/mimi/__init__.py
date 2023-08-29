"""
====================================
 :mod:`argoslabs.ai.mimi`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/03/25]
#     - 그룹에 "1 - AI Solutions" 넣음
#  * [2020/03/07]
#     - Change displayName 'mimi AI' => 'Fairy Devices mimi AI'
#  * [2020/03/02]
#     - Debug --out-wave
#  * [2020/03/01]
#     - 계속 dumpspec 에서 문제가 발생하여 확인하여 보니,
#       choices=Mimi.LANGS.keys() => choices=list(Mimi.LANGS.keys())
#       dict의 generator를 넣고 있었던 문제 였음
#  * [2020/02/29]
#     - Mimi class
#  * [2020/02/26]
#     - starting
#     - hot to get token : https://mimi.readme.io/docs/first-step#section-%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9%E3%83%88%E3%83%BC%E3%82%AF%E3%83%B3%E3%81%AE%E7%99%BA%E8%A1%8C
#     - sample python code : https://github.com/FairyDevicesRD/mimi.example.python

################################################################################
import os
import sys
import csv
import json
import time
import requests
import warnings
from tempfile import gettempdir
from multiprocessing import Process
# noinspection PyPackageRequirements
from playsound import playsound
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
def play_sound(audio_file):
    playsound(audio_file)


################################################################################
class Mimi(object):
    OPS = [
        'Audio Recognition',
        'Text to Speech',
        'Translation',
    ]
    LANGS = {
        'Japanese': 'ja',
        'English': 'en',
        'Spanish': 'es',
        'French': 'fr',
        'Indonesia': 'id',
        'Korean': 'ko',
        'Myanmar': 'my',
        'Thai': 'th',
        'Vietnamese': 'vi',
        'Chinese': 'zh',
    }

    # ==========================================================================
    def __init__(self, app_id, client_id, secret):
        self.app_id = app_id
        self.client_id = client_id
        self.secret = secret
        # for internal
        self.token = None
        self.get_token()

    # ==========================================================================
    def get_token(self):
        files = {
            'grant_type': (None,
                           'https://auth.mimi.fd.ai/grant_type/client_credentials'),
            'client_id': (None, f'{self.app_id}:{self.client_id}'),
            'client_secret': (None, f'{self.secret}'),
        }
        data = {
            'scope': 'https://apis.mimi.fd.ai/auth/asr/websocket-api-service;'
                     'https://apis.mimi.fd.ai/auth/asr/http-api-service;'
                     'https://apis.mimi.fd.ai/auth/nict-asr/http-api-service;'
                     'https://apis.mimi.fd.ai/auth/nict-asr/websocket-api-service;'
                     'https://apis.mimi.fd.ai/auth/nict-tts/http-api-service;'
                     'https://apis.mimi.fd.ai/auth/nict-tra/http-api-service',
        }

        rp = requests.post('https://auth.mimi.fd.ai/v2/token', files=files,
                           data=data)
        jd = json.loads(rp.content)
        # print(rp.content)
        if rp.status_code // 10 != 20:
            raise ReferenceError(f'Cannot get token: {jd.get("error")}')
        self.token = jd['accessToken']
        return self.token

    # ==========================================================================
    def audio_recognize(self, raw_file):
        if not os.path.exists(raw_file):
            raise IOError(f'Cannot read raw file {raw_file}')
        try:
            headers = {
                'Content-Type': 'audio/x-pcm;bit=16;rate=16000;channels=1',
                'x-mimi-process': 'asr',
                'x-mimi-input-language': 'ja',
                'Authorization': f'Bearer {self.token}',
            }
            with open(raw_file, 'rb') as ifp:
                file_data = ifp.read()
            rp = requests.post('https://service.mimi.fd.ai/',
                               headers=headers, data=file_data)
            if rp.status_code // 10 != 20:
                raise ReferenceError(f'Cannot recognize audio: {rp.content.decode()}')
            jd = json.loads(rp.content)
            ch = ('pronunciation', 'result', 'start', 'end')
            c = csv.writer(sys.stdout, lineterminator='\n')
            c.writerow(ch)
            for rd in jd.get('response', []):
                row = [
                    rd['pronunciation'], rd['result'],
                    rd['time'][0], rd['time'][1]
                ]
                c.writerow(row)
        except Exception:
            raise

    # ==========================================================================
    def tts(self, lang, text, outfile):
        if lang not in self.LANGS.keys():
            raise ValueError(f'Not supported language "{lang}"')
        headers = {
            'Authorization': f'Bearer {self.token}',
        }
        data = {
            'text': text,
            'lang': self.LANGS[lang],
            'engine': 'nict',
        }

        url = 'https://tts.mimi.fd.ai/speech_synthesis'
        resp = requests.post(url, headers=headers, data=data)
        if resp.status_code // 10 != 20:
            msg = f'TTS error: {resp.content.decode()}'
            sys.stderr.write(f'{msg}\n')
            # raise RuntimeError(msg)
        with open(outfile, 'wb') as fout:
            fout.write(resp.content)

    # ==========================================================================
    def tranlate(self, in_lang, text, out_lang):
        if in_lang not in self.LANGS.keys():
            raise ValueError(f'Not supported language "{in_lang}" for input')
        if out_lang not in self.LANGS.keys():
            raise ValueError(f'Not supported language "{out_lang}" for output')
        if in_lang == out_lang:
            raise ValueError(f'Input language and Out language must not same')
        if in_lang != 'Japanese' and out_lang != 'Japanese':
            raise ValueError(f'One of Input language or Out language must be Japanese')
        headers = {
            'Authorization': f'Bearer {self.token}',
        }
        data = {
            'text': text,
            'source_lang': self.LANGS[in_lang],
            'target_lang': self.LANGS[out_lang],
        }
        url = 'https://tra.mimi.fd.ai/machine_translation'
        resp = requests.post(url, headers=headers, data=data)
        if resp.status_code // 10 != 20:
            msg = f'Translate error: {resp.content.decode()}'
            sys.stderr.write(f'{msg}\n')
            # raise RuntimeError(msg)
        else:
            rj = resp.json()
            print('\n'.join(rj))


################################################################################
@func_log
def do_vr(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        warnings.simplefilter("ignore", ResourceWarning)
        mm = Mimi(argspec.app_id, argspec.client_id, argspec.client_secret)
        if Mimi.OPS.index(argspec.op) == 0:     # Audio Recognition
            if not (argspec.audio_file and os.path.exists(argspec.audio_file)):
                raise IOError(f'Invalid Audio file for {argspec.op}')
            mm.audio_recognize(argspec.audio_file)
        elif Mimi.OPS.index(argspec.op) == 1:   # Text to Speech
            if not argspec.text:
                raise ValueError(f'Empty Input Text for {argspec.op}')
            if argspec.out_wave:
                out_wave = argspec.out_wave
                is_temp = False
            else:
                out_wave = os.path.join(gettempdir(), 'mimi-audio.wav')
                is_temp = True
            try:
                mm.tts(argspec.in_lang, argspec.text, out_wave)
                if not os.path.exists(out_wave):
                    raise IOError(f'Connot get audio error, not saved {out_wave}')
                # playsound(audio_file)
                p = Process(target=play_sound, args=(out_wave,))
                p.start()
                p.join()
            finally:
                if is_temp and os.path.exists(out_wave):
                    for _ in range(100):
                        try:
                            os.remove(out_wave)
                            break
                        except Exception as e:
                            time.sleep(1)
                            sys.stdout.write(str(e))
        elif Mimi.OPS.index(argspec.op) == 2:   # Translation
            if not argspec.text:
                raise ValueError(f'Empty Input Text for {argspec.op}')
            mm.tranlate(argspec.in_lang, argspec.text, argspec.out_lang)
        return 0
    except Exception as err:
        msg = str(err).rstrip()
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
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
        group='1',  # AI Solutions
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Fairy Devices mimi AI',
        icon_path=get_icon_path(__file__),
        description='Mimi AI for Audio reconition, TTS and translation. Refer '
                    '{{https://console.mimi.fd.ai/console/v1/login}}',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--audio-file',
                          display_name='Audio file', input_method='fileread',
                          help='Raw audio file to recognize')
        mcxt.add_argument('--text',
                          display_name='Input Text',
                          help='Input text for TTS or Translation')
        ##
        mcxt.add_argument('--in-lang', choices=list(Mimi.LANGS.keys()),
                          display_name='Input language', default='Japanese',
                          help='Input language for Input Text')
        mcxt.add_argument('--out-lang', choices=list(Mimi.LANGS.keys()),
                          display_name='Output language', default='Japanese',
                          help='Output language for Translation')
        mcxt.add_argument('--out-wave',
                          display_name='Out Wave File', input_method='filewrite',
                          help='Output wave file for Text to Speech.')
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Operation', choices=Mimi.OPS,
                          help='Choose an Operation using Mimi AI')
        mcxt.add_argument('app_id',
                          display_name='App Id', input_method='password',
                          help='Application Id from Mimi')
        mcxt.add_argument('client_id',
                          display_name='Client Id', input_method='password',
                          help='Client Id from Mimi')
        mcxt.add_argument('client_secret',
                          display_name='Client Secret', input_method='password',
                          help='Client Secret from Mimi')
        argspec = mcxt.parse_args(args)
        return do_vr(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
