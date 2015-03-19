'''
laplace-sobel.py

Experiment with OpenCV for FITS files.

http://docs.opencv.org/trunk/doc/py_tutorials/py_tutorials.html

Author: S.T. Castle
Created: 20150209
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
        # OpenCV. Display image.
        #cv2.imshow(filename, img)
        #cv2.waitKey(0)

        print 'Shape: ' + str(img.shape)
        print 'Size: ' + str(img.size)
        print 'Type: ' + str(img.dtype.name)

        # Convert image data to uint8, so Canny edge detection will work.
        #img = np.uint8(img)
        #print 'Converted to uint8.'

        #print 'Shape: ' + str(img.shape)
        #print 'Size: ' + str(img.size)
        #print 'Type: ' + str(img.dtype.name)

        ## Compare converted image to original.
        #print 'Displaying converted image...'
        #cv2.imshow('uint8', img)
        #cv2.waitKey(0)
        # cv2.destroyAllWindows()

        laplacian = cv2.Laplacian(img,cv2.CV_64F)

        print 'Shape: ' + str(laplacian.shape)
        print 'Size: ' + str(laplacian.size)
        print 'Type: ' + str(laplacian.dtype.name)

        sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
        sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)

        # Plot the images
        plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
        plt.title('Original'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
        plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
        plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
        plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

        plt.show()

        # Display edges.
        #print 'Displaying edges...'
        #cv2.imshow('Edges!', edges)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        # Write the edges file.
        #print 'Writing edges file...'
        #image.img = edges
        #image.write('new.fits')
        #print 'Done with ' + filename

        fileinput.nextfile()

    fileinput.close()



if __name__ == '__main__':
    main()
