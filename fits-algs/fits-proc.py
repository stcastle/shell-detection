''' Module: fits-proc 

    Classes contained: FitsProc

    Created by S.T. Castle on 2015-01-16
    
    Loads data files for processing and rewriting.
'''

import numpy as np
import scipy
from astropy.io import fits
#import pyfits as fits  # May need to use this if astropy library unavailable.

from fmfe import fmfe
import edge-detect

class FitsProc:
    ''' A class to load a FITS image file, manipulate the image,
        and write new FITS files.'''

    # Constructor.
    # param: path to the desired FITS file.
    # throws: I/O Exception.
    def __init__(self, filename):
        try:
            self.hdulist = fits.open(filename)
            self.header = self.hdulist[0].header  # Header of the FITS file.
            try:
                self.data = self.hdulist[1].data  # Data ndarray of FITS file.
            except IndexError:
                self.data = self.hdulist[0].data  # FITS file is single-exten.
            self.h = self.data.shape[0]           # Size of data along y axis.
            self.w = self.data.shape[1]           # Size of data along x axis.
            # self.hdulist.close()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)


    # Accessor Methods

    # Return the ndarray data set.
    def get_data(self):
        return self.data

    # Return the width  (x) of the data set.
    def get_width(self):
        return self.w

    # Return the height (y) of the data set.
    def get_height(self):
        return self.h

    # Write the image to a specified FITS file.
    def write(self, filename):
        try:
            self.hdulist.writeto(filename)
        except IOError as e:
            print e
            x = raw_input('Okay to overwrite (y/n)? ')
            if (x == 'y') or (x == 'Y'):
                self.hdulist.writeto(filename, clobber=True)
            

    # Mutator Methods.
    def blur(self):
        self.data = fmfe(self.data, self.w, self.h, 0.5)

    def edges(self):
        self.data = edge_detect.find_edges(self.data, self.h, self.w)

    def subtract_mask(self, filename):
        '''Must be same dimensions'''
        try:
            msk_hdulist = fits.open(filename)
            msk_data = msk_hdulist[1].data
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        try:
            self.data -= msk_data
        except:
            print 'error'
        msk_hdulist.close()

# End FitsProc
