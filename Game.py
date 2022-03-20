import math
import random
import time
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone


cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
counter=0
score=0
startTime=time.time()
totalTime=20

detector=HandDetector(detectionCon=0.8,maxHands=1)
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)
color=(255,0,255)
cx,cy=250,250

while True:
    timeLeft = totalTime - (time.time() - startTime)
    success,img=cap.read()
    img=cv2.flip(img,1)
    if time.time()-startTime<totalTime:
        hands= detector.findHands(img,draw=False)

        # manually
        if hands:
            lmlist=hands[0]['lmList']
            x,y,w,h=hands[0]['bbox']
            x1,y1=lmlist[5]
            x2,y2=lmlist[17]
            distance=math.sqrt(pow(x2-x1,2)+pow(y2-y1,2))
            distanceCM=coff[0]*distance**2+coff[1]*distance+coff[2]
            if distanceCM<40:
                if x<cx<x+w and y<cy<y+h:
                    counter=1
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
            #print(distanceCM,distance)
            cvzone.putTextRect(img, f'{int(distanceCM)} cm',(x+5,y-10))
        if counter:
            counter+=1
            color = (0, 255, 0)
            if counter==3:
                cx=random.randint(100,1100)
                cy=random.randint(100,600)
                color = (255, 0, 255)
                score+=1
                counter=0

           #Draw button
        cv2.circle(img, (cx,cy),  30, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255,255,255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (255,255,255), 2)
        cv2.circle(img, (cx, cy), 30, (50,50,50), 2)

        cvzone.putTextRect(img,f'Time: {int(timeLeft)}',(1000,75),scale=3,offset=20)
        cvzone.putTextRect(img,f'Score: {str(score).zfill(2)}', (60, 75), scale=3, offset=20)
    else:
        cvzone.putTextRect(img,'Game over!',(400,400),5,7,offset=30)
        cvzone.putTextRect(img, f'Your score is: {str(score)}', (435, 500), 3,  offset=20)
        cvzone.putTextRect(img, f'Press R to restart', (450, 575), 2, offset=10)
    cv2.imshow("Image", img)
    key=cv2.waitKey(1)
    if key==ord('r'):
        startTime=time.time()
        score=0
