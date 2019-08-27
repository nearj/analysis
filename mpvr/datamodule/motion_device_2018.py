import numpy as np
import pandas as pd
import cv2
from numba import jit

def load_motion_gen(path, axes, sensored_axes_tag, target_sampling_rate, indices, timediffs):
    df = pd.read_csv(path, encoding="ISO-8859-1")
    unsensored_axes = ['surge', 'sway']
    for i in indices[1:]:
        ret = []
        for ax in axes:
            if ax in sensored_axes_tag.keys() and ax not in unsensored_axes:
                ret.append(df[sensored_axes_tag[ax]][i])
            else:
                ret.append(0)
        yield np.array(ret)

def load_visual_gen(path, target_sampling_rate, extension, indices, timediffs):
    src = _visual_src_maker(path, indices, extension)
    prev = next(src)
    for t in timediffs[1:]:
        cur = next(src)
        flow = cv2.calcOpticalFlowFarneback(prev, cur, None, 0.5, 4, 15, 3, 5, 1.2, 0)
        polars = np.asarray(cv2.cartToPolar(flow[...,0], flow[...,1], None, None, True))
        polars = polars.reshape(2, polars.shape[1] * polars.shape[2]).T / t \
            / target_sampling_rate
        prev = cur
        yield polars

def _visual_src_maker(path, indices, extension):
    if extension == '.mp4':
        cap = cv2.VideoCapture(path)
        max_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        for i in range(indices[0], int(max_frame)):
            if i in indices:
                yield cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
            else:
                cap.read()
        cap.release()

    elif extension == '.png':
        for i in indices:
            yield cv2.cvtColor(cv2.imread(path + "{:0>4d}.png".format(i)),
                               cv2.COLOR_BGR2GRAY)

def classification_motion(motion_vector, bins = None):
    return _classification_motion_helper(motion_vector)

def classification_visual(polars):
    return np.array(_classification_visual_helper(polars), dtype=int)

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
def _classification_visual_helper(polars):
    ret = np.zeros(polars.shape[0])
    for i in range(len(polars)):
        mag = polars[i,0]
        deg = polars[i,1]
        if mag < 6:
            if deg < 195:
                if deg < 105:
                    if deg < 45:
                        if deg > 15:
                            ret[i] = 1
                    else:
                        if deg < 75:
                            ret[i] = 2
                        else:
                            ret[i] = 3
                else:
                    if deg < 165:
                        if deg < 135:
                            ret[i] = 4
                        else:
                            ret[i] = 5
                    else:
                        ret[i] = 6
            else:
                if deg < 315:
                    if deg < 255:
                        if deg < 225:
                            ret[i] = 7
                        else:
                            ret[i] = 8
                    else:
                        if deg < 285:
                            ret[i] = 9
                        else:
                            ret[i] = 10
                else:
                    if deg < 345:
                        ret[i] = 11
        if mag < 20:
            if mag > 6:
                ret[i] += 12
        else:
            ret[i] += 24
    return ret


# def _save_as_table(self, data, tag):
#     if tag not in self._save_options.keys():
#         raise Exception('unsupported tag')
#     directory = self._save_dir + self._save_options['pro'] + self._save_options['tbl'] + \
#                 self._save_options[tag] + self._scenario + self._extension['csv']
#     df = pd.DataFrame(data)
#     df.index = self._timestamp[1:]
#     df.index.name = 'time'
#     df.columns = [self._save_options[tag]]
#     df.to_csv(directory)

# def _save_as_graph(self, data, tag, xlabel, ylabel, ylim):
#     from matplotlib import pyplot as plt
#     from matplotlib.collections import LineCollection
#     from matplotlib.colors import ListedColormap, BoundaryNorm

#     if tag not in self._save_options.keys():
#         raise Exception('unsupported tag')
#     directory = self._save_dir + self._save_options['pro'] + self._save_options['grp'] + \
#                 self._save_options[tag] + self._scenario + self._extension['png']

#     if not ylim:
#         ylim = [min(data) - 0.1 * np.abs(min(data)),
#                 max(data) + 0.1 * np.abs(max(data))]

#     plt.clf()
#     x = []
#     y = []
#     for i in range(len(data)-1):
#         x.append(self._timestamp[i])
#         y.append(data[i])
#         if data[i] * data[i + 1] <= 0:
#             x.append((self._timestamp[i] + self._timestamp[i+1]) / 2)
#             if data[i] > 0:
#                 y.append(-0.0000000001)
#             else:
#                 y.append(0.000000001)
#     i += 1
#     x.append(self._timestamp[i])
#     y.append(data[i])

#     points = np.array([x, y]).T.reshape(-1,1,2)
#     segments = np.concatenate([points[:-1], points[1:]], axis=1)

#     fig, axes = plt.subplots()
#     axes.set_xlabel(xlabel, fontsize = 18)
#     axes.set_ylabel(ylabel, fontsize = 18)
#     axes.set_xlim(x[0], x[-1])
#     axes.set_ylim(ylim)
#     cmap = ListedColormap(['C1', 'C0'])
#     norm = BoundaryNorm([-10000000, 0, 10000000], cmap.N)

#     lc = LineCollection(segments, cmap=cmap, norm=norm)
#     lc.set_array(np.array([1 if t > 0 else -1 for t in y]))
#     axes.add_collection(lc)

#     plt.savefig(directory, dpi = 300, bbox_inches = "tight")
#     plt.close()
# def _sampling_motion(self, motion_data):
#     for mv in motion_data.reshape((int) (motion_data.size / len(self._axis))
#                                   , len(self._axis)):
#         mv[3] = 2 # surge
#         mv[5] = 2 # sway
#         yield mv
# def _sampling_video(self, sampled_indices, load_dir):
#     cap = cv2.VideoCapture(load_dir)
#     prev = cv2.cvtColor(cap.read()[1][self._roi], cv2.COLOR_BGR2GRAY)
#     frame_max = cap.get(cv2.CAP_PROP_FRAME_COUNT)
#     frame_num = 1
#     while frame_num <= frame_max:
#         if frame_num in sampled_indices:
#             cur = cv2.cvtColor(cap.read()[1][self._roi], cv2.COLOR_BGR2GRAY)
#             flow = cv2.calcOpticalFlowFarneback(prev, cur, None, 0.5, 4, 15, 3, 5, 1.2, 0)
#             polars = np.asarray(cv2.cartToPolar(flow[...,0], flow[...,1], None, None, True))
#             yield polars.reshape(2, polars.shape[1] * polars.shape[2]).T
#             prev = cur
#         else:
#             cap.read()
#         frame_num += 1
#     cap.release()
