import numpy as np
import pandas as pd
import glob, os, codecs
import cv2

from numba import jit

import configure
from . import datamanager

class UOS2018(datamanager.DataManager):
    def __init__(self, *args, **kwargs):
        super(UOS2018, self).__init__(*args, **kwargs)
        setting = kwargs.get('conf').THREEDI
        self._scenarios   = setting['scenarios']
        self._sensored    = setting['motion']['sensored']
        self._time_column = setting['time']['time_column']
        self._unsensored  = [axis for axis in self._axis if axis not in self._sensored.keys()]
        self._start_index = setting['time']['start_index']
        self._end_index   = setting['time']['end_index']
        self._step_min    = setting['time']['step_min']
        self._step_max    = setting['time']['step_max']

    def _get_scenarios():
        return self._scenarios

    def _load(self):
        motion_load_directory = self._load_motion_dir + self._scenario + self._extension['csv']
        video_load_directory = self._load_video_dir + self._scenario + '/'

        df = pd.read_csv(motion_load_directory)

        times = pd.to_datetime(df[self._time_column].str.split().str[1]).astype(int) / 10 ** 9
        times -= times[self._start_index]
        sampled_indices, sampled_deltatimes = self._sampling_time(times)

        self._timestamp = times[sampled_indices]

        sensored_motion_vectors = np.diff(df[self._sensored.values()].values, axis = 0)
        # order: pitch, yaw, roll
        motion_vectors = np.hstack((
            sensored_motion_vectors, np.zeros((
                sensored_motion_vectors.shape[0], len(self._unsensored)))))

        return zip(*(self._classification_motion(
            self._sampling_motion(sampled_deltatimes, sampled_indices, motion_vectors)), \
            self._sampling_video_with_classification(sampled_deltatimes,
                                                     sampled_indices,
                                                     video_load_directory)))

    def _classification_video(self, mag, deg):
        return _classification_video_helper(mag, deg)

    def _sampling_time(self, times):
        delta_time = 0
        j = self._start_index
        ret_dts = [] # delta times
        ret_ind = [self._start_index] # sampled indices
        for i in range(self._start_index, self._end_index):
            if times[i] - times[j] >= self._step_min:
                ret_dts.append(times[i] - times[j])
                ret_ind.append(i)
                j = i
            elif delta_time > self._step_max:
                raise Exception('time sampling exceed step max({})'.format(times[i] - times[j]))
        return np.array(ret_ind, dtype = np.int), np.array(ret_dts)

    def _sampling_motion(self, delta_times, indices, motion_vectors):
        j = indices[0]
        ret = []
        for x in list(zip(indices[1:], delta_times)):
            ret.append(np.sum(motion_vectors[j:x[0]] /  x[1], axis = 0))
            j = x[0]
        return ret

    def _sampling_video_with_classification(self, delta_times, indices, load_dir):
        prev = cv2.cvtColor(cv2.imread(load_dir + "{:0>4d}.png".format(indices[0])),
                            cv2.COLOR_BGR2GRAY)
        for x in list(zip(indices[1:], delta_times)):
            cur = cv2.cvtColor(cv2.imread(load_dir +
                                          "{:0>4d}.png".format(x[0])), cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prev, cur, None, 0.5, 4, 15, 3, 5, 1.2, 0)
            polars = np.asarray(cv2.cartToPolar(flow[...,0], flow[...,1], None, None, True))
            # polars = polars.reshape(2, polars.shape[1] * polars.shape[2]).T / x[1] * 3 # TO-DO: 3hz?
            polars = polars.reshape(2, polars.shape[1] * polars.shape[2]).T / x[1] / 3
            prev = cur
            yield np.array([self._classification_video(polar[0], polar[1]) for polar in polars])

    def _classification_motion(self, motion_vectors):
        max_values = np.max(np.abs(motion_vectors), axis = 0)
        bins = [self._bin_seperator * m for m in max_values]
        for mv in motion_vectors:
            yield self._classification_motion_helper(mv, bins)

    def _classification_motion_helper(self, motion_vector, bins):
        modifier = 1
        ret = 0
        for i in range(len(motion_vector)):
            if bins[i][0] == bins[i][1]:
                ret += 2 * modifier
                modifier *= 5
                continue
            if motion_vector[i] >= bins[i][-1]:
                ret += 4 * modifier
                modifier *= 5
                continue
            for j in range(len(bins[i])):
                if motion_vector[i] < bins[i][j]:
                    ret += j * modifier
                    modifier *= 5
                    break
            else:
                continue
        return np.array(ret)

    def _save_as_table(self, data, tag):
        if tag not in self._save_options.keys():
            raise Exception('unsupported tag')
        directory = self._save_dir + self._save_options['pro'] + self._save_options['tbl'] + \
                    self._save_options[tag] + self._scenario + self._extension['csv']

        df = pd.DataFrame(data)
        df.index = self._timestamp[1:]
        df.columns = [time, self._save_options[tag]]
        df.to_csv(directory)

    def _save_as_graph(self, data, tag, xlabel, ylabel, ylim):
        from matplotlib import pyplot as plt
        from matplotlib.collections import LineCollection
        from matplotlib.colors import ListedColormap, BoundaryNorm

        if tag not in self._save_options.keys():
            raise Exception('unsupported tag')
        directory = self._save_dir + self._save_options['pro'] + self._save_options['grp'] + \
                    self._save_options[tag] + self._scenario + self._extension['png']

        if not ylim:
            ylim = [min(data) - 0.1 * np.abs(min(data)),
                    max(data) + 0.1 * np.abs(max(data))]

        plt.clf()
        x = []
        y = []
        for i in range(len(data)-1):
            x.append(self._timestamp[1:].iloc[i])
            y.append(data[i])
            if data[i] * data[i + 1] <= 0:
                x.append((self._timestamp[1:].iloc[i] + self._timestamp[1:].iloc[i+1]) / 2)
                if data[i] > 0:
                    y.append(-0.0000000001)
                else:
                    y.append(0.000000001)
        i += 1
        x.append(self._timestamp[1:].iloc[i])
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
