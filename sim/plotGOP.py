import pickle
import numpy as np
from matplotlib import pyplot as plt
import sys

from matplotlib.colors import LinearSegmentedColormap
colors = ["gold","lawngreen","royalblue", "midnightblue","royalblue","lawngreen","gold"]
nodes = np.linspace(0, 1, len(colors))
cmap_phase = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))

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

def plot_GOP(t_phase_smp, spatial_phi, gop):
    fig, (ax1, ax2) = plt.subplots(ncols=1, nrows=2, figsize=(8,4),sharex=True, gridspec_kw = {'height_ratios':[2,1]})
    fig.set_tight_layout(20)
    n_neurons = np.arange(spatial_phi.shape[0])
    t = t_phase_smp

    tg, ig = np.meshgrid(n_neurons, t)
    hm = ax1.pcolor(ig, tg, spatial_phi.T, cmap=cmap_phase, vmax=2*np.pi)
    cax = plt.axes([1., 0.45, 0.01, 0.45])
    cbar = plt.colorbar(hm, ax=ax1, ticks=[0, np.pi, 2*np.pi], cax=cax)# format=formater )
    cbar.ax.set_yticklabels(['0', '$\pi$', '$2 \pi$']) 
    cbar.set_label('$\phi(t)$', rotation=0, labelpad=10)
    ax1.set_title('$g_{ex}='+f'{gex}$ S/cm²' + 5*' '+ '$I='+f'{amp}$ nA')
    ax1.set_ylabel('$n^{th}$ Neuron')
    ax1.set_ylim(0,len(n_neurons))
    # plt.savefig('./figures/YamadaModel_Space_param_cv',dpi=600,)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.plot(t_phase_smp, gop, color='darkred')
    ax2.set_xlabel('Tempo (ms)')
    ax2.set_ylabel('GOP$(t)$')
    plt.savefig(file+f'_PlotGOP_{gex}_{amp}.png', dpi=600, bbox_inches='tight')

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
gop = np.zeros(phase_smp.shape[1])

for i, spatial_phase in enumerate(phase_smp.T):
    gop[i] = metrics.kuramoto_param_global_order(spatial_phase)

print('Plot: '+file+'_gop_phase.png')
plot_GOP(t_phase_smp, phase_smp, gop)




