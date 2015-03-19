'''
Author: S.T. Castle
Created: 20150319
'''

import numpy as np
import cv2
import os.path
import scipy
import fileinput
from astropy.io import fits

def lpf():
    '''
    A low-pass filter using Fast Fourier Transform (FFT).
    name: original filename of the image
    orig_img: The image to be processed.
    keep: radius of pixel square to keep from frequency space LPF.
    '''
    keep = 40

    for file in fileinput.input():

        filename = fileinput.filename()

        #img = cv2.imread(filename, 0)
        img_hdulist = fits.open(filename)
        # !!! Assume only a primary HDU on the FITS file. !!!
        img = img_hdulist[0].data
        print 'Opened ' + filename

        # Split filename and extension.
        (name_pref, name_ext) = os.path.splitext(filename)

        # Optional smoothing filter.
        #img = cv2.bilateralFilter(img,9,75,75)
        #img = scipy.ndimage.filters.gaussian_filter(img, 5)

        # Fourier transform to generate magnitude spectrum in frequency space.
        print 'FFT...'
        f = np.fft.fft2(img)
        # Shift spectrum for convenience.
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20*np.log(np.abs(fshift))
        print 'Done.'

        # Keep specified number of low frequency pixels.
        rows, cols = img.shape
        crow,ccol = rows/2 , cols/2
        keep = 40
        fshift[:crow-keep, :] = 0
        fshift[crow+keep:, :] = 0
        fshift[:, :ccol-keep] = 0
        fshift[:, ccol+keep:] = 0

        # Shift back and inverse FFT.
        print 'Inverse FFT.'
        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        print 'Done.'

        # Write image.
        img_hdulist[0].data = img_back
        newname = name_pref + '_fft-lpf-keep=' + str(keep) + name_ext
        img_hdulist.writeto(newname)
        print 'New image written to ' + newname

        # Remove low frequency pixels.
        #cut = 100
        #fshift[crow-cut:crow+cut, ccol-cut:ccol+cut] = 0

        fileinput.nextfile()

    fileinput.close()


if __name__ == '__main__':
    lpf()
