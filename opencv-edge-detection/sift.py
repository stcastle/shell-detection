'''
sift.py

Experiment with OpenCV for FITS files.

http://docs.opencv.org/trunk/doc/py_tutorials/py_tutorials.html

Author: S.T. Castle
Created: 20150223
'''

import numpy as np
import cv2
import fileinput
from matplotlib import pyplot as plt
import sys
from fits-proc import FitsProc

def main():
    for file in fileinput.input():
        filename = fileinput.filename()

        # Open FITS file with custom class.
        if filename[-4:] == 'fits':
            image = FitsProc(filename)
            # Get numpy ndarray of image data.
            img = image.get_data()

        elif filename[-3:] == 'png':
            img = cv2.imread(filename, 0)  # Grayscale.

        else:
            sys.exit(filename + " is not a valid file type.")
        print 'Opened ' + filename

        sift = cv2.SIFT()
        imgcopy = np.ndarray.copy(img)
        kp = sift.detect(imgcopy,None)

        img=cv2.drawKeypoints(imgcopy,kp)

        cv2.imwrite('sift.jpg',img)
        print 'New file written as sift.jpg'        

        fileinput.nextfile()

    fileinput.close()


if __name__ == '__main__':
    main()
