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

from matplotlib.colors import LinearSegmentedColormap
colors = ["gold","royalblue", "midnightblue","royalblue","gold"]
nodes = np.linspace(0, 1, len(colors))
cmap_phase = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))

def plotPhase(t_phase_smp, spatial_phi):
    fig, ax1 = plt.subplots(ncols=1, nrows=1, figsize=(8,4),sharex=True)
    fig.set_tight_layout(20)
    n_neurons = np.arange(spatial_phi.shape[0])
    t = t_phase_smp
    tg, ig = np.meshgrid(n_neurons, t)
    hm1 = ax1.pcolor(ig, tg, spatial_phi.T, cmap=cmap_phase, vmax=2*np.pi)
    
    cbar1 = fig.colorbar(hm1, ax=ax1, ticks=[0, np.pi, 2*np.pi])#, cax=cax1, format=formater)
    cbar1.set_label('$\phi(t)$')
    cbar1.ax.set_yticklabels(['0', '$\pi$', '$2 \pi$']) 
    ax1.set_title('$g_{ex}='+f'{gex}$ S/cm²' + 5*' '+ '$I='+f'{amp}$ nA')
    ax1.set_ylabel('$n$ neurônio')
    ax1.set_ylim(0,len(n_neurons))
    plt.savefig(file+f'_PlotPhase_{gex}_{amp}.png', dpi=600, bbox_inches='tight')


v = 'v'+str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)
file = f'../data/{v}_{batch_number}/{v}_{batch_number}_{subbatch_number}'

print(f'Reading: "{file}"')
with open(file + '_data.pkl', 'rb') as f:
    data = pickle.load(f)

gex = data['simConfig']['gex']
amp = data['simConfig']['IClamp0']['amp']
t_phase = data['t_phase']
phases = data['phases']

plotPhase(t_phase, phases)
