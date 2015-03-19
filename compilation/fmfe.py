''' Module: fmfe

    Fast Multilevel Fuzzy Enhancement
    Implementation of algorithm from J. Wu et al. 2007. 

    Created by S.T. Castle on 2015-01-25
    
    Enahnces an image prior to edge detection.
'''

import numpy as np
import scipy
#from astropy.io import fits
#import pyfits as fits  # May need to use this if astropy library unavailable.

def fmfe(data, w, h, fuzzy_t):
    '''Fast Multilevel Fuzzy Enhancement
    data: 2d array
    w: width
    h: height
    fuzzy_t: fuzzy threshold for enhancement
    ''' 
    # Get the threshold to separate into two sets of pixels.
    q = get_threshold(data, w, h)

    # Now get the mean values for the two sets, ab for the low (background)
    # pixels and ao for the high (object) pixels.
    sumb = 0.0  # Sum or pixel values.
    numb = 0    # Number of pixels.
    sumo = 0.0
    numo = 0
    # Also record min and max pixel values.
    min = data[0][0] 
    max = 0.0
    for i in xrange(h):
        for j in xrange(w):
            val = data[i][j]
            if val < min: min = val
            if val > max: max = val
            if val < q:
                sumb += val
                numb += 1
            else:
                sumo += val
                numo += 1
    ab = sumb/numb
    ao = sumo/numo

    r = 2   # Number of times to enhance.
    # Convert pixel values to values in fuzzy domain.
    # Then enhance using the fuzzy threshold, and return to spatial domain.
    for i in xrange(h):
        for j in xrange(w):
            p = convert_to_fuzzy(data[i][j], ab, ao, min, max)
            # Enhance.
            for k in range(r):
                p = enhance(p, fuzzy_t)
            # Transform back to the spatial domain.
            p = convert_to_spatial(p, ab, ao, min, max)
            data[i][j] = p

    return data
    # End fmfe.
    

def get_threshold(data, w, h):
    '''Return the average pixel value, excluding zero-valued pixels.'''
    sum = 0.0  # Sum of pixel values.
    num = 0    # Number of nonzero pixel values.
    for i in xrange(h):
        for j in xrange(w): 
            val = data[i][j]
            if val:           # if nonzero
                sum += val
                num += 1
    return (sum/num)

def convert_to_fuzzy(x, ab, ao, min, max):
    '''Linear mapping transformation from pixel value to fuzzy value.''' 
    if x > ao:
       return ( (max-x)/(max-ao) )
    if x > ((ao+ab)/2):
       return ( (2*x-ao-ab)/(ao-ab) )
    if x > ab:
       return ( (ao+ab-2*x)/(ao-ab) )
    return ( (x-min)/(ab-min) )

def convert_to_spatial(x, ab, ao, min, max):
    '''Linear mapping transformation from fuzzy value to pixel value.'''
    if x > ao:
        return ( max-(max-ao)*x )
    if x > ((ao+ab)/2):
        return ( ((ao-ab)*x+ao+ab)/2 )
    if x > ab:
        return ( (ao+ab-(ao-ab)*x)/2 )
    return ( (ab-min)*x+min )

def enhance(x, t):
    '''Enhance a fuzzy value x according to the threshold t.'''
    if x > t:
       return ( 1-((1-x)**2/(1-t)) )
    return ( x**2/t )

