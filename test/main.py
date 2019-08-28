from mpvr.datamodule.manager import Manager as dm
from mpvr.utils.process import *
from scipy.signal import savgol_filter
import numpy as np
import pandas as pd
import argparse
import os

MOTION_SEPERATOR = [-0.8, -0.2, 0.2, 0.8]
AXES = ['pitch', 'yaw', 'roll', 'surge', 'heave', 'sway']
SENSORED_AXES_TAG = {'pitch': 'PitchEulerAngle', 'roll': 'RollEulerAngle'}

def motion_visual_data_gen(data_manager, motion_path, visual_path, indices, timediffs):
    motion_gen = data_manager.get_motion_data_gen(path=motion_path,
                                        timediffs=timediffs,
                                        indices=indices,
                                        axes=AXES,
                                        sensored_axes_tag=SENSORED_AXES_TAG,
                                        target_sampling_rate=3)
    classified_motion_gen = data_manager.get_classified_motion_data_gen(gen=motion_gen,
                                                             is_classified=False,
                                                             seperator=MOTION_SEPERATOR)
    visual_gen = data_manager.get_visual_data_gen(path=video_path,
                                        timediffs=timediffs,
                                        indices=indices,
                                        extension='.mp4',
                                        target_sampling_rate=3)
    classified_visual_gen = data_manager.get_classified_visual_data_gen(gen=visual_gen)
    return data_manager.make_tuple_gen(classified_motion_gen, classified_visual_gen)

def mpentropy_handler(motion_path, video_path, output_path):
    dm = dm.from_config(dm.section_list()[0])

    times, timediffs, indices = dm.extract_timestamp_by_grid(1, 0, 105, 3, path = motion_path)
    histograms = (np.zeros(5**6), np.zeros(36))
    make_histogram(motion_visual_data_gen(dm, motion_path, visual_path, indices, timediffs),
                   histograms)
    for hist in histograms:
        hist /= np.sum(hist)

    mapped = mapping_src_to_histogram(
        motion_visual_data_gen(dm, motion_path, visual_path, indices, timediffs),
        histograms)
    mp_entropy = [0]
    for x in to_mp_entropy(mapped):
        mp_entropy.append(x)

    incidence = [0]
    for x in dm.extract_incidence('DizzinessRange', indices):
        incidence.append(x)

    df = pd.DataFrame([mp_entropy, incidence], times)
    df.index.name = ['Time']
    df.columns = ['MP Entropy', 'Incidence']
    df.to_csv(output_path)

def main(args):
    motion_path = args.motion_path
    video_path = args.video_path
    output_path = args.output_path
    mpentropy_handler(motion_path, video_path, output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('motion_path', type=str)
    parser.add_argument('video_path', type=str)
    parser.add_argument('output_path', type=str)
    args = parser.parse_args()
    main(args)
