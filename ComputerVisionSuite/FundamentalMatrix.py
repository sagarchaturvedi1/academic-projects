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
   
    
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    for mat in matches:

        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

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
#matches = bf.match(des1,des2)

matches = bf.knnMatch(des1,des2, k=2)

a_list = []
# Apply ratio test
for m,n in matches:
    a_list.append(m)

matches = sorted(a_list, key = lambda x:x.distance)

img3 = drawMatches(img1,kp1,img2,kp2,matches[:200])

plt.imshow(img3)
plt.show()

src_pts = np.float32([ kp1[m.queryIdx].pt for m in a_list ]).reshape(-1,1,2)
dst_pts = np.float32([ kp2[m.trainIdx].pt for m in a_list ]).reshape(-1,1,2)
F, mask = cv2.findFundamentalMat(src_pts, dst_pts, cv2.RANSAC, 5.0)

print F
 
