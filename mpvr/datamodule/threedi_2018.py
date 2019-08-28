import numpy as np
import pandas as pd
import cv2
from numba import jit

def load_motion_gen(path, axes, sensored_axes_tag, target_sampling_rate, indices, timediffs):
    df = pd.read_csv(path, encoding="ISO-8859-1")
    tmp = []
    for ax in axes:
        if ax in sensored_axes_tag.keys():
            mvs = np.diff(df[sensored_axes_tag[ax]][indices].values)
            tmp.append(mvs / timediffs[1:] / target_sampling_rate)
        else:
            tmp.append(np.zeros(len(indices[1:])))
    tmp = np.array(tmp).T
    for t in tmp:
        yield t

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
    return _classification_motion_helper(motion_vector, bins)

def make_bins(motion_data_gen, seperator):
    max_values = np.max(np.abs([mv for mv in motion_data_gen]), axis = 0)
    return np.array([np.array(seperator) * m for m in max_values])

def classification_visual(polars):
    return np.array(_classification_visual_helper(polars), dtype=int)

@jit(nopython = True)
def _classification_motion_helper(motion_vector, bins):
    modifier = 1
    ret = 0
    for i in range(len(motion_vector)):
        if bins[i][0] == bins[i][-1]:
            ret += 0
            modifier *= 5
            continue

        if motion_vector[i] >= bins[i][-1]:
            ret += 2 * modifier
        else:
            for j in range(len(bins[i])):
                if motion_vector[i] < bins[i][j]:
                    ret += (j-2) * modifier
                    break
        modifier *= 5
    return np.array(ret)

@jit(nopython = True)
def _classification_visual_helper(polars):
    ret = np.zeros(polars.shape[0])
    for i in range(len(polars)):
        mag = polars[i,0]
        deg = polars[i,1]
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



# for polar in polars:
# tmp = []
# tmp.append((polars[:,0] <= 6) \
#            & ((polars[:,1] <= 15) | (polars [:,1] > 345)))
# tmp.append((polars[:,0] > 6) & (polars[:,0] <= 20) \
#            & ((polars[:,1] <= 15) | (polars [:,1] > 345)))
# tmp.append((polars[:,0] > 20) \
#            & ((polars[:,1] <= 15) | (polars [:,1] > 345)))

# j = 15
# for i in np.linspace(45, 345, 11):
#     tmp.append((polars[:,0] <= 6) \
#                & ((polars[:,1] > j) & (polars [:,1] <= i)))
#     tmp.append((polars[:,0] > 6) & (polars[:,0] <= 20) \
#                & ((polars[:,1] > j) & (polars [:,1] <= i)))
#     tmp.append((polars[:,0] > 20) \
#                & ((polars[:,1] > j) & (polars [:,1] <= i)))
#     j = i

# i = 0
# for i in range(12):
#     polars[tmp[3 * i]] = i + 0
#     polars[tmp[3 * i + 1]] = i + 12
#     polars[tmp[3 * i + 2]] = i + 24

# @jit(nopython = True)
# def _classification_visual_helper(mag, deg):
#     tmp = 0
#     if deg < 195:
#         if deg < 105:
#             if deg < 45:
#                 if deg > 15:
#                     tmp = 1
#             else:
#                 if deg < 75:
#                     tmp = 2
#                 else:
#                     tmp = 3
#         else:
#             if deg < 165:
#                 if deg < 135:
#                     tmp = 4
#                 else:
#                     tmp = 5
#             else:
#                 tmp = 6
#     else:
#         if deg < 315:
#             if deg < 255:
#                 if deg < 225:
#                     tmp = 7
#                 else:
#                     tmp = 8
#             else:
#                 if deg < 285:
#                     tmp = 9
#                 else:
#                     tmp = 10
#         else:
#             if deg < 345:
#                 tmp = 11

#     if mag < 20:
#         if mag > 6:
#             tmp += 12
#     else:
#         tmp += 24
#     return tmp

    # def _load_with_preset(self):
    #     """Implementation method of :meth:'mpvr.datamanager.Datamanager.load()'

    #     :returns: Generator of classified motion and video process in experiment
    #     :rtype: Iterator[(int, list)]
    #     """
    #     motion_load_directory = _load_motion_dir + _scenario + _extension['csv']
    #     video_load_directory = _load_video_dir + _scenario + '/'

    #     df = pd.read_csv(motion_load_directory)

    #     times = pd.to_datetime(df[_time_column].str.split().str[1]).astype(int) / 10 ** 9
    #     times -= times[_start_index] # to set timestamps 0 at start index
    #     sampled_indices, sampled_deltatimes = _sampling_time(times)
    #     # to make sampling rate approximately about 3hz as previous works

    #     sensored_motion_vectors = np.diff(df[_sensored.values()].values, axis = 0)
    #     # order: pitch, yaw, roll
    #     motion_vectors = np.hstack((
    #         sensored_motion_vectors, np.zeros((
    #             sensored_motion_vectors.shape[0], len(_unsensored)))))
    #     # to make 6 axis motion, e.g.) (1.1, 2.2, 3.3) > (1.1, 2.2, 3.3, 0, 0, 0)

    #     sampled_motion = _sampling_motion(sampled_deltatimes,
    #                                             sampled_indices,
    #                                             motion_vectors)
    #     sampled_video = _load_visual_gen_from_png(sampled_deltatimes,
    #                                           sampled_indices,
    #                                           video_load_directory)
    #     motion_bins = _make_motion_bins(sampled_motion)

    #     # TODO: stands for rewind... >
    #     sampled_motion = _sampling_motion(sampled_deltatimes,
    #                                             sampled_indices,
    #                                             motion_vectors)

    #     for sample in zip(*(sampled_motion, sampled_video)):
    #         yield classification_motion(sample[0], motion_bins), \
    #             classification_visual(sample[1])

# def load_visual_gen(path, indices):
#     cap = cv2.VideoCapture(path)
#     i = 0
#     while i < indices[0]:
#         cap.read()

#     frame_max = cap.get(cv2.CAP_PROP_FRAME_COUNT)
#     while i <= frame_max:
#         if i in indices:
#             yield cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
#         else:
#             cap.read()
#         i += 1
#     cap.release()
# def _load_visual_gen_from_png(path, target_sampling_rate, timediffs, indices):
#     prev =
#     for x in list(zip(indices[1:], timediffs)):
#         cur = cv2.cvtColor(cv2.imread(load_dir +
#                                       "{:0>4d}.png".format(x[0])), cv2.COLOR_BGR2GRAY)
#         flow = cv2.calcOpticalFlowFarneback(prev, cur, None, 0.5, 4, 15, 3, 5, 1.2, 0)
#         polars = np.asarray(cv2.cartToPolar(flow[...,0], flow[...,1], None, None, True))
#         polars = polars.reshape(2, polars.shape[1] * polars.shape[2]).T / x[1] / 3
#         # to make approximately 3hz
#         prev = cur
#         yield polars

# def _visual_src_maker(path, indices, extension):
#     if extension == '.mp4':
#         cap = cv2.VideoCapture(path)
#         for i in indices:
#             cap.set(cv2.CAP_PROP_POS_FRAMES, i)
#             yield cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
#         cap.release()

#     elif extension == '.png':
#         for i in indices:
#             yield cv2.cvtColor(cv2.imread(path + "{:0>4d}.png".format(i)),
#                                cv2.COLOR_BGR2GRAY)
