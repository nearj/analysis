# coding: utf-8
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import config.definitions as defs

time_tag = 'Time'
incidence_tag = 'DizzinessRange'
res = [f for f in glob.glob(defs.DATA_RAW_MOTION_DIR + "*.csv") if "3DI" in f and "3DI_0" not in f]

tmp = []
for f in res:
    print(f)
    df = pd.read_csv(f)
    times = pd.to_datetime(df[time_tag].str.split().str[1]).astype(int) / 10 ** 9
    times -= times[1]
    tmp.append(pd.DataFrame(df[incidence_tag].values[1:], times.values[1:]))
    
def _sampling_time(times):
    ret_dts = [] # delta times
    ret_ind = [] # sampled indices
    grid = np.linspace(0, 105, 3*105 + 1)
    grid_idx = 0
    for i in range(0, 941):
        diff = times[i] - grid[grid_idx]
        if  np.abs(diff) < 0.061:
            ret_dts.append(times[i])
            ret_ind.append(i + 1)
            grid_idx += 1
            if grid_idx >= 316:
                return np.array(ret_ind, dtype = np.int), np.array(ret_dts)
    return None

res = []
for t in tmp:
    ind, ts = _sampling_time(t.index.values)
    res.append(ts)
    res.append(ind)
df = pd.DataFrame(np.asarray(res).T)

k = 1
for t in tmp:
    res = []
    ind, ts = _sampling_time(t.index.values)
    res.append(ts)
    res.append(ind)
    df = pd.DataFrame(np.asarray(res).T)
    df.columns = ['Time', 'Index']
    df.to_csv('./data/raw/timestamp/3DI_{:2}.csv'.format(k))
    incidence = []
    j = 0
    for i in range(len(ind)):
        incidence.append(np.sum(t.values[j:i+1]))
        j = i
    df = pd.DataFrame(np.asarray(incidence))
    df.to_csv('./data/raw/incidence/3DI_{:2}.csv'.format(k))


columns = []
for i in range(30):
    index.append('3DI_{:02}_Time'.format(i))
    index.append('3DI_{:02}_Incidence'.format(i))
df.columns = columns

for i in range(5):
    plt.clf()
    plt.figure(figsize=(18, 6))
    axes = [plt.subplot(321+j) for j in range(6)]
    for j in range(6):
        axes[j].bar(df.iloc[:,6*i+3*j], df.iloc[:,6*i+3*j+2], width=0.1)
        axes[j].set_ylim([0,3])
        axes[j].set_xlabel('3DI_{:02}'.format(6*i+j+1), fontsize=7)
    plt.tight_layout()
    plt.savefig('./data/raw/test/3DI_{:02}.png'.format(6*i+1, 6*i+6))
tot = np.sum(df.iloc[:,2::3], axis=1)
plt.clf()
plt.figure(figsize=(18,6))
plt.bar(df.iloc[:,0], tot, width=0.1)
plt.xlabel('3DI_total', fontsize=7)
plt.tight_layout()
plt.savefig('./data/raw/test/3DI_total.png')

def save_fig(scenario, data, incidence, time):
    from matplotlib import pyplot as plt
    from matplotlib.collections import LineCollection
    from matplotlib.colors import ListedColormap, BoundaryNorm
    directory = './data/processed/result/3di_2018/graph/MPentropy/{:s}.png'.format(scenario)
    ylim = [-250000, 250000]
    plt.close()

    x = []
    y = []
    for i in range(len(data)-1):
        x.append(time[i])
        y.append(data[i])
        if data[i] * data[i + 1] <= 0:
            x.append((time[i] + time[i+1]) / 2)
            if data[i] > 0:
                y.append(-0.0000000001)
            else:
                y.append(0.000000001)
    i += 1
    x.append(time[i])
    y.append(data[i])

    points = np.array([x, y]).T.reshape(-1,1,2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fig, axes = plt.subplots(2, 1, sharex=True)
    fig.set_size_inches(18, 6)

    cmap = ListedColormap(['C1', 'C0'])
    norm = BoundaryNorm([-10000000, 0, 10000000], cmap.N)

    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(np.array([1 if t > 0 else -1 for t in y]))
    axes[0].add_collection(lc)
    axes[1].bar(time, incidence, width=0.1)

    axes[0].set_xlabel('time', fontsize = 18)
    axes[0].set_ylabel('MP Entropy', fontsize = 18)
    axes[0].set_xlim(x[0], x[-1])
    axes[0].set_ylim(ylim)
    axes[0].set_xticks(np.arange(int(time[0]), int(time[-1])+1, 2))
    axes[0].grid(axis='x')

    axes[1].set_ylabel('Incidence', fontsize = 18)
    axes[1].set_ylim([0,3])
    axes[1].set_xticks(np.arange(int(time[0]), int(time[-1])+1, 2))
    axes[1].grid(axis='x')

    plt.tight_layout()
    plt.savefig(directory)

def save_fig_total(scenario, datas, incidence, time):
    from matplotlib import pyplot as plt
    from matplotlib.collections import LineCollection
    from matplotlib.colors import ListedColormap, BoundaryNorm
    
    plt.close()
    ylim = [-250000, 250000]
    fig, axes = plt.subplots(2, 1, sharex=True)
    fig.set_size_inches(18, 6)

    for data in datas:
        x = []
        y = []
        for i in range(len(data)-1):
            x.append(time[i])
            y.append(data[i])
            if data[i] * data[i + 1] <= 0:
                x.append((time[i] + time[i+1]) / 2)
                if data[i] > 0:
                    y.append(-0.0000000001)
                else:
                    y.append(0.000000001)
        i += 1
        x.append(time[i])
        y.append(data[i])

        points = np.array([x, y]).T.reshape(-1,1,2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        cmap = ListedColormap(['C1', 'C0'])
        norm = BoundaryNorm([-10000000, 0, 10000000], cmap.N)

        lc = LineCollection(segments, cmap=cmap, norm=norm)
        lc.set_array(np.array([1 if t > 0 else -1 for t in y]))
        axes[0].add_collection(lc)


    axes[1].bar(time, incidence, width=0.1)

    axes[0].set_xlabel('time', fontsize = 18)
    axes[0].set_ylabel('MP Entropy', fontsize = 18)
    axes[0].set_xlim(x[0], x[-1])
    axes[0].set_ylim(ylim)
    axes[0].set_xticks(np.arange(int(time[0]), int(time[-1])+1, 2))
    axes[0].grid(axis='x')

    axes[1].set_ylabel('Incidence', fontsize = 18)
    axes[1].set_ylim([0,3])
    axes[1].set_xticks(np.arange(int(time[0]), int(time[-1])+1, 2))
    axes[1].grid(axis='x')
    plt.tight_layout()

    directory = './data/processed/result/3di_2018/graph/MPentropy/{:s}.png'.format(scenario)
    plt.savefig(directory)
