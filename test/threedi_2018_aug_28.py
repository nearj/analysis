from mpvr.datamodule.manager import Manager as dm
from mpvr.utils.process import *
from scipy.signal import savgol_filter
import numpy as np
import pandas as pd

dm = dm.from_config(dm.section_list()[0])
def make_tuple_gen(motion, visual):
    for data in zip(*(motion, visual)):
        yield data

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)
    motion_data = np.array([x for x in dm.get_motion_data_gen()])
    filtered_motion_data = savgol_filter(motion_data, 3, 2, axis=0)
    histograms = [np.zeros(5**6), np.zeros(36)]
    mot_vis_gen = make_tuple_gen(
         dm.get_classified_motion_data_gen(gen = filtered_motion_data),
         dm.get_classified_visual_data_gen())
    make_histogram(mot_vis_gen, histograms)
    for hist in histograms:
        hist /= np.sum(hist)

    mot_vis_gen = make_tuple_gen(
         dm.get_classified_motion_data_gen(gen = filtered_motion_data),
         dm.get_classified_visual_data_gen())
    mapped = mapping_src_to_histogram(mot_vis_gen, histograms)
    mpe = [x for x in to_mp_entropy(mapped)]
    print(mpe)
    dm._load_timestamp_data()
    dm.save_scenario_as_table(mpe, 'mpe', remark_dir='savgol/')

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)
    motion_data = np.array([x for x in dm.get_motion_data_gen()])
    filtered_motion_data = savgol_filter(motion_data, 3, 2, axis=0)
    histograms = [np.zeros(5**6), np.zeros(36)]
    mot_vis_gen = make_tuple_gen(
         dm.get_classified_motion_data_gen(gen = filtered_motion_data),
         dm.get_classified_visual_data_gen())
    make_histogram(mot_vis_gen, histograms)
    for hist in histograms:
        hist /= np.sum(hist)

    mot_vis_gen = make_tuple_gen(
         dm.get_classified_motion_data_gen(gen = filtered_motion_data),
         dm.get_classified_visual_data_gen())
    mapped = mapping_src_to_histogram(mot_vis_gen, histograms)
    mpe = [x for x in to_mp_entropy(mapped)]
    print(mpe)
    dm._load_timestamp_data()
    dm.save_scenario_as_table(mpe, 'mpe', remark_dir='savgol/')
