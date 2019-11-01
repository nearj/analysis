from mpvr.utils.process import *
from scipy.signal import savgol_filter
import numpy as np
import pandas as pd
import argparse

def to_category(mpe_path, categories = [-170681, -73149, 73149, 170681]):
    df = pd.read_csv(mpe_path)
    times, mpe = df['Time'].values, df['MP Entropy'].values
    return times, absolute_category_rating(mpe, categories)

def make_fig(times, data, output_name):
    from mpvr.datamodule.manager import Manager as dm
    dm = dm.from_config(dm.section_list()[0])
    fig, axes = dm.fig_setup(1, 'ACR', np.arange(0, 108, 2), times = times)

    axes.plot(times, data)
    axes.set_yticks(np.arange(1, 6, 1))
    dm.fig_finalize(None, path = './' + output_name + '.png')


def main(args):
    mpe_path, output_name = args.mpe_path, args.output_name
    times, acr_mpe = to_category(mpe_path)

    df = pd.DataFrame(np.array(acr_mpe), times)
    df.columns = ['Categorized MP Entropy']
    df.index.name = 'Time'
    df.to_csv(output_name, float_format="%6f")

    make_fig(times, acr_mpe, output_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mpe_path', type=str)
    parser.add_argument('output_name', type=str)
    args = parser.parse_args()
    main(args)
