from mpvr.datamodule.manager import Manager as dm
from mpvr.utils.process import *
import numpy as np
import pandas as pd
dm = dm.from_config(dm.section_list()[1])

S3 = [x for x in dm.get_scenarios() if 'S3' in x]
histograms = [np.zeros(5**6), np.zeros(36)]
for scenario in S3:
    print(scenario)
    dm.set_scenario(scenario)
    make_histogram(dm.get_motion_visual_tuple_gen(), histograms)

for histogram in histograms:
    histogram /= np.sum(histogram)

mpe = []
incidences = []
for scenario in S3:
    print(scenario)
    dm.set_scenario(scenario)
    if scenario in ['S3_surge', 'S3_sway', 'S3_surge', 'S3_sway', 'S3_surge', 'S3_sway', 'S4', 'S5', 'S6']:
        for x in to_mp_entropy(
                mapping_src_to_histogram(dm.get_motion_visual_tuple_gen(),
                                         histograms,
                                         factor = 0.1)):
            mpe.append(x)
    else:
        for x in to_mp_entropy(
                mapping_src_to_histogram(dm.get_motion_visual_tuple_gen(),
                                         histograms)):
            mpe.append(x)
    dm._load_incidence_data()
    for _incidence in dm._incidence:
        incidences.append(_incidence)
incidences = np.array(incidences)
mpe = np.array(mpe)
cor['S3'] = correlation(incidences, mpe)
indices = mpe > np.quantile(mpe, 0.75)
cor['S3_q1'] = correlation(incidences[indices], mpe[indices])

mpe = np.array(mpe)
times = np.linspace(1.0/3, 110, 110*3)
path = dm._setting.save_result_path + 'MPEntropy/table/total/S3.csv'
df = pd.DataFrame(mpe, times)
df.index.name = 'Time'
df.columns = ['MP entropy']
df.to_csv(path)

fig, axes = dm.fig_setup(2, ['MP Entropy', 'Incidence'], np.arange(0, 114, 2), times = times)

dm.ax_color_by_value(axes[0], times, mpe, 0)
axes[0].set_ylim([-200000, 200000])
axes[1].bar(times, incidences, width=0.2)
dm.fig_finalize(tag='mpe', file_name='S3', remark_dir='total/')



S6 = ['S6']
histograms = [np.zeros(5**6), np.zeros(36)]
for scenario in S6:
    print(scenario)
    dm.set_scenario(scenario)
    make_histogram(dm.get_motion_visual_tuple_gen(), histograms)

for histogram in histograms:
    histogram /= np.sum(histogram)

mpe = []
incidences = []
for scenario in S6:
    print(scenario)
    dm.set_scenario(scenario)
    if scenario in ['S6_surge', 'S6_sway', 'S6_surge', 'S6_sway', 'S6_surge', 'S6_sway', 'S6', 'S6', 'S6']:
        for x in to_mp_entropy(
                mapping_src_to_histogram(dm.get_motion_visual_tuple_gen(),
                                         histograms,
                                         factor = 0.1)):
            mpe.append(x)
    else:
        for x in to_mp_entropy(
                mapping_src_to_histogram(dm.get_motion_visual_tuple_gen(),
                                         histograms)):
            mpe.append(x)
    dm._load_incidence_data()
    for _incidence in dm._incidence:
        incidences.append(_incidence)
incidences = np.array(incidences)
mpe = np.array(mpe)
cor['S6'] = correlation(incidences, mpe)
indices = mpe > np.quantile(mpe, 0.75)
cor['S6_q1'] = correlation(incidences[indices], mpe[indices])


for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)
    histograms = [np.zeros(5**6), np.zeros(36)]
    motion_data = np.array([x for x in dm.get_motion_data_gen()])

    mot_vis_gen = dm.make_tuple_gen(
        dm.get_classified_motion_data_gen(motion_data),
        dm.get_classified_visual_data_gen())
    make_histogram(mot_vis_gen, histograms)
    for hist in histograms:
        hist /= np.sum(hist)

    mot_vis_gen = dm.make_tuple_gen(
        dm.get_classified_motion_data_gen(motion_data),
        dm.get_classified_visual_data_gen())
    mapped = mapping_src_to_histogram(mot_vis_gen, histograms)
    mpe = [x for x in to_mp_entropy(mapped)]
    dm._load_timestamp_data()
    dm.save_scenario_as_table(mpe, 'mpe', remark_dir='ongame')

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)

    df = dm.get_processed_data('mpe', remark_dir='ongame/')
    time, mpe_ongame = df['Time'].values, df['MPEntropy'].values
    df = dm.get_processed_data('mpe')
    mpe = df['MPEntropy'].values
    incidence = dm.get_incidence_data()

    fig, axes = dm.fig_setup(2, ['MP Entropy', 'Incidence'], np.arange(0, len(time)/3, 2), times = time)
    axes[0].plot(time, mpe_ongame, ':', label='After 3D motion')
    axes[0].plot(time, mpe, label='Before 3D motion')
    axes[0].legend()
    axes[0].set_ylim([-300000, 300000])
    axes[1].bar(time, incidence, width = 0.2)
    axes[1].set_yticks(np.arange(0, 5, 1))
    dm.fig_finalize(tag='mpe', remark_dir='ongame/')
