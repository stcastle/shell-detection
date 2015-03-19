'''
canny.py

Experiment with OpenCV for FITS files.

http://docs.opencv.org/trunk/doc/py_tutorials/py_tutorials.html

Author: S.T. Castle
Created: 20150216
'''

import numpy as np
import cv2
import fileinput
from matplotlib import pyplot as plt
from fits_proc import FitsProc

def main():
    for file in fileinput.input():
        filename = fileinput.filename()

        # Open FITS file with custom class.
        if filename[-4:] == 'fits':
            image = FitsProc(filename)
            # Get numpy ndarray of image data.
            img = image.get_data()
            # Convert image data to uint8, so Canny edge detection will work.
            data = np.uint8(data)

        elif filename[-3:] == 'png':
            img = cv2.imread(filename, 0)  # Grayscale.

        else:
            sys.exit(filename + " is not a valid file type.")
        imgcopy = np.ndarray.copy(img)
        
        print 'Opened ' + filename
        print 'Shape: ' + str(img.shape)
        print 'Size: ' + str(img.size)
        print 'Type: ' + str(img.dtype.name)

        images = [img]
        titles = ["Original"]

        # Canny threshold values
        t1 = 100
        t2 = 200
        plt.gcf().suptitle('Canny threshold 1 = ' + str(t1) +
                            '\nthreshold 2 = ' + str(t2))
        # Canny on Original
        titles.append('Canny')
        images.append(cv2.Canny(img,t1,t2,L2gradient=True))
        # Bilateral filter and Canny
        titles.append('Bilat Blur and Canny')
        img = cv2.bilateralFilter(imgcopy,9,75,75)
        images.append(cv2.Canny(img,t1,t2,L2gradient=True))
        # Bilateral filter, adaptive mean threshold, and Canny    
        titles.append('Bilat Blur, Adaptive Mean Thresh, and Canny')
        # img is already bilat filtered
        blockSize = 201
        c = 0
        th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,blockSize,c)
        images.append(cv2.Canny(th2,t1,t2,L2gradient=True))
        # Bilateral filter, Otsu's Threshold, and Canny
        titles.append('Bilat Blur, Otsu\'s Thresh, and Canny')
        ret4,th4 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        images.append(cv2.Canny(th4,t1,t2,L2gradient=True))
 
        # Plot the images
        ncols = 2
        nrows = 3
        # plot first image on its own row
        plt.subplot(nrows,ncols,1),plt.imshow(images[0],'gray')
        plt.title(titles[0])
        plt.xticks([]),plt.yticks([])

        for i in xrange(1,ncols*(nrows-1)+1):
            try:
                plt.subplot(nrows,ncols,i+ncols),plt.imshow(images[i],'gray')
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
