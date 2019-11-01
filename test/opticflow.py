
import cv2
import argparse
import sys
import numpy as np

keep_processing = True;

def draw_flow(img, flow, step=8):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis

cap = cv2.VideoCapture();

windowName = "Dense Optic Flow"; # window name

if (((args.video_file) and (cap.open(str(args.video_file))))
    or (cap.open(args.camera_to_use))):

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL);

    if (cap.isOpened):
        ret, frame = cap.read();

    prevgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    while (keep_processing):

        if (cap.isOpened):
            ret, frame = cap.read();

            if (ret == 0):
                keep_processing = False;
                continue;

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        prevgray = gray
        tmp = gray
        tmp[192:576, 258:768] = draw_flow(gray, flow)[192:576, 258:768, 0]

        cv2.imshow(windowName, tmp)
        key = cv2.waitKey(40) & 0xFF;
        
        if (key == ord('x')):
            keep_processing = False;
        elif (key == ord('f')):
            cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

    cv2.destroyAllWindows()

else:
    print("No video file specified or camera connected.");
