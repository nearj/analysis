# coding: utf-8
from mpvr.utils.process import *

UNSENSORED_MODIFIER = 0.1
UNSENSORED = ['S1_surge', 'S1_sway', 'S2_surge', 'S2_sway', 'S3_surge', 'S3_sway',
              'S4', 'S5', 'S6']

def main():
    from mpvr.datamanager.uos2018 import UOS2018 as dm
    dm = dm.from_config()
    for scenario in dm.get_scenarios():
        print(scenario)
        dm.set_scenario(scenario)
        data = [x for x in dm.load()]
        histograms = make_histogram(data, (5**6, 36))
        if scenario in UNSENSORED:
            mp_entropy = [x for x in to_mp_entropy(
                [(y[0] * UNSENSORED_MODIFIER, y[1])
                 for y in mapping_src_to_histogram(data, histograms)])]
        else:
            mp_entropy = [x for x in to_mp_entropy(mapping_src_to_histogram(data, histograms))]
        entropy = [x for x in to_entropy(
            [x[1] for x in mapping_src_to_histogram(data, histograms)])]

        dm.save_as_table(entropy, 'ent')
        dm.save_as_table(mp_entropy, 'mpe')
        dm.save_as_graph(entropy, 'ent', ylim=[0, 300000])
        dm.save_as_graph(mp_entropy, 'mpe', ylim=[-300000, 300000])

if __name__ == '__main__':
    main()
