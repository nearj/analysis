import numpy as np
import pandas as pd
import glob, os, codecs

from etaprogress.progress import ProgressBar

_sub_bin_names = ['pitch', 'yaw', 'roll', 'surge', 'heave', 'sway']
RAW_DATA_FRAME_SIZE = 6

RAW_DATA_DIR = './data/raw/motion/'
EXT_RAW_DATA = '.txt'
EXT_RAW_META = '.meta'
EXT_JSON     = '.json'
EXT_EXCEL    = '.xlsx'
SAVE_DIR  = './data/preprocessed/motion/'

def _load_file(directory):
    """ load file from directory

    Args:
       directory directory to load

    Returns:
        (str), [[arr]]

    """
    _raw_data = np.genfromtxt(codecs.open(directory).
                              readline().replace(u'\ufeff', '').split(' ')[:-1], dtype='i4')
    return _raw_data.reshape(_raw_data.size / RAW_DATA_FRAME_SIZE, RAW_DATA_FRAME_SIZE)

def _load_dir(directory=RAW_DATA_DIR):
    """load files from directory

    Args:
       directory (str) directory to load (default RAW_DATA_DIR: ./data/raw/motion)

    Returns:
        {(str): [[arr]]} all data in directory of format txt-files about sampled at 3hz
    """

    ret = {}
    for _file in glob.glob(directory + "*" + EXT_RAW_DATA):
        _file_name = os.path.splitext(os.path.basename(_file))[0]
        _raw_data = np.genfromtxt(codecs.open(_file, encoding='UTF8').
                                  readline().replace(u'\ufeff', '').split(' ')[:-1], dtype='i4')
        ret[_file_name] = _raw_data.reshape((int)(_raw_data.size / RAW_DATA_FRAME_SIZE),
                                            RAW_DATA_FRAME_SIZE)
    return ret

def _save(save_dir, rows, data):
    """ save data to directory

    Args:
       save_dir (str)
       data (var)
    """
    save_json_path = save_dir+ EXT_JSON
    save_excel_path = save_dir + EXT_EXCEL

    df = pd.DataFrame(data = list(zip(*[rows, data])), columns=['motion vector', 'probability'])
    df.to_json(save_json_path)
    df.to_excel(save_excel_path)

def _make_lookup_tbl(motion_vectors):
    """ make lookup table in file(scanning) which check probability of a motion vector of a frame up
        to all frames to decide the motion vector is how many occured in the experiment

    Args:
       motion_vectors (arr;2d) data for make lookup table

    Returns:
       tuple([arr], [float]) lookup-table to decide probability of a motion vector
    """

    ret = np.unique(motion_vectors, axis=0, return_counts=True)
    ret = (ret[0], ret[1] / ret[1].sum())
    return ret

def _to_probability(motion_vectors):
    """ decide probabiltiy of a motion vectors

    Args:
       motion_vectors (arr; 2d)

    Returns:
       tuple([arr], [float]) the probabiltiy of a motion vectors in frames
    """
    for mtvec in motion_vectors:
        mtvec[3] = 0 # surge
        mtvec[5] = 0 # sway
    lookup_tbl = _make_lookup_tbl(motion_vectors)
    _tmp_prob = []
    for mtvec in motion_vectors:
        for i in range(len(lookup_tbl[0])):
            if np.array_equal(mtvec, lookup_tbl[0][i]):
                _tmp_prob.append(lookup_tbl[1][i])
    return motion_vectors, _tmp_prob


def main():
    load = _load_dir()
    for key in load.keys():
        mtvecs, probs = _to_probability(load[key])
        save_dir = SAVE_DIR + key
        _save(save_dir, mtvecs, probs)

if __name__ == '__main__':
    main()
