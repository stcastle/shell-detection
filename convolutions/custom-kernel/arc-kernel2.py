import fileinput
import numpy as np
import scipy

import cv2
import os.path
from math import pi, sqrt, exp

def main():
    for file in fileinput.input():
        # Get filename.
        filename = fileinput.filename()

        # Open current file as a grayscale image.
        img = cv2.imread(filename, 0)
        print 'Opened ' + filename

        # Split filename into prefix and extension.
        (name_pref, name_ext) = os.path.splitext(filename)

        # Build custom kernel.
        vals = gauss(5,1)
        #print np.sum(vals)
        #vals = [x*6.1 for x in vals]
        # There will by 11*11 - 5*11 = 66 spaces not covered by the kernel.
        # Want overall kernel to be normalized.
        # So the 11 occurences of vals must give an overall sum of 1.
        # Want:  -66 + 11*np.sum(vals) = 1
        # np.sum(vals) should equal (1+66)/11.0.
        scale_val = (1+66)/11.0/np.sum(vals)
        vals = [scale_val*x for x in vals]
        #print np.sum(vals)
        #print vals
        kernel_mtx = [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,vals[0],vals[0],vals[0],-1,-1,-1,-1],
            [-1,-1,vals[0],vals[0],vals[1],vals[1],vals[1],vals[0],vals[0],-1,-1],
            [vals[0],vals[0],vals[1],vals[1],vals[2],vals[2],vals[2],vals[1],vals[1],vals[0],vals[0]],
            [vals[1],vals[1],vals[2],vals[2],vals[1],vals[1],vals[1],vals[2],vals[2],vals[1],vals[1]],
            [vals[2],vals[2],vals[1],vals[1],vals[0],vals[0],vals[0],vals[1],vals[1],vals[2],vals[2]],
            [vals[1],vals[1],vals[0],vals[0],-1,-1,-1,vals[0],vals[0],vals[1],vals[1]],
            [vals[0],vals[0],-1,-1,-1,-1,-1,-1,-1,vals[0],vals[0]],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
            ]

        kernel = np.asarray(kernel_mtx)
        #print kernel

        #print np.sum(kernel)

        # Convolve image with kernel.
        img = cv2.filter2D(img, -1, kernel)

        # Write image to file.
        newname = name_pref + '_arcfilter2' + name_ext
        cv2.imwrite(newname, img)

        fileinput.nextfile()

    fileinput.close()


def gauss(n=11,sigma=1):
    r = range(-int(n/2),int(n/2)+1)
    return [1 / (sigma * sqrt(2*pi))*exp(-float(x)**2/(2*sigma**2)) for x in r]

if __name__ == '__main__':
    main()
