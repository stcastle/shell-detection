'''
threshold.py

Experiment with OpenCV for FITS files.

http://docs.opencv.org/trunk/doc/py_tutorials/py_tutorials.html

Author: S.T. Castle
Created: 20150213
'''

import numpy as np
import cv2
import fileinput
import os.path

def main():
    for file in fileinput.input():
        filename = fileinput.filename()

        img = cv2.imread(filename, 0)  # Grayscale.
        imgcopy = np.ndarray.copy(img)

        # Split filename and extension.    
        (name_pref, name_ext) = os.path.splitext(filename)

        # No filter!
        ret,th = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        tname = name_pref + '_otsu' + name_ext
        cv2.imwrite(tname, th)

        # Median Blur
        img = cv2.medianBlur(imgcopy,5)
        ret,th = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        tname = name_pref + 'smooth=median_otsu' + name_ext
        cv2.imwrite(tname, th)
    
        # Gaussian Blur
        img = cv2.GaussianBlur(imgcopy,(5,5),0) 
        ret,th = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        tname = name_pref + 'smooth=gauss_otsu' + name_ext
        cv2.imwrite(tname, th)
        
        # Bilateral Blur
        img = cv2.bilateralFilter(imgcopy,9,75,75) 
        ret,th = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        tname = name_pref + 'smooth=bilat_otsu' + name_ext
        cv2.imwrite(tname, th)
 
        fileinput.nextfile()

    fileinput.close()


if __name__ == '__main__':
    main()
