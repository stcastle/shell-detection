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
#import fits_proc
from astropy.io import fits

def canny(name, orig_img, blockSize, c, t1, t2):
    '''
    name: original filename of the image
    orig_img: The fits image to be processed.
    blockSize: size of the pixel neighborhood for adaptive thresholding.
    c: Correction to apply before thresholding.
    t1: first threshold for hysteresis procedure
    t2: second threshold for hysteresis procedure
    '''
    img = fits.PrimaryHDU.copy(orig_img)    # Copy of original for smoothing.
    # Convert to 'float32' data type for OpenCV.
    orig_img.data = orig_img.data.astype('float32')
    print 'here1'

    # Split filename and extension.
    spl = os.path.splitext(name)
    name_pref = spl[0]  # Name prefix.
    print 'here1.5'

    # Apply a smoothing filter.
    orig_img.data = cv2.bilateralFilter(orig_img.data,9,75,75)
    name_pref = name_pref + '_smooth=bilat'
    print 'here2'

    # Just canny, no thresholding.
    can_name = name_pref + '_canny' + spl[1]
    #img.data = cv2.Canny(orig_img.data,t1,t2)
    img.writeto(can_name, clobber=True)
    print 'here3'

    # Adaptive mean thresholding and Canny.
    am_name = name_pref + '_adapt-mean-thr_canny' + spl[1]
    am_thr = cv2.adaptiveThreshold(orig_img.data,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                                   cv2.THRESH_BINARY,blockSize,c)
    img.data = am_thr
    #img.data = cv2.Canny(am_thr,t1,t2)
    img.writeto(am_name, clobber=True)

    # Adaptive Gaussian thresholding and Canny.
    ag_name = name_pref + '_adapt-gauss-thr_canny' + spl[1]
    ag_thr = cv2.adaptiveThreshold(orig_img.data,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                   cv2.THRESH_BINARY,blockSize,c)
    img.data = ag_thr
    #img.data = cv2.Canny(ag_thr,t1,t2)
    img.writeto(ag_name, clobber=True)

    # Otsu's thresholding and Canny.
    ot_name = name_pref + '_otsu-thr_canny' + spl[1]
    ret, ot_thr = cv2.threshold(orig_img.data,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img.data = ot_thr
    #img.data = cv2.Canny(ot_thr,t1,t2)
    img.writeto(ot_name, clobber=True)
