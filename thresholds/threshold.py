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
        imgcopy = np.ndarray.copy(img)

        images = [img]
        titles = ["Original"]

        blockSize = 201  # Block size for adaptive thresholding.
        c = 0  # Amount to subtract from adaptive mean.
        plt.gcf().suptitle('Adaptive block size = ' + str(blockSize) +
                '\nAdaptive substraction = ' + str(c))
        
        # No filter!
        filter = ''
        # im1
        titles.append('Global Thresh' + filter)
        ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        images.append(th1)
        # im2
        titles.append('Adaptive Mean Thresh' + filter)
        th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,blockSize,c)
        images.append(th2)
        # im3
        titles.append('Adaptive Gaussian Thresh' + filter)
        th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,blockSize,c)
        images.append(th3)
        # im4
        titles.append('Otsu\'s Thresh' + filter)
        ret,th4 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        images.append(th4)

        # Median Blur
        img = cv2.medianBlur(imgcopy,5)
        filter = ' Median Blur'
        # im1
        titles.append('Global Thresh' + filter)
        ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        images.append(th1)
        # im2
        titles.append('Adaptive Mean Thresh' + filter)
        th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,blockSize,c)
        images.append(th2)
        # im3
        titles.append('Adaptive Gaussian Thresh' + filter)
        th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,blockSize,c)
        images.append(th3)
        # im4
        titles.append('Otsu\'s Thresh' + filter)
        ret,th4 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        images.append(th4)
    
        # Gaussian Blur
        img = cv2.GaussianBlur(imgcopy,(5,5),0) 
        filter = ' Gauss Blur'
        # im1
        titles.append('Global Thresh' + filter)
        ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        images.append(th1)
        # im2
        titles.append('Adaptive Mean Thresh' + filter)
        th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,blockSize,c)
        images.append(th2)
        # im3
        titles.append('Adaptive Gaussian Thresh' + filter)
        th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,blockSize,c)
        images.append(th3)
        # im4
        titles.append('Otsu\'s Thresh' + filter)
        ret,th4 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        images.append(th4)
        
        # Bilateral Blur
        img = cv2.bilateralFilter(imgcopy,9,75,75) 
        filter = ' Bilat Blur'
        # im1
        titles.append('Global Thresh' + filter)
        ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        images.append(th1)
        # im2
        titles.append('Adaptive Mean Thresh' + filter)
        th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,blockSize,c)
        images.append(th2)
        # im3
        titles.append('Adaptive Gaussian Thresh' + filter)
        th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,blockSize,c)
        images.append(th3)
        # im4
        titles.append('Otsu\'s Thresh' + filter)
        ret,th4 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        images.append(th4)
 

        # Plot the images
        plotx = 4
        ploty = 5

        # plot first on its own line.
        plt.subplot(ploty,plotx,1),plt.imshow(images[0],'gray')
        plt.title(titles[0])
        plt.xticks([]),plt.yticks([])

        for i in xrange(1,plotx*(ploty-1)+1):
            try:
                plt.subplot(ploty,plotx,i+plotx),plt.imshow(images[i],'gray')
                plt.title(titles[i])
                plt.xticks([]),plt.yticks([])
            except IndexError:
                print 'IndexError in plot.'
                break

        #plt.gcf().suptitle(filename)
        plt.gcf().canvas.set_window_title(filename)
        plt.show()
        fileinput.nextfile()

    fileinput.close()


if __name__ == '__main__':
    main()
