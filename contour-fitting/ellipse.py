import cv2
import numpy as np

#img = cv2.imread('./test-data/noise_blur_full_ellipse_small.png',0)
img = cv2.imread('./test-data/ellipse.png',0)
ret,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,\
    cv2.CHAIN_APPROX_NONE) 
#contours,hierarchy = cv2.findContours(thresh, 1, 2)
#img = cv2.imread('noise_blur_full_ellipse_small.png',0)

print len(contours)
print type(contours)
print type(contours[0])

cnt = contours[0]
print

print 'len'
print len(cnt)
print type(cnt)

print    
print 'shape'
print cnt.shape
print cnt.size
print cnt.dtype.name
print cnt.dtype

print
print 'cnt'
print cnt
ellipse = cv2.fitEllipse(cnt)

(x,y),radius = cv2.minEnclosingCircle(cnt)
center = (int(x),int(y))
radius = int(radius)
cv2.circle(img,center,radius,(0,255,0),2)
#cv2.drawContours(img, contours, -1, (0,255,0), 2)
#cv2.ellipse(img,ellipse,(0,255,0),2)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()    

#M = cv2.moments(cnt)
#print M

