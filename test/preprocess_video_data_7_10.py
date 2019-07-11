import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os, sys, glob

from numba import jit, vectorize, int32
from etaprogress.progress import ProgressBar
"""
This module calculate real values of KLD of optical optflows_in_frame with motion platform vector. See
https://en.wikipedia.org/wiki/Kullback-Leibler_divergence.

Examples:
    Nope.

Attributes:
    _optflow_to_hist(bin_magnitude, bin_degree, optflows_in_video)

Todo:
    *using cuda to calculate optical optflows_in_frame, farneback3d see https://pypi.org/project/farneback3d/.
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
BIN_SIZE     = 36
BIN_MAGNITUDE = [6,20,100000]
BIN_DEGREE    = np.linspace(15, 345, 12)
COLUMNS       = [str((n % 12) * 30) + 'deg//~' + str(BIN_MAGNITUDE[n // 12]) for n in range(BIN_SIZE)]
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

def _cap_to_optflow(cap, sample_len):
    optflows_in_video = []
    prevgray      = cv2.cvtColor(cap.read()[1][OPT_FLOW_REGION], cv2.COLOR_BGR2GRAY)
    frame_max     = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_num     = 1
    bar           = ProgressBar(frame_max, max_width = 100)
    tick          = 0
    while frame_num < frame_max:
        ret, frame = cap.read()
        if frame_num % sample_len == sample_len - 1:
            gray = cv2.cvtColor(frame[OPT_FLOW_REGION], cv2.COLOR_BGR2GRAY)
            optflows_in_video.append(
                cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 4, 15, 3, 5, 1.2, 0))
        if frame_num % sample_len == 0:
            prevgray = cv2.cvtColor(frame[OPT_FLOW_REGION], cv2.COLOR_BGR2GRAY)
        bar.numerator = tick
        print(bar, end = '\r')
        sys.stdout.flush()
        frame_num += 1
        tick += 1
    return optflows_in_video

@guvectorize([(int32[:], float32[:])], '(n),()->(n)')
def _map_hist_to_prob(hist_in_frame, lookup_tbl):
    for i in range(len(hist_in_frame)):
        hist_in_frame[i] = lookup_tbl[hist_in_frame[i]]


def _optflow_to_hist(optflows_in_video):
    """Make histogam of optical flows. Currently, it calculate all of frame at end of frame. However
       THIS will be change when problem of motion platform vector distribution is solved.

       Args:
           optflows_in_video (arr)

       Returns:
           probability of optical optflows_in_frame(12 * 5): sumupped probability
    """
    polars_in_video = []
    for optflows_in_frame in optflows_in_video:
        polars_in_frame = np.asarray(cv2.cartToPolar(optflows_in_frame[...,0],
                                            optflows_in_frame[...,1],None,None,True))
        polars_in_video.append(polars_in_frame.reshape
                               (2, polars_in_frame.shape[1] * polars_in_frame.shape[2]).T)

    bar2   = ProgressBar(len(polars_in_video), max_width = 100)
    tick   = 0
    lookup_tbl = np.zeros(BIN_SIZE)
    ret = []
    for polars_in_frame in polars_in_video:
        tmp = []
        for polar in polars_in_frame:
            _bin = bin_selection(polar)
            lookup_tbl[_bin] += 1
            tmp.append(_bin)
        ret.append(tmp)
        bar2.numerator = tick
        tick += 1
        print(bar2, end = '\r')
        sys.stdout.flush()
    lookup_tbl /= lookup_tbl.sum() # create bins lookup-table
    for hist_in_frame in ret:
        _map_hist_to_prob(hist_in_frame, lookup_tbl)
    return ret, lookup_tbl

def _optflow_to_prob_in_video(video_file, sample_len): # helper function on file
    cap = cv2.VideoCapture(video_file)
    optflows_in_video = _cap_to_optflow(cap, sample_len)
    cap.release()
    probability, _ = _optflow_to_hist(optflows_in_video)
    return probability

def _optflow_to_prob_in_dir(load_dir, sample_len): # helper function on directory
    video_files = glob.glob(load_dir + "*" + EXT_MP4)
    ret = []
    for video_file in video_files:
        video_name  = os.path.splitext(os.path.basename(video_file))[0]
        probability = _optflow_to_prob_in_video(video_file)
        ret.append([video_name, probability])
    return ret

def save(video_name, probability, save_dir = SAVE_DIR):
    save_json_path = save_dir + video_name + EXT_JSON
    df = pd.DataFrame(probability)
    df.to_json(save_json_path)

def main(args):
    if args.use_default:
        data_set = _optflow_to_prob_in_dir(LOAD_DIR)
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
