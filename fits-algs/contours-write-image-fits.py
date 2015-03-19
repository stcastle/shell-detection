'''
contours_write_image.py

Experiment with OpenCV for FITS files.

http://docs.opencv.org/trunk/doc/py_tutorials/py_tutorials.html

Author: S.T. Castle
Created: 20150226
'''

import numpy as np
import cv2
import os.path

def contours(name, orig_img, blockSize, c):
    '''
    name: original filename of the image
    orig_img: The image to be processed.
    blockSize: size of the pixel neighborhood for adaptive thresholding.
    c: Correction to apply before thresholding.
    '''
    img = np.ndarray.copy(orig_img)    # Copy of original for smoothing.
    #cnt_imgcopy = np.ndarray.copy(img) # for contours without thresholding.
    am_imgcopy = np.ndarray.copy(img)  # for adaptive mean thresholding.
    ag_imgcopy = np.ndarray.copy(img)  # for adaptive Gaussian thresholding.
    ot_imgcopy = np.ndarray.copy(img)  # for Otsu's thresholding.
    ca_imgcopy = np.ndarray.copy(img)  # for canny edge detection.

    cnt_width = 25  # Thickness of the drawn contours. No algorithmic influence.

    # Split filename and extension.
    spl = os.path.splitext(name)
    name_pref = spl[0]  # Name prefix.

    # Apply a smoothing filter.
    img = cv2.bilateralFilter(img,9,75,75)
    name_pref = name_pref + '_smooth=bilat'
    
    # Just contours, no thresholding.
    #cnt_name = name_pref + '_contours' + spl[1]
    #contours, hierarchy = cv2.findContours(cnt_imgcopy,cv2.RETR_TREE,\
    #                                       cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(cnt_imgcopy, contours, -1, (0,255,0), cnt_width)
    #cv2.imwrite(cnt_name, cnt_imgcopy)

    # Adaptive mean thresholding and contours.
    am_name = name_pref + '_adapt-mean-thr_contours' + spl[1]
    am_thr = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                                   cv2.THRESH_BINARY,blockSize,c)
    am_contours, am_hierarchy = cv2.findContours(am_thr,cv2.RETR_TREE,\
                                                 cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(am_imgcopy, am_contours, -1, (0,255,0), cnt_width)
    cv2.imwrite(am_name, am_imgcopy)

    # Adaptive Gaussian thresholding and contours.
    ag_name = name_pref + '_adapt-gauss-thr_contours' + spl[1]
    ag_thr = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                   cv2.THRESH_BINARY,blockSize,c)
    ag_contours, ag_hierarchy = cv2.findContours(ag_thr,cv2.RETR_TREE,\
                                                 cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(ag_imgcopy, ag_contours, -1, (0,255,0), cnt_width)
    cv2.imwrite(ag_name, ag_imgcopy)
           
    # Otsu's thresholding and contours.
    ot_name = name_pref + '_otsu-thr_contours' + spl[1]
    ret, ot_thr = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ot_contours, ot_hierarchy = cv2.findContours(ot_thr,cv2.RETR_TREE,\
                                                 cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(ot_imgcopy, ot_contours, -1, (0,255,0), cnt_width)
    cv2.imwrite(ot_name, ot_imgcopy)

    # Canny edge detection and contours.
    ca_name = name_pref + '_canny_contours' + spl[1]
    canny = cv2.Canny(img,100,200)
    ca_contours, ca_hierarchy = cv2.findContours(canny,cv2.RETR_TREE,\
                                                 cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(ca_imgcopy, ca_contours, -1, (0,255,0), cnt_width)
    cv2.imwrite(ca_name, ca_imgcopy)
