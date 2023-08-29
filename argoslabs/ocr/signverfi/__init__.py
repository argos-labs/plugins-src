"""
======================================
 :mod: 'argoslabs.ocr.signiverfi'
======================================
 ..modeulauthor: Irene Cho <irene@argos-labs.com>
 ..note:: ARGOS-LABS Lincense

 Description
 ===========
 Argos Labs plugin module for signature verfication
"""
#
# Authors
# ============
#
# * Irene Cho
# Change Log
# ----------
#
# * [2021/05/20]
# - build a plugin
# * [2021/05/20]
# - starting

################################################################################
import os
import sys
import json
import base64
import warnings
import requests
from alabs.common.util.vvargs import func_log, get_icon_path, ArgsError, \
    ArgsExit, \
    ModuleContext

warnings.simplefilter("ignore")

################################################################################
@func_log
def do(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        headers = {
            'authorizationToken': argspec.token,
            'x-api-key': argspec.apikey,
            'Content-Type': 'application/json'
        }

        def convertimg(img):
            lst = []
            for i in img:
                if not os.path.exists(i):
                    raise IOError(f'{i} does not exist.')
                with open(i, 'rb') as f:
                    fn = base64.b64encode(f.read()).decode('utf8')
                    lst.append('"b ' + fn + '"')
            return lst

        if argspec.op == 'Signature Verfication':
            url = "https://api.intellica.ai/signature-verification"
            dt = json.dumps({
                "train_imgs": convertimg(argspec.trainimgs),
                "test_imgs": convertimg([argspec.testimgs])
            })
        elif argspec.op == 'Signature Checking':
            url = "https://api.intellica.ai/signature-checking"
            dt = json.dumps({"image": convertimg(argspec.trainimgs)[0]})
        response = requests.request("POST", url, headers=headers, data=dt,
                                    verify=False)
        if response.status_code // 10 != 20:
            # print(response.text, end='')
            msg = response.text
            mcxt.logger.error(msg)
            sys.stderr.write('%s' % (msg))
            return 9
        res = response.json()
        if len(res.keys())==1:
            res = res['result']
        for i in res.keys():
            print(i + ',', end='')
        print('\n', end='')
        for i in res.values():
            print(str(i) + ',', end='')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg.os.linesep))
        return 1
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS',
            group='1',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Signature Verfication',
            icon_path=get_icon_path(__file__),
            description='Verfiy Signauture images',
    ) as mcxt:
        # ######################################### for app dependent parameters
        mcxt.add_argument('op', display_name='OP Type', help='operation types',
                          choices=['Signature Verfication',
                                   'Signature Checking'])
        # ----------------------------------------------------------------------
        mcxt.add_argument('apikey', display_name='API Key', help='API Key',
                          input_method='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('token', display_name='API Token',
                          input_method='password',
                          help='API Token')
        # ----------------------------------------------------------------------
        mcxt.add_argument('trainimgs', display_name='(Train) Images',
                          nargs='+',
                          help='Images to train or for checking',
                          input_method='fileread')
        # ###################################### for app dependent options
        mcxt.add_argument('--testimgs', display_name='Test Images',
                          help='An image to test',
                          input_method='fileread',
                          show_default=True)
        argspec = mcxt.parse_args(args)
        return do(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
