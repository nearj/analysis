import numpy as np
from numba import jit

def make_histogram(src, sizes):
    motion_histogram = np.zeros(sizes[0])
    video_histogram = np.zeros(sizes[1])
    for motion, video in src:
        motion_histogram[motion] += 1
        video_histogram[video] += 1
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
def _to_mp_entropy_helper(motion, video):
    return np.sum(video * (np.log2(video) - np.log2(motion)))

@jit(nopython=True)
def _to_entropy_helper(data):
    return np.sum(data * np.log2(data)) * -1

# ###################################################################################################
# def save_2d(data, name, xlabel, ylabel, directory, time, ylim = [-300000, 300000]):
#     plt.clf()

#     scale = int(np.ceil(float(len(data))/time[1]))
#     start = time[0] * scale
#     end = time[1] * scale
#     x = np.linspace(time[0], time[1], end - start)
#     y = np.asarray(data[slice(start, end)])
#     z = np.array([1 if t >= 0 else -1 for t in y])

#     points = np.array([x, y]).T.reshape(-1,1,2)
#     segments = np.concatenate([points[:-1], points[1:]], axis=1)

#     fig, axes = plt.subplots()
#     axes.set_xlabel(xlabel, fontsize = 18)
#     axes.set_ylabel(ylabel, fontsize = 18)
#     axes.set_xlim(time)
#     axes.set_ylim(ylim)
#     cmap = ListedColormap(['C1', 'C0'])
#     norm = BoundaryNorm([-10000000, 0, 10000000], cmap.N)

#     lc = LineCollection(segments, cmap=cmap, norm=norm)
#     lc.set_array(z)
#     axes.add_collection(lc)

#     plt.savefig(directory + name + EXT_PNG, dpi = 300, bbox_inches = "tight")
#     plt.close()
#     pass

# # HERE!
# def do_it(target, max_time):
#     optflow_dist = prevideo.opt_flow_prob_from_file('./data/raw/video/' + target + '.mp4')
#     # optflow_dist = optflow_dist[:(max_time * 3)] # here
#     # directory = SAVE_DIR + SAVE_GRAPH_OPTION + SAVE_OPT_ENT + SAVE_OPT_OPT
#     # ent = to_entropy(optflow_dist)
#     # _save(ent, target, SAVE_DIR + SAVE_TABLE_OPTION + SAVE_OPT_ENT)
#     # save_2d(ent, target, 'sec', 'entropy', directory, [0,max_time], [0, 300000])

#     motion_prob_dist_list = load_motion_data_dir()

#     # directory = SAVE_DIR + SAVE_GRAPH_OPTION + SAVE_OPT_MOT
#     if target in ['S1_surge', 'S1_sway', 'S2_surge', 'S2_sway', 'S3_surge', 'S3_sway']:
#         motion_dist = motion_prob_dist_list[target]
#         motion_dist = np.ones(len(motion_prob_dist_list[target])) * 0.1
#         # reflecting surge and sway are not detected in motion of platform,
#         # we set it as 0.1 of modifier to probability of motion platform
#     elif target in ['S4', 'S5', 'S6']:
#         motion_dist = motion_prob_dist_list[target]
#         motion_dist = motion_prob_dist_list[target] * 0.1
#         # reflecting surge and sway are not detected in motion of platform,
#         # we set it as 0.1 of modifier to probability of motion platform
#     else:
#         motion_dist = motion_prob_dist_list[target]
#     # save_2d(motion_dist, target, 'sec', 'probability', directory, [0, max_time], [0, 1.05])

#     # directory = SAVE_DIR + SAVE_GRAPH_OPTION + SAVE_OPT_KLD
#     kld = kullback_leibler_divergence(optflow_dist, motion_dist)
#     _save(kld, target, SAVE_DIR + SAVE_TABLE_OPTION + SAVE_OPT_KLD)
#     # cum = _to_cumulative(kld)
#     # save_2d(kld, target, 'sec', 'entropy', directory, [0, max_time], [min(kld), max(kld)])
#     # save_2d(kld, target, 'sec', 'entropy', directory, [0, max_time])
#     directory = SAVE_DIR + SAVE_GRAPH_OPTION + SAVE_OPT_KLD
#     kld = to_mp_entropy(optflow_dist, motion_dist)
#     save_2d(kld, target, 'sec', 'entropy', directory, [0, max_time])

# def main(args):
#     targets0 = ['S1_pitch', 'S1_yaw', 'S1_roll', 'S1_surge', 'S1_sway',
#                 'S2_pitch', 'S2_yaw', 'S2_roll', 'S2_surge', 'S2_sway',
#                 'S3_pitch', 'S3_yaw', 'S3_roll', 'S3_surge', 'S3_sway']
#     # targets0 = [ 'S1_surge', 'S1_sway',
#                  # 'S2_surge', 'S2_sway',
#                  # 'S3_surge', 'S3_sway']
#     # targets0 = ['S1_pitch', 'S1_roll', 'S1_yaw']
#     # targets1 = ['S4', 'S5', 'S6']
#     targets1 = ['S5', 'S6']
#     targets2 = ['S1_heave', 'S2_heave', 'S3_heave']
#     target_set = [targets0, targets1, targets2]
#     if args == 0:
#         max_time = 20
#     elif args == 1:
#         max_time = 60
#     else:
#         max_time = 10
#     for target in target_set[args]:
#         do_it(target, max_time)

# if __name__ == '__main__':
#     # main(0)
#     main(1)
#     main(2)

############################################ obselete ##############################################
# def default_preprocess(x, y):
#     return x, y

# def apply_on_dir(optflow_list, motion_list, action,
#                  preprocess_at_file = default_preprocess):
#     return [optflow_list[0],                                                 # add file names.
#             [[action(*preprocess_at_file(data_file[0], data_file[1]))        # action
#               for data_file in list(zip(*[data_dir[0], data_dir[1]]))]     # on file
#              for data_dir in list(zip(*[optflow_list[1], motion_list[1]]))]] # on directory

# def apply_on_file(optflow_data, motion_data, action,
#                  preprocess_at_file = default_preprocess):
#     return [action(*preprocess_at_file(data_file[0], data_file[1]))        # action
#               for data_file in list(zip(*[optflow_data, motion_data]))]     # on file

# def _to_difference_of_entropy(data):
#     ret = []
#     for tmp in data:
#         tmp1 = 0
#         for prob in tmp:
#             if prob != 0:
#                 tmp1 += - prob * np.log2(prob)
#         ret.append(tmp1)

#     dif = []
#     dif = [ret[i + 1] - ret[i] for i in range(len(ret) - 1)]
#     dif = np.asarray(dif)
#     return dif;

# def _to_cumulative(data):
#     ret = []
#     _sum = 0
#     for tmp in data:
#         _sum += tmp
#         ret.append(_sum)
#     return ret

# def save_dir(data_list_with_tag, action, directory):
#     for tmp in list(zip(*data_list_with_tag)):
#         name = tmp[0]
#         processed = action(tmp[1])

#         df = pd.DataFrame(processed)
#         save_json_path = directory + name + EXT_JSON
#         save_excel_path = directory + name + EXT_EXCEL
#         df.to_json(save_json_path)
#         df.to_excel(save_excel_path)
#     pass

# def save_fig_dir(data_list_with_tag, action, directory, xlabel, ylabel, time):
#     directory += str(time[0]) + '_' + str(time[1]) + 's/'
#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     for tmp in list(zip(*data_list_with_tag)):
#         name = tmp[0]
#         processed = action(tmp[1])
#         save_2d(processed, name, xlabel, ylabel, directory, time)
#     plt.clf()
#     pass

# def load_video_data_dir(directory = LOAD_VIDEO_DIR):
#     ret = {}
#     for file in glob.glob(directory + "*" + EXT_JSON):
#         ret[os.path.splitext(os.path.basename(file))[0]] = load_file(file)
#     return ret


# optflow_dist_list = prevideo.opt_flow_prob_from_dir(prevideo.LOAD_DIR)
# motion_prob_dist_list = load_motion_data_dir(is_compact = True)

# motion_cumul_dist_list = load_motion_data_dir(is_cumulative = True, is_compact = True)
# kld_prob_list = apply_on_dir(optflow_dist_list, motion_prob_dist_list,
                             # to_mp_entropy,
                             # lambda x, y: (x, y))
# kld_cumul_list = apply_on_dir(optflow_dist_list, motion_cumul_dist_list,
                              # to_mp_entropy,
                              # lambda x, y: (x, y))


# directory = SAVE_DIR + SAVE_TABLE_OPTION + SAVE_OPT_ENT + SAVE_OPT_OPT
# save_dir(optflow_dist_list, to_entropy, directory)

# directory = SAVE_DIR + SAVE_GRAPH_OPTION + SAVE_OPT_ENT + SAVE_OPT_OPT
# save_fig_dir(optflow_dist_list,
#              to_entropy,
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
# def _to_cumulative(data):
#     ret = []
#     _sum = 0
#     for tmp in data:
#         _sum += tmp
#         ret.append(_sum)
#     return ret
# HERE!
# def load_file(file):
#     return pd.read_json(file).sort_index().to_numpy()


# def save_dir(data_list_with_tag, action, directory):
#     for tmp in list(zip(*data_list_with_tag)):
#         name = tmp[0]
#         processed = action(tmp[1])

#         df = pd.DataFrame(processed)
#         save_json_path = directory + name + EXT_JSON
#         save_excel_path = directory + name + EXT_EXCEL

#         df.to_json(save_json_path)
#         df.to_excel(save_excel_path)
#     pass

# def save_fig_dir(data_list_with_tag, action, directory, xlabel, ylabel, time):
#     directory += str(time[0]) + '_' + str(time[1]) + 's/'
#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     for tmp in list(zip(*data_list_with_tag)):
#         name = tmp[0]
#         processed = action(tmp[1])
#         save_2d(processed, name, xlabel, ylabel, directory, time)
#     plt.clf()
#     pass

# def _save(data, name, directory):
#     df = pd.DataFrame(data)
#     save_json_path = directory + name + EXT_JSON
#     # save_excel_path = directory + name + EXT_EXCEL
#     df.to_json(save_json_path)
#     # df.to_excel(save_excel_path)
