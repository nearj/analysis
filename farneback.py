#####################################################################

# Example : perform live visualization of optic flow from a video file
# specified on the command line (e.g. python FILE.py video_file) or from
# an attached web camera

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2017 School of Engineering & Computing Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
import math

#####################################################################

keep_processing = True;
camera_to_use = 0; # 0 if you have one camera, 1 or > 1 otherwise
frameNum = 0;
number = 1;
sumCount = 0;
frame_max = [];
pi=[];
count = np.zeros([12,5]);
temp_count = np.zeros([12,5]);
prob = np.zeros([12,5]);
R = len(temp_count);
C = len(temp_count[0]);
temp_ent = 0;
entropy = [];

#####################################################################

# draw optic flow visualization on image using a given step size for
# the line glyphs that show the flow vectors on the image

def draw_flow(img, flow, step=8):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    #cv2.polylines(vis, lines, 0, (0, 255, 0))
    #for (x1, y1), (x2, y2) in lines:
    #    cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis

def check_r(mag, section):
    if(mag<1):
        temp_count[section][0] += 1
    elif(mag >=1 and mag<6):
        temp_count[section][1] += 1
    elif(mag >=6 and mag<20):
        temp_count[section][2] += 1
    elif(mag >=20 and mag<50):
        temp_count[section][3] += 1
    elif(mag >=50):
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

# define video capture object

cap = cv2.VideoCapture();

# define display window name

windowName = "Dense Optic Flow"; # window name

file = open('S4.txt', 'w');
file2 = open('S4q.txt', 'r');
file3 = open('S4-Entropy.txt', 'w');
file4 = open('S4-P.txt', 'w');
file5 = open('S4-Q.txt', 'w');

# if command line arguments are provided try to read video_name
# otherwise default to capture from attached H/W camera

if (((len(sys.argv) == 2) and (cap.open(str(sys.argv[1]))))
    or (cap.open(camera_to_use))):

    # create window by name (as resizable)

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL);

    # if video file successfully open then read an initial frame from video

    if (cap.isOpened):
        ret, frame = cap.read();

    # convert image to grayscale to be previous frame

    prevgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    while (keep_processing):
        # if video file successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read();

            # when we reach the end of the video (file) exit cleanly

            if (ret == 0):
                keep_processing = False;
                continue;

        # convert image to grayscale

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # compute dense optic flow using technique of Farneback 2003
        # parameters from example (OpenCV 3.2):
        # https://github.com/opencv/opencv/blob/master/samples/python/opt_flow.py

        flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, cv2.OPTFLOW_USE_INITIAL_FLOW)
        prevgray = gray

		# calculate Entropy
        if(frameNum == 0 or frameNum == 10 or frameNum == 20):
            H, W = frame.shape[:2]
            assert(flow.shape == (H, W, 2))
            assert(flow.dtype == np.float32)
            mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1],None,None,True)
            r = mag.reshape(-1)
            theta = ang.reshape(-1)
            length = len(r)

            for index in range(0, length) :
                if (theta[index] >= 0 and theta[index] < 15 or theta[index] > 345 and theta[index] <= 360) :
                    check_r(r[index], 0)
                elif(theta[index] >= 15 and theta[index] < 45) :
                    check_r(r[index], 1)
                elif(theta[index] >= 45 and theta[index] < 75) :
                    check_r(r[index], 2)
                elif(theta[index] >= 75 and theta[index] < 105) :
                    check_r(r[index], 3)
                elif(theta[index] >= 105 and theta[index] < 135) :
                    check_r(r[index], 4)
                elif(theta[index] >= 135 and theta[index] < 165) :
                    check_r(r[index], 5)
                elif(theta[index] >= 165 and theta[index] < 195) :
                    check_r(r[index], 6)
                elif(theta[index] >= 195 and theta[index] < 225) :
                    check_r(r[index], 7)
                elif(theta[index] >= 225 and theta[index] < 255) :
                    check_r(r[index], 8)
                elif(theta[index] >= 255 and theta[index] < 285) :
                    check_r(r[index], 9)
                elif(theta[index] >= 285 and theta[index] < 315) :
                    check_r(r[index], 10)
                elif(theta[index] >= 315 and theta[index] <= 345) :
                    check_r(r[index], 11)

            max, row, col = check_count();
            sumCount = Copy_Count();
            frame_max.append(max);
            frame_max.append(row);
            frame_max.append(col);
            Init_Count();





        #z = 0
        #for i in range(0,length-1):
        #    for j in range(0, length):
        #        z += 1;
        #ax = plt.subplot(111, projection='polar')
        #ax.plot(theta, r)
        #ax.set_rmax(40)
        #ax.set_rticks([5, 10, 15, 20,25,30])
        #ax.set_rlabel_position(-22.5)
        #ax.grid(True)

        #ax.set_title("A line plot on a polar axis", va='bottom')
        #plt.show()

        # display image with optic flow overlay

        cv2.imshow(windowName, draw_flow(gray, flow))

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in milliseconds).
        # It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of multi-byte response)

        key = cv2.waitKey(40) & 0xFF; # wait 40ms (i.e. 1000ms / 25 fps = 40 ms)

        # It can also be set to detect specific key strokes by recording which key is pressed

        if(frameNum <30) :
            frameNum = frameNum +1;
        elif(frameNum == 30) :
            frameNum = 0;

        # e.g. if user presses "x" then exit

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
                pdivq = prob[r][c];
                pi.append(prob[r][c]);
                temp_ent = ((-1) * prob[r][c] * math.log(pdivq));
            string = "%i - "%i + "Probability : %f, "%prob[r][c] + "CountingSum : %i, "%frame_max[3*i] + "Section : %i,"%r + "%i\n"%c;
            file.write(string);
            entropy.append(temp_ent);

    for ent in entropy:
        string = " %i : "%number + "%s /"%ent;
        string2 = "%s "%ent;
        file.write(string);
        file3.write(string2);
        number = number + 1;
    number = 0;
    for p in pi:
        string3 = "%i : "%number + "%s\n"%p;
        file4.write(string3);
        number = number +1;
    number = 0;
    for q in platformQ:
        string3 = "%i : "%number + "%s\n"%q;
        file5.write(string3);
        number = number +1;

    file.close();
    file2.close();
    file3.close();
    file4.close();
    file5.close();
    # close all windows

    cv2.destroyAllWindows()

else:
    print("No video file specified or camera connected.");

#####################################################################
