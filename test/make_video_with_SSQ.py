import cv2
import argparse
import sys
import numpy as np
import pandas as pd
import os, sys, glob

#####################################################################
LOAD_DIR = './data/raw/video/'
SAVE_DIR = './data/processed/'
SAVE_DIR = './data/processed/'
SAVE_OPT_VIDEO = 'video/'
SAVE_OPT_DATA = 'data/'
EXT_MP4 = '.mp4'
EXT_JSON = '.json'
EXT_EXCEL = '.xlsx'
SSQ = { 'S1_pitch': [6, 18], 'S1_yaw': [10], 'S1_roll':[9],
        'S1_surge': [9], 'S1_heave': [], 'S1_sway': [7, 14],
        'S2_pitch': [6, 16], 'S2_yaw': [5,6,16], 'S2_roll':[5,6,7,9,16,17],
        'S2_surge': [6,7], 'S2_heave': [], 'S2_sway': [6,7,13],
        'S3_pitch': [10,11,14,19], 'S3_yaw': [6,10], 'S3_roll':[5],
        'S3_surge': [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
        'S3_heave': [], 'S3_sway': [3,4,5,6,7,8,12],
        'S4': [2,3,4,5,6,7,12,15,22,23,24,25,26,27,33,43,54],
        'S5': [7,8,24,25, 42, 54],
        'S6': [3,4,17,18,19,20,21,22,23,36,37,38,39,40,41,42] }
ROI = np.index_exp[191:576, 255:768] #region of interest
ROI_RECT = ((ROI[1].start, ROI[0].start), (ROI[1].stop, ROI[0].stop))

#####################################################################
# draw optic flow visualization on image using a given step size for
# the line glyphs that show the flow vectors on the image

def draw_flow(img, flow, step=8):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    fx = [t if np.abs(t) > 2 else 0 for t in fx]
    fy = [t if np.abs(t) > 2 else 0 for t in fy]
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.00001)

    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # cv2.polylines(vis, lines, 0, (0, 255, 0))

    # for (x1, y1), (x2, y2) in lines:
        # cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    for (x1, y1), (x2, y2) in lines:
        d = np.linalg.norm(np.asarray([x2-x1,y2-y1]))
        if d > 30:
            cv2.arrowedLine(vis, (x1, y1), (x2, y2), (0, 200, 200), 1, 4, tipLength = 0.1)
        elif d > 20:
            cv2.arrowedLine(vis, (x1, y1), (x2, y2), (0, 200, 0), 1, 4, tipLength = 0.1)
        else:
            cv2.arrowedLine(vis, (x1, y1), (x2, y2), (200, 200, 80), 1, 4, tipLength = 0.1)
    return vis

#####################################################################
def make_optflow_video(video_file, directory_to_save):
    video_name = os.path.splitext(os.path.basename(video_file))[0]
    save_dir = directory_to_save + video_name + EXT_MP4

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    cap = cv2.VideoCapture(video_file)
    out = cv2.VideoWriter(save_dir, fourcc, 3, (1024, 768))
    ret, frame = cap.read();
    prevgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_max = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_num = 1
    while (frame_num < frame_max):
        ret, frame = cap.read();

        if frame_num % 20 == 19:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            img_with_optflow = draw_flow(gray, flow)
            if frame_num - 19 in SSQ[video_name]:
                cv2.rectangle(img_with_optflow, ROI_RECT[0], ROI_RECT[1], (0,0,255), 2)
            else:
                cv2.rectangle(img_with_optflow, ROI_RECT[0], ROI_RECT[1], (0,255,0), 2)
            out.write(img_with_optflow)
        if frame_num % 20 == 0:
            prevgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_num += 1
    cap.release()
    out.release()
    pass

def make_optflow_class_data(video_file, directory_to_save):
    video_name = os.path.splitext(os.path.basename(video_file))[0]
    print(video_name)

    cap = cv2.VideoCapture(video_file)
    ret, frame = cap.read();
    prevgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_max = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_num = 1

    dat = []
    while (frame_num < frame_max):
        ret, frame = cap.read();

        if frame_num % 20 == 19:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            d = np.asarray([np.linalg.norm(v) for v in flow.reshape(-1, 2)])
            dat.append([(d <= 20).sum() / 786432, ((30 >= d) & (d > 20)).sum() / 786432, (d > 30).sum() / 786432])
        if frame_num % 20 == 0:
            prevgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_num += 1
    cap.release()

    df = pd.DataFrame(dat)
    df.to_json(directory_to_save + video_name + EXT_JSON)
    df.to_excel(directory_to_save + video_name + EXT_EXCEL)
    pass


def act_on_dir(action, directory_to_save, directory_to_load = LOAD_DIR,):
    video_files_to_load = glob.glob(directory_to_load + "*" + EXT_MP4)

    for video_file in video_files_to_load:
        action(video_file, directory_to_save)

    pass


###############################################################################
for key in SSQ.keys():
    SSQ[key] = np.asarray(SSQ[key])
    SSQ[key] *= 60
for key in SSQ.keys():
    SSQ[key] = np.vstack((SSQ[key]-40, SSQ[key]-20, SSQ[key])).transpose().reshape(-1)

def main():
    # act_on_dir(make_optflow_video, SAVE_DIR + SAVE_OPT_VIDEO)
    act_on_dir(make_optflow_class_data, SAVE_DIR + SAVE_OPT_DATA)

if __name__ == '__main__':
    main()

#####################################################################
