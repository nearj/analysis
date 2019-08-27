import numpy as np
import pandas as pd
import cv2

from numba import jit
from . import datamanager

class ThreeDI(datamanager.DataManager):
    """data manager for 3DI
    :param _scenarios: list of scenario
    :type _scenarios: dict
    :param _sensored: sensored axis list in 3di experiment
    :type _sensored: list
    :param _unsensored: sensored axis list in 3di experiment
    :type _unsensored: list
    :param _time_column: time column name in 3di.csv
    :type _time_column: str
    :param _start_index: start index of experiment
    :type _start_index: int
    :param _end_index: end index of experiment
    :type _end_index: int
    :param _step_min: minimum time step size of time stamps
    :type _step_min: int
    :param _step_max: maximum time step size of time stamps
    :type _step_max: int

    """
    def __init__(self, *args, **kwargs):
        """Constructor for 3DI data manager"""
        super(ThreeDI, self).__init__(*args, **kwargs)

    # to make 6 axis motion, e.g.) (1.1, 2.2, 3.3) > (1.1, 2.2, 3.3, 0, 0, 0)


    # def _load_with_preset(self):
    #     """Implementation method of :meth:'mpvr.datamanager.Datamanager.load()'

    #     :returns: Generator of classified motion and video process in experiment
    #     :rtype: Iterator[(int, list)]
    #     """
    #     motion_load_directory = self._load_motion_dir + self._scenario + self._extension['csv']
    #     video_load_directory = self._load_video_dir + self._scenario + '/'

    #     df = pd.read_csv(motion_load_directory)

    #     times = pd.to_datetime(df[self._time_column].str.split().str[1]).astype(int) / 10 ** 9
    #     times -= times[self._start_index] # to set timestamps 0 at start index
    #     sampled_indices, sampled_deltatimes = self._sampling_time(times)
    #     # to make sampling rate approximately about 3hz as previous works

    #     sensored_motion_vectors = np.diff(df[self._sensored.values()].values, axis = 0)
    #     # order: pitch, yaw, roll
    #     motion_vectors = np.hstack((
    #         sensored_motion_vectors, np.zeros((
    #             sensored_motion_vectors.shape[0], len(self._unsensored)))))
    #     # to make 6 axis motion, e.g.) (1.1, 2.2, 3.3) > (1.1, 2.2, 3.3, 0, 0, 0)

    #     sampled_motion = self._sampling_motion(sampled_deltatimes,
    #                                             sampled_indices,
    #                                             motion_vectors)
    #     sampled_video = self._sampling_visual_from_png(sampled_deltatimes,
    #                                           sampled_indices,
    #                                           video_load_directory)
    #     motion_bins = self._make_motion_bins(sampled_motion)

    #     # TODO: stands for rewind... >
    #     sampled_motion = self._sampling_motion(sampled_deltatimes,
    #                                             sampled_indices,
    #                                             motion_vectors)

    #     for sample in zip(*(sampled_motion, sampled_video)):
    #         yield self._classification_motion(sample[0], motion_bins), \
    #             self._classification_video(sample[1])
