from mpvr.utils.process import *
from scipy.signal import savgol_filter
import numpy as np
import pandas as pd
import argparse

MOTION_SEPERATOR = [-0.8, -0.2, 0.2, 0.8]
AXES = ['pitch', 'yaw', 'roll', 'surge', 'heave', 'sway']
SENSORED_AXES_TAG = {'pitch': 'PitchEulerAngle', 'roll': 'RollEulerAngle'}

def motion_visual_data_gen(data_manager, motion_path, visual_path, indices, timediffs, mute_svg):
    motion_gen = data_manager.get_motion_data_gen(path=motion_path,
                                                  timediffs=timediffs,
                                                  indices=indices,
                                                  axes=AXES,
                                                  sensored_axes_tag=SENSORED_AXES_TAG,
                                                  target_sampling_rate=3)
    if not mute_svg:
        motion_gen = savgol_filter([x for x in motion_gen], 9, 5, axis=0)
    classified_motion_gen = data_manager.get_classified_motion_data_gen(gen=motion_gen,
                                                             is_classified=False,
                                                             seperator=MOTION_SEPERATOR)
    visual_gen = data_manager.get_visual_data_gen(path=visual_path,
                                                  timediffs=timediffs,
                                                  indices=indices,
                                                  extension='.mp4',
                                                  target_sampling_rate=3)
    classified_visual_gen = data_manager.get_classified_visual_data_gen(gen=visual_gen)
    return data_manager.make_tuple_gen(classified_motion_gen, classified_visual_gen)

def mpentropy_handler(args):
    from mpvr.datamodule.manager import Manager as dm
    dm = dm.from_config(dm.section_list()[0])

    # arguments
    motion_path, visual_path, output_path = args.motion_path, args.visual_path, args.output_path
    mute_svg, mute_acr, mute_norm= args.mute_svg, args.mute_acr, args.mute_norm
    acr_categories = np.array([-170681, -73149, 73149, 170681])

    # time extract
    times, timediffs, indices = dm.extract_timestamp_by_grid(1, 0, 105, 3, path = motion_path)

    ###############################################################################################
    #                                          incidence                                          #
    ###############################################################################################
    incidence = [0]
    for x in dm.extract_incidence('DizzinessRange', indices, motion_path):
        incidence.append(x)

    ###############################################################################################
    #                                        make histogram                                     #
    ###############################################################################################
    histograms = (np.zeros(5**6), np.zeros(36))
    make_histogram(
        motion_visual_data_gen(dm, motion_path, visual_path, indices, timediffs, mute_svg),
        histograms)
    for hist in histograms:
        hist /= np.sum(hist)

    ###############################################################################################
    #                                          mp entropy                                         #
    ###############################################################################################
    mp_entropy = [0]
    mapped = mapping_src_to_histogram(
        motion_visual_data_gen(dm, motion_path, visual_path, indices, timediffs, mute_svg),
        histograms)
    for x in to_mp_entropy(mapped):
        mp_entropy.append(x)
    mp_entropy = np.asarray(mp_entropy)

    if not mute_norm:
        mp_entropy = mp_entropy / 2440
        acr_categories = acr_categories / 2440

    ###############################################################################################
    #                                             save                                            #
    ###############################################################################################
    if mute_acr:
        to_save = mp_entropy
    else:
        to_save = absolute_category_rating(mp_entropy, acr_categories)

    df = pd.DataFrame(np.array([to_save, incidence]).T, times)
    df.index.name = 'Time'
    if mute_acr:
        df.columns = ['MP Entropy', 'Incidence']
    else:
        df.columns = ['ACR', 'Incidence']
    df.to_csv(output_path, float_format="%6f")


def main(args):
    mpentropy_handler(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate MP Entropy from motion data and video file.')
    parser.add_argument("motion_path", type=str, help='data of signal of motion platform (csv)')
    parser.add_argument("visual_path", type=str, help='video file corresponding to motion path (mp4)')
    parser.add_argument("output_path", type=str, help='the name of output file (csv)')
    parser.add_argument('--mute_svg', type=bool, nargs='?', const=1, default=0, help='mute savitzky-golay filtering')
    parser.add_argument('--mute_acr', type=bool, nargs='?', const=1, default=0, help='mute absolute category rating')
    parser.add_argument('--mute_norm', type=bool, nargs='?', const=1, default=0, help='mute normalization')
    # parser.add_argument('--make_figure', type=bool, nargs='?', const=0, default=0, help='make figure')

    args = parser.parse_args()
    main(args)
