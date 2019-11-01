import numpy as np
import pandas as pd
import glob, os

LOAD_MOTION_DIR = './data/processed/motion/'
LOAD_PROB_DIST = 'prob_dist/'
LOAD_CUMUL_DIST = 'cumul_dist/'
LOAD_COMPACT = 'compact/'
LOAD_VIDEO_DIR = './data/processed/video/'

SAVE_DIR = './data/processed/'

SAVE_GRAPH_OPTION = 'graph/'
SAVE_OPT_DIF_20S = 'optical_flow_dif_20s/'

EXT_PNG = '.png'
EXT_JSON = '.json'
EXT_EXCEL = '.xlsx'

def load_file(file, is_cumulative = False, is_compact = False):
    return pd.read_json(file).sort_index().to_numpy()

def load_motion_data_dir(dir = LOAD_MOTION_DIR, is_cumulative = False, is_compact = False):
    if is_cumulative:
        dir += LOAD_CUMUL_DIST
    else:
        dir += LOAD_PROB_DIST

    if is_compact:
        dir += LOAD_COMPACT

    tmp_data_list = []
    name_list = []
    for file in glob.glob(dir + "*" + EXT_JSON):
        tmp_data_list.append(load_file(file))
        name_list.append(os.path.splitext(os.path.basename(file))[0])

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
            data_list.append(file_data)
            verbose_list.append(file_verbose)
    else:
        data_list = tmp_data_list

    return [name_list, data_list, verbose_list]

def load_video_data_dir(dir = LOAD_VIDEO_DIR):
    data_list = []
    name_list = []
    for file in glob.glob(dir + "*" + EXT_JSON):
        data_list.append(load_file(file))
        name_list.append(os.path.splitext(os.path.basename(file))[0])

    return [name_list, data_list]

def save_data(data):
    pass

def save_dir(dir):
    pass

def save_fig_dir(data):
    pass

def kullback_leibler_divergence_per_frame(optflow_dist_per_frame, motion_dist_per_frame):
    # assert optical flows[0] == motion data[0]; is it same file?
    non_zero_optflow_dist = optflow_dist_per_frame[np.where(optflow_dist_per_frame > 0)[0]]
    non_zero_motion_dist = np.asarray(motion_dist_per_frame)
    res = 0
    for tmp in non_zero_motion_dist:
        res += np.sum(non_zero_optflow_dist * np.log2(non_zero_optflow_dist) -
                      non_zero_optflow_dist * np.log2(tmp))
    return res / len(motion_dist_per_frame)

def action_on_file(optflow_dist_per_file, motion_dist_per_file, action):
    optflow_dist_per_file = optflow_dist_per_file
    return [action(tmp[0], tmp[1]) for tmp
            in list(zip(*[optflow_dist_per_file, motion_dist_per_file]))]

def apply_on_dir(optflow_list, motion_list, action):
    name_list = optflow_list[0]
    return [name_list,
            [action_on_file(tmp[0][:-1:2], tmp[1], action) for tmp
             in list(zip(*[optflow_list[1], motion_list[1]]))]]

def difference_opt_flow_entrophy(optical_flow):
    res = []
    for data in data_list:
        tmp = 0
        for prob in data:
            if prob != 0:
                tmp += - prob * np.log2(prob)
        res.append(tmp)

    dif = []
    dif = [res[i + 1] - res[i] for i in range(len(res) - 1)]
    dif = np.asarray(dif)
    return dif;

def save_dif_opt_flow_entropy(dif_opt_flow_ent, filename,
                              dir = SAVE_DIR + SAVE_GRAPH_OPTION,
                              save_20s = False):
    if save_20s:
        plt.plot(np.linspace(2, 20, 54), dif_opt_flow_ent[12:120:2])
    else:
        plt.plot(range(len(dif_opt_flow_ent)), dif_opt_flow_ent)
    plt.savefig(dir + filename)
