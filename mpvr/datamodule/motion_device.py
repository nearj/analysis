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
        self._scenarios = self.conf.threedi_scenarios()

    def _get_scenarios(self):
        """Implementation method of :meth:'mpvr.datamanager.Datamanager.get_scenarios'"""
        return self._scenarios

    def _set_scenario(self, scenario):
        self.setting = self.conf(scenario)
        self._scenario = scenario

    # to make 6 axis motion, e.g.) (1.1, 2.2, 3.3) > (1.1, 2.2, 3.3, 0, 0, 0)
    def _load_motion(self):
        df = pd.read_csv(self.setting.motion_data.path, encoding="ISO-8859-1")

        sensored_tag = self.setting.motion_data.sensored_axes_tag # order: pitch, yaw, roll
        unsensored_axes = [ax for ax in self.setting.motion_data.axes \
                           if ax not in sensored_tag.keys()]
        sensored_motion_vectors = np.diff(df[sensored_tag.values()].values, axis = 0)
        motion_vectors = np.hstack((
            sensored_motion_vectors, np.zeros((
                sensored_motion_vectors.shape[0], len(unsensored_axes)))))
        return motion_vectors

    def _load_visual_from_video(self, sampled_indices):
        cap = cv2.VideoCapture(self.video_data.path)
        i = 0
        while i < sampled_indices[0]:
            cap.read()

        frame_max = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        while i <= frame_max:
            if i in sampled_indices:
                yield cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
            else:
                cap.read()
            i += 1
        cap.release()

    def _load_timestamp(self):
        # to make sampling rate approximately about 3hz as previous works
        df = pd.read_csv(self.setting.timestamp_path, encoding="ISO-8859-1")
        tags = self.setting.tags

        self._timestamp = df[tags['time']['title']].values
        sampled_deltatimes = np.diff(self._timestamp)
        sampled_indices   = np.array(df[tags['index']['title']].values, dtype=int)
        return sampled_deltatimes, sampled_indices

    def _load_incidence(self):
        df = pd.read_csv(self.setting.incidence_data_path, encoding="ISO-8859-1")
        return df[self.setting.tags['incidence']['title']].values[1:]

    def _load_processed_data(self, option: str):
        tags = self.setting.tags
        path = self.setting.save_result_path + tags['tbl']['dir'] + tags[option]['dir'] \
            + self._scenario + tags['tbl']['ext']
        df = pd.read_csv(path)
        return df[tags['time']['title']].values, df[tags[option]['title']].values

    def _load(self):
        """Implementation method of :meth:'mpvr.datamanager.Datamanager.load()'

        :returns: Generator of classified motion and video process in experiment
        :rtype: Iterator[(int, list)]
        """
        sampled_deltatimes, sampled_indices = self._load_timestamp()
        motion_vectors = self._load_motion()

        sampled_motion = self._sampling_motion(sampled_deltatimes,
                                                sampled_indices,
                                                motion_vectors)
        sampled_video = self._sampling_visual_from_video(sampled_deltatimes,
                                              sampled_indices)
        motion_bins = self._make_motion_bins(sampled_motion)

        for sample in zip(*(sampled_motion, sampled_video)):
            yield self._classification_motion(sample[0], motion_bins), \
                self._classification_video(sample[1])

    def _sampling_time(self, times):
        j = self._start_index
        ret_dts = [] # delta times
        ret_ind = [self._start_index] # sampled indices
        for i in range(self._start_index, self._end_index):
            delta_time = times[i] - times[j]
            if  delta_time >= self._step_min:
                ret_dts.append(delta_time)
                ret_ind.append(i)
                j = i
            elif delta_time > self._step_max:
                raise Exception('time sampling exceed step max({})'.format(times[i] - times[j]))
        return np.array(ret_ind, dtype = np.int), np.array(ret_dts)

    def _sampling_motion(self, delta_times, indices, motion_vectors):
        j = indices[0]
        for x in list(zip(indices[1:], delta_times)):
            yield np.sum(motion_vectors[j:x[0]] /  x[1], axis = 0)
            j = x[0]

    def _make_motion_bins(self, sampled_motion):
        max_values = np.max(np.abs([mv for mv in sampled_motion]), axis = 0)
        return np.array([np.array(self.setting.motion_data.motion_seperator) * m for m in max_values])

    def _sampling_visual_from_video(self, delta_times, indices):
        cap = cv2.VideoCapture(self.setting.video_data.path)
        i = 0
        while i < indices[0]:
            cap.read()
            i += 1

        prev = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
        i += 1

        frame_max = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        j = 0
        while i <= frame_max:
            if i in indices:
                cur = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
                flow = cv2.calcOpticalFlowFarneback(prev, cur, None, 0.5, 4, 15, 3, 5, 1.2, 0)
                polars = np.asarray(cv2.cartToPolar(flow[...,0], flow[...,1], None, None, True))
                polars = polars.reshape(2, polars.shape[1] * polars.shape[2]).T / delta_times[j] / 3
                # to make approximately 3hz
                prev = cur
                yield polars
                j += 1
            else:
                cap.read()
            i += 1
        cap.release()

    def _sampling_visual_from_png(self, delta_times, indices, load_dir):
        prev = cv2.cvtColor(cv2.imread(load_dir + "{:0>4d}.png".format(indices[0])),
                            cv2.COLOR_BGR2GRAY)
        for x in list(zip(indices[1:], delta_times)):
            cur = cv2.cvtColor(cv2.imread(load_dir +
                                          "{:0>4d}.png".format(x[0])), cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prev, cur, None, 0.5, 4, 15, 3, 5, 1.2, 0)
            polars = np.asarray(cv2.cartToPolar(flow[...,0], flow[...,1], None, None, True))
            polars = polars.reshape(2, polars.shape[1] * polars.shape[2]).T / x[1] / 3
            # to make approximately 3hz
            prev = cur
            yield polars

    def _classification_motion(self, motion_vector, bins):
        return _classification_motion_helper(motion_vector, bins)

    def _classification_video(self, polars):
        return np.array([_classification_video_helper(polar[0], polar[1]) for polar in polars])

    def _save_as_table(self, data, tag):
        tags = self.setting.tags
        if tag not in tags.keys():
            raise Exception('unsupported tag')
        directory = self.setting.save_result_path + tags['tbl']['dir'] \
            + tags[tag]['dir'] + self._scenario + tags['tbl']['ext']

        df = pd.DataFrame(data)
        df.index = self._timestamp[1:]
        df.index.name = tags['time']['Title']
        df.columns = [tags[tag]['title']]
        df.to_csv(directory)

    def _save_correaltion_as_table(self, data, tag):
        tags = self.setting.tags
        df = pd.DataFrame.from_dict(data)
        df.index = ['{:s}_{:s}'.format(tags['pearson']['title'], tags['correlation']['title']),
                    '{:s}_{:s}'.format(tags['pearson']['title'], tags['pvalue']['title']),
                    '{:s}_{:s}'.format(tags['spearmanr']['title'], tags['correlation']['title']),
                    '{:s}_{:s}'.format(tags['spearmanr']['title'], tags['pvalue']['title']),
                    '{:s}_{:s}'.format(tags['kendalltau']['title'], tags['correlation']['title']),
                    '{:s}_{:s}'.format(tags['kendalltau']['title'], tags['pvalue']['title'])]
        directory = self.setting.save_correlation_path + tags['tbl']['dir'] \
            + tags[tag]['dir'] + 'correaltion' + tags['tbl']['ext']
        df.to_csv(directory)

    def _save_as_graph(self, data, tag, xlabel, ylabel, ylim):
        from matplotlib import pyplot as plt
        from matplotlib.collections import LineCollection
        from matplotlib.colors import ListedColormap, BoundaryNorm

        tags = self.setting.tags
        if tag not in tags.keys():
            raise Exception('unsupported tag')
        directory = self.setting.save_result_path + tags['grp'] \
                    + tags[tag] + self._scenario + '.png'

        if not ylim:
            ylim = [min(data) - 0.1 * np.abs(min(data)),
                    max(data) + 0.1 * np.abs(max(data))]

        plt.clf()
        x = []
        y = []
        for i in range(len(data)-1):
            x.append(self._timestamp[1:][i])
            y.append(data[i])
            if data[i] * data[i + 1] <= 0:
                x.append((self._timestamp[1:][i] + self._timestamp[1:][i+1]) / 2)
                if data[i] > 0:
                    y.append(-0.0000000001)
                else:
                    y.append(0.000000001)
        i += 1
        x.append(self._timestamp[1:][i])
        y.append(data[i])

        points = np.array([x, y]).T.reshape(-1,1,2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        fig, axes = plt.subplots()
        axes.set_xlabel(xlabel, fontsize = 18)
        axes.set_ylabel(ylabel, fontsize = 18)
        axes.set_xlim(x[0], x[-1])
        axes.set_ylim(ylim)
        cmap = ListedColormap(['C1', 'C0'])
        norm = BoundaryNorm([-10000000, 0, 10000000], cmap.N)

        lc = LineCollection(segments, cmap=cmap, norm=norm)
        lc.set_array(np.array([1 if t > 0 else -1 for t in y]))
        axes.add_collection(lc)

        plt.savefig(directory, dpi = 300, bbox_inches = "tight")
        plt.close()


@jit(nopython = True)
def _classification_motion_helper(motion_vector, bins):
    modifier = 1
    ret = 0
    for i in range(len(motion_vector)):
        for j in range(len(bins[i])):
            if motion_vector[i] < bins[i][j]:
                ret += (j-2) * modifier
                break
            elif motion_vector[i] >= bins[i][-1]:
                ret += (j-1) * modifier
        modifier *= 5
    return np.array(ret)

@jit(nopython = True)
def _classification_video_helper(mag, deg):
    tmp = 0
    if deg < 195:
        if deg < 105:
            if deg < 45:
                if deg > 15:
                    tmp = 1
            else:
                if deg < 75:
                    tmp = 2
                else:
                    tmp = 3
        else:
            if deg < 165:
                if deg < 135:
                    tmp = 4
                else:
                    tmp = 5
            else:
                tmp = 6
    else:
        if deg < 315:
            if deg < 255:
                if deg < 225:
                    tmp = 7
                else:
                    tmp = 8
            else:
                if deg < 285:
                    tmp = 9
                else:
                    tmp = 10
        else:
            if deg < 345:
                tmp = 11

    if mag < 20:
        if mag > 6:
            tmp += 12
    else:
        tmp += 24
    return tmp

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
