import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os, sys

from numba import jit
from etaprogress.progress import ProgressBar
"""Previous version of Kullback Leivier Divergence(KLD).

This module calculate real values of KLD of optical flow with motion platform vector. See
https://en.wikipedia.org/wiki/Kullback–Leibler_divergence.

Examples:
    Nope.

Attributes:
    optflow_to_hist(bin_magnitude, bin_degree, optical_flows)

Todo:
    *using cuda to calculate optical flow, farneback3d see https://pypi.org/project/farneback3d/.
    *Motion platform probability integrity check
"""

########################################## GOLBAL VARIABLES ########################################
DIM_OF_IMG    = (768, 1024) # Or, we can get dimension of image from file
EXT_JSON      = '.json'
EXT_EXCEL     = '.xlsx'
SAVE_DIR      = '../VideoDataProcessed/'
BIN_MAGNITUDE = [1,6,20,50,100000]
BIN_DEGREE    = np.linspace(15, 345, 12)

####################################################################################################

############################################# FUNCTIONS ############################################
@jit()
def bin_selection(polar):
    tmp = 0
    if polar[1] < 195:
        if polar[1] < 105:
            if polar[1] < 45:
                if polar[1] > 15:
                    tmp = 1
            else:
                if polar[1] < 75:
                    tmp = 2
                else:
                    tmp = 3
        else:
            if polar[1] < 165:
                if polar[1] < 135:
                    tmp = 4
                else:
                    tmp = 5
            else:
                tmp = 6
    else:
        if polar[1] < 315:
            if polar[1] < 255:
                if polar[1] < 195:
                    tmp = 7
                else:
                    tmp = 8
            else:
                if polar[1] < 285:
                    tmp = 9
                else:
                    tmp = 10
        else:
            if polar[1] < 345:
                tmp = 11

    if polar[0] < 6:
        if polar[0] > 1:
            tmp += 12
    else:
        if polar[0] < 50:
            if polar[0] < 20:
                tmp += 24
            else:
                tmp += 36
        else:
            tmp += 48
    return tmp

def caption_to_optflow(cap):
    optical_flows = []
    prevgray      = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
    frame_max     = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_num     = 1
    bar           = ProgressBar(frame_max, max_width = 100)
    tick          = 0
    while frame_num < frame_max:
        ret, frame = cap.read()

        if frame_num % 10 == 1:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            optical_flows.append(
                cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0))
        if frame_num % 10 == 0:
            prevgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            bar.numerator = tick
        print(bar, end = '\r')
        sys.stdout.flush()
        frame_num += 1
        tick += 1
    return optical_flows

def optflow_to_hist(optical_flows,
                    bin_magnitude = BIN_MAGNITUDE,
                    bin_degree = BIN_DEGREE):
    """Make histogam of optical flows. Currently, it calculate all of frame at end of frame. However
       THIS will be change when problem of motion platform vector distribution is solved.

       Args:
    	   bin_magnitude:
           bin_degree:
           optical_flows:

       Returns:
           probability of optical flow(12 * 5): sum-upped probability

       TODO:
           *parallelization
	   *do not sum up, take each probability.
    """
    #assert polars[0].shape == DIM_OF_IMG and polars[1].shape == DIM_OF_IMG,\
    #'Error: dimention of image is not' + str(DIM_OF_IMG)
    polars_total = []
    for flow in optical_flows:
        polars = np.asarray(cv2.cartToPolar(flow[...,0], flow[...,1],None,None,True))
        polars_total.append(polars.reshape(2, polars.shape[1] * polars.shape[2]).T)

    bar2   = ProgressBar(len(polars_total), max_width = 100)
    tick   = 0
    counts_set = []
    counts = np.zeros(60)
    for polars in polars_total:
        for polar in polars:
            counts[bin_selection(polar)] += 1
        counts_set.append(counts / counts.sum())
        bar2.numerator = tick
        tick += 1
        print(bar2, end = '\r')
        sys.stdout.flush()
    return counts_set

def main(args):
    video_name    = os.path.splitext(os.path.basename(args.video_file))[0]
    save_dir      = args.save_path
    save_json     = save_dir + video_name + EXT_JSON
    save_excel    = save_dir + video_name + EXT_EXCEL

    cap           = cv2.VideoCapture(args.video_file)
    optical_flows = caption_to_optflow(cap)
    histogram     = optflow_to_hist(optical_flows)

    df = pd.DataFrame(histogram)
    df.columns = [str((n % 12) * 30) + 'deg//~' + str(BIN_MAGNITUDE[n // 12]) for n in range(60)]
    df.to_json(save_json)
    df.to_excel(save_excel)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Calculate optical flows of video per 10frame and save it as json and excel')
    parser.add_argument('video_file', nargs='?', type=str, help='mp4 file')
    parser.add_argument('save_path', nargs='?', type=str, default=SAVE_DIR)
    main(parser.parse_args())
