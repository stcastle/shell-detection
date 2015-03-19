'''
fmfe_main_write_image.py

Call the Fast Multilevel Fuzzy Edge Detection Algorithm from J.Wu et al. 2007.

Author: S.T. Castle
Created: 20150226
'''

import numpy as np
import cv2
import fmfe
#import edge_detect
import os.path

def run_fmfe(name, orig_img, fuzzy_t):
    '''
    name: original filename of the image.
    orig_img: The image to be processed.
    fuzzy_t: fuzzy threshold parameter.
    '''
    img = np.ndarray.copy(orig_img)    # Copy of original for smoothing.
    
    # Split filename and extension.
    spl = os.path.splitext(name)
    name_pref = spl[0]  # Name prefix.

    # Get height and width of image.
    h = img.shape[0]
    w = img.shape[1]

    # FMFE
    fuzzy_name = name_pref + '_fmfe' + spl[1]
    fuzzy = fmfe.fmfe(img, w, h, fuzzy_t)
    cv2.imwrite(fuzzy_name, fuzzy)
    
    # Apply a smoothing filter.
    # Bilateral blur.
    #img = cv2.bilateralFilter(img,9,75,75)
    #name_pref = name_pref + '_smooth=bilat'

    # FMFE again on smoothed image.
    #fuzzy_filter_name = name_pref + '_fmfe' + spl[1]
    #fuzzy_filter = fmfe.fmfe(img, w, h, fuzzy_t)
    #cv2.imwrite(fuzzy_filter_name, fuzzy_filter)

    # Detect edges to finish FMFED.
    #edges = edge_detect.find_edges(fuzzy, h, w)
