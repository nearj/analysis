import configure

class DataManager:
    def __init__(self, *args, **kwargs):
        import numpy as np
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
        return cls(conf=conf)

    def set_scenario(self, scenario):
        self._scenario = scenario

    def get_scenarios(self):
        return self._get_scenarios()

    def load(self):
        return self._load()

    def save_as_table(self, data, tag):
        self._save_as_table(data, tag)

    def save_as_graph(self, data, tag, xlabel='sec', ylabel='entropy', ylim=None):
        self._save_as_graph(data, tag, xlabel, ylabel, ylim)
