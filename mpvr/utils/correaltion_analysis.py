import pandas as pd
import numpy as np
import os, sys, glob

from scipy.stats import linregress
from scipy.stats import spearmanr
from scipy.stats import kendalltau

LOAD_DIR = './data/processed/table/'
LOAD_DIR_SSQ = './data/raw/ssq/'
LOAD_OPT_MPE = 'MPentropy/'
LOAD_OPT_ENT = 'entropy/'

SAVE_DIR = './data/postprocessed/table/'
SAVE_OPT_PEARSON = 'pearson/'
SAVE_OPT_SPRMAN = 'spearman/'
SAVE_OPT_KNDTAU = 'kendall/'

EXT_JSON = '.json'
EXT_EXCEL = '.xlsx'
EXT_CSV = '.csv'

SCENARIOS = ['S1_pitch', 'S1_yaw', 'S1_roll', 'S1_surge', 'S1_heave', 'S1_sway',
             'S2_pitch', 'S2_yaw', 'S2_roll', 'S2_surge', 'S2_heave', 'S2_sway',
             'S3_pitch', 'S3_yaw', 'S3_roll', 'S3_surge', 'S3_heave', 'S3_sway',
             'S4', 'S5', 'S6']

class DATA_MANAGER:
    _load_opt_mpe: str = LOAD_OPT_MPE
    _load_opt_ent: str = LOAD_OPT_ENT
    _save_opt_pearson: str = SAVE_OPT_PEARSON
    _save_opt_sprman: str = SAVE_OPT_SPRMAN
    _save_opt_kndtau: str = SAVE_OPT_KNDTAU
    _ext_json: str = EXT_JSON
    _ext_excel: str = EXT_EXCEL
    _ext_csv: str = EXT_CSV

    def __init__(self, load_dir: str = LOAD_DIR, load_dir_ssq: str = LOAD_DIR_SSQ, save_dir: str = SAVE_DIR):
        self._load_dir = load_dir
        self._load_dir_ssq = load_dir_ssq
        self._save_dir = save_dir
        pass

    def set_scenario(self,scenario: str):
        self._scenario = scenario

    def load(self, load_data_type):
        if load_data_type == 'm':
            load_path = self._load_dir + self._load_opt_mpe
        elif load_data_type == 'e':
            load_path = self._load_dir + self._load_opt_ent
        load_path += self._scenario + self._ext_csv

        # return np.mean(pd.read_json(load_path).values.reshape(-1, 3), axis = 1)
        return pd.read_csv(load_path).values[:,1]

    def load_ssq(self):
        load_path = self._load_dir_ssq
        load_path += self._scenario + self._ext_csv
        ssq = pd.read_csv(load_path)['0'].values

        return np.stack((ssq,ssq,ssq), axis=1).reshape(-1) # super sampling

    def save(self, data, correlation_type, load_data_type):
        df = pd.DataFrame.from_dict(data)
        df.index = ['correlation', 'p-value']
        save_path = self._save_dir
        if load_data_type == 'm': # MP entorpy
            save_path += self._load_opt_mpe
        elif load_data_type == 'e': # entropy of optical flow
            save_path += self._load_opt_ent

        if correlation_type == 'p': # pearson
            save_path += self._save_opt_pearson
        elif correlation_type == 's': # spearman
            save_path += self._save_opt_sprman
        elif correlation_type == 'k': # kendall tau
            save_path += self._save_opt_kndtau

        df.to_json(save_path + 'correaltions' + self._ext_json)
        df.to_csv(save_path + 'correaltions' + self._ext_csv)
        pass
    pass

def procedure():
    spearman_holder = {}
    kendalltau_holder = {}
    pearson_holder = {}
    dm = DATA_MANAGER()
    for scenario in SCENARIOS:
        dm.set_scenario(scenario)
        ssq = dm.load_ssq()
        tmp_pearson = linregress(dm.load('m'), ssq)

        spearman_holder[scenario] = spearmanr(dm.load('m'), ssq)
        kendalltau_holder[scenario] = kendalltau(dm.load('m'), ssq)
        pearson_holder[scenario] = [tmp_pearson.rvalue, tmp_pearson.pvalue]

    dm.save(spearman_holder, 's', 'm')
    dm.save(kendalltau_holder, 'k', 'm')
    dm.save(pearson_holder, 'p', 'm')
    dm.save(spearman_holder, 's', 'e')
    dm.save(kendalltau_holder, 'k', 'e')
    dm.save(pearson_holder, 'p', 'e')

def main():
    procedure()

if __name__ == '__main__':
    main()
