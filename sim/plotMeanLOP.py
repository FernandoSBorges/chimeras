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

def plot_MeanLOP(t_phase_smp, lop, delta):
    fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(8,3), sharey=True, gridspec_kw={'width_ratios':[10,1]})
    fig.set_tight_layout(20)
    fig.suptitle('$g_{ex}='+f'{gex}$ S/cm²' + ' | '+'$I='+f'{amp}$ nA'+ '\n' +f'PopRate $={popRates:.2f}$Hz'+ ' | '+f'$r$: {float(r)}', fontsize=14)
    for axis in ax:
        axis.spines['top'].set_visible(False)
        axis.spines['right'].set_visible(False)

    ax[0].set_title('Série temporal do $\overline{LOP}$', pad=20)
    ax[0].plot(t_phase_smp[1000:-100], lop[1000:-100], color='purple', linewidth=0.5)
    ax[0].set_xlabel('Tempo (ms)')
    ax[0].set_ylim(-0.05, 1.05)
    ax[0].set_xlim(t_phase_smp[1000], t_phase_smp[-100])
    ax[0].set_ylabel('$\overline{LOP}(t)$')

    
    ax[1].set_title('Box Plot', fontsize=10)
    bp = ax[1].boxplot(lop[1000:-100], showmeans=True, showfliers=False)
    ax[0].legend([bp['medians'][0], bp['means'][0]], ['Mediana', 'Média'])
    ax[1].spines['bottom'].set_visible(False)
    ax[1].spines['left'].set_visible(False)
    ax[1].xaxis.set_visible(False)
    ax[1].yaxis.set_visible(False)
    plt.savefig(file+f'_PlotMeanLOP{delta}_{gex}_{amp}.png', dpi=600, bbox_inches='tight')

v = str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)

file = f'../data/v{v}_{batch_number}/v{v}_{batch_number}_{subbatch_number}'
# file = f'../data/v1_batch0/v1_batch0'

print('~~ Plot Mean LOP')
print(f'Reading: "{file}"')
with open(file + '_data.pkl', 'rb') as f:
    data = pickle.load(f)

gex = data['simConfig']['gex']
amp = data['simConfig']['IClamp0']['amp']
popRates = data['simData']['popRates']['sPY']
n_neighbors = data['simConfig']['n_neighbors']
cellNumber = data['simConfig']['cellNumber']
r = n_neighbors / cellNumber
t_phase = data['t_phase']
lop_delta = data['LOP_delta']

for delta, lop in lop_delta.items():
    mean_lop = lop.mean(axis=1)
    print('Plot: '+file+f'_lop{delta}.png')
    plot_MeanLOP(t_phase, mean_lop, delta)
    print('\n~~')



