'''
threshold_write_image.py

Experiment with OpenCV for FITS files.

http://docs.opencv.org/trunk/doc/py_tutorials/py_tutorials.html

Author: S.T. Castle
Created: 20150226
'''

import numpy as np
import cv2
import os.path

def fft(name, orig_img, blockSize, c):
    '''
    name: original filename of the image
    orig_img: The image to be processed.
    blockSize: size of the pixel neighborhood for adaptive thresholding.
    c: Correction to apply before thresholding.
    '''
    img = np.ndarray.copy(orig_img)    # Copy of original for smoothing.

    # Split filename and extension.
    spl = os.path.splitext(name)
    name_pref = spl[0]  # Name prefix.

    # Apply a smoothing filter.
    # Bilateral blur.
    img = cv2.bilateralFilter(img,9,75,75) 
    name_pref = name_pref + '_smooth=bilat'

    # Adaptive mean threshold.
    am_name = name_pref + '_adapt-mean-thr' + spl[1]
    am_thr = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                                   cv2.THRESH_BINARY,blockSize,c)
    cv2.imwrite(am_name, am_thr)

    # Adaptive Gaussian threshold.
    ag_name = name_pref + '_adapt-gauss-thr' + spl[1]
    ag_thr = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                   cv2.THRESH_BINARY,blockSize,c)
    cv2.imwrite(ag_name, ag_thr)

    # Otsu's threshold.
    ot_name = name_pref + '_otsu-thr' + spl[1]
    ret, ot_thr = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imwrite(ot_name, ot_thr)
