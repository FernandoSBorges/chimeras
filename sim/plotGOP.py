import pickle
import numpy as np
from matplotlib import pyplot as plt
import sys

def plot_params():
    plt.rc('text', usetex=True)
    plt.rc('font', size=13)
    plt.rc('xtick', labelsize=11)
    plt.rc('ytick', labelsize=11)
    plt.rc('axes', labelsize=14)
    plt.rc('legend', fontsize=8)
    plt.rc('lines', linewidth=1.0)
    plt.rcParams["axes.formatter.limits"] = (-3, 4)
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
plot_params()

def plot_GOP(t_phase_smp, gop):
    fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(8,3), gridspec_kw={'width_ratios':[10,1]})
    fig.set_tight_layout(20)
    for axis in ax:
        axis.spines['top'].set_visible(False)
        axis.spines['right'].set_visible(False)

    ax[0].set_title('Série temporal do GOP(t)', pad=20)
    ax[0].plot(t_phase_smp, gop, color='darkred')
    ax[0].set_xlabel('Tempo (ms)')
    ax[0].set_xlim(t_phase_smp[0], t_phase_smp[-1])
    ax[0].set_ylabel('GOP$(t)$')
    ax[1].set_title('Blox Plot', fontsize=10)
    bp = ax[1].boxplot(data['GOP'], showmeans=True, showfliers=False)
    ax[0].legend([bp['medians'][0], bp['means'][0]], ['Mediana', 'Média'])
    ax[1].spines['bottom'].set_visible(False)
    ax[1].spines['left'].set_visible(False)
    ax[1].xaxis.set_visible(False)
    ax[1].yaxis.set_visible(False)
    plt.savefig(file+f'_PlotGOP_{gex}_{amp}.png', dpi=600, bbox_inches='tight')

v = 'v'+str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)

file = f'../data/{v}_{batch_number}/{v}_{batch_number}_{subbatch_number}'
print('~~ Plot GOP')
print(f'Reading: "{file}"')
with open(file + '_data.pkl', 'rb') as f:
    data = pickle.load(f)

gex = data['simConfig']['gex']
amp = data['simConfig']['IClamp0']['amp']
t_phase = data['t_phase']
global_order_parameter = data['GOP']

print('Plot: '+file+'_gop_phase.png')
plot_GOP(t_phase, global_order_parameter)
print('\n~~')



