'''
canny_write_image.py

Experiment with OpenCV for FITS files.

http://docs.opencv.org/trunk/doc/py_tutorials/py_tutorials.html

Author: S.T. Castle
Created: 20150226
'''

import numpy as np
import cv2
import os.path

def canny(name, orig_img, blockSize, c, t1, t2):
    '''
    name: original filename of the image
    orig_img: The image to be processed.
    blockSize: size of the pixel neighborhood for adaptive thresholding.
    c: Correction to apply before thresholding.
    t1: first threshold for hysteresis procedure
    t2: second threshold for hysteresis procedure
    '''
    img = np.ndarray.copy(orig_img)    # Copy of original for smoothing.

    # Split filename and extension.
    spl = os.path.splitext(name)
    name_pref = spl[0]  # Name prefix.

    # Apply a smoothing filter.
    img = cv2.bilateralFilter(img,9,75,75)
    name_pref = name_pref + '_smooth=bilat'

    # Just canny, no thresholding.
    can_name = name_pref + '_canny' + spl[1]
    can = cv2.Canny(img,t1,t2)
    cv2.imwrite(can_name, can)

    # Adaptive mean thresholding and Canny.
    am_name = name_pref + '_adapt-mean-thr_canny' + spl[1]
    am_thr = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                                   cv2.THRESH_BINARY,blockSize,c)
    am_canny = cv2.Canny(am_thr,t1,t2)
    cv2.imwrite(am_name, am_canny)

    # Adaptive Gaussian thresholding and Canny.
    ag_name = name_pref + '_adapt-gauss-thr_canny' + spl[1]
    ag_thr = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                   cv2.THRESH_BINARY,blockSize,c)
    ag_canny = cv2.Canny(ag_thr,t1,t2)
    cv2.imwrite(ag_name, ag_canny)

    # Otsu's thresholding and Canny.
    ot_name = name_pref + '_otsu-thr_canny' + spl[1]
    ret, ot_thr = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ot_canny = cv2.Canny(ot_thr,t1,t2)
    cv2.imwrite(ot_name, ot_canny)
