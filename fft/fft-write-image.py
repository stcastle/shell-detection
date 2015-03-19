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

def fft(name, orig_img):
    '''
    name: original filename of the image
    orig_img: The image to be processed.
    '''
    img = np.ndarray.copy(orig_img)    # Copy of original for smoothing.

    # Split filename and extension.
    (name_pref, name_ext)  = os.path.splitext(name)

    # Apply a smoothing filter.
    # Bilateral blur.
    img = cv2.bilateralFilter(img,9,75,75) 
    name_pref = name_pref + '_smooth=bilat'

    # Apply FFT and shift spectrum so low frequencies are at center of image.
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    name_pref = name_pref + '_fft'

    # Write the magnitude spectrum
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    mag_name = name_pref + '_magspec' + name_ext
    cv2.imwrite(mag_name, magnitude_spectrum)

    # Remove part of the magnitude spectrum and calculate inverse FFT
    rows, cols = img.shape
    crow,ccol = rows/2 , cols/2
    
    # High pass filter: Remove low frequencies.
    #cut = 30
    #fshift[crow-cut:crow+cut, ccol-cut:ccol+cut] = 0

    # Low pass filter: Remove high frequencies.
    keep = 20
    fshift[:crow-keep, :] = 0
    fshift[crow+keep:, :] = 0
    fshift[:, :ccol-keep] = 0
    fshift[:, ccol+keep:] = 0

    # Shift back into place and inverse FFT.
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    # Write final image.
    fft_name = name_pref + name_ext
    cv2.imwrite(fft_name, img_back)
