'''
Module: edge-detect

Implementation of Two-Stage Edge Detection from J. Wu et al. 2007.

Code Author: S.T. Castle

Created: 2015-01-26
'''

import numpy

def find_edges(data, h, w):
    '''First-stage edge detection.
       data: 2-D array of pixel values.
       w: width of data.
       h: height of data.
    '''
    # For each pixel, calculate the mean value of the surrounding pixels.
    # Check a distance rad in every direction, including diagonals,
    # from each pixel.
    # Call the second stage on each pixel that is an edge candidate.
    edge_data = numpy.empty_like(data)
    rad = 1
    for i in xrange(h):
        for j in xrange(w):
            z = average_box(data, h, w, i, j, rad)
            if data[i][j] < z:  # If current pixel is an edge candidate.
                edge_data[i][j] = second_stage(data, h, w, i, j)
            else:
                edge_data[i][j] = 0

    return edge_data

def average_box(data, h, w, i, j, rad):
    '''In the data array, compute the average of all neighbors within
       rad of the center pixel (i,j). w and h are the width and height
       of the data. Include the center pixel in the average.
    '''
    sum = 0.0
    num = 0
    for r in range(i-rad,i+rad+1):
        for c in range(j-rad,j+rad+1):
            if valid_cell(r, c, h, w):
                sum += data[r][c]
                num += 1
    return (sum/num)

def valid_cell(r, c, h, w):
    '''Return true if (r,c) is defined within the data with height h
       and width w. Return false otherwise.
    '''
    if r < 0 or r > h-1:
        return False
    if c < 0 or c > w-1:
        return False
    return True  

def second_stage(data, h, w, i, j):
    '''The pixel (i,j) is an edge candidate within the data.
       Determine whether (i,j) is actually an edge pixel.
    '''
    # Define the 8 detection windows described in J. Wu et al. 2007.
    windows = [(0,1),(-1,0),(1,1),(-1,-1),(0,1),(0,-1),(-1,1),(1,-1)]
    grads = []  # Store the nonzero gradient values from each window.
    for window in windows:
        grads.append(compute_gradient(data, h, w, i, j, window[1], window[0]))
    return max(grads)


def compute_gradient(data, h, w, i, j, r, c):
    '''Compute the gradient of pixel (i,j) within the data set with width w
       and height h. Consider the the four pixels defined by r and c, that
       is, (i+r+r,j+c+c), (i+r,j+c), (i,j), and (i-r,j-c).
       Return the gradient value for pixel (i,j) if it is larger than the
       other two gradients described in J. Wu et al. 2007.
       Otherwise, return 0. 
    '''
    if valid_cell(i+r, j+c, h, w):
        pix_grad = data[i+r][j+c] - data[i][j]  # Gradient of pixel (i,j)
    else:
        return
    if valid_cell(i-r, j-c, h, w):
        grad1 = abs(data[i][j] - data[i-r][j-c])
    else:
        grad1 = 0
    if valid_cell(i+r+r, j+c+c, h, w):
        grad2 = abs(data[i+r+r][j+c+c] - data[i+r][j+c])
    else:
        grad2 = 0

    if (pix_grad > grad1) and (pix_grad > grad2):
        return pix_grad
    return 0
