'''
Created on Feb 12, 2017

@author: sagar
'''

import os
import sys
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt


def drawMatches(img1, kp1, img2, kp2, matches):
   
    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


    return out

    
img1 = cv2.imread(sys.argv[1].strip(),0)  #queryimage # left image
img2 = cv2.imread(sys.argv[2].strip(),0) #trainimage # right image

detector = cv2.FeatureDetector_create("SIFT")    # SURF, FAST, SIFT
descriptor = cv2.DescriptorExtractor_create("SIFT") # SURF, SIFT

kp1 = detector.detect(img1)
kp2 = detector.detect(img2) 

k1, des1 = descriptor.compute(img1,kp1)
k2, des2 = descriptor.compute(img2,kp2)

# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.match(des1,des2)

#matches = bf.knnMatch(des1,des2, k=2)


matches = sorted(matches, key = lambda x:x.distance)

img3 = drawMatches(img1,kp1,img2,kp2,matches[:200])

plt.imshow(img3)
plt.show()

 
#===============================================================================
# good = []
#  
# # Apply ratio test
# for m,n in matches:
#     if m.distance < 0.7*n.distance:
#             good.append(m)
#  
# MIN_MATCH_COUNT = 10
# if len(good)>MIN_MATCH_COUNT:
#===============================================================================
src_pts = np.float32([ kp1[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
dst_pts = np.float32([ kp2[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)
F, mask = cv2.findFundamentalMat(src_pts, dst_pts, cv2.RANSAC, 5.0)
matchesMask = mask.ravel().tolist()
print F
#===============================================================================
# else:
#     print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
#     matchesMask = None
#  
# print F    
#===============================================================================
