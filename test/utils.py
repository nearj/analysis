import numpy as np
import pandas as pd
import matplotlib
import preprocess_video_data as prevideo
import glob, os

from matplotlib import pyplot as plt
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
           'S1_surge': 20, 'S1_heave': 20, 'S1_sway': 20,
           'S2_pitch': 20, 'S2_yaw': 20, 'S2_roll': 20,
           'S2_surge': 20, 'S2_heave': 20, 'S2_sway': 20,
           'S3_pitch': 20, 'S3_yaw': 20, 'S3_roll': 20,
           'S3_surge': 20, 'S3_heave': 20, 'S3_sway': 20,
           'S4': 60, 'S5': 60, 'S6': 60}
# experiment set
# keys: name of experiment
# values: times of experiment

# def load_file(file, is_cumulative = False, is_compact = False):
def load_file(file):
    """load file with name

    Args:
       file (str): the name of file

    Returns:
        (list) data in file

    """
    return pd.read_json(file).sort_index().to_numpy()



def load_motion_data_dir(directory = LOAD_MOTION_DIR, is_cumulative = False, is_compact = False):
    if is_cumulative:
        directory += LOAD_CUMUL_DIST
    else:
        directory += LOAD_PROB_DIST

    if is_compact:
        directory += LOAD_COMPACT

    tmp_data_list = []
    name_list = []
    for file in glob.glob(directory + "*" + EXT_JSON):
        tmp_data_list.append(load_file(file))
        name_list.append(os.path.splitext(os.path.basename(file))[0])

    verbose_list = None
    data_list = []
    if is_compact:
        # verbose_list = []
        for data in tmp_data_list:
            file_data = []
            # file_verbose = []
            for compact in data:
                compact_data = []
                # compact_verbose = []
                for tmp in compact:
                    if tmp:
                        compact_data.append(tmp)
                file_data.append(compact_data)
                # file_verbose.append(compact_verbose)
            data_list.append(file_data)
            # verbose_list.append(file_verbose)
    else:
        data_list = tmp_data_list

    return [name_list, data_list, verbose_list]
def load_motion_data_dir(directory = LOAD_MOTION_DIR):
    """ load motion data from directroy

    Args:
       directory directory for load data (default LOAD_MOTION_DIR = './data/preprocessed/motion/')

    Returns:
        (list) [name_list, data_list, verbost_list]
    """
    tmp_data_list = []
    name_list = []
    ret = {}

    for file in glob.glob(directory + "*" + EXT_JSON):

        tmp_data_list.append(load_file(file))
        name_list.append(os.path.splitext(os.path.basename(file))[0])




def load_video_data_dir(directory = LOAD_VIDEO_DIR):
    data_list = []
    name_list = []
    for file in glob.glob(directory + "*" + EXT_JSON):
        data_list.append(load_file(file))
        name_list.append(os.path.splitext(os.path.basename(file))[0])

    return [name_list, data_list]

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

def save_2d(data, name, xlabel, ylabel, directory, time):
    plt.clf()
    plt.xlabel(xlabel, fontsize = 18)
    plt.ylabel(ylabel, fontsize = 18)
    # plt.ylim([0,4.3])
    scale = int(np.ceil(float(len(data))/60))
    # scale = int(np.ceil(float(len(data))/20))
    # print(scale)
    start = time[0] * scale
    end = time[1] * scale
    print(start, end)
    plt.plot(np.linspace(time[0], time[1], end - start), data[slice(start, end)])

    plt.savefig(directory + name + EXT_PNG, dpi = 300, bbox_inches = "tight")
    plt.close()
    pass

def kullback_leibler_divergence(optflow_dist, motion_dist, is_compact = False):
    # assert optical flows[0] == motion data[0]; is it same file?
    # optflow_dist = np.asarray(optflow_dist)
    # non_zero_optflow_dist = optflow_dist[np.where(optflow_dist > 0)[0]]
    # non_zero_optflow_dist= optflow_dist
    # if is_compact:
        # non_zero_motion_dist = np.asarray(motion_dist)
    # else:
        # non_zero_motion_dist = np.asarray(
            # [0.0001 if tmp == 0 else tmp for tmp in motion_dist])

    ret = []
    # for tmp in non_zero_motion_dist:
        # ret += np.sum(non_zero_optflow_dist * np.log2(non_zero_optflow_dist) -
                      # non_zero_optflow_dist * np.log2(tmp))

    for frame in optflow_dist:
        # ret += tmp * np.log2(tmp) - tmp * np.log2(motion_dist)
        ret.append(_kullback_helper(frame, motion_dist[0]))
    return ret

@jit(forceobj=True)
def _kullback_helper(optflow, motion):
    ret = 0
    motion = np.log2(motion[0])
    for elt in optflow:
        ret += elt * np.log2(elt)
        ret -= elt * motion
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

def to_difference_of_entropy(data):
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

def to_entropy(data):
    ret = []
    for tmp in data:
        tmp = np.asarray(tmp)
        ret.append(-np.sum(tmp[np.where(tmp > 0)[0]] * np.log2(tmp[np.where(tmp > 0)[0]])))
    return ret

def to_cumulative(data):
    ret = []
    _sum = 0
    for tmp in data:
        _sum += tmp
        ret.append(_sum)
    return ret

def do_it(target):
    optflow_dist = prevideo.opt_flow_prob_from_file('./data/raw/video/' + target + '.mp4')
    optflow_dist = optflow_dist[:180]
    directory = SAVE_DIR + SAVE_GRAPH_OPTION + SAVE_OPT_ENT + SAVE_OPT_OPT
    ent = to_entropy(optflow_dist)
    save_2d(ent, target, 'sec', 'entropy', directory + '60s/', [0,60])
    # save_2d(ent, target, 'sec', 'entropy', directory, [0,20])

    motion_prob_dist_list = load_motion_data_dir(is_compact=True)
    motion_prob_dist_list[0]

    motion_dist = motion_prob_dist_list[1][motion_prob_dist_list[0].index(target)]
    directory = SAVE_DIR + SAVE_GRAPH_OPTION + SAVE_OPT_KLD
    kld = kullback_leibler_divergence(optflow_dist, motion_dist)
    save_2d(kld, target, 'sec', 'entropy', directory + '60s/', [0, 60])
    # save_2d(kld, target, 'sec', 'entropy', directory, [0, 20])


targets = ['S1_pitch', 'S1_yaw', 'S1_roll', #'S1_surge',
           'S1_heave',
           'S2_pitch', 'S2_yaw', 'S2_roll', #'S2_surge',
           'S2_heave',
           'S3_pitch', 'S3_yaw', 'S3_roll', #'S3_surge',
           'S3_heave']
for target in targets:
    do_it(target)


# optflow_dist_list = prevideo.opt_flow_prob_from_dir(prevideo.LOAD_DIR)
# motion_prob_dist_list = load_motion_data_dir(is_compact = True)

# motion_cumul_dist_list = load_motion_data_dir(is_cumulative = True, is_compact = True)
# kld_prob_list = apply_on_dir(optflow_dist_list, motion_prob_dist_list,
                             # kullback_leibler_divergence,
                             # lambda x, y: (x, y))
# kld_cumul_list = apply_on_dir(optflow_dist_list, motion_cumul_dist_list,
                              # kullback_leibler_divergence,
                              # lambda x, y: (x, y))


directory = SAVE_DIR + SAVE_TABLE_OPTION + SAVE_OPT_ENT + SAVE_OPT_OPT
save_dir(optflow_dist_list, to_entropy, directory)

directory = SAVE_DIR + SAVE_GRAPH_OPTION + SAVE_OPT_ENT + SAVE_OPT_OPT
save_fig_dir(optflow_dist_list,
             to_entropy,
             directory,
             'sec',
             'entropy',
             [0,60])

save_graph = SAVE_DIR + SAVE_GRAPH_OPTION + SAVE_OPT_ENT + SAVE_OPT_MOT + SAVE_OPT_PROB
save_fig_dir(kld_prob_list,
             lambda x: x,
             save_graph,
             'sec',
             'entropy')

for optflow in list(zip(*optflow_dist_list)):
    plt.cla()
    name = optflow[0]
    dif = to_difference_of_entropy(optflow[1])
    save_2d(dif, name)
