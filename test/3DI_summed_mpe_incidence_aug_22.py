# coding: utf-8
from mpvr.datamanager.threedi import ThreeDI as dm
from mpvr.utils.process import *
import pandas as pd

dm = dm.from_config()
holder = {}
for scenario in dm.get_scenarios():
    dm.set_scenario(scenario)
    mpe = dm._load_processed_data('mpe')[1]
    incidence = dm._load_incidence()
    holder[scenario] = correlation(mpe, incidence)
dm._save_correaltion_as_table(holder, 'mpe')
dm.set_scenario('3DI_01')
mpe = dm._load_processed_data('mpe')[1]
incidence = pd.read_csv('./data/raw/incidence/3DI_total.csv').values[:,1]
correlation(mpe, incidence)
for scenario in dm.get_scenarios():
    dm.set_scenario(scenario)
    mpe = dm._load_processed_data('mpe')[1]
    incidence = pd.read_csv('./data/raw/incidence/3DI_total.csv').values[:,1]
    print(correlation(mpe, incidence))
    
dm.set_scenario('3DI_01')
time, mpe = dm._load_processed_data('mpe')
time
np.where(time > 30)
time[90]
tmp = np.zeros(len(time[90:]))
for scenario in dm.get_scenarios():
    dm.set_scenario(scenario)
    tmp += dm._load_processed_data('mpe')[1][90:]
    
    
incidence = pd.read_csv('./data/raw/incidence/3DI_total.csv').values[:,1]
incidence = incidence[90:]
mpe30to104 = tmp
mpe30to104 /= 30
save_fig('3DI_summed', mpe, incidence, time)
def save_fig(directory, scenario, data, incidence, time):
    directory = './data/processed/result/3di_2018/graph/MPentropy/{:s}.png'.format(scenario)
    ylim = [-250000, 250000]
    plt.close()

    axes[1].bar(time, incidence, width=0.1)

    plt.tight_layout()
    plt.savefig(directory)

np.where(mpe30to104 >= np.quantile(mpe30to104, .75))
mpe30to104_q1 = mpe30to104[np.where(mpe30to104 >= np.quantile(mpe30to104, .75))[0]]
incidence30to104_q1 = incidence[np.where(mpe30to104 >= np.quantile(mpe30to104, .75))[0]]
correlation(mpe30to104_q1, incidence30to104_q1)
plt.scatter(time[np.where(mpe30to104 >= np.quantile(mpe30to104, .75))[0]], mpe30to104_q1)
np.where(mpe30to104 >= np.quantile(mpe30to104, .75))[0]
time[np.where(mpe30to104 >= np.quantile(mpe30to104, .75))[0]]
time[90:][np.where(mpe30to104 >= np.quantile(mpe30to104, .75))[0]]
plt.scatter(time[90:][np.where(mpe30to104 >= np.quantile(mpe30to104, .75))[0]], mpe30to104_q1)
plt.scatter(time[90:][np.where(mpe30to104 >= np.quantile(mpe30to104, .75))[0]], mpe30to104_q1)
plt.plot(time[90:][np.where(mpe30to104 >= np.quantile(mpe30to104, .75))[0]], mpe30to104_q1)

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
axes[1].set_xticks(np.arange(int(time[0]), int(time[-1])+1, 2))
axes[1].grid(axis='x')

plt.tight_layout()
plt.savefig(directory)

mpe30 = mpe[90:]
time30 = time[90:]
incd30 = incidence[90:]

axes[0].scatter(time30[np.where(mpe30>=np.quantile(mpe30, .75))[0]], mpe30[np.where(mpe30>=np.quantile(mpe30, .75))[0]], marker='o', facecolors='none', edgecolors='r')
axes[0].axhline(y=np.max(mpe30)*.75, color='b', linestyle='-')
for t in time30[np.where(mpe30>=np.quantile(mpe30, .75))[0]]:
    axes[0].axvline(x=t, color='r', linestyle='-', linewidth=0.2)
    axes[1].axvline(x=t, color='r', linestyle='-', linewidth=0.2)
