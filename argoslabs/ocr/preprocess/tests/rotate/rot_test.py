import os
import sys 
import math
from typing import Tuple, Union
import cv2
import numpy as np
from fpdf import FPDF
from PIL import Image
from deskew import determine_skew
from pdf2image import convert_from_path

outputDir = "imag/"
def rotate(
        image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
) -> np.ndarray:
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)

def convert(file, outputDir):
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    print(file)
    pages = convert_from_path(file, poppler_path=r"C:\Users\Pavan\Downloads\New folder (12)\poppler-0.68.0\bin")
    counter = 1 
    for page in pages:
        myfile = outputDir +'output' + str(counter) +'.jpg'
        counter = counter + 1
        page.save(myfile, "JPEG")
        image = cv2.imread(myfile)
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        angle = determine_skew(grayscale)
        rotated = rotate(image, angle, (0, 0, 0)) 
        cv2.imwrite('test_output_image.jpg', rotated)
        img = Image.open(r"test_output_image.jpg")  
        imgg = img.convert("RGB")
        imgg.save(r"test_output.pdf") 

args = sys.argv
if len(args) > 1:
    file = args[1]
    convert(file, outputDir)