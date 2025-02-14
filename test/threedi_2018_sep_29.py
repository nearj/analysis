from mpvr.datamodule.manager import Manager as dm
from mpvr.utils.process import *
from scipy.signal import savgol_filter
import numpy as np
import pandas as pd

dm = dm.from_config(dm.section_list()[0])
max_val = 0
sum_of_incidence = np.zeros(315)
for scenario in dm.get_scenarios():
    dm.set_scenario(scenario)
    df = dm.get_processed_data('mpe')
    sum_of_incidence += dm.get_incidence_data()
    mpe = df['MPEntropy'].values
    if np.max(np.abs(mpe)) > max_val:
        max_val = np.max(np.abs(mpe))
grid = np.array([-0.7, -0.3, 0.3, 0.7]) * max_val

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)

    df = dm.get_processed_data('mpe')
    time, mpe = df['Time'].values, df['MPEntropy'].values
    mos = absolute_category_rating(mpe, grid)

    df = dm.get_processed_data('mpe', remark_dir='savgol92/')
    mpe92 = df['MPEntropy'].values
    mos92 = absolute_category_rating(mpe92, grid)

    incidence = dm.get_incidence_data()

    fig, axes = dm.fig_setup(3, ['MPEntropy', 'MOS', 'Incidence'], np.arange(0, 108, 2), times = time)
    axes[0].plot(time, mpe, ':', label='Before Filtering')
    axes[0].plot(time, mpe92, '', label='After Savgol 92')
    for y in grid:
        axes[0].axhline(y, color='r', linestyle=':')
    axes[1].plot(time, mos, ':', label='Before Filtering')
    axes[1].plot(time, mos92, '', label='After Savgol 92')
    axes[2].bar(time, incidence, width=0.2)

    axes[1].set_yticks(np.arange(1, 6, 1))
    axes[2].set_yticks(np.arange(0, 5, 1))

    axes[0].legend()
    axes[1].legend()
    dm.fig_finalize(tag='mpe', remark_dir='mos/')

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)

    df = dm.get_processed_data('mpe')
    time, mpe = df['Time'].values, df['MPEntropy'].values
    mos = absolute_category_rating(mpe, grid)
    incidence = dm.get_incidence_data()

    fig, axes = dm.fig_setup(3, ['MPEntropy', 'MOS', 'Incidence'], np.arange(0, 108, 2), times = time)
    axes[0].plot(time, mpe, ':')
    for y in grid:
        axes[0].axhline(y, color='r', linestyle=':')
    axes[1].plot(time, mos)
    axes[2].bar(time, incidence, width=0.2)

    axes[1].set_yticks(np.arange(1, 6, 1))
    axes[2].set_yticks(np.arange(0, 5, 1))
    dm.fig_finalize(tag='mpe', remark_dir='mos/')
