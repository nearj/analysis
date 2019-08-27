# coding: utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

SSQ = { 'S1_pitch': [6, 18], 'S1_yaw': [10], 'S1_roll':[9],
        'S1_surge': [9], 'S1_heave': [], 'S1_sway': [7, 14],
        'S2_pitch': [6, 16], 'S2_yaw': [5,6,16], 'S2_roll':[5,6,7,9,16,17],
        'S2_surge': [6,7], 'S2_heave': [], 'S2_sway': [6,7,13],
        'S3_pitch': [10,11,14,19], 'S3_yaw': [6,10], 'S3_roll':[5],
        'S3_surge': [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
        'S3_heave': [], 'S3_sway': [3,4,5,6,7,8,12],
        'S4': [2,3,4,5,6,7,12,15,22,23,24,25,26,27,33,43,54],
        'S5': [7,8,24,25, 42, 54],
        'S6': [3,4,17,18,19,20,21,22,23,36,37,38,39,40,41,42] }

EXP_SET = {'S1_pitch': 20, 'S1_yaw': 20, 'S1_roll': 20,
           'S1_surge': 20, 'S1_heave': 10, 'S1_sway': 20,
           'S2_pitch': 20, 'S2_yaw': 20, 'S2_roll': 20,
           'S2_surge': 20, 'S2_heave': 10, 'S2_sway': 20,
           'S3_pitch': 20, 'S3_yaw': 20, 'S3_roll': 20,
           'S3_surge': 20, 'S3_heave': 10, 'S3_sway': 20,
           'S4': 60, 'S5': 60, 'S6': 60}

tmp = {}
base = {}

for key in EXP_SET.keys():
    base[key] = np.zeros(EXP_SET[key])
    
for key in SSQ.keys():
    for sickness_occured in SSQ[key]:
        base[key][sickness_occured - 1] = 1
        
base['S2_yaw'][6] = 2
base['S2_yaw'][6]
base['S2_roll'][6] = 2
base['S2_roll'][16] = 2
base['S2_surge'][8] = 4

save_path = './data/raw/ssq/'

for key in base.keys():
    df = pd.DataFrame(base[key])
    df.to_csv(save_path + key + '.csv')

for key in SSQ.keys():
    df = pd.read_csv(save_path + key + '.csv')
    plt.clf()
    plt.bar(df.index.values, df['0'].values, align='center')
    plt.xticks(df.index.values[::2], fontsize = 6)
    plt.yticks(np.arange(0,7))
    plt.xlabel('second')
    plt.ylabel('SSQ value')

    plt.savefig(save_path + key + '.png', dpi=300, bbox_inches = "tight")
