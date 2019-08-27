import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

def fig_setup(time, row, ylabels, xticks, ylims, width, height):
    plt.close()
    fig, axes = plt.subplots(row, 1, sharex=True)
    fig.set_size_inches(width, height)

    if row == 1:
        axes.set_xlabel('time')
        axes.set_xlim(time[0], time[-1])
        axes.set_ylabel(ylabels, fontsize = 18)
        axes.grid(axis='x')
        if xticks:
            axes.set_xticks(xticks)
        if ylims:
            axes.set_ylim(_ax[1])

    else:
        axes[-1].set_xlabel('time')
        axes[-1].set_xlim(time[0], time[-1])

        if xticks is not None:
            for _ax in axes:
                _ax.set_xticks(xticks)

        if ylims is not None:
            for _ax in zip(*(axes, ylims)):
                _ax[0].set_ylim(_ax[1])

        for _ax in zip(*(axes, ylabels)):
            _ax[0].set_ylabel(_ax[1], fontsize = 18)
            _ax[0].grid(axis='x')

    return fig, axes

def fig_finalize(path):
    plt.tight_layout()
    plt.savefig(path)

def ax_color_by_value(ax, time, data, y_value):
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
    norm = BoundaryNorm([-10000000, y_value, 10000000], cmap.N)

    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(np.array([1 if t > 0 else -1 for t in y]))
    ax.add_collection(lc)



# def save_as_graph(data, tag, xlabel='sec', ylabel='entropy', ylim=None):
#     tags = self._setting.tags
#     if tag not in tags.keys():
#         raise Exception('unsupported tag')
#     path = self._setting.save_result_path + tags['grp'] \
#                 + tags[tag] + self._scenario + '.png'

#     if not ylim:
#         ylim = [min(data) - 0.1 * np.abs(min(data)),
#                 max(data) + 0.1 * np.abs(max(data))]

#     plt.clf()
#     x = []
#     y = []
#     for i in range(len(data)-1):
#         x.append(self._timestamp[1:][i])
#         y.append(data[i])
#         if data[i] * data[i + 1] <= 0:
#             x.append((self._timestamp[1:][i] + self._timestamp[1:][i+1]) / 2)
#             if data[i] > 0:
#                 y.append(-0.0000000001)
#             else:
#                 y.append(0.000000001)
#     i += 1
#     x.append(self._timestamp[1:][i])
#     y.append(data[i])

#     points = np.array([x, y]).T.reshape(-1,1,2)
#     segments = np.concatenate([points[:-1], points[1:]], axis=1)

#     fig, axes = plt.subplots()
#     axes.set_xlabel(xlabel, fontsize = 18)
#     axes.set_ylabel(ylabel, fontsize = 18)
#     axes.set_xlim(x[0], x[-1])
#     axes.set_ylim(ylim)
#     cmap = ListedColormap(['C1', 'C0'])
#     norm = BoundaryNorm([-10000000, 0, 10000000], cmap.N)

#     lc = LineCollection(segments, cmap=cmap, norm=norm)
#     lc.set_array(np.array([1 if t > 0 else -1 for t in y]))
#     axes.add_collection(lc)

#     plt.savefig(path, dpi = 300, bbox_inches = "tight")
#     plt.close()
