#coding: utf-8

import cv2
import numpy as np
import statistics

filename = "ooo.png"

def cvHough(img0):

    height, width = img0.shape[:2]
    print("(%d,%d)"%(height, width))
    img = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    th, img = cv2.threshold(img, 196, 255, cv2.THRESH_BINARY)#THRESH_OTSU for gray ##THRESH_BINARY
    ## BACKGROUND:255, FOREGROUND:0
    ##img = cv2.bitwise_not(img)
    globalAnswer=[]
    for r2r in range(40):
        r2=60-r2r
        circles = cv2.HoughCircles(
            img, 
            cv2.HOUGH_GRADIENT, 
            dp=1.0, ##値が大きいほど検出基準が緩くなり、値が小さいほど検出基準が厳しくなります。##0.8 ~ 1.2 くらいの幅で調整する
            minDist=50, 
            param1=100, ###  Canny法のHysteresis処理の閾値 ## 100前後を固定
            param2=r2, ### 円の中心を検出する際の閾値 ## 30だと小さい
            minRadius=20, 
            maxRadius=min(height, width))
        localAnswer=[]
        if isinstance(circles,np.ndarray):
            for circle in circles[0, :]:
                cx, cy, cr=circle[0], circle[1], circle[2]
                count=0
                for t in range(60):
                    check=False
                    for s in range(21):
                        dx=int(cx+(cr+s-10)*np.cos(2*t*np.pi/60))
                        dy=int(cy+(cr+s-10)*np.sin(2*t*np.pi/60))
                        if 0<=dx and dx<width and 0<=dy and dy<height:
                            if img.item(dy, dx)<200:
                                check=True
                                break
                    if check:
                        count += 1 
                if count>50:
                    localAnswer.append([cx,cy,cr,count])
            globalAnswer.append(localAnswer)
    answerSizes=[len(answer) for answer in globalAnswer] 
    bestAnswerSize = statistics.mode(answerSizes)
    bestAnswers = [answer for answer in globalAnswer if len(answer)==bestAnswerSize]
    bestAnswer=bestAnswers[int(len(bestAnswers)/2)]
    # 円周を描画する
    for cc in bestAnswer:
        cv2.circle(img0, center=(int(cc[0]), int(cc[1])), radius=int(cc[2]), color=(0, 165, 255), thickness=2)
        print("(%f,%f),%f"%(cc[0], cc[1], cc[2]))
    cv2.imshow("img",img0)
    k = cv2.waitKey(0)
    pass

def scratchHough(img):
    height, width = img.shape[:2]
    print("(%d,%d)"%(height, width))
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
    for y in range(height):
        col=[]
        for x in range(width):
            col.append(0)
        hough.append(col)

    print ("step 2 done")

    answer=[]

    PI=3.1415926535
    for r0 in range(20,200):
        r=r0-20
        if r0%2==1:
            continue
        print("r=%d"%(r0),end=":")
        for y in range(height):
            for x in range(width):
                hough[y][x]=0
        for y in range(height):
            for x in range(width):
                if pixels[y][x]==1:
                    circle=int(2*r0+2)
                    for t in range(circle):
                        theta=2*PI*t/(2*r0)
                        yy=int(y+r0*np.sin(theta))
                        xx=int(x+r0*np.cos(theta))
                        if 0<=yy and yy<height and 0<=xx and xx<width:
                            hough[yy][xx] += 1
                            ##print ("(%d,%d,%d)%d"%(r,yy,xx,hough[r][yy][xx]), end=":")
                        if 0<=yy+1 and yy+1<height and 0<=xx and xx<width:
                            hough[yy+1][xx] += 1
                        if 0<=yy and yy<height and 0<=xx+1 and xx+1<width:
                            hough[yy][xx+1] += 1
                        if 0<=yy+1 and yy+1<height and 0<=xx+1 and xx+1<width:
                            hough[yy+1][xx+1] += 1
                
                pass
            pass
        pass
        for y in range(height):
            for x in range(width):
                if hough[y][x]>0:
                    if len(answer)==0:
                        answer.append({'x':x, 'y':y, 'r':r0, 'hough':hough[y][x]})
                    elif len(answer)<100 and hough[y][x]<=answer[-1]['hough']:
                        answer.append({'x':x, 'y':y, 'r':r0, 'hough':hough[y][x]})
                    elif hough[y][x]>answer[-1]['hough']:
                        lenans=len(answer)## mayby this is 30
                        top=True
                        for i in range(1,lenans):
                            j=lenans-1-i
                            if answer[j]['hough']>hough[y][x]:
                                answer.insert(j+1, {'x':x, 'y':y, 'r':r0, 'hough':hough[y][x]})
                                del answer[-1]
                                top=False
                                break;
                        if top:
                            answer.insert(0, {'x':x, 'y':y, 'r':r0, 'hough':hough[y][x]})
                            del answer[-1]
        print(",%d,%d,%0.3f"%(r0,answer[0]['r'],answer[0]['hough']/r0))
    print ("step 2 done")

# readImage
img = cv2.imread(filename)
#scratchHough(img)
cvHough(img)

