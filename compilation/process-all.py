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
from contours_write_image import contours
from threshold_write_image import threshold
from canny_write_image import canny
from fmfe_main_write_image import run_fmfe

def main():
    # Set threshold parameters.
    blockSize = 201  # Pixel size of the neighborhood area.
    thresh_correction = 0  # Correction subtracted from adaptive threshold.
    fuzzy_thresh = 0.5  # Threshold for FMFED.
    canny_t1 = 100      # First threshold for Canny edge detection.
    canny_t2 = 200      # Second threshold for Canny edge detection.

    count = 1  # Count the number of images.
    # Process files.
    for file in fileinput.input():
        filename = fileinput.filename()

        print '-----Image Number ' + str(count) + '-----'
        img = cv2.imread(filename, 0)  # Open as grayscale image.
        print 'Opened ' + filename

        # Thresholds.
        print 'Applying thresholds to image...',
        threshold(filename, img, blockSize, thresh_correction)
        print 'Done.'

        # Contours.
        print 'Calculating and drawing image contours...',
        contours(filename, img, blockSize, thresh_correction)
        print 'Done.'

        # Canny.
        print 'Running Canny edge detection...',
        canny(filename, img, blockSize, thresh_correction, canny_t1, canny_t2)
        print 'Done.'

        # FMFE
        print 'Running FMFE...',
        run_fmfe(filename, img, fuzzy_thresh)
        print 'Done.' 
       
        fileinput.nextfile()
        count += 1

    fileinput.close()

if __name__ == '__main__':
    main()
