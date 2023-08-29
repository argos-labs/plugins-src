"""
====================================
 :mod:`argoslabs.api.easyocr`
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
#  * [2023/02/08]
#     - Use LazarusForms API Server

################################################################################
import os
import sys
import csv
import json
import yaml
import requests
from pathlib import Path
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
def get_questions(mcxt, argspec):
    ql = argspec.question
    if argspec.question_file and os.path.exists(argspec.question_file):
        with open(argspec.question_file, encoding=argspec.encoding) as ifp:
            for line in ifp:
                line = line.strip()
                ql.append(line)
    if not ql:
        raise ValueError(f'Invalid "Question"')
    return ql


################################################################################
def do_ocr(mcxt, argspec):
    ifp = None
    url = "https://api.lazarusforms.com/api/rikai"

    try:
        ifp = open(argspec.img, 'rb')
        ql = get_questions(mcxt, argspec)
        payload = {'question': ql}
        fn = Path(argspec.img).stem
        files = [
            ('file', (fn, ifp, 'application/octet-stream'))
        ]

        headers = {
            'orgId': argspec.org_id,
            'authKey': argspec.auth_key
        }

        rp = requests.request(
            "POST", url,
            headers=headers, data=payload,
            files=files
        )
        if rp.status_code // 10 != 20:
            emg = f'do_ocr: status_code={rp.status_code}: {rp.text}'
            raise RuntimeError(emg)

        rj = rp.json()
        cw = csv.writer(sys.stdout, lineterminator='\n')
        cw.writerow(['question', 'answer'])
        for qa in rj['data']:
            cw.writerow([
                qa['question'],
                qa['answer'],
            ])
        # print(rj['data'][0]['answer'], end='')
        if argspec.json_file:
            with open(argspec.json_file, 'w', encoding='utf-8') as ofp:
                ofp.write(json.dumps(rj, ensure_ascii=False))
        if argspec.yaml_file:
            with open(argspec.yaml_file, 'w', encoding='utf-8') as ofp:
                yaml.safe_dump(rj, ofp, allow_unicode=True)
        return 0
    finally:
        if ifp is not None:
            ifp.close()


################################################################################
# noinspection PyProtectedMember
@func_log
def do_main(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if not argspec.org_id:
            raise ValueError(f'Invalid "Org ID"')
        if not argspec.auth_key:
            raise ValueError(f'Invalid "Auth Key"')
        # if not argspec.question:
        #     raise ValueError(f'Invalid "Question"')
        if not os.path.exists(argspec.img):
            raise IOError(f'Invalid file "{argspec.img}"')
        return do_ocr(mcxt, argspec)
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
        display_name='Lazarus RikAI',
        icon_path=get_icon_path(__file__),
        description='This is a plugin for RikAI API call and get the result',
    ) as mcxt:

        # ##################################### for app dependent parameters
        mcxt.add_argument('org_id',
                          display_name='Org ID',
                          input_method='password',
                          help='Organization ID')
        mcxt.add_argument('auth_key',
                          display_name='Auth Key',
                          input_method='password',
                          help='Auth Key')
        mcxt.add_argument('img',
                          display_name='Img File',
                          input_method='fileread',
                          help='Image file to OCR')
        mcxt.add_argument('question', nargs='*',
                          display_name='Question',
                          help='Question for OCR')

        # ######################################## for app dependent options
        mcxt.add_argument('--question-file',
                          input_method='fileread',
                          display_name='Questions File',
                          help='File contains questions line by line')
        mcxt.add_argument('--encoding',
                          default='utf-8',
                          display_name='Encoding',
                          help='Encoding for Questions File')
        mcxt.add_argument('--json-file',
                          display_name='JSON File',
                          input_method='filewrite',
                          help='If this JSON file is given API result will be saved')
        mcxt.add_argument('--yaml-file',
                          display_name='YAML File',
                          input_method='filewrite',
                          help='If this YAML file is given API result will be saved')
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
