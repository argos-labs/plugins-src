#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.line_id_card_ocr`
====================================
.. moduleauthor:: Taiki Shimasaki <shimasaki@argos-service.com>
.. note:: ARGOS-LABS License

Description
===========
Input Plugin Description
"""
# Authors
# ===========
#
# * Taiki Shimasaki
#
# Change Log
# --------
#
#  * [2021/08/11]
#     Create

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import mimetypes
from PIL import Image
import random
import string
import base64
import requests
import json

################################################################################
class POST_ID(object):

    # ==========================================================================
    ENDPOINT = 'https://apigw.linebrain.ai/a2xemtle5d/ID-Card-OCR-Plugin/ocr/v2/forms/AUTO_DETECT/recognize'

    # ==========================================================================
    def __init__(self, key, language):
        self.post_url = self.ENDPOINT
        self.api_key = key
        self.headers = {"Content-Type": "application/json",
                        "x-linebrain-apigw-api-key": self.api_key}
        self.files = {"imageContent": None}
        self.data = {"language": language,
                     # "attributes": ["estimatedLanguage, boundingBoxes"]
                     }

        self.img = None
        self.mime = None
        self.type = None
        self.tif_data = None

        self.img_data = None
        self.file_name = ''.join(
            random.choices(string.ascii_letters + string.digits, k=20))
        self.post_img_path = None
        self.post_img = None

        self.resp = None
        self.err_code = None
        self.err_msg = None

        self.out_key = None
        self.resp_text = None

    # ==========================================================================
    def img_path_check(self, img):
        if os.path.exists(img):
            self.img = os.path.abspath(img)
        else:
            raise IOError('{} is not exists!'.format(img))

    # ==========================================================================
    def file_type_check(self):
        self.mime = mimetypes.guess_type(self.img)[0]
        if self.mime == 'image/jpeg':
            self.type = 'jpg'
            return 'jpg'
        elif self.mime == 'image/jpx':
            self.type = 'jpx'
            return 'jpx'
        elif self.mime == 'image/png':
            self.type = 'png'
            return 'png'
        elif self.mime == 'image/gif':
            self.type = 'gif'
            return 'gif'
        elif self.mime == 'image/tiff':
            self.type = 'tif'
            self.tif_data = Image.open(self.img)
            if self.tif_data.n_frames != 1:
                raise IOError('Multi-page TIFFs cannot be handled!')
            else:
                return 'tif'
        elif self.mime == 'image/bmp':
            self.type = 'bmp'
            return 'bmp'
        elif self.mime == 'application/pdf':
            self.type = 'pdf'
            raise IOError('Sorry, PDF is not available')

        else:
            raise IOError('Cannot handle this filetype!')

    # ==========================================================================
    def convert_img(self):
        if self.type in ('jpg', 'jpx', 'gif', 'bmp', 'tif'):
            self.img_data = Image.open(self.img)
            while os.path.exists('./{}.png'.format(self.img)) == True:
                self.file_name = ''.join(random.choices(string.ascii_letters
                                                        + string.digits, k=20))

            else:
                self.img_data.save('./{}.png'.format(self.file_name), 'png')
            self.img_data.close()

            self.post_img_path = './{}.png'.format(self.file_name)

        elif self.type == 'png':
            self.post_img_path = self.img

        else:
            raise IOError('Unexpected Error Occurred')

        """
        with open(self.post_img_path, 'rb') as img_file:
            self.post_img = base64.b64encode(img_file.read())
            self.post_img = self.post_img.decode('utf-8')
        """

    # ==========================================================================
    def post_data(self):
        with open(self.post_img_path, 'rb') as img:
            self.post_img = base64.b64encode(img.read())

        self.post_img = self.post_img.decode('utf-8')

        self.files = {"imageContent": self.post_img}
        self.files.update(self.data)
        # print(self.files)
        # print(self.data)

        self.resp = requests.post(self.post_url,
                                  headers=self.headers,
                                  data=json.dumps(self.files))

    """
    # ==========================================================================
    def post_data_sub(self):
        with open(self.post_img_path, 'rb') as img:
            self.post_img = img.read()

        self.headers = {"Content-Type": "multipart/form-data",
                        "x-linebrain-apigw-api-key": self.api_key}
        self.data = [{"language": (None, 'ja')}]
        self.files = [{"image": ('img.png', self.post_img)}]
        # self.files.update(self.data)
        # print(self.files)
        # print(self.data)

        self.resp = requests.post(self.post_url,
                                  headers=self.headers,
                                  files=self.files,
                                  data=self.data)

        print(self.resp)
        print(self.resp.text)
    """

    # ==========================================================================
    def return_data(self):
        if self.resp.status_code == 200:
            resp = self.resp.json()
            if resp["status"] == "FAILED":
                print("It was not readable.", end="")
            else:
                print(self.resp.text)

        else:
            self.resp = self.resp.json()
            self.err_code = self.resp["errorCode"]
            self.err_msg = self.resp["errorMessage"]
            raise IOError('Error: {} - Code: {}'.format(self.err_msg, self.err_code))

    # ==========================================================================
    def select_data(self, out_key):
        self.out_key = out_key
        self.resp = self.resp.json()
        form = self.resp["formID"]

        if form == "JP_DRIVER_LICENSE_FRONT":
            if self.out_key == 'Type':
                print("Driver License (JP) Front", end="")

            elif self.out_key == 'Name':
                self.resp_text = self.resp["fields"]["name"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == "Last Name":
                raise IOError("Select \"Name\" as that option is not available!")

            elif self.out_key == "First Name":
                raise IOError("Select \"Name\" as that option is not available!")

            elif self.out_key == 'Birthday':
                self.resp_text = self.resp["fields"]["birthday_dateType"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'Address':
                self.resp_text = self.resp["fields"]["address"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'Expiry Date':
                self.resp_text = self.resp["fields"]["expiryDate_dateType"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'Issue Date':
                self.resp_text = self.resp["fields"]["issueDate_dateType"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'ID Number':
                self.resp_text = self.resp["fields"]["IDNumber"]["value"]
                print(self.resp_text, end="")

            else:
                raise IOError('Unexpected Error Occurred.')

        elif form == "JP_DRIVER_LICENSE_BACK":
            if self.out_key == "Type":
                print("Driver License (JP) Back", end="")

            elif self.out_key in ["Name", "Last Name", "First Name",
                                  "Birthday", "Address", "Expiry Date",
                                  "Issue Date", "ID Number"]:
                raise IOError("Only \"Type\" option is available!")

            else:
                raise IOError('Unexpected Error Occurred.')

        elif form == "JP_PASSPORT_FRONT":
            if self.out_key == "Type":
                print("Passport (JP)", end="")

            elif self.out_key == 'Name':
                raise IOError("Select \"Name\" as that option is not available!")

            elif self.out_key == "Last Name":
                self.resp_text = self.resp["fields"]["lastName"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == "First Name":
                self.resp_text = self.resp["fields"]["firstName"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'Birthday':
                self.resp_text = self.resp["fields"]["birthday_dateType"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'Address':
                self.resp_text = self.resp["fields"]["registeredDomicile"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'Expiry Date':
                self.resp_text = self.resp["fields"]["expiryDate_dateType"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'Issue Date':
                self.resp_text = self.resp["fields"]["issueDate_dateType"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'ID Number':
                self.resp_text = self.resp["fields"]["passportType"]["value"]
                print(self.resp_text, end="")

            else:
                raise IOError('Unexpected Error Occurred.')

        elif form == "JP_RESIDENCE_CARD_FRONT":
            if self.out_key == "Type":
                print("Residence Card (JP) Front", end="")

            elif self.out_key == 'Name':
                self.resp_text = self.resp["fields"]["name"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == "Last Name":
                raise IOError("Select \"Name\" as that option is not available!")

            elif self.out_key == "First Name":
                raise IOError("Select \"Name\" as that option is not available!")

            elif self.out_key == 'Birthday':
                self.resp_text = self.resp["fields"]["birthday_dateType"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'Address':
                self.resp_text = self.resp["fields"]["address"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'Expiry Date':
                self.resp_text = self.resp["fields"]["expiryDate_dateType"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'Issue Date':
                self.resp_text = self.resp["fields"]["issueDate_dateType"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'ID Number':
                self.resp_text = self.resp["fields"]["passportType"]["value"]
                print(self.resp_text, end="")

            else:
                raise IOError('Unexpected Error Occurred.')

        elif form == "JP_RESIDENCE_CARD_BACK":
            if self.out_key == "Type":
                print("Residence Card (JP) Back", end="")

            elif self.out_key in ["Name", "Last Name", "First Name",
                                  "Birthday", "Address", "Expiry Date",
                                  "Issue Date", "ID Number"]:
                raise IOError("Only \"Type\" option is available!")

            else:
                raise IOError('Unexpected Error Occurred.')

        elif form == "JP_MY_NUMBER_CARD_FRONT":
            if self.out_key == "Type":
                print("My Number Card (JP) Front", end="")

            elif self.out_key == 'Name':
                self.resp_text = self.resp["fields"]["name"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == "Last Name":
                raise IOError("Select \"Name\" as that option is not available!")

            elif self.out_key == "First Name":
                raise IOError("Select \"Name\" as that option is not available!")

            elif self.out_key == 'Birthday':
                self.resp_text = self.resp["fields"]["birthday_dateType"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'Address':
                self.resp_text = self.resp["fields"]["address"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'Expiry Date':
                self.resp_text = self.resp["fields"]["expiryDate_dateType"]["value"]
                print(self.resp_text, end="")

            elif self.out_key == 'Issue Date':
                raise IOError("This option is not available!")

            elif self.out_key == 'ID Number':
                raise IOError("This option is only available on \"Back\"")

            else:
                raise IOError('Unexpected Error Occurred.')

        elif form == "JP_MY_NUMBER_CARD_FRONT":
            if self.out_key == "Type":
                print("Residence Card (JP) Back", end="")

            elif self.out_key in ["Name", "Last Name", "First Name",
                                  "Birthday", "Address", "Expiry Date",
                                  "Issue Date"]:
                raise IOError("Only \"Type\" & \"ID Number\" option is available!")

            elif self.out_key == 'ID Number':
                self.resp_text = self.resp["fields"]["passportType"]["value"]
                print(self.resp_text, end="")

            else:
                raise IOError('Unexpected Error Occurred.')

        else:
            pass

    # ==========================================================================
    def del_file(self):
        if self.type in ('jpg', 'jpx', 'gif', 'bmp', 'tif'):
            os.remove('./{}.png'.format(self.file_name))

        else:
            pass


################################################################################
@func_log
def read_id(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        P_ID = POST_ID(argspec.key, argspec.language)

        P_ID.img_path_check(argspec.img)

        FT = P_ID.file_type_check()
        P_ID.convert_img()

        try:
            P_ID.post_data()

            if argspec.out_key:
                P_ID.select_data(argspec.out_key)
            else:
                P_ID.return_data()

        finally:
            if FT in ('jpg', 'jpx', 'gif', 'bmp', 'tif'):
                P_ID.del_file()
        mcxt.logger.info('>>>end...')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-SERVICE-JAPAN',
        group='1',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='LINE ID Card OCR',
        icon_path=get_icon_path(__file__),
        description='Plugin that uses LINE CLOVA\'s API to perform OCR on ID-Cards',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('key',
                          display_name='API Key',
                          input_method='password',
                          help='Input your API Key')
        mcxt.add_argument('img',
                          display_name='Receipt Image',
                          input_method='fileread',
                          help='Select Receipt Image file')
        # ######################################## for app dependent options
        mcxt.add_argument('--language',
                          display_name='Language',
                          default='ja',
                          choices=['ja'],
                          help='Select the language of the receipt')
        mcxt.add_argument('--out_key',
                          display_name='Output Key',
                          choices=['Type',
                                   'Name',
                                   'Last Name',
                                   'First Name',
                                   'Birthday',
                                   'Address',
                                   'Expiry Date',
                                   'Issue Date',
                                   'ID Number',],
                          help='Select the key want to output')

        argspec = mcxt.parse_args(args)
        return read_id(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
