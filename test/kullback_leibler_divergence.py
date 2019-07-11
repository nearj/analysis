import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import glob, os

LOAD_MOTION_DIR = './data/preprocessed/motion/'
LOAD_PROB_DIST = 'prob_dist/'
LOAD_CUMUL_DIST = 'cumul_dist/'
LOAD_COMPACT = 'compact/'
LOAD_VIDEO_DIR = './data/preprocessed/video/'

SAVE_DIR = './data/processed/'

SAVE_TABLE_OPTION = 'table/'
SAVE_GRAPH_OPTION = 'graph/'
SAVE_OPT_DIF = 'difference/'
SAVE_OPT_KLD = 'kullback_leibler_divergence/'
SAVE_OPT_ENT = 'entropy/'
SAVE_OPT_OPT = 'optical_flow/'
SAVE_OPT_MOT = 'motion/'
SAVE_OPT_PROB = 'probability/'
SAVE_OPT_CUMUL = 'cumulative/'

SAVE_OPT_20S = '20s/'
SAVE_OPT_AFTER = '20-60s/'

EXT_PNG = '.png'
EXT_JSON = '.json'
EXT_EXCEL = '.xlsx'

def load_file(file, is_cumulative = False, is_compact = False):
    return pd.read_json(file).sort_index().to_numpy()

def load_motion_data_dir(directory = LOAD_MOTION_DIR, is_cumulative = False, is_compact = False):
    if is_cumulative:
        directory += LOAD_CUMUL_DIST
    else:
        directory += LOAD_PROB_DIST

    if is_compact:
        directory += LOAD_COMPACT

    tmp = {}
    tmp_data_list = []
    name_list = []
    for file in glob.glob(directory + "*" + EXT_JSON):
        tmp[os.path.splitext(os.path.basename(file))[0]] = load_file(file)
        tmp_data_list.append()
        name_list.append()

    ret = {}
    if is_compact:
        verbose_list = []
    verbose_list = None
    data_list = []
    if is_compact:
        verbose_list = []
        for data in tmp_data_list:
            file_data = []
            file_verbose = []
            for compact in data:
                compact_data = []
                compact_verbose = []
                for tmp in compact:
                    if tmp:
                        compact_data.append(tmp[-1])
                        compact_verbose.append(tmp[0:-1])
                file_data.append(compact_data)
                file_verbose.append(compact_verbose)
            ret
            data_list.append(file_data)
            verbose_list.append(file_verbose)
    else:
        data_list = tmp_data_list

    return [name_list, data_list, verbose_list]

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

def save_2d(data, name, xlabel, ylabel, directory, time):
    plt.clf()
    plt.xlabel(xlabel, fontsize = 18)
    plt.ylabel(ylabel, fontsize = 18)
    # plt.ylim([0,4.3])
    scale = int(np.ceil(float(len(data))/60))
    start = time[0] * scale
    end = time[1] * scale
    plt.plot(np.linspace(time[0], time[1], end - start), data[slice(start, end)])

    plt.savefig(directory + name + EXT_PNG, dpi = 300, bbox_inches = "tight")
    plt.close()
    pass

def kullback_leibler_divergence(optflow_dist, motion_dist, is_compact = False):
    # assert optical flows[0] == motion data[0]; is it same file?
    non_zero_optflow_dist = optflow_dist[np.where(optflow_dist > 0)[0]]
    if is_compact:
        non_zero_motion_dist = np.asarray(motion_dist)
    else:
        non_zero_motion_dist = np.asarray(
            [0.0001 if tmp == 0 else tmp for tmp in motion_dist])
        
    ret = 0
    for tmp in non_zero_motion_dist:
        ret += np.sum(non_zero_optflow_dist * np.log2(non_zero_optflow_dist) -
                      non_zero_optflow_dist * np.log2(tmp))
    return ret 

def default_preprocess(x, y):
    return x, y

def apply_on_dir(optflow_list, motion_list, action,
                 preprocess_at_file = default_preprocess):
    return [optflow_list[0],                                                 # add file names.
            [[action(*preprocess_at_file(data_file[0], data_file[1]))        # action
              for data_file in list(zip(*[data_dir[0], data_dir[1]]))]     # on file
             for data_dir in list(zip(*[optflow_list[1], motion_list[1]]))]] # on directory

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

optflow_dist_list = load_video_data_dir()
motion_prob_dist_list = load_motion_data_dir(is_compact = True)
motion_cumul_dist_list = load_motion_data_dir(is_cumulative = True, is_compact = True)
kld_prob_list = apply_on_dir(optflow_dist_list, motion_prob_dist_list,
                             kullback_leibler_divergence,
                             lambda x, y: (x, y))
kld_cumul_list = apply_on_dir(optflow_dist_list, motion_cumul_dist_list,
                              kullback_leibler_divergence,
                              lambda x, y: (x, y))


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
