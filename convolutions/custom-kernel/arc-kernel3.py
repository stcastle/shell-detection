import fileinput
import numpy as np
import scipy

import cv2
import os.path

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
        kernel_mtx = [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,10,11,10,-1,-1,-1,-1],
            [-1,-1,10,10,-1,-1,-1,10,10,-1,-1],
            [10,10,-1,-1,-1,-1,-1,-1,-1,10,10],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
            ]

        kernel = np.asarray(kernel_mtx)

        # Convolve image with kernel.
        img = cv2.filter2D(img, -1, kernel)

        # Write image to file.
        newname = name_pref + '_arcfilter3' + name_ext
        cv2.imwrite(newname, img)

        fileinput.nextfile()

    fileinput.close()

if __name__ == '__main__':
    main()
