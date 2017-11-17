'''
Created on Feb 11, 2017

@author: sagar
'''
from __future__ import division

import itertools
import sys

import cv2
from sympy import *
from sympy.geometry import *
from sympy.geometry.line import Line
from sympy.geometry.point import Point

import numpy as np


#===============================================================================
# def getline(p1, p2):
#     A = (p1[1] - p2[1])
#     B = (p2[0] - p1[0])
#     C = (p1[0]*p2[1] - p2[0]*p1[1])
#     return A, B, -C
# 
# def intersection(L1, L2):
#     D  = L1[0] * L2[1] - L1[1] * L2[0]
#     Dx = L1[2] * L2[1] - L1[1] * L2[2]
#     Dy = L1[0] * L2[2] - L1[2] * L2[0]
#     if D != 0:
#         x = Dx / D
#         y = Dy / D
#         return x,y
#     else:
#         return False
#===============================================================================
def get_VP(image_data):
    line_dict = {}
    count = 0
    threshold_dist = float(sys.argv[3].strip())
    for line in image_data:
        a = line.strip().split()
        a = map(float, a[0:4])
        l = Line(Point(a[0],a[1]),Point(a[2],a[3]))
        a.append(l)   
        line_dict['L'+str(count)] = a
        count+=1
    
    print 'lines in the image ::'
    print line_dict
    print
    print
    
    line_pairs = list(itertools.combinations(line_dict.keys(), 2))
    vp = [[]]
    result = {}
        
    for pair in line_pairs[0:50]:
        line1 = line_dict[pair[0]][4]
        line2 = line_dict[pair[1]][4]
        intersec = line1.intersection(line2)
        res = [pair[0]+'-'+pair[1]]
        if len(intersec):
            res.append(intersec[0])
            vp.append(res)
    vp = filter(None,vp)
    
    print 'Number of lines in the image ---->> ',len(line_dict)
    print
    print
    print 'Number of line pairs in the image ---->> ',len(line_pairs)
    print
    print
    print 'Number of intersection points in 1000 line pairs ---->> ',len(vp)
    print
    print
    
    skip_lines=[]
    
    for point in vp:
        inliers = []
        p = point[1]
        for key in line_dict.keys():
            try: 
                l = line_dict[key][4]
                if l.distance(p) <= threshold_dist and key not in skip_lines:
                    inliers.append(key)
                    skip_lines.append(key)
            except Exception:
                continue
        print 'Vanishing Point - ',point[0],p,':: inliers - ',inliers
        result[point[0]] = inliers
        
    #print result
    
    keys = sorted(result, key=lambda k: len(result[k]), reverse=True)[0:3]
    
    print
    print
    print 'Top 3 vanishing points are -----------'
    print
    
    count = 0
    for k in keys:
        img = cv2.imread(sys.argv[2].strip(),1)
        print k,[element for element in vp if element[0] == k][0][1],':: number of inliers - ',len(result[k])
        print 'inliers for this vanishing point are -'
        for i in result[k]:
            print i,'::Point1-',line_dict[i][0],line_dict[i][1],'::Point2-',line_dict[i][2],line_dict[i][3]
            cv2.line(img, (np.float32(line_dict[i][0]),np.float32(line_dict[i][1])), (np.float32(line_dict[i][2]),np.float32(line_dict[i][3])), (0,0,255),2)
        cv2.imwrite(str(count)+sys.argv[2].strip(),img)
        count+=1
        #cv2.imshow('1.jpg',img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        print
    
    #cv2.line(img, (50,50), (300,300), (0,0,255),4)
    
    
        
        
    
    #===========================================================================
    #     #line1 = getline(line1[0:2], line1[2:4])
    #     #line2 = getline(line2[0:2], line2[2:4])           
    #     point = intersection(line1, line2)
    #     res = [pair[0],pair[1]]
    #     if point:
    #         res.append(point[0])
    #         res.append(point[1])
    #     else:
    #         res.append('inf')
    #         res.append('inf')
    #     vp.append(res)
    # vp = filter(None,vp)
    # print vp
    #===========================================================================

if __name__ == '__main__':
    image = open(sys.argv[1].strip(), 'r').readlines()
    get_VP(image)
