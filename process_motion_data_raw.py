import numpy as np
import pandas as pd
import glob, os

from etaprogress.progress import ProgressBar

_sub_bin_names = ['pitch', 'yaw', 'roll', 'heave']
_sub_bin_units = [125, 25, 5, 1] # bin of [pitch, yaw, roll, heave]
_sub_bin_nums  = [5, 5, 5, 5] # # of [pitch, yaw, roll, heave]
_total_bin_num = np.prod(_sub_bin_nums)
_sub_bins      = [np.linspace(bin[0], bin[0] * bin[1], bin[1])
                  for bin in np.stack((_sub_bin_units, _sub_bin_nums), axis = 1)]
_sub_bins_prop = [list(item) for item in zip(*[_sub_bin_names, _sub_bin_units, _sub_bin_nums])]

RAW_DATA_DIR = './data/raw/motion/'
EXT_RAW_DATA = '.txt'
EXT_RAW_META = '.meta'
EXT_JSON = '.json'
EXT_EXCEL = '.xlsx'
SAVE_DIR_PD = './data/processed/motion/prob_dist/'
SAVE_DIR_CD = './data/processed/motion/cumul_dist/'
SAVE_COMPACT_OPTION = 'compact/'
COLUMNS_NON_COMP = [str([n % 5, (n % 25) // 5, (n % 125) // 25, n // 625]) for n in range(625)]



def _select_sub_bin(sub_bin, indices):
    tmp = []
    for prop in _sub_bins_prop:
        if prop[1] == sub_bin[0]:
            bin_prop = prop
            break
    bin_modulo = bin_prop[1] * bin_prop[2]
    for val in indices % bin_modulo:
        tmp.append(np.where(sub_bin - val > 0)[0][0])
    return tmp

def _select_bins(indices):
    tmp = []
    for sub_bin in _sub_bins:
        tmp.append(_select_sub_bin(sub_bin, indices))
    return tmp

def _to_compact(data):
    indices = np.where(data != 0)[0]
    bins = _select_bins(indices)
    vals = data[indices]
    bins.append(vals)
    return [list(item) for item in zip(*bins)]

def raw_to_prob_densities(raw_data_set):
    for raw_data in raw_data_set:
        assert np.sum(raw_data) != 0
    prob_densities = [[tmp / np.sum(tmp) for tmp in raw_data] for raw_data in raw_data_set]
    return [prob_densities,
            [[_to_compact(tmp) for tmp in prob_density] for prob_density in prob_densities]]

def raw_to_cumul_densities(raw_data_set):
    prob_densities, _ = raw_to_prob_densities(raw_data_set)
    cumul_densities = []
    for prob_density in prob_densities:
        cumul_densities.append(
            [np.sum(prob_density[:i + 1], axis =0) / (i + 1) for i in range(len(prob_density))])
    return [cumul_densities,
            [[_to_compact(tmp) for tmp in cumul_density] for cumul_density in cumul_densities]]

def extract_raw_set(dir = RAW_DATA_DIR, data_ext = EXT_RAW_DATA, meta_ext = EXT_RAW_META):
    raw_data_set = []
    raw_meta_set = []
    for raw_data_file in glob.glob(dir + "*" + data_ext):
        tmp = np.loadtxt(raw_data_file)
        raw_data_set.append(tmp.reshape((int) (tmp.size / _total_bin_num), _total_bin_num))
        raw_meta_set.append([os.path.splitext(os.path.basename(raw_data_file))[0],
            np.fromfile(os.path.splitext(raw_data_file)[0] + meta_ext, float, sep = ' ')])
    return [raw_data_set, raw_meta_set]

def process():
    raw_data_set, raw_meta_set =  extract_raw_set()
    return raw_to_prob_densities(raw_data_set), raw_to_cumul_densities(raw_data_set), raw_meta_set


def save(data_name, probability, is_cumulative = False, is_compact = False):
    if is_cumulative:
        save_dir = SAVE_DIR_CD
    else:
        save_dir = SAVE_DIR_PD

    if is_compact:
        save_dir += SAVE_COMPACT_OPTION

    save_json_path = save_dir + data_name + EXT_JSON
    save_excel_path = save_dir + data_name + EXT_EXCEL

    df = pd.DataFrame(probability)
    # if not is_compact:
    #     df.columns = COLUMNS_NON_COMP
    df.to_json(save_json_path)
    df.to_excel(save_excel_path)


def main(args):
    if args.use_default:
        data_set = process()
    data_set = list(zip*([data_set[0][0], data_set[0][1], data_set[1][0], data_set[1][1], data_set[2]]))
    bar = ProgressBar(len(data_set), max_width = 100)
    tick = 0
    for data in data_set:
        save(data[-1][0], data[0], is_cumulative = False, is_compact = False)
        save(data[-1][0], data[1], is_cumulative = False, is_compact = True)
        save(data[-1][0], data[2], is_cumulative = True, is_compact = False)
        save(data[-1][0], data[3], is_cumulative = True, is_compact = True)
        bar.numerator = tick
        tick += 1
        print(bar, end = '\r')
        sys.stdout.flush()

if __name__ == '__main__':
    import argparse, sys
    parser = argparse.ArgumentParser(
        description='caculate data and save it as json and excel')

    parser.add_argument('-use_default', "--use_default", action='store_true')
    parser.add_argument('-dir', "--dir", nargs='?', type=str, help='directory')
    parser.add_argument('-file', "--file", nargs='?', type=str, help = 'YET IMPLEMENTED!')
    main(parser.parse_args())
