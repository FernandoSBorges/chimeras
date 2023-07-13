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
# plot_params()

def plot_GOP(t_phase_smp, gop):
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(8,2))
    fig.set_tight_layout(20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.plot(t_phase_smp, gop, color='darkred')
    ax.set_xlim(t_phase_smp[0], t_phase_smp[-1])
    ax.set_xlabel('Tempo (ms)')
    ax.set_ylabel('GOP$(t)$')
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



