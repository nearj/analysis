from config.data import Config
import mpvr.datamodule._fig_preset as fig_preset

import importlib
import pandas as pd
import numpy as np

class Manager:
    def __init__(self, *args, **kwargs):
        self.conf = kwargs.get('conf')
        self._section = kwargs.get('section')
        self._tags = self.conf.get_tags()
        self._load_state = {'scenario': False,
                            'incidence': False,
                            'timestamp': False}
        self._preprocess = importlib.import_module( 'mpvr.datamodule.' + str.lower(self._section))

    @classmethod
    def from_config(cls, section, conf = Config):
        return cls(conf=conf, section=section)

    @staticmethod
    def section_list():
        return Config.section_list()

    def get_scenarios(self):
        return Config.get_section_scenarios(self._section)

    def set_scenario(self, scenario):
        self._setting = self.conf.get_config(self._section, scenario)
        self._scenario = scenario
        self._load_state_init()
        self._load_state['scenario'] = True

    def _load_state_init(self):
        for key in self._load_state.keys():
            self._load_state[key] = False

    def _check_and_load(self, states):
        load_funcs = {'incidence': self._load_incidence_data,
                      'timestamp': self._load_timestamp_data}

        for state in states:
            if not self._load_state[state]:
                load_funcs[state]()

    ###############################################################################################
    #                                        get functions                                        #
    ###############################################################################################
    def get_motion_data_gen(self,
                            path=None,
                            timediffs=None,
                            indices=None,
                            axes = None,
                            sensored_axes_tag=None,
                            target_sampling_rate=None):
        if timediffs is None:
            self._check_and_load(['timestamp'])
            indices = self._indices
            timediffs = self._timediffs
        if path is None:
            path = self._setting.motion_data.path
        if axes is None:
            axes = self._setting.motion_data.axes
        if sensored_axes_tag is None:
            sensored_axes_tag = self._setting.motion_data.sensored_axes_tag
        if target_sampling_rate is None:
            target_sampling_rate = self._setting.target_sampling_rate
        return self._preprocess.load_motion_gen(path,
                                                axes,
                                                sensored_axes_tag,
                                                target_sampling_rate,
                                                indices,
                                                timediffs)

    def get_classified_motion_data_gen(self, gen=None, is_classified=None, seperator=None):
        if gen is None:
            gen = self.get_motion_data_gen()

        if is_classified is None:
            is_classified = self._setting.motion_data.is_classified

        if seperator is None:
            seperator = self._setting.motion_data.motion_seperator

        if is_classified:
            for motion_vector in gen:
                yield self._preprocess.classification_motion(motion_vector)
        else:
            motion_data = [x for x in gen]
            bins = self._preprocess.make_bins(motion_data, seperator)
            for motion_vector in motion_data:
                yield self._preprocess.classification_motion(motion_vector, bins)


    def get_visual_data_gen(self,
                            path=None,
                            indices=None,
                            timediffs=None,
                            extension=None,
                            target_sampling_rate=None):
        if timediffs is None:
            self._check_and_load(['timestamp'])
            indices = self._indices
            timediffs = self._timediffs
        if path is None:
            path = self._setting.video_data.path
        if extension is None:
            extension = self._setting.video_data.extension
        if target_sampling_rate is None:
            target_sampling_rate = self._setting.target_sampling_rate
        return self._preprocess \
                   .load_visual_gen(path,
                                    target_sampling_rate,
                                    extension,
                                    indices,
                                    timediffs)

    def get_classified_visual_data_gen(self, gen=None):
        if gen is None:
            gen = self.get_visual_data_gen()
        for polars in gen:
            yield self._preprocess.classification_visual(polars)

    def make_tuple_gen(self, gen1, gen2):
        for d in zip(*(gen1, gen2)):
            yield d

    def get_incidence_data(self):
        self._check_and_load(['incidence'])
        return self._incidence

    def get_timestamp_data(self):
        self._check_and_load(['timestamp'])
        return self._times, self._timediffs, self._indices

    def get_processed_data(self, tag, path=None, remark_dir=''):
        tags = self._tags
        if path is None:
            path = self._setting.save_result_path + tags[tag]['dir'] + tags['tbl']['dir'] \
                + remark_dir + self._scenario + tags['tbl']['ext']
        df = pd.read_csv(path, encoding="ISO-8859-1")
        return df

    ###############################################################################################
    #                                        set functions                                        #
    ###############################################################################################
    def set_paths(self, motion_src_path, video_src_path):
        pass

    ###############################################################################################
    #                                        load functions                                       #
    ###############################################################################################
    def load_raw_data(self):
        self._load_incidence_data()
        self._load_timestamp_data()

    def _load_incidence_data(self):
        self._load_state['incidence'] = True
        df = pd.read_csv(self._setting.incidence_data_path, encoding="ISO-8859-1")
        self._incidence = df[self._tags['incidence']['title']].values[1:]

    def _load_timestamp_data(self):
        self._load_state['timestamp'] = True
        df = pd.read_csv(self._setting.timestamp_path, encoding="ISO-8859-1")
        tags = self._tags
        self._times     = df[tags['time']['title']].values
        self._timediffs = df[tags['timediff']['title']].values
        self._indices   = df[tags['index']['title']].values.astype(int)

    ###############################################################################################
    #                                        save functions                                       #
    ###############################################################################################
    def save_scenario_as_table(self, data, tag, remark_dir = '', file_name = None):
        tags = self._tags
        self._check_and_load(['timestamp'])
        if tag not in tags.keys():
            raise Exception('unsupported tag')
        if not file_name:
            file_name = self._scenario

        path = self._setting.save_result_path + tags[tag]['dir'] + tags['tbl']['dir'] \
            + remark_dir + file_name + tags['tbl']['ext']
        df = pd.DataFrame(data)
        df.index = self._times[1:]
        df.index.name = tags['time']['title']
        df.columns = [tags[tag]['title']]
        df.to_csv(path)

    def save_section_as_table(self, data, tag, index=None, columns=None, remark_dir='', file_name = ''):
        if len(file_name) == 0:
            file_name = self._section

        tags = self._tags
        path = self._setting.save_result_path + tags[tag]['dir'] + tags['tbl']['dir']  + remark_dir \
            + file_name + tags['tbl']['ext']

        df = pd.DataFrame.from_dict(data)

        if index is not None:
            df.index = index
        if columns is not None:
            df.columns = columns
        df.to_csv(path)

    def fig_setup(self, row, ylabels, xticks=None, ylims=None, width=18, height=6, times = None):
        if times is None:
            times = self._times

        return fig_preset.fig_setup(times, row, ylabels, xticks, ylims, width, height)

    def fig_finalize(self, tag, remark_dir='', path=None):
        tags = self._tags
        if path is None:
            path = self._setting.save_result_path + tags[tag]['dir'] + tags['grp']['dir'] \
                + remark_dir + self._scenario + tags['grp']['ext']
        fig_preset.fig_finalize(path)

    def ax_color_by_value(self, ax, time, data, y_value=0):
        fig_preset.ax_color_by_value(ax, time, data, y_value)

    ###############################################################################################
    #                                             misc                                            #
    ###############################################################################################
    def extract_timestamp_by_step(self, step_size, start_ind):
        tags = self._tags
        df = pd.read_csv(self._setting.motion_data.path, encoding="ISO-8859-1")
        times = df[tags['time']['title']]
        times -= times[start_ind]
        times = times.values[start_ind:]

        timediffs = [0]
        indices = [start_ind]
        for i in range(start_ind, len(times)):
            diff = times[i] - times[start_ind]
            if diff >= step_size:
                timediffs.append(diff)
                indices.append(i)
                start_ind = i

        df = pd.DataFrame([times[indices], timediffs, indices]).T
        df.columns = [tags['time']['title'], tags['timediff']['title'], tags['index']['title']]
        df[tags['index']['title']] = df[tags['index']['title']].astype(np.int)
        df.to_csv(self._setting.timestamp_path, float_format='%0.6f')

    def extract_timestamp_by_grid(self, start_ind,
                                  start_time, end_time,
                                  target_sampling_rate, error=0.061, path = None):
        if path is None:
            path = self._setting.motion_data.path
        tags = self._tags
        df = pd.read_csv(path, encoding="ISO-8859-1")
        times = pd.to_datetime(df[tags['time']['title']].str.split().str[1]).astype(np.int64) \
            / 10**6
        times -= times[start_ind]
        times = times.values[start_ind:]
        times /= 10**3

        prev_t = times[0]
        ret_times = []
        ret_timediffs = [] # delta times
        ret_indices = [] # sampled indices
        grid = np.linspace(start_time, end_time, target_sampling_rate * end_time + 1)
        grid_idx = 0

        for i in range(0, len(times)):
            diff = times[i] - grid[grid_idx]
            if np.abs(diff) < error:
                ret_times.append(times[i])
                ret_timediffs.append(times[i]-prev_t)
                ret_indices.append(i + start_ind)
                prev_t = times[i]
                grid_idx += 1
                if grid_idx >= target_sampling_rate * end_time + 1:
                    break
        return ret_times, ret_timediffs, ret_indices

    def save_timestamps(self, times, timediffs, indices, path=None):
        if path is None:
            path = self._setting.timestamp_path
        df = pd.DataFrame(np.array([times, timediffs, indices]).T)
        df[2] = df[2].astype(int)
        df.columns = [tags['time']['title'], tags['timediff']['title'], tags['index']['title']]
        df.to_csv(path, float_format='%0.6f')

    def extract_incidence(self, incidence_col_name, indices, path=None):
        if path is None:
            path = self._setting.motion_data.path
        tags = self._tags
        raw = pd.read_csv(path, encoding="ISO-8859-1")[incidence_col_name].values

        i = indices[0]
        sampled = [0]
        for j in indices[1:-1]:
            sampled.append(np.sum(raw[i:j]))
            i = j

        # i = self._indices[0]
        # mid = int((self._indices[0] + self._indices[1]) / 2)
        # sampled = [np.sum(raw[i:mid])]

        # i = self._indices[1]
        # for j in self._indices[2:]:
        #     sampled.append(np.sum(raw[mid:int((i+j)/2)]))
        #     mid = int((i+j)/2)
        #     i = j

        # sampled.append(np.sum(raw[mid:j]))
        return sampled

    def save_incidence(self, times, incidence, path=None):
        if path is None:
            path = self._setting.incidence_data_path
        df = pd.DataFrame(np.array([times, incidence])).T
        df.columns = [tags['time']['title'], tags['incidence']['title']]
        df[tags['incidence']['title']] = df[tags['incidence']['title']].astype(int)
        df.to_csv(path)
