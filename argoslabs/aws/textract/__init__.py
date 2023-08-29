"""
====================================
 :mod:`argoslabs.aws.textract`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS AWS Text Recognition plugin module
"""
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2021/03/26]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2020/04/02]
#     - add icon
#  * [2020/04/02]
#     - starting

################################################################################
import os
import sys
# noinspection PyPackageRequirements
import boto3
import warnings
from io import StringIO
# noinspection PyPackageRequirements
from PIL import Image, ImageDraw
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class AWSTextAPI(object):
    # ==========================================================================
    OP_TYPE = [
        'OCR',
        'Rekognition Text'
    ]

    # ==========================================================================
    def __init__(self, argspec, alpha=0.7):
        self.argspec = argspec
        self.key_id = argspec.key_id
        self.key = argspec.key
        imgfile = argspec.imgfile
        if not os.path.exists(imgfile):
            raise IOError('Cannot read image file "%s"' % imgfile)
        self.imgfile = imgfile
        self.alpha = alpha
        self.box_imgfile = argspec.box_imgfile
        self.rd = None
        self.image = Image.open(imgfile)
        self.width, self.height = self.image.size
        self.draw = ImageDraw.Draw(self.image)

    # ==========================================================================
    def get_image_api_result(self):
        client = boto3.client('rekognition', aws_access_key_id=self.key_id,
                              aws_secret_access_key=self.key,
                              region_name='us-west-2')
        with open(self.imgfile, 'rb') as image:
            self.rd = client.detect_text(Image={'Bytes': image.read()})
        if self.rd['ResponseMetadata']['HTTPStatusCode'] // 10 != 20:
            raise RuntimeError('Error of API')
        return self.rd

    # ==========================================================================
    def get_text_api_result(self):
        client = boto3.client('textract', aws_access_key_id=self.key_id,
                              aws_secret_access_key=self.key,
                              region_name='us-west-2')
        with open(self.imgfile, 'rb') as image:
            self.rd = client.analyze_document(Document={'Bytes': image.read()},
                                              FeatureTypes=["FORMS", "TABLES"])
        if self.rd['ResponseMetadata']['HTTPStatusCode'] // 10 != 20:
            raise RuntimeError('Error of API')
        return self.rd

    # ==========================================================================
    def image_text_box(self):
        if not self.rd:
            raise RuntimeError('Call get_api_result() first')
        blocks = self.rd['TextDetections']
        for block in blocks:
            if block['Type'] == 'WORD':
                box = block['Geometry']['BoundingBox']
                left = self.width * box['Left']
                top = self.height * box['Top']
                self.draw.rectangle(
                    [left, top, left + (self.width * box['Width']),
                     top + (self.height * box['Height'])], outline='red')
        self.image.save(self.box_imgfile)

    # ==========================================================================
    def text_box(self):
        if not self.rd:
            raise RuntimeError('Call get_api_result() first')
        blocks = self.rd['Blocks']
        for block in blocks:
            if block['BlockType'] == 'WORD':
                box = block['Geometry']['BoundingBox']
                left = self.width * box['Left']
                top = self.height * box['Top']
                self.draw.rectangle(
                    [left, top, left + (self.width * box['Width']),
                     top + (self.height * box['Height'])], outline='red')
        self.image.save(self.box_imgfile)

    # ==========================================================================
    def extract_image_data(self):
        with StringIO() as outst:
            self.get_image_api_result()
            line_infos = self.rd['TextDetections']
            c = 0
            for i in line_infos:
                if i['Type'] == 'LINE':
                    c += 1
            for i in range(0, c):
                outst.write(line_infos[i]['DetectedText'])
                outst.write('\n')
            if self.box_imgfile:
                self.image_text_box()
            print(outst.getvalue(), end='')

    # ==========================================================================
    def extract_text_data(self):
        with StringIO() as outst:
            self.get_text_api_result()
            blocks = self.rd['Blocks']
            for i in range(0, len(blocks) - 1):
                if blocks[i]['BlockType'] == 'WORD':
                    left1 = self.width * blocks[i]['Geometry']['BoundingBox'][
                        'Left']
                    left2 = self.width * \
                        blocks[i + 1]['Geometry']['BoundingBox']['Left']
                    outst.write(blocks[i]['Text'])
                    outst.write(' ')
                    if left1 > left2:
                        outst.write('\n')
            if self.box_imgfile:
                self.text_box()
            print(outst.getvalue(), end='')

    # ==========================================================================
    def do(self, op):
        if op == 'Rekognition Text':
            self.extract_image_data()
        elif op == 'OCR':
            self.extract_text_data()
        else:
            raise RuntimeError('Invalid vision operation "%s"' % op)


################################################################################
@func_log
def awstext_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    warnings.filterwarnings("ignore", category=ResourceWarning,
                            message="unclosed.*<ssl.SSLSocket.*>")
    try:
        res = AWSTextAPI(argspec)
        res.do(argspec.op)
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
            group='1',   #  AI Solutions
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='AWS Textra/Rekog',
            icon_path=get_icon_path(__file__),
            description='AWS Textract and Rekognition'
                        '{{https://aws.amazon.com/textract/features/}}',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--box-imgfile',
                          display_name='Out Img File', input_method='filewrite',
                          help='If set with file path to write then save result')

        # # ##################################### for app dependent parameters
        mcxt.add_argument('key_id', display_name='Access key ID',
                          help='customized key id', input_method='password')
        mcxt.add_argument('key', display_name='Secret access key',
                          help='customized key', input_method='password')
        mcxt.add_argument('imgfile', display_name='Image file',
                          input_method='fileread',
                          help='test image')
        mcxt.add_argument('op',
                          display_name='AWS Text Type',
                          choices=AWSTextAPI.OP_TYPE,
                          help='AWS detective type of operation')
        argspec = mcxt.parse_args(args)
        return awstext_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
