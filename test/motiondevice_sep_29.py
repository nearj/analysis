from mpvr.datamodule.manager import Manager as dm
from mpvr.utils.process import *
from scipy.signal import savgol_filter
import numpy as np
import pandas as pd

dm = dm.from_config(dm.section_list()[1])
max_val = 0

for scenario in dm.get_scenarios():
    dm.set_scenario(scenario)
    df = dm.get_processed_data('mpe')
    mpe = df['MPEntropy'].values
    if np.max(np.abs(mpe)) > max_val:
        max_val = np.max(np.abs(mpe))

print(max_val)

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)

    df = dm.get_processed_data('mpe')
    time, mpe = df['Time'].values, df['MPEntropy'].values
    acr = absolute_category_rating(mpe, grid)
    incidence = dm.get_incidence_data()

    fig, axes = dm.fig_setup(2, ['ACR', 'Incidence'], np.arange(0, len(time)/3, 2), times = time, width = 3, height=3)
    axes[0].plot(time, acr)
    axes[1].bar(time, incidence, width=0.2)

    axes[0].set_yticks(np.arange(1, 6, 1))
    axes[1].set_yticks(np.arange(0, 5, 1))
    dm.fig_finalize(tag='mpe', remark_dir='acr/')
