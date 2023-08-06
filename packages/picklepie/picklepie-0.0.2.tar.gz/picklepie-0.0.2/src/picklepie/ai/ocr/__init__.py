import pytesseract as __ts
import cv2 as __cv

from . import pdf

import picklepie as __pp

# download & install tesseract : https://github.com/UB-Mannheim/tesseract/wiki
# install as administrator if needed (or if error occured)

# for more trained data, please download from : https://tesseract-ocr.github.io/tessdoc/Data-Files
# then save to dir : C:\Program Files\Tesseract-OCR\tessdata
# see the explanation from https://www.programmersought.com/article/57222588100/

# https://ichi.pro/id/ocr-dengan-tesseract-opencv-dan-python-231743215466598

# setting this

class settings :
    exe = None

# If you don't have tesseract executable in your PATH, include the following:
# __ts.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

def read (a_settings='',a_file='',b_lang='') :
    __ts.pytesseract.tesseract_cmd = a_settings.exe
    if (b_lang == '') :
        loc_result = __ts.image_to_string(a_file)
    elif (b_lang == 'chinese') :
        loc_result = __ts.image_to_string(a_file,lang = "chi_sim")
    elif (b_lang == 'korean') :
        loc_result = __ts.image_to_string(a_file,lang = "kor")
    elif (b_lang == 'indonesian') :
        loc_result = __ts.image_to_string(a_file,lang = "ind")
    return loc_result
    # print(loc_result) for better view

def car_plate (a_settings='',a_file='') :
    '''
    loc_img,loc_roi = __pp.ai.cv.car_plate(a_file)
    loc_gray = __cv.cvtColor(loc_roi,__cv.COLOR_BGR2GRAY)
    loc_thresh = __cv.adaptiveThreshold(loc_gray,255,__cv.ADAPTIVE_THRESH_GAUSSIAN_C,__cv.THRESH_BINARY,11,2)
    loc_text = __ts.image_to_string(loc_roi)
    '''
    loc_text = ''
    return loc_text
    