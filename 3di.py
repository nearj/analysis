# coding: utf-8
from mpvr.utils.process import *

def main():
    from mpvr.datamanager.threedi import ThreeDI as dm

    dm = dm.from_config()
    dm.set_scenario('3DI')
    histograms = make_histogram(dm.load(), (5**6, 36))
    mp_entropy = [x for x in to_mp_entropy(mapping_src_to_histogram(dm.load(), histograms))]
    entropy = [x for x in to_entropy(
        [x[1] for x in mapping_src_to_histogram(dm.load(), histograms)])]

    dm.save_as_table(entropy, 'ent')
    dm.save_as_table(mp_entropy, 'mpe')
    dm.save_as_graph(entropy, 'ent')
    dm.save_as_graph(mp_entropy, 'mpe')

if __name__ == '__main__':
    main()
