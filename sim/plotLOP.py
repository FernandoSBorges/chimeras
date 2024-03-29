import pickle
import numpy as np
from matplotlib import pyplot as plt
import sys

from matplotlib.colors import ListedColormap,LinearSegmentedColormap
colors = ["darkorange", "gold", "lawngreen", "lightseagreen","darkgreen"]
cmap_LOP = ListedColormap(colors)

# colors = ["black", "purple", "darkorange","lawngreen", "gold"]
# nodes = np.linspace(0, 1, len(colors))
# cmap_LOP = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))


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

def plot_LOP(t_phase_smp, lop, vizinhos, n):
    fig, ax2 = plt.subplots(ncols=1, nrows=1, figsize=(8,3),sharex=True)
    fig.set_tight_layout(20)
    fig.suptitle('$g_{ex}='+f'{gex}$ S/cm²' + ' | '+'$I='+f'{amp}$ nA'+ '\n' +f'PopRate $={popRates:.2f}$Hz'+ ' | '+f'$r$: {float(r)}', fontsize=14)
    n_neurons = np.arange(lop.shape[1])
    t = t_phase_smp
    tg, ig = np.meshgrid(n_neurons, t)
    hm2 = ax2.pcolor(ig, tg, lop, cmap=cmap_LOP, vmax=1.0, vmin=0.)#cmap_LOP)

    cbar2= plt.colorbar(hm2, ax=ax2, ticks=[0, 1])
    cbar2.ax.set_yticklabels(['0.9', '1,0']) 
    cbar2.set_label('LOP$(t)$')
    ax2.set_title('$\delta='+f'{vizinhos}'+'$')
    ax2.set_ylabel('$n$ neurônio')
    ax2.set_ylim(0,len(n_neurons))
    ax2.set_xlabel('Tempo (ms)')
    # ax2.set_xlim(5000, 6000)
    plt.savefig(file+f'_PlotLOP_{gex}_{amp}_{vizinhos}_({n}).png', dpi=600, bbox_inches='tight')

v = str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)

file = f'../data/v{v}_{batch_number}/v{v}_{batch_number}_{subbatch_number}'
# file = f'../data/v6_batch0001/v6_batch0001_0_1'

print('\n~~ Plot LOP ')
print(f'Reading: "{file}"')
with open(file + '_data.pkl', 'rb') as f:
    data = pickle.load(f)

gex = data['simConfig']['gex']
amp = data['simConfig']['IClamp0']['amp']
n_neighbors = data['simConfig']['n_neighbors']
cellNumber = data['simConfig']['cellNumber']
r = n_neighbors / cellNumber
popRates = data['simData']['popRates']['sPY']

lops = data['LOP_delta']
t_phase = data['t_phase']

ti1 = int(0.1*len(t_phase))
ti2 = int(0.5*len(t_phase))
tf  = int(len(t_phase))


for delta, lop in lops.items():
    print(f'--> Plot LOP: delta = {delta}')
    plot_LOP(t_phase[ti1:tf], lop[ti1:tf,:], vizinhos=delta, n=1)
    plot_LOP(t_phase[ti1:ti2], lop[ti1:ti2,:], vizinhos=delta, n=2)

print('\n~~')



