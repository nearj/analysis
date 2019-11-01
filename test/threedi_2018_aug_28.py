from mpvr.datamodule.manager import Manager as dm
from mpvr.utils.process import *
from scipy.signal import savgol_filter
import numpy as np
import pandas as pd

dm = dm.from_config(dm.section_list()[0])

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)
    motion_data = np.array([x for x in dm.get_motion_data_gen()])
    motion_data_95 = savgol_filter(motion_data, 9, 5, axis=0)

    histograms = [np.zeros(5**6), np.zeros(36)]
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
    dm.save_scenario_as_table(mpe, 'mpe')


    histograms = [np.zeros(5**6), np.zeros(36)]
    mot_vis_gen = dm.make_tuple_gen(
         dm.get_classified_motion_data_gen(gen = motion_data_95),
         dm.get_classified_visual_data_gen())
    make_histogram(mot_vis_gen, histograms)
    for hist in histograms:
        hist /= np.sum(hist)

    mot_vis_gen = dm.make_tuple_gen(
         dm.get_classified_motion_data_gen(gen = motion_data_95),
         dm.get_classified_visual_data_gen())
    mapped = mapping_src_to_histogram(mot_vis_gen, histograms)
    mpe = [x for x in to_mp_entropy(mapped)]
    dm._load_timestamp_data()
    dm.save_scenario_as_table(mpe, 'mpe', remark_dir='savgol95/')

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)
    motion_data = np.array([x for x in dm.get_motion_data_gen()])
    histograms = [np.zeros(5**6), np.zeros(36)]
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
    dm.save_scenario_as_table(mpe, 'mpe')

mpe = np.zeros(315)
incidence = np.zeros(315)
for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)
    mpe += dm.get_processed_data('mpe')['MPEntropy'].values
    incidence += dm.get_incidence_data()

times = dm.get_timestamp_data()[0]
fig, axes = dm.fig_setup(2, ['MP Entropy', 'Incidence'], np.arange(0, 108, 2), times = times)

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)

    df = dm.get_processed_data('mpe')
    time, mpe = df['Time'].values, df['MPEntropy'].values
    df = dm.get_processed_data('mpe', remark_dir='savgol/')
    mpe52 = df['MPEntropy'].values
    incidence = dm.get_incidence_data()

    fig, axes = dm.fig_setup(2, ['MP Entropy', 'Incidence'], np.arange(0, 108, 2), times = time)
    axes[0].plot(time, mpe, label='Base')
    axes[0].plot(time, mpe52, ':', label='Savgol filter')
    axes[1].bar(time, incidence, width=0.2)
    axes[1].set_yticks(np.arange(0, 5, 1))
    axes[0].legend()
    dm.fig_finalize(tag='mpe', remark_dir='savgol/')

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)

    df = dm.get_processed_data('mpe')
    time, mpe = df['Time'].values, df['MPEntropy'].values
    incidence = dm.get_incidence_data()

    fig, axes = dm.fig_setup(2, ['MP Entropy', 'Incidence'], np.arange(0, 108, 2), times = time)
    dm.ax_color_by_value(axes[0], time, mpe)
    axes[0].set_ylim([-200000, 200000])
    axes[1].bar(time, incidence, width=0.2)
    axes[1].set_yticks(np.arange(0, 5, 1))

    dm.fig_finalize(tag='mpe')

cor = {}
for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)
    mpe = dm.get_processed_data('mpe')['MPEntropy'].values
    incidence = dm.get_incidence_data()
    cor[scenario] = correlation(mpe, incidence)

dm.save_section_as_table(cor, tag, index = ['PLCC', 'PLCC p-val', 'SROCC', 'SROCC p-val', 'KENDALL', 'KENDALL p-val'])


_vectors = []

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)
    _vectors.append(np.amin(np.array([x for x in dm.get_motion_data_gen()]), axis=0))
    _vectors.append(np.amax(np.array([x for x in dm.get_motion_data_gen()]), axis=0))

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)
    motion_data = np.array([x for x in dm.get_motion_data_gen()])
    motion_data_52 = savgol_filter(motion_data, 5, 2, axis=0)
    motion_data_92 = savgol_filter(motion_data, 9, 2, axis=0)
    motion_data_93 = savgol_filter(motion_data, 9, 3, axis=0)

    histograms = [np.zeros(5**6), np.zeros(36)]
    mot_vis_gen = dm.make_tuple_gen(
         dm.get_classified_motion_data_gen(gen = motion_data_52),
         dm.get_classified_visual_data_gen())
    make_histogram(mot_vis_gen, histograms)
    for hist in histograms:
        hist /= np.sum(hist)
    mot_vis_gen = dm.make_tuple_gen(
         dm.get_classified_motion_data_gen(gen = motion_data_52),
         dm.get_classified_visual_data_gen())
    mapped = mapping_src_to_histogram(mot_vis_gen, histograms)
    mpe = [x for x in to_mp_entropy(mapped)]
    dm._load_timestamp_data()
    dm.save_scenario_as_table(mpe, 'mpe', remark_dir='savgol52/')

    histograms = [np.zeros(5**6), np.zeros(36)]
    mot_vis_gen = dm.make_tuple_gen(
         dm.get_classified_motion_data_gen(gen = motion_data_92),
         dm.get_classified_visual_data_gen())
    make_histogram(mot_vis_gen, histograms)
    for hist in histograms:
        hist /= np.sum(hist)
    mot_vis_gen = dm.make_tuple_gen(
         dm.get_classified_motion_data_gen(gen = motion_data_92),
         dm.get_classified_visual_data_gen())
    mapped = mapping_src_to_histogram(mot_vis_gen, histograms)
    mpe = [x for x in to_mp_entropy(mapped)]
    dm._load_timestamp_data()
    dm.save_scenario_as_table(mpe, 'mpe', remark_dir='savgol92/')

    histograms = [np.zeros(5**6), np.zeros(36)]
    mot_vis_gen = dm.make_tuple_gen(
         dm.get_classified_motion_data_gen(gen = motion_data_93),
         dm.get_classified_visual_data_gen())
    make_histogram(mot_vis_gen, histograms)
    for hist in histograms:
        hist /= np.sum(hist)
    mot_vis_gen = dm.make_tuple_gen(
         dm.get_classified_motion_data_gen(gen = motion_data_93),
         dm.get_classified_visual_data_gen())
    mapped = mapping_src_to_histogram(mot_vis_gen, histograms)
    mpe = [x for x in to_mp_entropy(mapped)]
    dm._load_timestamp_data()
    dm.save_scenario_as_table(mpe, 'mpe', remark_dir='savgol93/')

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)

    df = dm.get_processed_data('mpe')
    time, mpe = df['Time'].values, df['MPEntropy'].values
    df = dm.get_processed_data('mpe', remark_dir='savgol52/')
    # mpe52 = df['MPEntropy'].values
    # df = dm.get_processed_data('mpe', remark_dir='savgol53/')
    mpe53 = df['MPEntropy'].values
    df = dm.get_processed_data('mpe', remark_dir='savgol92/')
    mpe92 = df['MPEntropy'].values
    # df = dm.get_processed_data('mpe', remark_dir='savgol93/')
    # mpe93 = df['MPEntropy'].values
    incidence = dm.get_incidence_data()

    fig, axes = dm.fig_setup(1, 'MP Entropy', np.arange(0, 108, 2), times = time)
    axes.plot(time, mpe, '', label='Base')
    axes.plot(time, mpe92, ':', label='Savgol 92')
    axes[0].legend()
    dm.fig_finalize(tag='mpe', remark_dir='savgol/')

    fig, axes = dm.fig_setup(3, ['MP Entropy', 'MP Entropy', 'Incidence'], np.arange(0, 108, 2), times = time)
    axes[0].plot(time, mpe, ':', label='Before Filtering')
    axes[0].plot(time, mpe52, '', label='After Savgol 52')
    # axes[0].plot(time, mpe53, '--', label='Savgol 53')
    axes[1].plot(time, mpe, ':', label='Before Filtering')
    axes[1].plot(time, mpe92, '', label='After Savgol 92')
    # axes[1].plot(time, mpe93, '--', label='Savgol 93')
    axes[2].bar(time, incidence, width=0.2)
    axes[2].set_yticks(np.arange(0, 5, 1))
    axes[0].legend()
    axes[1].legend()
    dm.fig_finalize(tag='mpe', remark_dir='savgol/')

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)

    df = dm.get_processed_data('mpe')
    time, mpe = df['Time'].values, df['MPEntropy'].values
    # df = dm.get_processed_data('mpe', remark_dir='savgol52/')
    # mpe52 = df['MPEntropy'].values
    df = dm.get_processed_data('mpe', remark_dir='savgol95/')
    mpe95 = df['MPEntropy'].values
    incidence = dm.get_incidence_data()

    fig, axes = dm.fig_setup(1, 'MP Entropy', np.arange(0, 108, 2), times = time)
    axes.plot(time, mpe, '', label='Before Filtering')
    axes.plot(time, mpe95, ':', label='After Savgol 95')
    axes.legend()
    dm.fig_finalize(tag='mpe', remark_dir='savgol/')

    fig, axes = dm.fig_setup(3, ['MP Entropy', 'MP Entropy', 'Incidence'], np.arange(0, 108, 2), times = time)
    axes[0].plot(time, mpe, ':', label='Before Filtering')
    axes[0].plot(time, mpe52, '', label='After Savgol 52')
    # axes[0].plot(time, mpe53, '--', label='Savgol 53')
    axes[1].plot(time, mpe, ':', label='Before Filtering')
    axes[1].plot(time, mpe92, '', label='After Savgol 92')
    # axes[1].plot(time, mpe93, '--', label='Savgol 93')
    axes[2].bar(time, incidence, width=0.2)
    axes[2].set_yticks(np.arange(0, 5, 1))
    axes[0].legend()
    axes[1].legend()
    dm.fig_finalize(tag='mpe', remark_dir='savgol/')
