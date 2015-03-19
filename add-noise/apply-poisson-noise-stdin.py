'''
apply_poisson_noise-stdin.py

Apply Poisson noise to input images.

Author: S.T. Castle
Created: 20150226
'''

import noise  # Custom module.

import numpy as np
import cv2
import fileinput
import os.path
import sys

def generate_noise():
    for filename in sys.stdin:
        if filename == '': continue

        image = cv2.imread(filename, 0) # open grayscale

        print 'Opened ' + filename

        #print 'Displaying image...'
        #cv2.imshow(filename, image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        #print 'Shape: ' + str(image.shape)
        #print 'Size: ' + str(image.size)
        #print 'dtype: ' + str(image.dtype)

        print 'Working...'
        noise_image = noise.poisson_noise(image)

        #print 'Shape: ' + str(noise_image.shape)
        #print 'Size: ' + str(noise_image.size)
        #print 'dtype: ' + str(noise_image.dtype)

        #cv2.imshow('Noise!', noise_image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        # Get the new filename and write the file.
        spl = os.path.splitext(filename)
        newname = spl[0] + '_noise' + spl[1] # Insert _noise before extension.
        cv2.imwrite(newname, noise_image)
        print 'Wrote ' + newname


if __name__ == '__main__':
    generate_noise()
