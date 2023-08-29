"""
====================================
 :mod:`argoslabs.msazure.text`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS MS Azure Text Analytics plugin module
"""
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2020/03/19]
#     - add icon
#  * [2020/03/19]
#     - starting

################################################################################
import os
import cv2
import sys
import requests
from io import StringIO
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class MSAzureTextsAPI(object):
    # ==========================================================================
    OCR_URL = "vision/v2.1/ocr"

    # ==========================================================================
    def __init__(self, argspec, alpha=0.7):
        self.argspec = argspec
        self.apimkey = argspec.apimkey
        self.endpoint = argspec.endpoint
        imgfile = argspec.imgfile
        if not os.path.exists(imgfile):
            raise IOError('Cannot read image file "%s"' % imgfile)
        self.imgfile = imgfile
        self.alpha = alpha
        self.box_imgfile = argspec.box_imgfile
        self.rd = None
        self.img = None

    # ==========================================================================
    def get_api_result(self):
        with open(self.imgfile, "rb") as ifp:
            image_data = ifp.read()
        headers = {'Content-Type': 'application/octet-stream',
                   'Ocp-Apim-Subscription-Key': self.apimkey}
        text_recognition_url = self.endpoint + self.OCR_URL
        rp = requests.post(text_recognition_url, headers=headers,
                           data=image_data,
                           params={'detectOrientation': 'true'})
        if rp.status_code // 10 != 20:
            raise RuntimeError(f'Error of API: '
                               f'{rp.json().get("error", {}).get("message", "")}')
        self.rd = rp.json()
        return self.rd

    # ==========================================================================
    def img_rotate(self):
        self.img = img = cv2.imread(self.imgfile, cv2.COLOR_BGR2RGB)
        if self.rd['orientation'] == 'Left':
            self.img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif self.rd['orientation'] == 'Right':
            # noinspection PyUnresolvedReferences
            self.img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif self.rd['orientation'] == 'Down':
            self.img = cv2.rotate(img, cv2.ROTATE_180)

    # ==========================================================================
    def text_box(self):
        if not self.rd:
            raise RuntimeError('Call get_api_result() first')
        self.img_rotate()
        overlay = self.img.copy()
        line_infos = [region["lines"] for region in self.rd["regions"]]
        word_infos = []
        for line in line_infos:
            for word_metadata in line:
                for word_info in word_metadata["words"]:
                    word_infos.append(word_info)
        for i in range(0, len(word_infos)):
            b = [int(num) for num in word_infos[i]['boundingBox'].split(",")]
            x1, y1 = b[0], b[1]
            x2, y2 = (b[0] + b[2]), (b[1] + b[3])
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color=(0, 0, 255),
                          thickness=1)
        image_new = cv2.addWeighted(overlay, self.alpha, self.img,
                                    1 - self.alpha, 0)
        cv2.imwrite(self.box_imgfile, image_new)

    # ==========================================================================
    def extract_data(self):
        with StringIO() as outst:
            self.get_api_result()
            line_infos = [region["lines"] for region in self.rd["regions"]]
            for line in line_infos:
                for word_metadata in line:
                    for i, word_info in enumerate(word_metadata["words"]):
                        if i > 0:
                            outst.write(' ')
                        outst.write(word_info['text'])
                    outst.write('\n')
                outst.write('\n')
            if self.box_imgfile:
                self.text_box()
            print(outst.getvalue(), end='')


################################################################################
@func_log
def msazuretexts_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        msa = MSAzureTextsAPI(argspec)
        msa.extract_data()
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
            display_name='MS Azure Text Analytics',
            icon_path=get_icon_path(__file__),
            description='MS Azure Text Analytics'
                        '{{https://docs.microsoft.com/bs-latn-ba/azure/'
                        'cognitive-services/computer-vision/quickstarts/'
                        'python-print-text}}',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--box-imgfile',
                          display_name='Out Img File', input_method='filewrite',
                          help='If set with file path to write then save result')

        # # ##################################### for app dependent parameters
        mcxt.add_argument('apimkey', display_name='key',
                          input_method='password',
                          help='customized key')
        mcxt.add_argument('endpoint', display_name='endpoint',
                          help='msazure endpoint')
        mcxt.add_argument('imgfile', display_name='image file',
                          input_method='fileread',
                          help='test image')
        argspec = mcxt.parse_args(args)
        return msazuretexts_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
