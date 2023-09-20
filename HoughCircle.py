#coding: utf-8

import cv2
import numpy as np

# readImage
img = cv2.imread('ooo.png')

height, width = img.shape[:2]
pixels=[]
for y in range(height):
    row=[]
    for x in range(width):
        pixelValue = img.item(y, x, 0)
        if pixelValue>128:
            row.append(0)
        else:
            row.append(1)
        pass
    pixels.append(row)

print ("step 1 done")
hough=[]
for r in range(20,300):
    row=[]
    for y in range(height):
        col=[]
        for x in range(width):
            col.append(0)
        row.append(col)
    hough.append(row)

print ("step 2 done")

PI=3.1415926535
for r0 in range(20,100):
    r=r0-20
    print("r=%d"%(r0))
    for y in range(height):
        for x in range(width):
            if pixels[y][x]==1:
                circle=int(5*r0+5)
                for t in range(circle):
                    theta=2*PI*t/(5*r0)
                    yy=int(y+r0*np.sin(theta))
                    xx=int(x+r0*np.sin(theta))
                    if 0<=yy and yy<height and 0<=xx and xx<width:
                        hough[r][yy][xx] += 1
                        ##print ("(%d,%d,%d)%d"%(r,yy,xx,hough[r][yy][xx]), end=":")
                    if 0<=yy+1 and yy+1<height and 0<=xx and xx<width:
                        hough[r][yy+1][xx] += 1
                    if 0<=yy and yy<height and 0<=xx+1 and xx+1<width:
                        hough[r][yy][xx+1] += 1
                    if 0<=yy+1 and yy+1<height and 0<=xx+1 and xx+1<width:
                        hough[r][yy+1][xx+1] += 1
                
            pass
        pass
    pass

print ("step 2 done")



