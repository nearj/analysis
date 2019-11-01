import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os, sys, glob

from numba import jit
from etaprogress.progress import ProgressBar
"""
This module calculate real values of KLD of optical flow with motion platform vector. See
https://en.wikipedia.org/wiki/Kullback-Leibler_divergence.

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
OPT_FLOW_REGION = np.index_exp[:, :]
EXT_JSON      = '.json'
EXT_EXCEL     = '.xlsx'
EXT_MP4       = '.mp4'
LOAD_DIR      = './data/raw/video/'
SAVE_DIR      = './data/preprocessed/video/'
BIN_MAGNITUDE = [6,20,100000]
BIN_DEGREE    = np.linspace(15, 345, 12)
COLUMNS       = [str((n % 12) * 30) + 'deg//~' + str(BIN_MAGNITUDE[n // 12]) for n in range(36)]
####################################################################################################

############################################# FUNCTIONS ############################################
# HERE!
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
                if polar[1] < 225:
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

    if polar[0] < 20:
        if polar[0] > 6:
            tmp += 12
    else:
            tmp += 24
    return tmp

# HERE!
def capture_to_optflow(cap):
    optical_flows = []
    prevgray      = cv2.cvtColor(cap.read()[1][OPT_FLOW_REGION], cv2.COLOR_BGR2GRAY)
    frame_max     = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_num     = 1
    bar           = ProgressBar(frame_max, max_width = 100)
    tick          = 0
    while frame_num < frame_max:
        ret, frame = cap.read()

        # here
        if frame_num % 20 == 19:
        # if frame_num % 10 == 9:
            gray = cv2.cvtColor(frame[OPT_FLOW_REGION], cv2.COLOR_BGR2GRAY)
            optical_flows.append(
                cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 4, 15, 3, 5, 1.2, 0))
        if frame_num % 20 == 0:
        # if frame_num % 10 == 0:
            prevgray = cv2.cvtColor(frame[OPT_FLOW_REGION], cv2.COLOR_BGR2GRAY)
        bar.numerator = tick
        print(bar, end = '\r')
        sys.stdout.flush()
        frame_num += 1
        tick += 1
    return optical_flows

# HERE!
def optflow_to_hist(optical_flows, # HERE!
                    bin_magnitude = BIN_MAGNITUDE,
                    bin_degree = BIN_DEGREE):
    """Make histogam of optical flows. Currently, it calculate all of frame at end of frame. However
       THIS will be change when problem of motion platform vector distribution is solved.

       Args:
    	   bin_magnitude:
           bin_degree:
           optical_flows:

       Returns:
           probability of optical flow(12 * 5): sumupped probability

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
    ret = []
    for polars in polars_total:
        # counts = np.zeros(60)
        tmp = []
        for polar in polars:
            _bin = bin_selection(polar)
            counts[_bin] += 1
            tmp.append(_bin)
        ret.append(tmp)
        bar2.numerator = tick
        tick += 1
        print(bar2, end = '\r')
        sys.stdout.flush()
    counts /= counts.sum() # create bins lookup-table
    for frame in ret:     # approximately 1024 * 768
        for i in range(len(frame)):
            frame[i] = counts[frame[i]]
    return ret

# HERE!
def opt_flow_prob_from_file(video_file): # helper function on file
    print(video_file)
    cap = cv2.VideoCapture(video_file)
    optical_flows = capture_to_optflow(cap)
    cap.release()
    probability = optflow_to_hist(optical_flows)
    return probability

############################################# obselete #############################################

def opt_flow_prob_from_dir(load_dir): # helper function on directory
    video_files = glob.glob(load_dir + "*" + EXT_MP4)
    total_bar = ProgressBar(len(video_files), max_width = 100)
    tick = 0
    tmp = []
    for video_file in video_files:
        video_name  = os.path.splitext(os.path.basename(video_file))[0]
        probability = opt_flow_prob_from_file(video_file)
        tmp.append([video_name, probability])
        total_bar.numerator = tick
        tick += 1
        print(str(tick) + "/21 :\n")
    return tmp

def save(video_name, probability, save_dir = SAVE_DIR):
    save_json_path = save_dir + video_name + EXT_JSON
    df = pd.DataFrame(probability)
    df.to_json(save_json_path)

def main(args):
    if args.use_default:
        data_set = opt_flow_prob_from_dir(LOAD_DIR)
    total_bar = ProgressBar(len(data_set), max_width = 100)
    tick = 0
    for data in data_set:
        save(data[0], data[1])
        total_bar.numerator = tick
        tick += 1
        print(total_bar, end = '\r')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Calculate optical flows of video per 10frame and save it as json and excel')

    parser.add_argument('-use_default', "--use_default", action='store_true')
    parser.add_argument('-dir', "--dir", nargs='?', type=str, help='directory')
    parser.add_argument('-file', "--file", nargs='?', type=str, help = 'YET IMPLEMENTED!')
    main(parser.parse_args())
############################################# obselete #############################################
