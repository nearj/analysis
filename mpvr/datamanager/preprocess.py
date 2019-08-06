import numpy as np
import pandas as pd
import cv2
import os, sys, glob

import configure

from etaprogress.progress import ProgressBar

########################################## GOLBAL VARIABLES ########################################
BIN_MAGNITUDE = [6,20,100000]
BIN_DEGREE    = np.linspace(15, 345, 12)
COLUMNS       = [str((n % 12) * 30) + 'deg//~' + str(BIN_MAGNITUDE[n // 12]) for n in range(36)]
####################################################################################################

class DataManager:
    def __init__(self, *args, **kwargs):
        setting = kwargs.get('conf').DATA_MANAGER
        self._load_motion_dir = setting['LOAD_MOTION_DIR']
        self._load_video_dir  = setting['LOAD_VIDEO_DIR']
        self._load_options    = setting['LOAD_OPTIONS']

        self._save_dir        = setting['SAVE_DIR']
        self._save_options    = setting['SAVE_OPTIONS']

        self._bin_seperator   = np.array(setting['BIN_SEPERATOR'])
        self._extension       = setting['EXTENSION']
        self._axis            = setting['AXIS']

    @classmethod
    def from_config(cls, conf = configure.Config):
        return cls(conf)

    def set_scenario(self, scenario):
        self._scenario = scenario

    def save(self, scenario, rows, data):
        """ save data to directory

        Args:
        motion_save_dir (str)
        data (var)
        """
        save_json_path = self._save_motion_dir + self._scenario + self._extension['json']
        save_csv_path = self._save_motion_dir + self._scenario + self._extension['csv']
        df = pd.DataFrame(data = list(zip(*[rows, data])), columns=['motion vector', 'probability'])
        df.to_json(save_json_path)
        df.to_csv(save_csv_path)

    def load(self):
        return self._load()

    def save_as_table(self, data, tag):
        self._save_as_table(data, tag)

    def save_as_graph(self, data, tag, xlabel='sec', ylabel='entropy', ylim=None):
        self._save_as_graph(data, tag, xlabel, ylabel, ylim)

class Preprocessor:
    def __init__(self, *args, **kwargs):
        self._bin_magnitude = kwarg.get('bin_magnitude')
        self._bin_degree = kwarg.get('bin_degree')
        self._resolution = kwarg.get('resolution')
        self._roi = kwarg.get('roi')
        self._video_histogram = np.zeros(len(self._bin_magnitude) * len(self._bin_degree))
        self._motion_histogram = None

    @classmethod
    def from_config(cls, conf):
        pass

    def set_video_src():
        pass

    def set_motion_src():
        pass

    def get_preprocessed_data():
        pass

    def clear(self):
        self._video_histogram = np.zeros(len(self._bin_magnitude) * len(self._bin_degree))
        self._motion_histogram = None

    def _video_bin_selection(polar) -> int:
        pass

    def _classification_video(self):
        pass

    def _make_video_histogram(self):
        pass

    def _make_motion_histogram(self):
        pass

    def _mapping_video_to_histogram(self):
        pass

    def _mapping_motion_to_histogram(self):
        pass
