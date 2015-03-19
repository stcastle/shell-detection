'''
noise.py

Functions for adding noise to images.

Author: S.T. Castle
Created: 2015-02-04
'''

import numpy as np

def poisson_noise(image):
    #Create noisy image. Poisson is based off image values.
    noise = np.empty_like(image)
    for i in xrange(noise.shape[0]):
        for j in xrange(noise.shape[1]):
            noise[i][j] = np.clip(np.random.poisson(image[i][j]),0,255)
    return noise
