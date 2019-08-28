from mpvr.datamodule.manager import Manager as dm
from mpvr.utils.process import *

dm = dm.from_config(dm.section_list()[0])

for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)
    histograms = make_histogram(dm.get_motion_visual_tuple_gen(), (5**6, 36))
    mp_entropy = [x for x in to_mp_entropy(mapping_src_to_histogram(dm.get_motion_visual_tuple_gen(),histograms))]
    dm.save_as_table(mp_entropy, 'mpe')

dm.set_scenario('3DI_01')
histograms = make_histogram(dm.get_motion_visual_tuple_gen(), (5**6, 36))
mp_entropy = [x for x in to_mp_entropy(mapping_src_to_histogram(dm.get_motion_visual_tuple_gen(),
                                                                    histograms))]
for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)
    mpe = dm.get_processed_data('mpe')
    dm.load_raw_data()
    fig, axes = dm.fig_setup(2, ['MP Entropy', 'Incidence'], xticks=np.arange(dm._times[0], dm._times[-1], 2))
    axes[1].bar(dm._times[1:], dm._incidence, width=0.15)
    axes[1].set_yticks(np.linspace(0, 3, 4))
    dm.ax_color_by_value(axes[0], dm._times[1:], mpe, 0)
    axes[0].set_ylim([-1000000, 1000000])
    dm.fig_finalize('mpe', 'default/')

cor = {}
for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)
    mpe = dm.get_processed_data('mpe')
    dm.load_raw_data()
    cor[scenario]= correlation(mpe, dm._incidence)

total_mpe = np.zeros(315)
total_incidence = np.zeros(315)
for scenario in dm.get_scenarios():
    dm.set_scenario(scenario)
    dm.load_raw_data()
    total_mpe += dm.get_processed_data('mpe')
    total_incidence += dm._incidence

fig, axes = dm.fig_setup(2, ['MP Entropy', 'Incidence'], xticks=np.arange(dm._times[0], dm._times[-1], 2))
axes[1].bar(dm._times[1:], total_incidence, width=0.2)
dm.ax_color_by_value(axes[0], dm._times[1:], np.array(total_mpe) / 30, 0)
axes[1].set_yticks(np.arange(np.min(total_incidence), np.max(total_incidence)+1, 2, dtype=int))
axes[0].set_ylim([-5000000, 5000000])

dm.fig_finalize('mpe', 'default/', '3DI_total')


for scenario in dm.get_scenarios():
    print(scenario)
    dm.set_scenario(scenario)
