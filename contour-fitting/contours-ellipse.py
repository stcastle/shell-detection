'''
contours_ellipse.py

Experiment with OpenCV for FITS files.

http://docs.opencv.org/trunk/doc/py_tutorials/py_tutorials.html

Author: S.T. Castle
Created: 20150217
'''

import numpy as np
import cv2
import fileinput
from matplotlib import pyplot as plt
import sys
from fits_proc import FitsProc

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

        # Start by applying a bilater filter to smooth noise.
        img = cv2.bilateralFilter(img,9,75,75)
        
        # Parameters for adaptive thresholding.
        blockSize = 201
        c = 0
        plt.gcf().suptitle('Adaptive block size = ' + str(blockSize) +
            '\nAdaptive substraction = ' + str(c))

        # Apply adaptive mean threshold.
        titles.append('Adapt Mean Thresh and Contour Ellipse')
        a_thr = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,blockSize,c)
        # Find contours. Store all with cv2.CHAIN_APPROX_NONE.
        a_contours, a_hierarchy = cv2.findContours(a_thr,cv2.RETR_TREE,\
                cv2.CHAIN_APPROX_NONE) 
        # Get ndarray of contour points.
        a_cnt = a_contours[0]
        print 'a_cnt:'
        print 'Shape: ' + str(a_cnt.shape)
        print 'Size: ' + str(a_cnt.size)
        print 'Type: ' + str(a_cnt.dtype.name)

        # Fit an ellipse then draw it on the image.
        a_ellipse = cv2.fitEllipse(a_cnt)
        cv2.ellipse(a_imgcopy,a_ellipse,(0,255,0),25) 
        images.append(a_imgcopy)

        # Repeat the previous steps using Otsu's Thresholding.
        titles.append('Otsu\'s Thresh and Contour Ellipse')
        ret,o_thr = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) 
        o_contours, o_hierarchy = cv2.findContours(o_thr,cv2.RETR_TREE,\
                cv2.CHAIN_APPROX_NONE)
        o_cnt = o_contours[0]
        o_ellipse = cv2.fitEllipse(o_cnt)
        cv2.ellipse(o_imgcopy,o_ellipse,(0,255,0),25)
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
