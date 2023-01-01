"""
====================================
:mod:`argoslabs.ocr.preprocess`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : PreProcessing for OCR
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/06/07]
#     - Op 추가
#  * [2022/05/31]
#     - starting

################################################################################
import os
import sys
import cv2
import math
import glob
import numpy as np
# import matplotlib.pyplot as plt
from skimage.filters import threshold_local
from PIL import Image
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from typing import Tuple, Union
from deskew import determine_skew


################################################################################
OPS = [
    'Extract Largest Rect',
    'Auto Rotate',
]

# TODO: need threshold methods except 'gaussian'
THRESHOLD_METHODS = [
]

################################################################################
def get_fname(s_file, suffix=None):
    if not suffix:
        return s_file
    fn, ext = os.path.splitext(s_file)
    return fn + f'.{suffix}' + ext


################################################################################
def clean_img_files(fname):
    fn, ext = os.path.splitext(fname)
    for f in glob.glob(f'{fn}.*{ext}'):
        os.remove(f)

################################################################################
def opencv_resize(image, ratio):
    width = int(image.shape[1] * ratio)
    height = int(image.shape[0] * ratio)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

################################################################################
# approximate the contour by a more primitive polygon shape
def approximate_contour(contour):
    peri = cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, 0.032 * peri, True)


################################################################################
def get_receipt_contour(contours):    
    # loop over the contours
    m_w = m_h = 0
    max_rec = None
    # get largest object
    for c in contours:
        approx = approximate_contour(c)
        # if our approximated contour has four points, we can assume it is receipt's rectangle
        if len(approx) >= 4:
            min_x = min_y = 1000000
            max_x = max_y = 0
            for i in range(len(approx)):
                if min_x > approx[i][0][0]:
                    min_x = approx[i][0][0]
                if max_x < approx[i][0][0]:
                    max_x = approx[i][0][0]
                if min_y > approx[i][0][1]:
                    min_y = approx[i][0][1]
                if max_y < approx[i][0][1]:
                    max_y = approx[i][0][1]
            c_w = max_x - min_x
            c_h = max_y - min_y
            if c_w > m_w or c_h > m_h:
                m_w = c_w
                m_h = c_h
                max_rec = approx
    if max_rec is None:
        raise RuntimeError(f'Cannot get receite rectangle')
    return max_rec


################################################################################
def get_distance(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return int(dist)


################################################################################
def contour_to_rect(contour, resize_ratio, near_pixels=20):
    if len(contour) == 4:
        pts = np.zeros((4, 2), dtype = "int32")
        # pts = contour.reshape(4, 2)
        for i in range(4):
            pts[i][0] = contour[i][0][0]
            pts[i][1] = contour[i][0][1]
    else:
        pts = np.zeros((4, 2), dtype = "int32")
        for i in range(len(contour)):
            cx, cy = contour[i][0][0], contour[i][0][1]
            # 기존 점에서 가장 가까운 점이 있는지 확인
            nearest_ndx = last_ndx = -1
            for j in range(4):
                px, py = pts[j]
                if px == 0 and py == 0:
                    break
                last_ndx = j
                dt = get_distance(cx, cy, px, py)
                if dt * resize_ratio <= near_pixels:
                    nearest_ndx = j
                    break
            # 가장 가까운 점이 발견되면 산술평균을 내어 다시 저장
            if nearest_ndx >= 0:
                pts[nearest_ndx][0] = (pts[nearest_ndx][0] + cx) // 2
                pts[nearest_ndx][1] = (pts[nearest_ndx][1] + cy) // 2
            else:
                if last_ndx >= 3:
                    # 더 이상 넣을 pts 가 없음
                    break 
                last_ndx += 1
                pts[last_ndx][0] = cx
                pts[last_ndx][1] = cy
    rect = np.zeros((4, 2), dtype = "float32")
    # top-left point has the smallest sum
    # bottom-right has the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # compute the difference between the points:
    # the top-right will have the minumum difference 
    # the bottom-left will have the maximum difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect / resize_ratio

################################################################################
def wrap_perspective(img, rect):
    # unpack rectangle points: top left, top right, bottom right, bottom left
    (tl, tr, br, bl) = rect
    # compute the width of the new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    # compute the height of the new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    # take the maximum of the width and height values to reach
    # our final dimensions
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))
    # destination points which will be used to map the screen to a "scanned" view
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    # calculate the perspective transform matrix
    M = cv2.getPerspectiveTransform(rect, dst)
    # warp the perspective to grab the screen
    return cv2.warpPerspective(img, M, (maxWidth, maxHeight))


################################################################################
def bw_scanner(argspec, image):
    if not argspec.gray_res:
        return image
    block_size=argspec.threshold_bs
    offset=argspec.threshold_os
    method='gaussian'
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if not argspec.threshold_res:
        return gray
    T = threshold_local(gray, block_size=block_size, offset=offset, method=method)
    return (gray > T).astype("uint8") * 255


################################################################################
def do_extrect(argspec):
    s_file = argspec.image
    result_file = argspec.target_image
    save_temp = argspec.save_temp

    clean_img_files(s_file)
    image = cv2.imread(s_file)
    # Downscale image as finding receipt contour is more efficient on a small image
    resize_ratio = 500 / image.shape[0]
    original = image.copy()
    image = opencv_resize(image, resize_ratio)

    # Convert to grayscale for further processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if save_temp:
        cv2.imwrite(get_fname(s_file, '01-gray'), gray)

    # Get rid of noise with Gaussian Blur filter
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    if save_temp:
        cv2.imwrite(get_fname(s_file, '02-blurred'), blurred)

    # Detect white regions
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilated = cv2.dilate(blurred, rectKernel)
    if save_temp:
        cv2.imwrite(get_fname(s_file, '03-white'), dilated)

    edged = cv2.Canny(dilated, 100, 200, apertureSize=3)
    if save_temp:
        cv2.imwrite(get_fname(s_file, '04-edged'), edged)

    # Detect all contours in Canny-edged image
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    image_with_contours = cv2.drawContours(image.copy(), contours, -1, (0,255,0), 3)
    if save_temp:
        cv2.imwrite(get_fname(s_file, '05-contours'), image_with_contours)

    # Get 10 largest contours
    largest_contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    image_with_largest_contours = cv2.drawContours(image.copy(), largest_contours, -1, (0,255,0), 3)
    if save_temp:
        cv2.imwrite(get_fname(s_file, '06-10large-countours'), image_with_largest_contours)

    # get_receipt_contour(largest_contours)
    receipt_contour = get_receipt_contour(largest_contours)
    image_with_receipt_contour = cv2.drawContours(image.copy(), [receipt_contour], -1, (0, 255, 0), 2)
    if save_temp:
        cv2.imwrite(get_fname(s_file, '07-receit-contour'), image_with_receipt_contour)

    scanned = wrap_perspective(original.copy(), contour_to_rect(receipt_contour, resize_ratio))
    # plt.figure(figsize=(16,10))
    # plt.imshow(scanned)

    result = bw_scanner(argspec, scanned)
    t_file = result_file if result_file else get_fname(s_file, 'result')
    cv2.imwrite(t_file, result)
    print(os.path.abspath(t_file), end='')


################################################################################
def rotate(
        image: np.ndarray, 
        angle: float, 
        background: Union[int, Tuple[int, int, int]]) -> np.ndarray:
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)


################################################################################
def do_auto_rotate(argspec):
    s_file = argspec.image
    result_file = argspec.target_image
    save_temp = argspec.save_temp

    clean_img_files(s_file)
    image = cv2.imread(s_file)
    
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    angle = determine_skew(grayscale)
    rotate_fill_color = eval(argspec.rotate_fill_color)
    rotated = rotate(image, angle, rotate_fill_color) 
    #cv2.imwrite('test_output_image.jpg', rotated)

    result = bw_scanner(argspec, rotated)
    t_file = result_file if result_file else get_fname(s_file, 'result')
    cv2.imwrite(t_file, result)
    print(os.path.abspath(t_file), end='')
    
    
################################################################################
@func_log
def do_pp(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if not os.path.exists(argspec.image):
            raise IOError(f'Cannot read image file "{argspec.image}"')
        if argspec.op == OPS[0]:    # 'Extract Largest Rect'
            do_extrect(argspec)
        elif argspec.op == OPS[1]:  # 'Auto Rotate'
            do_auto_rotate(argspec)
        else:
            raise ReferenceError(f'Invalid Operation "{argspec.op}"')
        return 0
    except IOError as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    except ReferenceError as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 2
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    try:
        with ModuleContext(
            owner='ARGOS-LABS',
            group='2',  # Business Apps
            version='4',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='OCR PreProcess',
            icon_path=get_icon_path(__file__),
            description='OCR Pre Processor',
        ) as mcxt:
            ##################################### for app dependent parameters
            mcxt.add_argument('op',
                                display_name='Operation', choices=OPS,
                                default=OPS[0],
                                help='PreProcessing operations')
            mcxt.add_argument('image',
                                display_name='Image file', 
                                input_method='fileread',
                                help='Image file to process')
            # ######################################## for app dependent options
            mcxt.add_argument('--save-temp',
                                display_name='Save Temp Images',
                                action='store_true',
                                help='If this flag is set save temporary images')
            mcxt.add_argument('--target-image',
                                display_name='Target Image File',
                                input_method='filewrite',
                                help='If this flag is set then save temporary images')
            mcxt.add_argument('--gray-res',
                                input_group='Result Process',
                                display_name='Gray Result',
                                action='store_true',
                                help='If this flag is set black/white result')
            mcxt.add_argument('--threshold-res',
                                input_group='Result Process',
                                display_name='B/W Threshold',
                                action='store_true',
                                help='If this flag is set black/white threshold')
            mcxt.add_argument('--threshold-bs',
                                input_group='Result Process',
                                display_name='B/W Blocksize',
                                type=int,
                                default=21,
                                help='Black/White threshold block size, default is [[21]]')
            mcxt.add_argument('--threshold-os',
                                input_group='Result Process',
                                display_name='B/W Offset',
                                type=int,
                                default=5,
                                help='Black/White threshold offset, default is [[5]]')
            mcxt.add_argument('--rotate-fill-color',
                                display_name='Rot Fill Color',
                                default='(255,255,255)',
                                help='When auto rotated set fill color with format "(R,G,B)",' 
                                'default is white, "(255,255,255)"')
            argspec = mcxt.parse_args(args)
            return do_pp(mcxt, argspec)
    except Exception as err:
        sys.stderr.write(f'Error: {err}')
        return 98

################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
