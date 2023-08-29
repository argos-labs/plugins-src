"""
====================================
 :mod:`argoslabs.google.vision`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for google vision API
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/07]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2020/11/05]
#     - Debug: module 'google.cloud.vision' has no attribute 'types'
#     TODO: argument op: invalid choice: 'invalid-op' (choose from 'OCR', 'Face', 'Label', 'Landmark', 'Logo', 'Localized Object', 'Dominant Colors')
#  * [2020/03/07]
#     - Chagne group "google" => "Google"
#  * [2019/10/31]
#     - add ocr output type option (--ocr-output)
#  * [2019/10/16]
#     - add opencv result
#  * [2019/09/24]
#     - 'Text' or 'Full Text' => 'OCR' internally with 'Full Text'
#  * [2019/09/13]
#     - starting

################################################################################
import os
import io
import cv2
import sys
import csv
import warnings
from google.auth.transport import requests
import google.auth.transport.requests
from google.auth.transport import grpc
import google.auth.transport.grpc
from google.cloud import vision
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
# noinspection PyUnresolvedReferences,PyUnboundLocalVariable
class GoogleVisionAPI(object):
    # ==========================================================================
    OP_TYPE = [
        'OCR',   # 'Text' or 'Full Text' => 'OCR'
        'Face',
        'Label',
        'Landmark',
        'Logo',
        'Localized Object',
        'Dominant Colors',
        # 'Crop Hints',
    ]

    # ==========================================================================
    def __init__(self, argspec, face_max_results=10):
        self.argspec = argspec
        json_credential = argspec.credential
        img_file = argspec.image
        if not os.path.exists(json_credential):
            raise IOError('Cannot read json credential file "%s"' % json_credential)
        self.json_credential = json_credential
        if not os.path.exists(img_file):
            raise IOError('Cannot read image file "%s"' % img_file)
        self.img_file = img_file
        self.face_max_results = face_max_results
        # for internal
        self.client = None
        self.image = None
        self._open()

    # ==========================================================================
    def _open(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.json_credential
        self.client = vision.ImageAnnotatorClient()
        with io.open(os.path.abspath(self.img_file), 'rb') as ifp:
            content = ifp.read()
        # noinspection PyUnresolvedReferences
        # self.image = vision.types.Image(content=content)
        self.image = vision.Image(content=content)

    # ==========================================================================
    def close(self):
        if self.client is not None:
            # self.client._http.http.close()
            ...

    # ==========================================================================
    @staticmethod
    def _get_vertics(_vts, bigger=0):
        vts = list()
        for i, v in enumerate(_vts):
            x, y = v.x, v.y
            if i == 0:
                x -= bigger
                y -= bigger
            elif i == 2:
                x += bigger
                y += bigger
            vts.append((x, y))
        return vts

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _save_ocr_result(self, rp, save_img_path):
        if save_img_path:
            img = cv2.imread(self.img_file)
            overlay = img.copy()
        rs = rp.full_text_annotation
        pages_l = list()
        paragraphs_l = list()
        words_l = list()
        for p in rs.pages:
            for b in p.blocks:
                # sys.stdout.write(b)
                if save_img_path:
                    vts = self._get_vertics(b.bounding_box.vertices, bigger=4)
                    cv2.rectangle(overlay, vts[0], vts[2], (0, 0, 255), 2)
                p_s = ''
                for pg in b.paragraphs:
                    if save_img_path:
                        vts = self._get_vertics(pg.bounding_box.vertices, bigger=2)
                        cv2.rectangle(overlay, vts[0], vts[2], (0, 255, 0), 2)
                    pg_s = ''
                    for wd in pg.words:
                        if save_img_path:
                            vts = self._get_vertics(wd.bounding_box.vertices)
                            cv2.rectangle(overlay, vts[0], vts[2], (255, 0, 0), 2)
                        wd_s = ''
                        for sb in wd.symbols:
                            t = sb.text
                            wd_s += t
                        if pg_s:
                            pg_s += ' '
                        pg_s += wd_s
                        words_l.append(wd_s)
                    if p_s:
                        p_s += '\t'
                    p_s += pg_s
                    paragraphs_l.append(pg_s)
                pages_l.append(p_s)
        if save_img_path:
            alpha = 0.3
            image_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
            cv2.imwrite(save_img_path, image_new)
        return pages_l, paragraphs_l, words_l

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _save_face_result(self, rp, save_img_path):
        if save_img_path:
            img = cv2.imread(self.img_file)
            overlay = img.copy()
        rs = rp.face_annotations
        cnt = 0
        for f in rs:
            box = [(vertex.x, vertex.y) for vertex in f.bounding_poly.vertices]
            if save_img_path:
                cv2.rectangle(overlay, box[0], box[2], (0, 255, 255), 2)
            cnt += 1
        if save_img_path:
            alpha = 0.5
            image_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
            cv2.imwrite(save_img_path, image_new)
        return cnt

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _save_label_result(self, rp, save_img_path):
        lines = list()
        rs = rp.label_annotations
        for lo in rs:
            lines.append([lo.description, float('%.2f' % lo.score)])
        return lines

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _save_landmark_result(self, rp, save_img_path):
        if save_img_path:
            img = cv2.imread(self.img_file)
            overlay = img.copy()
        lines = list()
        rs = rp.landmark_annotations
        for lm in rs:
            row = [lm.description, float('%.2f' % lm.score)]
            box = [(vertex.x, vertex.y) for vertex in lm.bounding_poly.vertices]
            if save_img_path:
                cv2.rectangle(overlay, box[0], box[2], (255, 0, 255), 2)
                cv2.putText(overlay, lm.description, (box[0][0]+10, box[0][1]+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            for loc in lm.locations:
                row.extend([loc.lat_lng.latitude, loc.lat_lng.longitude])
            lines.append(row)
        if save_img_path:
            alpha = 0.7
            image_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
            cv2.imwrite(save_img_path, image_new)
        return lines

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _save_logo_result(self, rp, save_img_path):
        if save_img_path:
            img = cv2.imread(self.img_file)
            overlay = img.copy()
        lines = list()
        rs = rp.logo_annotations
        for logo in rs:
            row = [logo.description, float('%.2f' % logo.score)]
            box = [(vertex.x, vertex.y) for vertex in logo.bounding_poly.vertices]
            if save_img_path:
                cv2.rectangle(overlay, box[0], box[2], (255, 255, 0), 2)
                cv2.putText(overlay, logo.description,
                            (box[0][0] + 10, box[0][1] + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            for loc in logo.locations:
                row.extend([loc.lat_lng.latitude, loc.lat_lng.longitude])
            lines.append(row)
        if save_img_path:
            alpha = 0.7
            image_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
            cv2.imwrite(save_img_path, image_new)
        return lines

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    @staticmethod
    def _get_normalized_vertices(w, h, vts):
        box = list()
        for x, y in vts:
            box.append((int(w * x), int(h * y)))
        return box

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _save_localization_result(self, rp, save_img_path):
        img = cv2.imread(self.img_file)
        height, width, _ = img.shape
        if save_img_path:
            overlay = img.copy()
        lines = list()
        rs = rp.localized_object_annotations
        for lo in rs:
            row = [lo.name, float('%.2f' % lo.score)]
            box = [(vertex.x, vertex.y) for vertex in lo.bounding_poly.normalized_vertices]
            box = self._get_normalized_vertices(width, height, box)
            if save_img_path:
                cv2.rectangle(overlay, box[0], box[2], (0, 255, 0), 2)
                cv2.putText(overlay, lo.name,
                            (box[0][0] + 10, box[0][1] + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            lines.append(row)
        if save_img_path:
            alpha = 0.7
            image_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
            cv2.imwrite(save_img_path, image_new)
        return lines

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _save_property_result(self, rp, save_img_path):
        lines = list()
        rs = rp.image_properties_annotation
        for color in rs.dominant_colors.colors:
            lines.append([
                color.pixel_fraction,
                int(color.color.red) if color.color.red else 0,
                int(color.color.green) if color.color.green else 0,
                int(color.color.blue) if color.color.blue else 0,
                int(color.color.alpha.value) if color.color.alpha.value else 0
            ])
        return lines

    # ==========================================================================
    def do(self, op):
        if op == 'OCR':  # 'Full Text':
            rp = self.client.document_text_detection(image=self.image)
            pages_l, paragraphs_l, words_l = \
                self._save_ocr_result(rp, self.argspec.output_image)
            if self.argspec.ocr_output == 'total':
                rs = rp.full_text_annotation
                sys.stdout.write(rs.text.strip())
            elif self.argspec.ocr_output == 'page':
                sys.stdout.write('\n'.join(pages_l))
            elif self.argspec.ocr_output == 'paragraph':
                sys.stdout.write('\n'.join(paragraphs_l))
            elif self.argspec.ocr_output == 'word':
                sys.stdout.write('\n'.join(words_l))
            else:
                raise ValueError('Invalid OCR Output type "%s"'
                                 % self.argspec.ocr_output)
        elif op == 'Face':
            rp = self.client.face_detection(image=self.image)
            r = self._save_face_result(rp, self.argspec.output_image)
            sys.stdout.write(str(r))
        elif op == 'Label':
            rp = self.client.label_detection(image=self.image)
            r = self._save_label_result(rp, self.argspec.output_image)
            c = csv.writer(sys.stdout, lineterminator='\n')
            c.writerow(['description', 'score'])
            if r:
                for line in r:
                    c.writerow(line)
        elif op == 'Landmark':
            rp = self.client.landmark_detection(image=self.image)
            r = self._save_landmark_result(rp, self.argspec.output_image)
            c = csv.writer(sys.stdout, lineterminator='\n')
            c.writerow(['description', 'score', 'latitude', 'longitude'])
            if r:
                for line in r:
                    c.writerow(line)
        elif op == 'Logo':
            rp = self.client.logo_detection(image=self.image)
            r = self._save_logo_result(rp, self.argspec.output_image)
            c = csv.writer(sys.stdout, lineterminator='\n')
            c.writerow(['description', 'score'])
            if r:
                for line in r:
                    c.writerow(line)
        elif op == 'Localized Object':
            rp = self.client.object_localization(image=self.image)
            r = self._save_localization_result(rp, self.argspec.output_image)
            c = csv.writer(sys.stdout, lineterminator='\n')
            c.writerow(['name', 'score'])
            if r:
                for line in r:
                    c.writerow(line)
        elif op == 'Dominant Colors':
            rp = self.client.image_properties(image=self.image)
            r = self._save_property_result(rp, self.argspec.output_image)
            c = csv.writer(sys.stdout, lineterminator='\n')
            c.writerow(['pixel_fraction', 'red', 'green', 'blue', 'alpha'])
            if r:
                for line in r:
                    c.writerow(line)
        else:
            raise RuntimeError('Invalid vision operation "%s"' % op)
        sys.stdout.flush()


################################################################################
@func_log
def do_vision_api(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    warnings.simplefilter("ignore")
    try:
        gv = GoogleVisionAPI(argspec)  # .credential, argspec.image)
        gv.do(argspec.op)
        gv.close()
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
        display_name='Google Vision API',
        icon_path=get_icon_path(__file__),
        description='Google Vision API. {{https://cloud.google.com/vision/docs/}}',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--output-image',
                          display_name='Out Img File', input_method='filewrite',
                          help='If set with file path to write then save result ')
        mcxt.add_argument('--ocr-output',
                          display_name='OCR Output',
                          choices=['total', 'page', 'paragraph', 'word'],
                          default='total',
                          help='Get the result type of OCR, default is [[total]]')
        # ##################################### for app dependent parameters
        mcxt.add_argument('credential',
                          display_name='Credential File', input_method='fileread',
                          help='Google API credential JSON file')
        mcxt.add_argument('op',
                          display_name='Vision API type',
                          choices=GoogleVisionAPI.OP_TYPE,
                          help='Google Visual type of operation')
        mcxt.add_argument('image',
                          display_name='Image File', input_method='fileread',
                          help='Google API image file')
        argspec = mcxt.parse_args(args)
        return do_vision_api(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
