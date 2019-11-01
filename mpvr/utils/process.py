import numpy as np
from numba import jit
from scipy.stats import linregress
from scipy.stats import spearmanr
from scipy.stats import kendalltau

def make_histogram(src, histograms):
    motion_histogram = histograms[0]
    video_histogram = histograms[1]
    for data in src:
        _make_histogram_helper(motion_histogram, np.array([data[0]]))
        _make_histogram_helper(video_histogram, data[1])

def mapping_src_to_histogram(src, histograms, factor = 1):
    for data in src:
        yield histograms[0][data[0].ravel()] * factor, histograms[1][data[1].ravel()]

def to_mp_entropy(mapped_src):
    for data in mapped_src:
        yield _to_mp_entropy_helper(data[0], data[1])

def to_entropy(data_src): # HERE!
    for data in data_src:
        yield _to_entropy_helper(data)

def correlation(data, incidence):
    p = linregress(data, incidence)
    s = spearmanr(data, incidence)
    k = kendalltau(data, incidence)
    return p.rvalue, p.pvalue, s.correlation, s.pvalue, k.correlation, k.pvalue

def absolute_category_rating(data_src, grid):
    res = []
    for i in range(len(data_src)):
        if data_src[i] < grid[1]:
            if data_src[i] < grid[0]:
                res.append(5)
            else: res.append(4)
        else:
            if data_src[i] < grid[3]:
                if data_src[i] < grid[2]:
                    res.append(3)
                else:
                    res.append(2)
            else: res.append(1)
    return res


@jit(nopython = True)
def _make_histogram_helper(histogram, data):
    for elt in data:
        histogram[elt] += 1

# @jit(nopython = True)
# def _make_histogram_helper(histogram, data):
#     for i in range(len(histogram)):
#         histogram[i] += np.sum(data == i)

# @cuda.jit
@jit(nopython = True)
def _to_mp_entropy_helper(motion, video):
    return np.sum(video * (np.log2(video) - np.log2(motion)))

@jit(nopython = True)
def _to_entropy_helper(data):
    return np.sum(data * np.log2(data)) * -1
