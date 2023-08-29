"""
====================================
 :mod:`argoslabs.naver.ocr`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Naver OCR plugin module
"""
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2020/03/27]
#     - add icon
#  * [2020/03/27]
#     - starting

################################################################################
import os
import cv2
import sys
import json
import time
import uuid
import base64
import requests
from io import StringIO
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class NaverOCRAPI(object):
    # ==========================================================================
    def __init__(self, argspec, alpha=0.7):
        self.argspec = argspec
        self.key = argspec.key
        self.url = argspec.url
        imgfile = argspec.imgfile
        if not os.path.exists(imgfile):
            raise IOError('Cannot read image file "%s"' % imgfile)
        self.imgfile = imgfile
        self.alpha = alpha
        self.box_imgfile = argspec.box_imgfile
        self.rd = None

    # ==========================================================================
    def get_api_result(self):
        with open(self.imgfile, "rb") as f:
            img = base64.b64encode(f.read())
        imgdir, ext = os.path.splitext(self.imgfile)
        img_format = ext.replace(".", "")
        headers = {'Content-Type': 'application/octet-stream',
                   'X-OCR-SECRET': self.key}
        data = {"version": "V2", "requestId": str(uuid.uuid4()),
                "timestamp": int(round(time.time() * 1000)),
                "images": [{"name": "image1", "format": img_format,
                            "data": img.decode('utf-8')}]}
        rp = requests.post(self.url, headers=headers,
                           data=json.dumps(data))
        if rp.status_code // 10 != 20:
            raise RuntimeError(f'Error of API: '
                               f'{rp.json().get("error", {}).get("message", "")}')
        self.rd = rp.json()
        return self.rd

    # ==========================================================================
    def text_box(self):
        if not self.rd:
            raise RuntimeError('Call get_api_result() first')
        line_infos = self.rd['images'][0]['fields']
        img = cv2.imread(self.imgfile, cv2.COLOR_BGR2RGB)
        overlay = img.copy()
        for i in range(0, len(line_infos)):
            b1 = list(line_infos[i]['boundingPoly']['vertices'][0].values())
            b2 = list(line_infos[i]['boundingPoly']['vertices'][2].values())
            x1, y1 = int(b1[0]), int(b1[1])
            x2, y2 = int(b2[0]), int(b2[1])
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
        image_new = cv2.addWeighted(overlay, self.alpha, img,
                                    1 - self.alpha, 0)
        cv2.imwrite(self.box_imgfile, image_new)

    # ==========================================================================
    def extract_data(self):
        if self.argspec.output_type=='json':
            self.get_api_result()
            print(json.dumps(self.rd,indent=4, ensure_ascii=False), end='')
        else:
            with StringIO() as outst:
                self.get_api_result()
                line_infos = self.rd['images'][0]['fields']
                lst = [-1]
                for i in range(0, len(line_infos) - 1):
                    bi = list(line_infos[i]['boundingPoly']['vertices'][0].values())
                    bj = list(line_infos[i + 1]['boundingPoly']['vertices'][0].values())
                    if bi[0] > bj[0]:
                        lst.append(i)
                lst = [i + 1 for i in lst]
                for i, line in enumerate(line_infos):
                    if i in lst:
                        outst.write('\n')
                    outst.write(line['inferText'])
                    outst.write(' ')
                if self.box_imgfile:
                    self.text_box()
                print(outst.getvalue(), end='')


################################################################################
@func_log
def naverocr_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        res = NaverOCRAPI(argspec)
        res.extract_data()
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        print(False)
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS',
            group='1',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='NAVER OCR',
            icon_path=get_icon_path(__file__),
            description='NAVER CLOUD PLATFORM OCR'
                        '{{https://www.ncloud.com/product/aiService/ocr}}',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--box-imgfile',
                          display_name='Out Img File', input_method='filewrite',
                          help='If set with file path to write then save result')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--output_type', display_name='Output Type',
                          help='output type', default='csv', choices = ['csv', 'json'])
        # # ##################################### for app dependent parameters
        mcxt.add_argument('key', display_name='Secret Key',
                          input_method='password',
                          help='customized key')
        # ----------------------------------------------------------------------
        mcxt.add_argument('url', display_name='APIGW Invoke URL',
                          help='customized URL')
        # ----------------------------------------------------------------------
        mcxt.add_argument('imgfile', display_name='Image file',
                          input_method='fileread',
                          help='test image')

        argspec = mcxt.parse_args(args)
        return naverocr_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
