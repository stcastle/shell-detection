'''
bilat_filter.py

Experiment with OpenCV for FITS files.

http://docs.opencv.org/trunk/doc/py_tutorials/py_tutorials.html

Author: S.T. Castle
Created: 20150213
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
        print 'Shape: ' + str(img.shape)
        print 'Size: ' + str(img.size)
        print 'Type: ' + str(img.dtype.name)

        images = [img]
        titles = ["Original"]

        # im: Gauss
        titles.append('Gaussian Blur')
        images.append(cv2.GaussianBlur(img,(5,5),0))
        # im2: Median
        titles.append('Median Blur')
        images.append(cv2.medianBlur(img,5))
        # im3: Bilateral
        titles.append('Bilateral Blur')
        images.append(cv2.bilateralFilter(img,9,75,75))
    
        # Plot the images
        for i in xrange(4):
            plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
            plt.title(titles[i])
            plt.xticks([]),plt.yticks([])

        #plt.gcf().suptitle(filename)
        plt.gcf().canvas.set_window_title(filename)
        plt.show()
        fileinput.nextfile()

    fileinput.close()


if __name__ == '__main__':
    main()
