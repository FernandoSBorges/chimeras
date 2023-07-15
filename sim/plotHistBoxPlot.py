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

def plot_GOP(gop):
    fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(8,4), gridspec_kw={'width_ratios':[1,3]})
    fig.set_tight_layout(20)
    for axis in ax:
        axis.spines['top'].set_visible(False)
        axis.spines['right'].set_visible(False)

    ax[0].set_title('Blox Plot', fontsize=10)
    bp = ax[0].boxplot(
        gop[100:-100],positions=[0.42], showmeans=True, showfliers=False,
        medianprops = dict(linewidth=1.5),
        )
    ax[0].set_xlim(0,.5)
    ax[0].legend([bp['medians'][0], bp['means'][0]], ['Mediana', 'Média'], loc='upper left')
    ax[0].spines['bottom'].set_visible(False)
    ax[0].spines['left'].set_visible(False)
    ax[0].xaxis.set_visible(False)
    ax[0].set_yticks([])

    ax[0].set_ylabel('GOP(t)')
    ax[1].set_xlabel('Frequência do GOP(t)')
    hist = ax[1].hist(gop[100:-100], color='red', orientation='horizontal',edgecolor='black', linewidth=1.2)
    ax[1].annotate(f'bins: {10}', xy=(hist[0][-1],0))
    plt.savefig(file+f'_HistBoxGOP_{gex}_{amp}.png', dpi=600, bbox_inches='tight')

v = 'v'+str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)

file = f'../data/{v}_{batch_number}/{v}_{batch_number}_{subbatch_number}'
print('~~ Plot GOP Histogram and BoxPlot')
print(f'Reading: "{file}"')
with open(file + '_data.pkl', 'rb') as f:
    data = pickle.load(f)

gex = data['simConfig']['gex']
amp = data['simConfig']['IClamp0']['amp']
global_order_parameter = data['GOP']

print('Plot: '+file+'_HistBoxGOP.png')
plot_GOP(global_order_parameter)
print('\n~~')



