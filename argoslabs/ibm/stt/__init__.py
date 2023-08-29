"""
====================================
 :mod:`argoslabs.ibm.stt`
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
#  * [2021/04/08]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2021/01/23]
#     - mis-spell "Waston" => "Watson"
#       It is required that you pass in a value for the "algorithms" argument
#       when calling decode().
#       upgrade to recent version for ibm-cloud-sdk-core and ibm-watson
#     - suppress InsecureRequestWarning
#  * [2020/03/05]
#     - change DisplayName starting with "IBM "
#  * [2019/08/11]
#     - starting

################################################################################
import os
import sys
import csv
import requests
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from requests.packages.urllib3.exceptions import InsecureRequestWarning


MODEL_LIST = [
    "ar-AR_BroadbandModel",
    "de-DE_BroadbandModel", "de-DE_NarrowbandModel",
    "en-GB_BroadbandModel", "en-GB_NarrowbandModel",
    "en-US_BroadbandModel", "en-US_NarrowbandModel",
    "en-US_ShortForm_NarrowbandModel",
    "es-AR_BroadbandModel", "es-AR_NarrowbandModel",
    "es-ES_BroadbandModel", "es-ES_NarrowbandModel",
    "es-CL_BroadbandModel", "es-CL_NarrowbandModel",
    "es-CO_BroadbandModel", "es-CO_NarrowbandModel",
    "es-MX_BroadbandModel", "es-MX_NarrowbandModel",
    "es-PE_BroadbandModel", "es-PE_NarrowbandModel",
    "fr-FR_BroadbandModel", "fr-FR_NarrowbandModel",
    "ja-JP_BroadbandModel", "ja-JP_NarrowbandModel",
    "ko-KR_BroadbandModel", "ko-KR_NarrowbandModel",
    "pt-BR_BroadbandModel", "pt-BR_NarrowbandModel",
    "zh-CN_BroadbandModel", "zh-CN_NarrowbandModel"
]

CONTENT_TYPE = [
    "application/octet-stream",
    "audio/alaw",
    "audio/basic",
    "audio/flac",
    "audio/g729",
    "audio/l16",
    "audio/mp3",
    "audio/mpeg",
    "audio/mulaw",
    "audio/ogg",
    "audio/ogg;codecs=opus",
    "audio/ogg;codecs=vorbis",
    "audio/wav",
    "audio/webm",
    "audio/webm;codecs=opus",
    "audio/webm;codecs=vorbis",
]

################################################################################
@func_log
def do_stt(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if not argspec.apikey:
            raise IOError('Invalid API key' % argspec.apikey)
        if not os.path.exists(argspec.audio):
            raise IOError('Cannot Open image file "%s"' % argspec.audio)

        # svc = SpeechToTextV1(
        #     url='https://stream.watsonplatform.net/speech-to-text/api',
        #     iam_apikey=argspec.apikey)

        authenticator = IAMAuthenticator(argspec.apikey)
        svc = SpeechToTextV1(authenticator=authenticator)
        svc.set_service_url('https://stream.watsonplatform.net/speech-to-text/api')
        # svc.set_service_url('https://api.us-east.speech-to-text.watson.cloud.ibm.com')
        svc.set_disable_ssl_verification(True)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        # model = svc.get_model(argspec.model).get_result()
        # response = svc.set_model()

        h = ('word', 'confidence')
        with open(argspec.audio, 'rb') as ifp:
            response = svc.recognize(
                audio=ifp,
                content_type=argspec.type,
                model=argspec.model,
                word_confidence=argspec.word_confidence,
                smart_formatting=argspec.smart_formatting,
                end_of_phrase_silence_time=argspec.end_time,
                background_audio_suppression=argspec.background_suppress,
            )
            if response.status_code // 10 != 20:
                raise RuntimeError('API response code is not 20? but "%s"'
                                   % response.status_code)
            # jds = json.dumps(response.result, indent=1)
            # print(jds)
            rj = response.result
            c = csv.writer(sys.stdout, lineterminator='\n')
            rjcl = rj.get('results')
            if not (rjcl and isinstance(rjcl, list)):
                raise ValueError('Invalid Result "%s"' % rj)
            rjcl = rjcl[0].get('alternatives')
            if not (rjcl and isinstance(rjcl, list)):
                raise ValueError('Invalid Result "%s"' % rj)
            if argspec.word_confidence:
                rjcl = rjcl[0].get('word_confidence')
                if not (rjcl and isinstance(rjcl, list)):
                    raise ValueError('Invalid Result "%s"' % rj)
                if rjcl:
                    c.writerow(h)
                for row in rjcl:
                    c.writerow(row)
            else:
                rjcl = rjcl[0].get('transcript')
                if not rjcl:
                    raise ValueError('Invalid Result "%s"' % rj)
                print(rjcl.strip(), end='')
        return 0
    except Exception as err:
        msg = str(err)
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
        display_name='IBM Speech to Text',
        icon_path=get_icon_path(__file__),
        description='IBM Watson Speech to Text. {{https://cloud.ibm.com/apidocs/speech-to-text?code=python}}',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--word-confidence',
                          display_name='Word Confidence', action='store_true',
                          help='If this flag is set, output is CSV format with "word, confidence"')
        mcxt.add_argument('--smart-formatting',
                          display_name='Smart Formatting', action='store_true',
                          help='If this flag is set, smart formatting is applied.')
        mcxt.add_argument('--end-time',
                          display_name='End Time', type=float, default=0.8,
                          min_value=0.0, max_value=120.0,
                          help='Set end of phrase silence time. Default is [[0.8]] sec.'
                               ' Value range is 0.0 ~ 120.0')
        mcxt.add_argument('--background-suppress',
                          display_name='Background Suppress', type=float, default=0.0,
                          min_value=0.0, max_value=1.0,
                          help='Set the level to which service is to suppress '
                               'background audio. Default is [[0.0]].'
                               ' Value range is 0.0 ~ 1.0')
        # ##################################### for app dependent parameters
        mcxt.add_argument('apikey',
                          display_name='API key', input_method='password',
                          help='Calendar for region')
        mcxt.add_argument('audio',
                          display_name='Audio file', input_method='fileread',
                          help='Audio file to recognize')
        mcxt.add_argument('type',
                          choices=CONTENT_TYPE,
                          display_name='Audio type',
                          help='Audio file type')
        mcxt.add_argument('model',
                          display_name='Lang Model',
                          choices=MODEL_LIST,
                          default='en-US_BroadbandModel',
                          help='Audio file to recognize')
        argspec = mcxt.parse_args(args)
        return do_stt(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
