'''
process_all.py

Script to call many image processing functions on a set of images.

Author: S.T. Castle
Created: 20150226
'''

import fileinput
import numpy as np
import cv2

# Custom modules.
from smooth-write-image import smooth

def main():
    count = 1  # Count the number of images.
    # Process files.
    for file in fileinput.input():
        filename = fileinput.filename()

        print '-----Image Number ' + str(count) + '-----'
        img = cv2.imread(filename, 0)  # Open as grayscale image.
        print 'Opened ' + filename

        # Smoothing
        print 'Smoothing image...'
        smooth(filename, img)
        print 'Done.'
       
        fileinput.nextfile()
        count += 1

    fileinput.close()

if __name__ == '__main__':
    main()
