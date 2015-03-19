'''

http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_transforms/py_fourier_transform/py_fourier_transform.html


http://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_Image_Fourier_Transform_FFT_DFT.php

'''

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('./fft_data/arc_D_skinny_2000x2000px_SNR=8.70_gblur=200x200_noise.png',0)

img = cv2.bilateralFilter(img,9,75,75)



f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))

plt.subplot(121),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()

rows, cols = img.shape
crow,ccol = rows/2 , cols/2
#cut = 30
#fshift[crow-cut:crow+cut, ccol-cut:ccol+cut] = 0
keep = 20
fshift[:crow-keep, :] = 0
fshift[crow+keep:, :] = 0
fshift[:, :ccol-keep] = 0
fshift[:, ccol+keep:] = 0
f_ishift = np.fft.ifftshift(fshift)
img_back = np.fft.ifft2(f_ishift)
img_back = np.abs(img_back)

plt.subplot(131),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(132),plt.imshow(img_back, cmap = 'gray')
plt.title('Image after LPF'), plt.xticks([]), plt.yticks([])
plt.subplot(133),plt.imshow(img_back)
plt.title('Result in JET'), plt.xticks([]), plt.yticks([])

plt.colorbar()
plt.show()
