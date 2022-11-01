from importlib import import_module
import math
import handtracker
import cv2 as cv
import mediapipe as mp
from subprocess import call
import time




wCam , hCam = 1500 , 1000

cap = cv.VideoCapture(0)



detector = handtracker.HandsDetector(MaxHands=1)


pTime = 0
mag = 0
fixed_mag = 1

OldMin = 80
OldMax = 93
NewMin = 0
NewMax = 100

while True:
    scs , img = cap.read()
    img = cv.resize(img , (1000,800))
    h , w , c = img.shape

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    
    detector.FindHands(img)
    mylist = detector.FindPosition(img , draw= False)
    if len(mylist) != 0:
        
        x1 , y1 = int(mylist[8][1] * w) , int(mylist[8][2] * h)
        x2 , y2 = int(mylist[4][1] * w) , int(mylist[4][2] * h)
        mag = (math.sqrt((mylist[8][1] - mylist[4][1]) ** 2) + (mylist[8][2] - mylist[4][1]) ** 2)
        fixed_mag =  (math.sqrt((mylist[8][1] - mylist[7][1]) ** 2) + (mylist[8][2] - mylist[7][1]) ** 2)
        cv.circle(img , (x1,y1) , 15 , (255,0,255) , cv.FILLED)
        cv.circle(img , (x2,y2) , 15 , (255,0,255) , cv.FILLED)
        OldRange = (OldMax - OldMin)  
        NewRange = (NewMax - NewMin)  
        NewValue = (((mag**fixed_mag * 100 - OldMin) * NewRange) / OldRange) + NewMin
        cv.putText(img , str(round((NewValue))) , (300 , 90) ,  cv.FONT_HERSHEY_PLAIN,3,(255,0,255) , 3)
        if round((NewValue)) > 100: v = 100
        elif round((NewValue)) < 0: v =0
        else: v = round((NewValue))
        cv.line(img , (x1 , y1) , (x2 , y2) , (255 - v * 2 , 0 , v) , 4)

        call((["amixer", "-D", "pulse", "sset", "Master", str(v)+"%"]))
        
        

    cv.putText(img , str(int(fps)) , (10 , 70) ,  cv.FONT_HERSHEY_PLAIN,3,(255,0,255) , 3)
    cv.imshow('s' , img)
    
    
    cv.waitKey(1)
