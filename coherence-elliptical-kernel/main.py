'''

Author: S.T. Castle
Created: 2015-03-15
'''

#import math
import numpy as np
from scipy import ndimage
from scipy import stats
import scipy.ndimage.filters
import scipy.linalg
#import skimage.feature
import cv2

from matplotlib import pyplot as plt

def main():
    '''
    Run the explicit coherence enhancing filter with spatial adaptive
    elliptical kernel from F.Li et al. 2012.
    '''
    # Params.
    window_size = 7
    sigma = 1  # Standard deviation of initial Gaussian kernel.
    rho = 6  # Std dev of Gaussian kernel used to compute structure tensor.
    gamma = 0.05
    eps = np.spacing(1)  # Very small positive number.

    filename = 'fingerprint1.png'
    # Open as grayscale image.
    orig_img = cv2.imread(filename, 0)
    print 'Opened ' + filename

    #plt.subplot(111),plt.imshow(img, cmap = 'gray')
    #plt.title('Input image'), plt.xticks([]), plt.yticks([])
    #plt.show()



    # Convolve image with a Gaussian kernel with standard deviation sigma.
    img = scipy.ndimage.filters.gaussian_filter(orig_img, sigma)

    #plt.subplot(111),plt.imshow(img, cmap = 'gray')
    #plt.title('Input image'), plt.xticks([]), plt.yticks([])
    #plt.show()



    print 'shape of img:',
    print img.shape

    # Compute the 2D structure tensor of the image.
    # The structure tensor is:
    # [j11 j12]
    # [j12 j22]
    #j11, j12, j22 = skimage.feature.structure_tensor(img, sigma=sigma)
    j11, j12, j22 = structure_tensor(img, sigma=sigma)

    #print 'j11'
    #print j11
    #print 'j12'
    #print j12
    #print 'j22'
    #print j22
    print 'shape of j11:',
    print j11.shape
    print 'shape of J:',
    print np.array([[j11,j12],[j12,j22]]).shape

    # Compute eigenvalues mu1, mu2 of structure tensor. mu1 >= mu2.
    mu1 = (j11 + j22) / 2 + np.sqrt(4 * j12 ** 2 + (j11 - j22) ** 2) / 2
    mu2 = (j11 + j22) / 2 - np.sqrt(4 * j12 ** 2 + (j11 - j22) ** 2) / 2

    print 'shape of mu1:',
    print mu1.shape

    # Compute corresponding normalized eigenvectors v1, v2.
    v1 = np.asarray([ 2*j12,
                      j22-j11 + np.sqrt((j11-j22)**2 + 4*(j12**2)) ])
    # Rearrange axis so that v1 is indexed as (x,y,(eigvector))
    v1 = np.rollaxis(v1,0,3)

    #print 'mu1'
    #print mu1
    #print 'mu2'
    #print mu2
    #print 'v1'
    #print v1
    #print 'v2'
    #print v2
    print 'shape of v1:',
    print v1.shape
    #print 'v1[0] =',
    #print v1[0]
    #print 'v1[0][0] =',
    #print v1[0][0]

    #print v1
    
   
    # Compute theta based on the angle of v1 and the positive direction of
    # the horizontal axis.
    # cos(theta) = x / magnitude.
    # If the magnitude is 0, then just try setting theta=0 for now.
    print 'Calculating theta...'
    theta = np.empty((v1.shape[0], v1.shape[1]))
    for i in xrange(v1.shape[0]):
        for j in xrange(v1.shape[1]):
            v = v1[i][j]
            mag = float(magnitude(v))
            if mag:
                theta[i][j] = np.arccos(v[0]/magnitude(v))
            else:
                theta[i][j] = 0
    print 'Done.'
    print 'shape of theta:',
    print theta.shape

    # Now that necessary values are calculated, proceed to filtering.
    print 'Filtering...'
    fimg = np.empty_like(img)  # Create a blank array for the filtered image.
    rad = window_size/2  # Radius of the filtering window.
    sig1 = 10*gamma
    # Current pixel is (x1,x2) and neighbor is (y1,y2).
    height = img.shape[0]
    width = img.shape[1]
    for x1 in xrange(height):
        for x2 in xrange(width):
            eig1 = mu1[x1][x2]
            eig2 = mu2[x1][x2]
            ang = theta[x1][x2]
            sig2 = 10*(gamma+(1-gamma)*np.exp(-1/((eig1-eig2)**2+eps)))
            wt_const = 1/(2*np.pi*sig1*sig2)  # Constant factor for weighting.
            # Add weighted value from neighbor pixel y.
            sum = 0
            wt_sum = 0  # Sum of the weights for normalization scaling.
            for i in xrange(-rad,rad+1):
                y1 = x1+i
                if (y1 < 0) or (y1 >= height):
                    continue
                for j in xrange(-rad,rad+1):
                    y2 = x2+i
                    if (y2 < 0) or (y2 >= width):
                        continue
                    # Calculate weight of neighboring position y.
                    s = (y1-x1)*np.cos(ang) + (y2-x2)*np.sin(ang)
                    t = -(y1-x1)*np.sin(ang) + (y2-x2)*np.cos(ang)
                    wt = wt_const * np.exp( -s**2/(2*sig1**2) - t**2/(2*sig2**2) )
                    sum = sum + wt*orig_img[y1][y2]  # Use original image or blurred? 
                    wt_sum = wt_sum + wt
            # Set value of this pixel x.
            #sum = sum * (1.0/wt_sum)  # Scale the pixel value.
            fimg[x1][x2] = sum
        print x1
    print 'Done.'


    # Display original and filtered images.
    plt.subplot(121),plt.imshow(img, cmap = 'gray')
    plt.title('Input image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(fimg, cmap = 'gray')
    plt.title('Filtered Image'), plt.xticks([]), plt.yticks([])
    plt.show()


def magnitude(v):
    """Magnitude of a vector."""
    return np.sqrt(np.dot(v, v))

# from skimage !!!!
def _compute_derivatives(image, mode='constant', cval=0):
    """Compute derivatives in x and y direction using the Sobel operator.

    Parameters
    ----------
    image : ndarray
        Input image.
    mode : {'constant', 'reflect', 'wrap', 'nearest', 'mirror'}, optional
        How to handle values outside the image borders.
    cval : float, optional
        Used in conjunction with mode 'constant', the value outside
        the image boundaries.

    Returns
    -------
    imx : ndarray
        Derivative in x-direction.
    imy : ndarray
        Derivative in y-direction.

    """

    imy = ndimage.sobel(image, axis=0, mode=mode, cval=cval)
    imx = ndimage.sobel(image, axis=1, mode=mode, cval=cval)

    return imx, imy

def structure_tensor(image, sigma=1, mode='constant', cval=0):
    """Compute structure tensor using sum of squared differences.

    The structure tensor A is defined as::

        A = [Axx Axy]
            [Axy Ayy]

    which is approximated by the weighted sum of squared differences in a local
    window around each pixel in the image.

    Parameters
    ----------
    image : ndarray
        Input image.
    sigma : float
        Standard deviation used for the Gaussian kernel, which is used as a
        weighting function for the local summation of squared differences.
    mode : {'constant', 'reflect', 'wrap', 'nearest', 'mirror'}, optional
        How to handle values outside the image borders.
    cval : float, optional
        Used in conjunction with mode 'constant', the value outside
        the image boundaries.

    Returns
    -------
    Axx : ndarray
        Element of the structure tensor for each pixel in the input image.
    Axy : ndarray
        Element of the structure tensor for each pixel in the input image.
    Ayy : ndarray
        Element of the structure tensor for each pixel in the input image.

    Examples
    --------
    >>> from skimage.feature import structure_tensor
    >>> square = np.zeros((5, 5))
    >>> square[2, 2] = 1
    >>> Axx, Axy, Ayy = structure_tensor(square, sigma=0.1)
    >>> Axx
    array([[ 0.,  0.,  0.,  0.,  0.],
           [ 0.,  1.,  0.,  1.,  0.],
           [ 0.,  4.,  0.,  4.,  0.],
           [ 0.,  1.,  0.,  1.,  0.],
           [ 0.,  0.,  0.,  0.,  0.]])

    """

    #image = _prepare_grayscale_input_2D(image)

    imx, imy = _compute_derivatives(image, mode=mode, cval=cval)

    # structure tensore
    Axx = ndimage.gaussian_filter(imx * imx, sigma, mode=mode, cval=cval)
    Axy = ndimage.gaussian_filter(imx * imy, sigma, mode=mode, cval=cval)
    Ayy = ndimage.gaussian_filter(imy * imy, sigma, mode=mode, cval=cval)

    return Axx, Axy, Ayy


if __name__ == '__main__':
    main()

