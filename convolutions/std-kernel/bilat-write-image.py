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

        # Bilateral smoothing filter.
        img = cv2.bilateralFilter(img,9,75,75)

        # Write image to file.
        newname = name_pref + '_smooth=bilat' + name_ext
        cv2.imwrite(newname, img)

        fileinput.nextfile()

    fileinput.close()

if __name__ == '__main__':
    main()
