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
from fits_proc import FitsProc
import fmfe
import edge_detect

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
        h = img.shape[0]
        w = img.shape[1]


        images = [img]
        titles = ["Original"]

        print 'Running fmfe...'
        fuzzy = fmfe.fmfe(img, w, h, 0.5)
        print 'Completed fmfe.'
        images.append(fuzzy)
        titles.append("FMFE")
        
        print 'Detecting edges...'
        edges = edge_detect.find_edges(fuzzy, h, w)
        print 'Found edges.'
        images.append(edges)
        titles.append("Edges")
        
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
