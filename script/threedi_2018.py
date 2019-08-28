# coding: utf-8
from mpvr.utils.process import *

def main():
    from mpvr.datamodule.manager import Manager as dm

    dm = dm.from_config(dm.section_list()[0])
    for scenario in dm.get_scenarios():
        print(scenario)
        dm.set_scenario(scenario)
        """MP Entropy to csv"""
        # histograms = make_histogram(dm.get_motion_visual_tuple(), (5**6, 36))
        # mpe = [x for x in to_mp_entropy(mapping_src_to_histogram(dm.load(), histograms))]
        # entropy = [x for x in to_entropy(
        #     [x[1] for x in mapping_src_to_histogram(dm.load(), histograms)])]


        """MP Entropy load and to figure"""
        mpe = dm.get_processed_data('mpe')
        dm.load_raw_data()
        fig, axes = dm\
            .fig_setup(2, ['MP Entropy', 'Incidence'], xticks=np.arange(dm._times[0], dm._times[-1], 2))
        axes[1].bar(dm._times[1:], dm._incidence, width=0.15)
        axes[1].set_yticks(np.linspace(0, 3, 4))
        dm.ax_color_by_value(axes[0], dm._times[1:], mpe, 0)
        axes[0].set_ylim([-1000000, 1000000])
        dm.fig_finalize('mpe', 'default/')

        """MP Entropy & Incidence Correaltion"""
        cor = {}
        for scenario in dm.get_scenarios():
            print(scenario)
            dm.set_scenario(scenario)
            mpe = dm.get_processed_data('mpe')
            dm.load_raw_data()
            cor[scenario]= correlation(mpe, dm._incidence)
        index=['PLCC', 'PLCC p-value', 'SROCC', 'SROCC p-value', 'KENDALL', 'KENDALL p-value']
        dm.save_section_as_table(data=cor, tag='mpe', index=index)

if __name__ == '__main__':
    main()
