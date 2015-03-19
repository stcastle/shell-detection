'''
otsu_iterative_fits.py

Script to run the otsu algorithm on a FITS image,
repeated an arbitrary number of times.

Author: S.T. Castle
Created: 20150314
'''

import fileinput
import numpy as np
import scipy

from astropy.io import fits
import cv2
import os.path
import sys

def main():


    # Get input from user for number of iterations.
    try:
        iters = int(raw_input('Number of iterations: '))
    except ValueError:
        print 'ERROR: Parameter must be an integer.'
        sys.exit()

    for file in fileinput.input():
        # Get filename.
        filename = fileinput.filename()

        # Open current file.
        img_hdulist = fits.open(filename)
        # !!! Assume only a primary HDU on the FITS file. !!!
        img = img_hdulist[0]
        print 'Opened ' + filename

        # Split filename into prefix and extension.
        (name_pref, name_ext) = os.path.splitext(filename)


        # Get mask file from user.
        try:
            mask_filename = raw_input('Name of mask file: ')
            mask_hdulist = fits.open(mask_filename)
            print 'Opened ' + mask_filename
            print 'Removing the mask...',
            img.data = remove_mask(img.data, mask_hdulist[0].data)
            print 'Done.'
            name_pref = name_pref + '_masked'
            # Write the masked file.
            img.writeto(name_pref+name_ext, clobber=True)
        except:
            print 'Mask not successfully removed. Continuing without mask.'
        
        # Change data type for use with OpenCV algorithms.
        newtype = 'uint8'
        cnv_data = img.data.astype('uint8')
        print 'Converted data to type ' + newtype

        print 'Applying bilateral filter...',
        cnv_data = cv2.bilateralFilter(cnv_data,9,75,75)
        name_pref = name_pref + '_smooth=bilat'
        print 'Done.'

        # Repeat Otsu's thresholding as specified by user.
        for i in range(iters):
            # Otsu's thresholding.
            print 'Applying Otsu thresholding iteration '+str(i+1)+'...',
            ret, ot_thr =\
                cv2.threshold(cnv_data,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            print 'Done.'

            # Update the FITS image to use the thresholded data.
            img_hdulist[0].data = ot_thr
            
            # Write the image to a new FITS file.
            newname = name_pref + '_otsu' + str(i+1) + name_ext
            img_hdulist.writeto(newname, clobber=True)
            print 'New image written to ' + newname

            # Remove the recently thresholded pixels from the data being used.
            cnv_data = remove_mask(cnv_data, ot_thr)

        # Next input file.
        fileinput.nextfile()

    fileinput.close()

def remove_mask(data, mask):
    '''
    Remove a mask of bad pixels from a given data array.
    Both paramaters are numpy ndarrays with the same shape.
    Exception thrown otherwise.
    In the mask, 0s represent good pixels, and all other values are bad pixels.
    Return the adjusted data.
    '''
    # Make sure shapes are identical.
    if data.shape != mask.shape:
        raise Exception('Data and mask array shapes do not match!')
        return

    # Make a new dataset to be filled in with the data, ignoring bad pixels.
    new_data = np.zeros_like(data)

    # Loop through data array, and set bad pixels to 0.
    for i in xrange(new_data.shape[0]):
        for j in xrange(new_data.shape[1]):
            # If current pixel is good, get the data value.
            if not mask[i][j]:
                new_data[i][j] = data[i][j]

    return new_data

if __name__ == '__main__':
    main()

