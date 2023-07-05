import pickle
import numpy as np
from matplotlib import pyplot as plt
import sys

from matplotlib.colors import LinearSegmentedColormap
colors = ["gold","lawngreen","royalblue", "midnightblue","royalblue","lawngreen","gold"]
nodes = np.linspace(0, 1, len(colors))
cmap_phase = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))

colors = ["magenta" , "darkviolet" , "blue" , "black"]
# nodes = [0.0, 0.75, 0.9, 1.0,]
nodes = np.linspace(0, 1, len(colors))
cmap_LOP = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))


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

def plot_LOP(t_phase_smp, spatial_phi, lop, vizinhos):
    # from matplotlib.ticker import FuncFormatter, MultipleLocator
    # formater = FuncFormatter(lambda val,pos: '{:.0g}$\pi$'.format(val/np.pi) if val !=0 else '0')

    fig, (ax1, ax2) = plt.subplots(ncols=1, nrows=2, figsize=(8,6),sharex=True)
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

    tg, ig = np.meshgrid(n_neurons, t)
    hm2 = ax2.pcolor(ig, tg, lop, cmap='gnuplot_r', vmax=1.0, vmin=0)#cmap_LOP)

    cbar2= plt.colorbar(hm2, ax=ax2, ticks=[0, 1])
    cbar2.ax.set_yticklabels(['0', '1,0']) 
    cbar2.set_label('LOP$(t)$')
    ax2.set_title('$k='+f'{k}'+'$')
    ax2.set_ylabel('$n$ neurônio')
    ax2.set_ylim(0,len(n_neurons))
    ax2.set_xlabel('Tempo (ms)')
    plt.savefig(file+f'_PlotLOP_{gex}_{amp}_{k}.png', dpi=600, bbox_inches='tight')

v = 'v'+str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)

file = f'../data6/{v}_{batch_number}/{v}_{batch_number}_{subbatch_number}'
print(50*'-=')
print(f'Reading: "{file}"')

with open(file + '_data.pkl', 'rb') as f:
    data = pickle.load(f)
with open(file + '_CV.pkl', 'rb') as f:
    data['CV'] = pickle.load(f)
with open(file + '_rate.pkl', 'rb') as f:
    data['rate'] = pickle.load(f)

import metrics

gex = data['simConfig']['gex']
amp = data['simConfig']['IClamp0']['amp']
trans_i = 30100
trans_f = 20100
ti = len(data['simData']['t'])- trans_i
tf = len(data['simData']['t'])- trans_f

t_data, v_data = metrics.get_numpy(data)
v_sample = v_data[:, ti:tf]
t_sample = t_data[ti:tf]
t_phase_smp, phase_smp = metrics.phase_of_v(t_sample, v_sample)
lop = np.zeros_like(phase_smp.T)
k = 2
for i, spatial_phase in enumerate(phase_smp.T):
    lop[i] = metrics.kuramoto_param_local_order(spatial_phase, k=2)

print('Plot: '+file+'_lop_phase.png')
plot_LOP(t_phase_smp, phase_smp, lop, vizinhos=k)



