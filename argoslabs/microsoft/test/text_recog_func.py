
################################################################################
import os
import sys
import cv2
import requests
# import pprint


################################################################################
class MSAzureTextsAPI(object):
    # ==========================================================================
    ENDPOINT = r'https://westus.api.cognitive.microsoft.com/'
    OCR_URL = "vision/v2.1/ocr"

    # ==========================================================================
    def __init__(self, apimkey, imgfile,
                 out=sys.stdout, box_imgfile=None, alpha=0.7):
        self.apimkey = apimkey
        if not os.path.exists(imgfile):
            raise IOError(f'Cannot access image file "{imgfile}"')
        self.imgfile = imgfile
        self.out = out
        self.box_imgfile = box_imgfile
        self.alpha = alpha
        # for internal
        self.rd = None
        self.img = None

    # ==========================================================================
    def get_api_result(self):  # func1: Prining the json result
        image_data = open(self.imgfile, "rb").read()
        headers = {'Content-Type': 'application/octet-stream',
                   'Ocp-Apim-Subscription-Key': self.apimkey}
        text_recognition_url = self.ENDPOINT + self.OCR_URL
        rp = requests.post(text_recognition_url, headers=headers,
                           data=image_data,
                           params={'detectOrientation': 'true'})
        if rp.status_code // 10 != 20:
            raise RuntimeError(f'Error of API: '
                               f'{rp.json().get("error", {}).get("message", "")}')
        self.rd = rp.json()
        return self.rd

    # ==========================================================================
    # func2: Rotate the img file depending on the orientation
    def img_rotate(self):
        #json results only include up,down,left and right so image is rotated 90,
        #180,270
        self.img = img = cv2.imread(self.imgfile, cv2.COLOR_BGR2RGB)
        if self.rd['orientation'] == 'Left':
            self.img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif self.rd['orientation'] == 'Right':
            # noinspection PyUnresolvedReferences
            self.img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISEE)
        elif self.rd['orientation'] == 'Down':
            self.img = cv2.rotate(img, cv2.ROTATE_180)

    # ==========================================================================
    # func3: Draw boundingboxes on the original image
    def text_box(self):
        if not self.rd:
            raise RuntimeError('Call get_api_result() first')
        self.img_rotate() #call the previous function
        overlay = self.img.copy()
        line_infos = [region["lines"] for region in self.rd["regions"]]
        word_infos = []
        for line in line_infos:
            for word_metadata in line:
                for word_info in word_metadata["words"]:
                    word_infos.append(word_info)
        for i in range(0, len(word_infos)):
            #Extract boundingbox from the json result
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
        self.get_api_result()
        # pprint.pprint(self.rd)
        line_infos = [region["lines"] for region in self.rd["regions"]]
        for line in line_infos:
            for word_metadata in line:
                for i, word_info in enumerate(word_metadata["words"]):
                    if i > 0:
                        self.out.write(' ')
                    self.out.write(word_info['text'])
                self.out.write('\n')
            self.out.write('\n')
        if self.box_imgfile:
            self.text_box()


################################################################################
if __name__ == '__main__':
    _apimkey = r'..'
    # _apimkey = r'..'
    # target = r"C:/work/form_recognition/test_imgs/ko_test1.png"

    test_imgs = (
        'image002.jpg',
        'image003.jpg',
        'image004.jpg',
        'image005.jpg',
        'image006.jpg',
        'image007.jpg',
    )
    # _imgfile = r"image003.jpg"
    # _box_img_path = 'image003.out.png'

    for test_img in test_imgs:
        fn, ext = os.path.splitext(test_img)
        box_file = fn + '.out.png'
        txt_file = fn + '.txt'
        with open(txt_file, 'w', encoding='utf-8') as ofp:
            print(f'Processing {test_img}...')
            msa = MSAzureTextsAPI(_apimkey, test_img, out=ofp,
                                  box_imgfile=box_file)
            msa.extract_data()
