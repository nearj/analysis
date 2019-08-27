import mpvr.utils.correaltion_analysis as ca
import numpy as np
import matplotlib.pyplot as plt

dm = ca.DATA_MANAGER()
for scenario in ca.SCENARIOS:
    dm.set_scenario(scenario)
    ssq = dm.load_ssq()
    mpe = dm.load('m')
    plt.clf()
    ax1 = plt.subplot(311)
    ax2 = plt.subplot(312, sharex=ax1)
    ax3 = plt.subplot(313, sharex=ax1)
    ax1.set_xlim([0, len(ssq) /3 + 1])
    ax1.set_ylim([0, 6])
    ax2.set_ylim([-300000, 300000])
    if scenario in ['S4', 'S5', 'S6']:
        ax1.set_xticks(np.linspace(0, len(ssq)/3, len(ssq)/6 + 1))
    else:
        ax1.set_xticks(np.linspace(0, len(ssq)/3, len(ssq)/3 + 1))
    ax1.tick_params(labelsize=6)
    ax2.tick_params(labelsize=6)
    ax3.tick_params(labelsize=6)
    ax1.set_xlabel('sec')
    ax1.set_ylabel('SSQ')
    ax2.set_ylabel('MP entropy')
    ax3.set_ylabel('MP Entropy Extended')
    ax1.grid(axis='x')
    ax2.grid(axis='x')
    ax3.grid(axis='x')
    ax1.bar(np.linspace(0+1/3, len(ssq)/3+1/3, len(ssq)+1)[1:], ssq, align='center', width = 0.2)
    ax2.plot(np.linspace(0, len(ssq)/3, len(ssq)+1[1:]),mpe)
    ax3.plot(np.linspace(0, len(ssq)/3, len(ssq)+1[1:]),mpe)
    plt.tight_layout()
    plt.savefig('./tmp/' + scenario + '.png', dpi=600)
