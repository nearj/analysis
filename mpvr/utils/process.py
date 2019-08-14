import numpy as np
from numba import jit

def make_histogram(src, sizes):
    motion_histogram = np.zeros(sizes[0])
    video_histogram = np.zeros(sizes[1])
    for motion, video in src:
        _make_histogram_helper(motion_histogram, np.array([motion]))
        _make_histogram_helper(video_histogram, video)
    return motion_histogram / np.sum(motion_histogram), video_histogram / np.sum(video_histogram)

def mapping_src_to_histogram(src, histograms):
    for motion, video in src:
        yield histograms[0][motion], histograms[1][video]

def to_mp_entropy(mapped_src):
    for motion, video in mapped_src:
        yield _to_mp_entropy_helper(motion, video)

def to_entropy(data_src): # HERE!
    for data in data_src:
        yield _to_entropy_helper(data)

@jit(nopython=True)
def _make_histogram_helper(histogram, data):
    for elt in data:
        histogram[elt] += 1

@jit(nopython=True)
def _to_mp_entropy_helper(motion, video):
    return np.sum(video * (np.log2(video) - np.log2(motion)))

@jit(nopython=True)
def _to_entropy_helper(data):
    return np.sum(data * np.log2(data)) * -1
