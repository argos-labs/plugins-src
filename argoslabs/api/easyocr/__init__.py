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
#  * [2023/02/01]
#     - Use EasyOCR API Server

################################################################################
import os
# import re
import sys
# import json
import csv
import glob
import yaml
import time
import asyncio
import requests
import functools
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
async def req_ocr(mcxt, argspec, img_dict):
    loop = asyncio.get_event_loop()

    headers = {
        'accept': 'application/json',
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
    }
    params = {
        'api_token': argspec.api_key,
    }
    url = argspec.url + 'ocr'
    # OCR 요청 : Non-blocking 호출
    for img_f, img_d in img_dict.items():
        fn, ext = os.path.splitext(img_f)
        img_d['img_fp'] = open(img_f, 'rb')
        files = {
            'file': img_d['img_fp'],  # , f'image/{ext}'),
        }
        img_d['future'] = loop.run_in_executor(
            None,
            functools.partial(
                requests.post,
                url, params=params, headers=headers, files=files,
                verify=False
            )
        )
    # 모든 OCR 호출의 결과를 걷어들임
    for img_d in img_dict.values():
        img_d['ocr_response'] = await img_d['future']

    # 각 OCR 호출 결과의 JSON을 구해옴
    for img_d in img_dict.values():
        if img_d['img_fp'] is not None:
            img_d['img_fp'].close()
            img_d['img_fp'] = None
        if img_d['ocr_response'].status_code // 10 != 20:
            img_d['task_status'] = 'ERROR'
            img_d['error'] = f'OCR call error: status_code={img_d["ocr_response"].status_code}'
            continue
        img_d['ocr_json'] = img_d['ocr_response'].json()

    # 모든 작업에 대하여 성공/오류가 아닌 (PENDING) 태스크에 대하여 결과 가져옴
    is_all_done = False
    while not is_all_done:
        pending_cnt = 0
        for img_d in img_dict.values():
            if img_d['ocr_json'] is None:
                continue
            if img_d['task_status'] in ('SUCCESS', 'ERROR'):
                continue
            pending_cnt += 1
            url = argspec.url + 'tasks/' + img_d['ocr_json']['task_id']
            img_d['task_response'] = requests.get(url, headers=headers, verify=False)
            if img_d['task_response'].status_code // 10 != 20:
                img_d['task_status'] = 'ERROR'
                img_d['error'] = f'Task call error: status_code={img_d["task_response"].status_code}'
            img_d['task_json'] = img_d['task_response'].json()
            img_d['task_status'] = img_d['task_json']['task_status']
        if pending_cnt == 0:
            is_all_done = True
        time.sleep(0.5)

    success_cnt = error_cnt = 0
    for img_d in img_dict.values():
        if img_d['task_status'] == 'SUCCESS' and not img_d['task_json']['task_result']['error']:
            success_cnt += 1
        else:
            error_cnt += 1

    # 결과를 CSV로 출력
    report_ocr(mcxt, argspec, img_dict)

    return success_cnt, error_cnt


################################################################################
def report_ocr(mcxt, argspec, img_dict):
    cw = csv.writer(sys.stdout, lineterminator='\n')
    cw.writerow(['index,img_file,result_text_file,result_yaml_file,is_error,error_msg'])
    for i, img_f in enumerate(sorted(img_dict.keys())):
        img_d = img_dict[img_f]
        task_json = img_d['task_json']
        if task_json is None:
            cw.writerow([
                i+1,
                img_f,
                '',
                '',
                'true',
                img_d['error'],
            ])
        else:
            bn, _ = os.path.splitext(img_f)
            # result text file
            with open(f'{bn}.txt', 'w', encoding='utf-8') as ofp:
                if not task_json['task_result']['text']:
                    ofp.write('')
                else:
                    ofp.write(task_json['task_result']['text'])
            # result yaml file
            with open(f'{bn}.yml', 'w', encoding='utf-8') as ofp:
                yaml.safe_dump(task_json, ofp, encoding='utf-8', allow_unicode=True)
            cw.writerow([
                i+1,
                img_f,
                f'{bn}.txt',
                f'{bn}.yml',
                'false',
                img_d['error'],
            ])


################################################################################
def do_ocr(mcxt, argspec, img_list):
    img_dict = {}
    for img_f in img_list:
        fn, ext = os.path.splitext(img_f)
        img_dict[img_f] = {
            'img_file': img_f,
            'img_fp': None,
            'txt_file': fn + '.txt',
            'future': None,
            'ocr_response': None,
            'ocr_json': None,
            'task_response': None,
            'task_status': None,
            'task_json': None,
            'start_ts': None,
            'end_ts': None,
            'error': '',
        }
    loop = asyncio.get_event_loop()
    success_cnt, error_cnt = loop.run_until_complete(req_ocr(mcxt, argspec, img_dict))
    loop.close()
    if error_cnt <= 0:
        # every OCR succeeded
        return 0
    if success_cnt > 0:
        # partial OCR have error
        return 1
    # NO succesful OCR
    return 2


################################################################################
# noinspection PyProtectedMember
@func_log
def do_main(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    rp = None
    try:
        if not os.path.exists(argspec.img_or_folder):
            raise IOError(f'Invalid file or folder "{argspec.img_or_folder}"')
        if not argspec.url:
            raise ValueError(f'Invalid URL')
        if not argspec.url.endswith('/'):
            argspec.url += '/'

        img_list = []
        if os.path.isfile(argspec.img_or_folder):
            argspec.img_or_folder = os.path.abspath(argspec.img_or_folder)
            fn, ext = os.path.splitext(argspec.img_or_folder)
            if ext.lower() not in argspec.img_ext_list.split(','):
                raise ValueError(f'Invalid extension "{ext}", not in "{argspec.img_ext_list}"')
            img_list.append(argspec.img_or_folder)
        elif os.path.isdir(argspec.img_or_folder):
            argspec.img_or_folder = os.path.abspath(argspec.img_or_folder)
            if argspec.recursive:
                glob_gn = glob.glob(os.path.join(argspec.img_or_folder, '**', '*.*'), recursive=True)
            else:
                glob_gn = glob.glob(os.path.join(argspec.img_or_folder, '*.*'))
            for f in glob_gn:
                fn, ext = os.path.splitext(f)
                if ext.lower() not in argspec.img_ext_list.split(','):
                    continue
                img_list.append(f)
        else:
            raise IOError(f'Invalid file or folder "{argspec.img_or_folder}"')

        return do_ocr(mcxt, argspec, img_list)
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
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='EasyOCR API',
        icon_path=get_icon_path(__file__),
        description='This is a plugin for EasyOCR API call and get the result',
    ) as mcxt:

        # ##################################### for app dependent parameters
        mcxt.add_argument('api_key',
                          display_name='API Key',
                          input_method='password',
                          help='API Key')
        mcxt.add_argument('img_or_folder',
                          display_name='Img or Folder',
                          # input_method='fileread',
                          help='Image file or folder in which containes images')

        # ######################################## for app dependent options
        mcxt.add_argument('--url',
                          display_name='API URL',
                          default='https://easyocr.argos-labs.com/',
                          help='URL for EasyOCR API server')
        mcxt.add_argument('--recursive', action="store_true",
                          display_name='Recursive',
                          help='If this flag is set and "Img or Folder" has the folder then proceed OCR for all images recursively')
        mcxt.add_argument('--img-ext-list',
                          display_name='Img Ext List',
                          default='.png,.jpg,.jpeg',
                          help='Image extension list, default is [[.png,.jpg,.jpeg]]')
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
