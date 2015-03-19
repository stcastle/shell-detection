import numpy as np
import cv2
import os.path

def smooth(name, orig_img):
    '''
    name: original filename of the image
    orig_img: The image to be processed.
    '''
    img = np.ndarray.copy(orig_img)    # Copy of original for smoothing.

    # Split filename and extension.
    spl = os.path.splitext(name)
    name_pref = spl[0]  # Name prefix.

    # Apply a smoothing filter.
    # Bilateral blur.
    img = cv2.bilateralFilter(orig_img,9,75,75)
    name_bilat = name_pref + '_smooth=bilat' + spl[1]
    cv2.imwrite(name_bilat, img)

    # Apply a smoothing filter.
    # Median blur.
    img = cv2.medianBlur(orig_img,5)
    name_median = name_pref + '_smooth=median' + spl[1]
    cv2.imwrite(name_median, img)

    # Apply a smoothing filter.
    # Gaussian blur.
    img = cv2.GaussianBlur(orig_img,(25,25),0)
    name_gauss = name_pref + '_smooth=gauss' + spl[1]
    cv2.imwrite(name_gauss, img)

    # Apply a smoothing filter.
    # Laplacian.
    img = cv2.Laplacian(orig_img,cv2.CV_64F)
    name_laplace = name_pref + '_laplace' + spl[1]
    cv2.imwrite(name_laplace, img)

    # Apply a smoothing filter.
    # Sobel
    img = cv2.Sobel(orig_img,cv2.CV_64F,1,0,ksize=9)  # sobel x
    name_sobelx = name_pref + '_sobelx' + spl[1]
    cv2.imwrite(name_sobelx, img)
