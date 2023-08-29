"""
====================================
 :mod:`argoslabs.api.openai`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for EasyOCR API Server
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# ----------
#
#  * [2023/06/11]
#     - Use OpenAI API

################################################################################
import os
import sys
import csv
import json
import yaml
import openai
import base64
import requests
#from pathlib import Path
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
OPS = [
    'Chat',
    'Gen Images',
    "Speech to Text",
    'List Models',
    'Model Info',
]

IMG_SIZES = [
    "256x256",
    "512x512",
    "1024x1024",
]


################################################################################
# noinspection PyProtectedMember
@func_log
def do_main(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if not argspec.org_id:
            raise ValueError(f'Invalid "Org ID"')
        if not argspec.api_key:
            raise ValueError(f'Invalid "API Key"')
        openai.organization = argspec.org_id
        openai.api_key = argspec.api_key

        if argspec.op == OPS[0]:        # Chat
            if not argspec.model:
                raise ValueError(f'Invalid Model name')
            messages = []

            if argspec.ref_text_file and os.path.exists(argspec.ref_text_file):
                with open(argspec.ref_text_file, encoding=argspec.encoding) as ifp:
                    content = ifp.read()
                messages.append({
                    'role': 'system',
                    'content': 'You are a helpful assistant.',
                })
                messages.append({
                    'role': 'assistant',
                    'content': content
                })
            if argspec.messages_yaml:
                if not os.path.exists(argspec.messages_yaml):
                    raise IOError(f'Invalid Messages YAML file: "{argspec.messages_yaml}"')
                with open(argspec.messages_yaml,
                          encoding=argspec.encoding) as ifp:
                    messages.extend(yaml.load(ifp, yaml.SafeLoader))
            if argspec.prompt:
                messages.append({
                    'role': 'user',
                    'content': argspec.prompt,
                })
            if not messages:
                raise ValueError(f'Invalid messages')
            ar = openai.ChatCompletion.create(
                model=argspec.model,
                messages=messages,
            )
            if argspec.text_output:
                ltxt = []
                for choice in ar['choices']:
                    ltxt.append(choice['message']['content'])
                print('\n'.join(ltxt))
            else:
                print(json.dumps(ar, ensure_ascii=False))
        elif argspec.op == OPS[1]:      # Gen Images
            if not argspec.prompt:
                raise ValueError(f'Invalid prompt to generate image')
            ar = openai.Image.create(
                prompt=argspec.prompt,
                n=argspec.num_imgs,
                size=argspec.img_size,
            )
            for i, data in enumerate(ar['data']):
                url = data['url']
                rp = requests.get(url)
                img_f = f'{argspec.img_prefix}{i}.jpg'
                with open(img_f, 'wb') as ofp:
                    ofp.write(rp.content)
                print(os.path.abspath(img_f))
        elif argspec.op == OPS[2]:      # Speech to Text
            if not (argspec.voice_file and os.path.exists(argspec.voice_file)):
                raise IOError(f'Invalid voice file: "{argspec.voice_file}"')
            with open(argspec.voice_file, 'rb') as ifp:
                ar = openai.Audio.transcribe('whisper-1', ifp)
            if argspec.text_output:
                print(ar['text'])
            else:
                print(json.dumps(ar, ensure_ascii=False))
        elif argspec.op == OPS[3]:      # List Models
            ar = openai.Model.list()
            for m in ar.data:
                print(f'{m["id"]}')
        elif argspec.op == OPS[4]:      # Model Info
            if not argspec.model:
                raise ValueError(f'Invalid Model name')
            ar = openai.Model.retrieve(argspec.model)
            print(ar)
        else:
            raise ValueError(f'Invalid Operation "{argspec.op}"')
        return 0
    except ValueError as e:
        msg = f'Invalid Argument Error: {str(e)}'
        sys.stderr.write(msg)
        mcxt.logger.error(msg)
        return 1
    except IOError as e:
        msg = f'IO Error: {str(e)}'
        sys.stderr.write(msg)
        mcxt.logger.error(msg)
        return 2
    except Exception as e:
        msg = f'Error: {str(e)}'
        sys.stderr.write(msg)
        mcxt.logger.error(msg)
        return 99
    finally:
        mcxt.logger.info('>>>ended!')


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
        display_name='OpenAI API',
        icon_path=get_icon_path(__file__),
        description='This is a plugin for Multi lingual RikAI API call and get the result',
    ) as mcxt:

        # ##################################### for app dependent parameters
        mcxt.add_argument('org_id',
                          display_name='Org ID',
                          input_method='password',
                          help='OpenAI Organization ID')
        mcxt.add_argument('api_key',
                          display_name='API Key',
                          input_method='password',
                          help='OpenAI API Key')
        mcxt.add_argument('op',
                          display_name='Operation',
                          choices=OPS,
                          default=OPS[0],
                          help=f'Operations, default is [[{OPS[0]}]]')

        # ######################################## for app dependent options
        mcxt.add_argument('--ref-text-file',
                          input_method='fileread',
                          display_name='Ref Txt File',
                          help='Text file and using this query is referenced for Chat')
        mcxt.add_argument('--prompt',
                          display_name='Prompt',
                          help='Prompt for Chating or Gen Image')
        mcxt.add_argument('--model',
                          display_name='Model Name',
                          help='OpenAI Model name for Chat and model info')
        mcxt.add_argument('--messages-yaml',
                          input_method='fileread',
                          display_name='Msgs YAML File',
                          help='Messages YAML File')
        mcxt.add_argument('--text-output',
                          action='store_true',
                          display_name='Is Text Out',
                          help='If this flag is set then text output not JSON')
        mcxt.add_argument('--voice-file',
                          input_method='fileread',
                          display_name='Voice file',
                          help='Voice recording file for "Speech to Text"')
        mcxt.add_argument('--num-imgs',
                          display_name='Num Imgs',
                          type=int,
                          default=1,
                          help='Number of Images to be generated, default if [[1]]')
        mcxt.add_argument('--img-size',
                          display_name='Img Size',
                          choices=IMG_SIZES,
                          default=IMG_SIZES[0],
                          help=f'Image size selections, default is [[{IMG_SIZES[0]}]]')
        mcxt.add_argument('--img-prefix',
                          display_name='Img Prefix',
                          default="gen_img_",
                          help='The prefix of file names to be generated and append number.jpg, default is [[gen_img_]]')
        mcxt.add_argument('--encoding',
                          default='utf-8',
                          display_name='Encoding',
                          help='Encoding for input File')
        argspec = mcxt.parse_args(args)
        return do_main(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
