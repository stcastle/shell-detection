'''
edges_trackbar.py

Experiment with OpenCV for FITS files.
Create a trackbar for adjusting thresholds in Canny edge detection.

http://docs.opencv.org/trunk/doc/py_tutorials/py_tutorials.html

Author: S.T. Castle
Created: 20150216
'''

import numpy as np
import cv2
import fileinput
from fits_proc import FitsProc

def nothing(x):
    pass

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

        # Create a window and trackbars
        cv2.namedWindow(filename)
        cv2.createTrackbar('t1',filename,0,255,nothing) # Threshold 1
        cv2.createTrackbar('t2',filename,0,255,nothing)

        # Create switch for ON/OFF functionality.
        switch = '0 : Off \n1 : ON'
        cv2.createTrackbar(switch,filename,0,1,nothing)

        while(1):
            cv2.imshow('image',img)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break

            # get current trackbar positions
            t1 = cv2.getTrackbarPos('t1',filename)
            t2 = cv2.getTrackbarPos('t2',filename)
            s = cv2.getTrackbarPos(switch,filename)

            if s:
                img = cv2.Canny(imgcopy,t1,t2)
            else:
                img = np.ndarray.copy(imgcopy)


        cv2.destroyAllWindows()
        fileinput.nextfile()

    fileinput.close()



if __name__ == '__main__':
    main()
