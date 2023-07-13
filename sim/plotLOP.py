import pickle
import numpy as np
from matplotlib import pyplot as plt
import sys

from matplotlib.colors import ListedColormap
colors = ["darkorange", "gold", "lawngreen", "lightseagreen","darkgreen"]
cmap_LOP = ListedColormap(colors)


def plot_params():
    # plt.rc('text', usetex=True)
    plt.rc('font', size=13)
    plt.rc('xtick', labelsize=11)
    plt.rc('ytick', labelsize=11)
    plt.rc('axes', labelsize=14)
    plt.rc('legend', fontsize=8)
    plt.rc('lines', linewidth=1.0)
    plt.rcParams["axes.formatter.limits"] = (-3, 4)
    # plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
plot_params()

def plot_LOP(t_phase_smp,lop, vizinhos):
    fig, ax2 = plt.subplots(ncols=1, nrows=1, figsize=(8,3),sharex=True)
    fig.set_tight_layout(20)
    n_neurons = np.arange(lop.shape[1])
    t = t_phase_smp
    tg, ig = np.meshgrid(n_neurons, t)
    hm2 = ax2.pcolor(ig, tg, lop, cmap=cmap_LOP, vmax=1.0, vmin=0)#cmap_LOP)

    cbar2= plt.colorbar(hm2, ax=ax2, ticks=[0, 1])
    cbar2.ax.set_yticklabels(['0', '1,0']) 
    cbar2.set_label('LOP$(t)$')
    ax2.set_title('$k='+f'{vizinhos}'+'$')
    ax2.set_ylabel('$n$ neurônio')
    ax2.set_ylim(0,len(n_neurons))
    ax2.set_xlabel('Tempo (ms)')
    plt.savefig(file+f'_PlotLOP_{gex}_{amp}_{vizinhos}.png', dpi=600, bbox_inches='tight')

v = 'v'+str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)
file = f'../data/{v}_{batch_number}/{v}_{batch_number}_{subbatch_number}'

print('\n~~ Plot LOP ')
print(f'Reading: "{file}"')
with open(file + '_data.pkl', 'rb') as f:
    data = pickle.load(f)

gex = data['simConfig']['gex']
amp = data['simConfig']['IClamp0']['amp']
lops = data['LOP_k']
t_phase = data['t_phase']

for k, lop in lops.items():
    print(f'--> Plot LOP: k = {k}')
    plot_LOP(t_phase, lop, vizinhos=k)

print('\n~~')



