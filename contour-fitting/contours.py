'''
contours.py

Experiment with OpenCV for FITS files.

http://docs.opencv.org/trunk/doc/py_tutorials/py_tutorials.html

Author: S.T. Castle
Created: 20150216
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
        a_imgcopy = np.ndarray.copy(img)  # for adaptive thresholding.
        o_imgcopy = np.ndarray.copy(img)  # for Otsu's thresholding.
    
        print 'Opened ' + filename
        print 'Shape: ' + str(img.shape)
        print 'Size: ' + str(img.size)
        print 'Type: ' + str(img.dtype.name)

        images = [img]
        titles = ["Original"]

        img = cv2.bilateralFilter(img,9,75,75)
        
        blockSize = 201
        c = 0
        plt.gcf().suptitle('Adaptive block size = ' + str(blockSize) +
            '\nAdaptive substraction = ' + str(c))

        titles.append('Adaptive Mean Thresh and Contours')
        a_thr = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,blockSize,c)
        a_contours, a_hierarchy = cv2.findContours(a_thr,cv2.RETR_TREE,\
                cv2.CHAIN_APPROX_SIMPLE) 
        cv2.drawContours(a_imgcopy, a_contours, -1, (0,255,0), 25)
        images.append(a_imgcopy)

        titles.append('Otsu\'s Thresh and Contours')
        ret,o_thr = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) 
        o_contours, o_hierarchy = cv2.findContours(o_thr,cv2.RETR_TREE,\
                cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(o_imgcopy, o_contours, -1, (0,255,0), 25)
        images.append(o_imgcopy)

        # Plot the images
        for i in xrange(3):
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
