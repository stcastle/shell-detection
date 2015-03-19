'''testing...'''

import numpy as np
import cv2
import noise

def make_image():
    image = np.zeros((300,300), np.uint8)

    print 'Made array'
    print 'Displaying image...'

    cv2.namedWindow('image')

    # Create trackbars for changing the grayscale.
    print cv2.createTrackbar('color','image',0,255,nothing)

    # Create switch for ON/OFF noise.
    switch = '0 : No noise \n1 : Apply noise'
    cv2.createTrackbar(switch, 'image',0,1,nothing)

    while(1):
        cv2.imshow('image',image)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # Esc
            break

        # Get current positions of trackbars
        val = cv2.getTrackbarPos('color','image')
        s = cv2.getTrackbarPos(switch,'image')

        # Set image to specified value
        image[:] = val

        # Add noise if switch is on.
        if s:
            image = noise.poisson_noise(image)

    cv2.destroyAllWindows()

# Empty function to call for trackbar.
def nothing(x):
    pass

if __name__ == '__main__':
    make_image()
