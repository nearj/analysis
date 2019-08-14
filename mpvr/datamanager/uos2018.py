import numpy as np
import pandas as pd
import cv2, codecs

from numba import jit

import configure
from . import datamanager

class UOS2018(datamanager.DataManager):
    def __init__(self, *args, **kwargs):
        super(UOS2018, self).__init__(*args, **kwargs)
        self._setting = kwargs.get('conf').UOS2018['scenarios']
        self._scenarios = self._setting.keys()
        self._roi = np.index_exp[:,:]

    def _get_scenarios(self):
        return self._scenarios

    def _load(self):
        motion_load_directory = self._load_motion_dir + self._scenario \
                                + self._setting[self._scenario]['motion']['extension']
        video_load_directory = self._load_video_dir + self._scenario \
                               + self._setting[self._scenario]['video']['extension']

        sampled_motion_data = np.genfromtxt(
            codecs.open(motion_load_directory, encoding='UTF8') \
            .readline() \
            .replace(u'\ufeff', '') \
            .split(' ')[:-1], dtype='i4')
        sampled_indices, sampled_timestamp = self._sampling_time()
        self._timestamp = sampled_timestamp
        sampled_motion = self._sampling_motion(sampled_motion_data)
        sampled_video = self._sampling_video(sampled_indices, video_load_directory)

        for sample in zip(*(sampled_motion, sampled_video)):
            yield self._classification_motion(sample[0]), \
                self._classification_video(sample[1])

    def _sampling_time(self):
        sampling_rate = self._setting[self._scenario]['motion']['sampling_rate']
        fps = self._setting[self._scenario]['video']['fps']
        time = self._setting[self._scenario]['video']['time']

        ret_indices = []
        ret_timestamp = []
        for t in range(fps * time + 1):
            if t % (fps / sampling_rate) == 0:
                ret_indices.append(t)
                ret_timestamp.append(t / fps)
        return ret_indices, ret_timestamp

    def _sampling_motion(self, motion_data):
        for mv in motion_data.reshape((int) (motion_data.size / len(self._axis))
                                      , len(self._axis)):
            mv[3] = 2 # surge
            mv[5] = 2 # sway
            yield mv

    def _sampling_video(self, sampled_indices, load_dir):
        cap = cv2.VideoCapture(load_dir)
        prev = cv2.cvtColor(cap.read()[1][self._roi], cv2.COLOR_BGR2GRAY)
        frame_max = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        frame_num = 1
        while frame_num <= frame_max:
            if frame_num in sampled_indices:
                cur = cv2.cvtColor(cap.read()[1][self._roi], cv2.COLOR_BGR2GRAY)
                flow = cv2.calcOpticalFlowFarneback(prev, cur, None, 0.5, 4, 15, 3, 5, 1.2, 0)
                polars = np.asarray(cv2.cartToPolar(flow[...,0], flow[...,1], None, None, True))
                yield polars.reshape(2, polars.shape[1] * polars.shape[2]).T
                prev = cur
            else:
                cap.read()
            frame_num += 1
        cap.release()

    def _classification_motion(self, motion_vector):
        return _classification_motion_helper(motion_vector)

    def _classification_video(self, polars):
        return np.array([_classification_video_helper(polar[0], polar[1]) for polar in polars])

    def _save_as_table(self, data, tag):
        if tag not in self._save_options.keys():
            raise Exception('unsupported tag')
        directory = self._save_dir + self._save_options['pro'] + self._save_options['tbl'] + \
                    self._save_options[tag] + self._scenario + self._extension['csv']
        df = pd.DataFrame(data)
        df.index = self._timestamp[1:]
        df.index.name = 'time'
        df.columns = [self._save_options[tag]]
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
            x.append(self._timestamp[i])
            y.append(data[i])
            if data[i] * data[i + 1] <= 0:
                x.append((self._timestamp[i] + self._timestamp[i+1]) / 2)
                if data[i] > 0:
                    y.append(-0.0000000001)
                else:
                    y.append(0.000000001)
        i += 1
        x.append(self._timestamp[i])
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
def _classification_motion_helper(motion_vector):
    modifier = 1
    ret = 0
    for axis_class in motion_vector:
        if axis_class == 0:     # low motion
            ret += 2 * modifier
        elif axis_class == 1:   # medium positive motion
            ret += 3 * modifier
        elif axis_class == 2:   # medium negative motion
            ret += 1 * modifier
        elif axis_class == 3:   # high positive motion
            ret += 4 * modifier
        else:                   # high negative motion
            ret += 0
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
