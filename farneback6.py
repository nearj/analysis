import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
import math
import os

#####################################################################

camera_to_use   = 0;                  ## TO-DO: DEPRECATED
keep_processing = True;               # keep processing, but?
frameNum        = 0;                  # TO-DO: ??
number          = 1;                  # TODO: Local variable Delete
sumCount        = 0;                  # TODO: Local variable
frame_max       = [];                 # TODO:
pi              = [];                 # optical flow distribution
count           = np.zeros([12,5]);   #
temp_count      = np.zeros([12,5]);
prob            = np.zeros([12,5]);
R               = len(temp_count);    # row?
C               = len(temp_count[0]); # column?
temp_ent        = 0;                  # temporary entropy
entropy         = [];                 # placeholder for entropy?

#####################################################################

def check_rotation(magnitude, section):
    if(magnitude<1):
        temp_count[section][0] += 1
    elif(magnitude >=1 and magnitude<6):
        temp_count[section][1] += 1
    elif(magnitude >=6 and magnitude<20):
        temp_count[section][2] += 1
    elif(magnitude >=20 and magnitude<50):
        temp_count[section][3] += 1
    elif(magnitude >=50):
        temp_count[section][4] += 1

def check_count():
    maxcount = 0;

    for x in range(0,R):
        for y in range(0,C):
            if(maxcount < temp_count[x][y]):
                maxcount = temp_count[x][y];
                row = x;
                col = y;

    return maxcount, row, col;

def Init_Count():
    temp_count[:][:] = 0;

def Copy_Count():
    for x in range(0,R):
        for y in range(0,C):
            count[x][y] += temp_count[x][y];

def Cal_Prob():
    R = len(count);
    C = len(count[0]);
    sum = 0;
    for i in range(0,R) :
        for j in range(0,C) :
            sum += count[i][j].astype(int);

    for x in range(0,R) :
        for y in range(0,C) :
            prob[x][y] = count[x][y]/sum;

    return sum;

#####################################################################
cap = cv2.VideoCapture("S4.mp4")
frame_max = cap.get(cv2.CAP_PRO
    while (keep_processing):
        if (cap.isOpened):
            ret, frame = cap.read();
        if (ret == 0):
            keep_processing = False;
            continue;
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        prevgray = gray

        if(frameNum == 0 or frameNum == 10 or frameNum == 20):
            H, W = frame.shape[:2]
            assert(flow.shape == (H, W, 2))
            assert(flow.dtype == np.float32)
            magnitude, ang = cv2.cartToPolar(flow[...,0], flow[...,1],None,None,True)
            r = magnitude.reshape(-1)
            theta = ang.reshape(-1)
            length = len(r)

            for index in range(0, length) :
                if (theta[index] >= 0 and theta[index] < 15 or theta[index] > 345 and theta[index] <= 360) :
                    check_rotation(r[index], 0)
                elif(theta[index] >= 15 and theta[index] < 45) :
                    check_rotation(r[index], 1)
                elif(theta[index] >= 45 and theta[index] < 75) :
                    check_rotation(r[index], 2)
                elif(theta[index] >= 75 and theta[index] < 105) :
                    check_rotation(r[index], 3)
                elif(theta[index] >= 105 and theta[index] < 135) :
                    check_rotation(r[index], 4)
                elif(theta[index] >= 135 and theta[index] < 165) :
                    check_rotation(r[index], 5)
                elif(theta[index] >= 165 and theta[index] < 195) :
                    check_rotation(r[index], 6)
                elif(theta[index] >= 195 and theta[index] < 225) :
                    check_rotation(r[index], 7)
                elif(theta[index] >= 225 and theta[index] < 255) :
                    check_rotation(r[index], 8)
                elif(theta[index] >= 255 and theta[index] < 285) :
                    check_rotation(r[index], 9)
                elif(theta[index] >= 285 and theta[index] < 315) :
                    check_rotation(r[index], 10)
                elif(theta[index] >= 315 and theta[index] <= 345) :
                    check_rotation(r[index], 11)

            max, row, col = check_count();
            sumCount = Copy_Count();
            frame_max.append(max);
            frame_max.append(row);
            frame_max.append(col);
            Init_Count();
        if(frameNum <30) :
            frameNum = frameNum +1;
        elif(frameNum == 30) :
            frameNum = 0;
        if (key == 27):
            keep_processing = False;

    Cal_Prob();
    line = file2.readline();
    platformQ = line.split(" ");
    for i in range(0, int(len(frame_max)/3)):
        r = frame_max[3*i+1];
        c = frame_max[3*i+2];
        if (i < int(len(platformQ))):
            if(prob[r][c] != 0 and platformQ[i] and platformQ[i] != ' '):
                if(platformQ[i] == '0'):
                    platformQ[i] = '0.0001';
                pdivq = prob[r][c];#/float(platformQ[i]);
                pi.append(prob[r][c]);
                temp_ent = ((-1) * prob[r][c] * math.log(pdivq));
            string = "%i - "%i + "Probability : %f, "%prob[r][c] + "CountingSum : %i, "%frame_max[3*i] + "Section : %i,"%r + "%i\n"%c;
            entropy.append(temp_ent);

#####################################################################
