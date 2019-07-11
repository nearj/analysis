import numpy as np
import pandas as pd
import matplotlib
import preprocess_video as prevideo
import glob, os

from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from numba import jit

LOAD_MOTION_DIR   = './data/preprocessed/motion/'
LOAD_PROB_DIST    = 'prob_dist/'
LOAD_CUMUL_DIST   = 'cumul_dist/'
LOAD_COMPACT      = 'compact/'
LOAD_VIDEO_DIR    = './data/preprocessed/video/'

SAVE_DIR          = './data/processed/'

SAVE_TABLE_OPTION = 'table/'
SAVE_GRAPH_OPTION = 'graph/'
SAVE_OPT_DIF      = 'difference/'
SAVE_OPT_KLD      = 'kullback_leibler_divergence/'
SAVE_OPT_ENT      = 'entropy/'
SAVE_OPT_OPT      = 'optical_flow/'
SAVE_OPT_MOT      = 'motion/'
SAVE_OPT_PROB     = 'probability/'
SAVE_OPT_CUMUL    = 'cumulative/'

SAVE_OPT_20S      = '20s/'
SAVE_OPT_AFTER    = '20-60s/'

EXT_PNG           = '.png'
EXT_JSON          = '.json'
EXT_EXCEL         = '.xlsx'

EXP_SET = {'S1_pitch': 20, 'S1_yaw': 20, 'S1_roll': 20,
           'S1_surge': 20, 'S1_heave': 10, 'S1_sway': 20,
           'S2_pitch': 20, 'S2_yaw': 20, 'S2_roll': 20,
           'S2_surge': 20, 'S2_heave': 10, 'S2_sway': 20,
           'S3_pitch': 20, 'S3_yaw': 20, 'S3_roll': 20,
           'S3_surge': 20, 'S3_heave': 10, 'S3_sway': 20,
           'S4': 60, 'S5': 60, 'S6': 60}
# experiment set
# keys: name of experiment
# values: times of experiment

# def load_file(file, is_cumulative = False, is_compact = False):
def load_file(file):
    return pd.read_json(file).sort_index().to_numpy()

def load_motion_data_dir(directory = LOAD_MOTION_DIR):
    ret = {}
    for file in glob.glob(directory + "*" + EXT_JSON):
        ret[os.path.splitext(os.path.basename(file))[0]] = load_file(file)[:,1]
    return ret

def load_video_data_dir(directory = LOAD_VIDEO_DIR):
    ret = {}
    for file in glob.glob(directory + "*" + EXT_JSON):
        ret[os.path.splitext(os.path.basename(file))[0]] = load_file(file)
    return ret

def save_dir(data_list_with_tag, action, directory):
    for tmp in list(zip(*data_list_with_tag)):
        name = tmp[0]
        processed = action(tmp[1])

        df = pd.DataFrame(processed)
        save_json_path = directory + name + EXT_JSON
        save_excel_path = directory + name + EXT_EXCEL
        df.to_json(save_json_path)
        df.to_excel(save_excel_path)
    pass

def save_fig_dir(data_list_with_tag, action, directory, xlabel, ylabel, time):
    directory += str(time[0]) + '_' + str(time[1]) + 's/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    for tmp in list(zip(*data_list_with_tag)):
        name = tmp[0]
        processed = action(tmp[1])
        save_2d(processed, name, xlabel, ylabel, directory, time)
    plt.clf()
    pass

############################################ funcions ##############################################
@jit(forceobj=True)
def _kullback_helper(optflow, motion):
    ret = 0
    motion = np.log2(motion[0])
    for elt in optflow:
        ret += elt * np.log2(elt)
        ret -= elt * motion
    return ret

def kullback_leibler_divergence(optflow_dist, motion_dist, is_compact = False):
    ret = []
    for frame in optflow_dist:
        ret.append(_kullback_helper(frame, motion_dist))
    return ret

def default_preprocess(x, y):
    return x, y

def apply_on_dir(optflow_list, motion_list, action,
                 preprocess_at_file = default_preprocess):
    return [optflow_list[0],                                                 # add file names.
            [[action(*preprocess_at_file(data_file[0], data_file[1]))        # action
              for data_file in list(zip(*[data_dir[0], data_dir[1]]))]     # on file
             for data_dir in list(zip(*[optflow_list[1], motion_list[1]]))]] # on directory

def apply_on_file(optflow_data, motion_data, action,
                 preprocess_at_file = default_preprocess):
    return [action(*preprocess_at_file(data_file[0], data_file[1]))        # action
              for data_file in list(zip(*[optflow_data, motion_data]))]     # on file

def _to_difference_of_entropy(data):
    ret = []
    for tmp in data:
        tmp1 = 0
        for prob in tmp:
            if prob != 0:
                tmp1 += - prob * np.log2(prob)
        ret.append(tmp1)

    dif = []
    dif = [ret[i + 1] - ret[i] for i in range(len(ret) - 1)]
    dif = np.asarray(dif)
    return dif;

def _to_entropy(data):
    ret = []
    for tmp in data:
        tmp = np.asarray(tmp)
        ret.append(-np.sum(tmp[np.where(tmp > 0)[0]] * np.log2(tmp[np.where(tmp > 0)[0]])))
    return ret

def _to_cumulative(data):
    ret = []
    _sum = 0
    for tmp in data:
        _sum += tmp
        ret.append(_sum)
    return ret

def save_2d(data, name, xlabel, ylabel, directory, time, ylim = [-200000, 200000]):
    plt.clf()

    scale = int(np.ceil(float(len(data))/time[1]))
    start = time[0] * scale
    end = time[1] * scale
    x = np.linspace(time[0], time[1], end - start)
    y = np.asarray(data[slice(start, end)])
    z = np.array([1 if t >= 0 else -1 for t in y])

    points = np.array([x, y]).T.reshape(-1,1,2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fig, axes = plt.subplots()
    axes.set_xlabel(xlabel, fontsize = 18)
    axes.set_ylabel(ylabel, fontsize = 18)
    axes.set_xlim(time)
    axes.set_ylim(ylim)
    cmap = ListedColormap(['C1', 'C0'])
    norm = BoundaryNorm([-10000000, 0, 10000000], cmap.N)

    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(z)
    axes.add_collection(lc)

    plt.savefig(directory + name + EXT_PNG, dpi = 300, bbox_inches = "tight")
    plt.close()
    pass

def do_it(target, max_time):
    optflow_dist = prevideo.opt_flow_prob_from_file('./data/raw/video/' + target + '.mp4')
    optflow_dist = optflow_dist[:(max_time * 3)] # here
    directory = SAVE_DIR + SAVE_GRAPH_OPTION + SAVE_OPT_ENT + SAVE_OPT_OPT
    ent = _to_entropy(optflow_dist)
    save_2d(ent, target, 'sec', 'entropy', directory, [0,max_time], [0, 300000])

    motion_prob_dist_list = load_motion_data_dir()
    if target in ['S1_surge', 'S1_sway', 'S2_surge', 'S2_sway', 'S3_surge', 'S3_sway']:
        motion_dist = np.ones(len(motion_prob_dist_list[target])) * 0.1
    elif target in ['S4', 'S5', 'S6']:
        motion_dist = motion_prob_dist_list[target] * 0.1
    else:
        motion_dist = motion_prob_dist_list[target]
    directory = SAVE_DIR + SAVE_GRAPH_OPTION + SAVE_OPT_KLD
    kld = kullback_leibler_divergence(optflow_dist, motion_dist)
    save_2d(kld, target, 'sec', 'entropy', directory, [0, max_time])

def main(idx):
    targets0 = ['S1_pitch', 'S1_yaw', 'S1_roll', 'S1_surge', 'S1_sway',
           'S2_pitch', 'S2_yaw', 'S2_roll', 'S2_surge', 'S2_sway',
           'S3_pitch', 'S3_yaw', 'S3_roll', 'S3_surge', 'S3_sway']
    targets1 = ['S4', 'S5', 'S6']
    targets2 = ['S1_heave', 'S2_heave', 'S3_heave']
    target_set = [targets0, targets1, targets2]
    if idx == 0:
        max_time = 20
    elif idx == 1:
        max_time = 60
    else:
        max_time = 10
    for target in target_set[idx]:
        do_it(target, max_time)


# optflow_dist_list = prevideo.opt_flow_prob_from_dir(prevideo.LOAD_DIR)
# motion_prob_dist_list = load_motion_data_dir(is_compact = True)

# motion_cumul_dist_list = load_motion_data_dir(is_cumulative = True, is_compact = True)
# kld_prob_list = apply_on_dir(optflow_dist_list, motion_prob_dist_list,
                             # kullback_leibler_divergence,
                             # lambda x, y: (x, y))
# kld_cumul_list = apply_on_dir(optflow_dist_list, motion_cumul_dist_list,
                              # kullback_leibler_divergence,
                              # lambda x, y: (x, y))


# directory = SAVE_DIR + SAVE_TABLE_OPTION + SAVE_OPT_ENT + SAVE_OPT_OPT
# save_dir(optflow_dist_list, _to_entropy, directory)

# directory = SAVE_DIR + SAVE_GRAPH_OPTION + SAVE_OPT_ENT + SAVE_OPT_OPT
# save_fig_dir(optflow_dist_list,
#              _to_entropy,
#              directory,
#              'sec',
#              'entropy',
#              [0,60])

# save_graph = SAVE_DIR + SAVE_GRAPH_OPTION + SAVE_OPT_ENT + SAVE_OPT_MOT + SAVE_OPT_PROB
# save_fig_dir(kld_prob_list,
#              lambda x: x,
#              save_graph,
#              'sec',
#              'entropy')

# for optflow in list(zip(*optflow_dist_list)):
#     plt.cla()
#     name = optflow[0]
#     dif = _to_difference_of_entropy(optflow[1])
#     save_2d(dif, name)
