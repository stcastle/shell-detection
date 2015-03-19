'''testing...'''

import numpy as np
import cv2
import fileinput
import noise

def generate_noise():
    for file in fileinput.input():
        filename = fileinput.filename()
        image = cv2.imread(filename, 0) # open grayscale

        print 'Opened ' + filename
        print 'Displaying image...'

        cv2.imshow(filename, image)
        cv2.waitKey(0)
        #cv2.destroyAllWindows()

        print 'Shape: ' + str(image.shape)
        print 'Size: ' + str(image.size)
        print 'dtype: ' + str(image.dtype)

        noise_image = noise.poisson_noise(image)

        print 'Shape: ' + str(noise_image.shape)
        print 'Size: ' + str(noise_image.size)
        print 'dtype: ' + str(noise_image.dtype)

        cv2.imshow('Noise!', noise_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        fileinput.nextfile()

    fileinput.close()

if __name__ == '__main__':
    generate_noise()
