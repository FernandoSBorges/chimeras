import pickle
import numpy as np
from matplotlib import pyplot as plt
import sys
import metrics

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

def plotMeanLOPWin(mean_lop_window, t_phase, gop, window, k):
    fig, ax = plt.subplots(ncols=1, nrows=2, figsize=(8, 6))
    fig.set_tight_layout(20)

    janela = t_phase[window]-t_phase[0]

    for axis in ax:
        axis.spines['top'].set_visible(False)
        axis.spines['right'].set_visible(False)
        
    ax[0].set_title(f'Média de $LOP_{k}(t)$ em janela de {int(janela)} ms')
    bp= ax[0].boxplot(
        mean_lop_window, showmeans=True,
        medianprops = dict(linewidth=2.))
    ax[0].legend([bp['medians'][0], bp['means'][0],bp['fliers'][0]], ['Mediana', 'Média', 'Outliers'])
    ax[0].xaxis.set_visible(False)

    ax[1].set_ylabel('GOP(t)')
    ax[1].plot(t_phase, gop, color='darkred')
    ax[1].set_xlim(t_phase[0], t_phase[-1])
    ax[1].set_xlabel('Tempo (ms)')
    plt.savefig(file+f'_plotMeanLOPWin_{gex}_{amp}_{k}.png', dpi=600, bbox_inches='tight')

v = 'v'+str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)

file = f'../data/{v}_{batch_number}/{v}_{batch_number}_{subbatch_number}'
print('~~ Plot Mean LOP Window')
print(f'Reading: "{file}"')
with open(file + '_data.pkl', 'rb') as f:
    data = pickle.load(f)

gex = data['simConfig']['gex']
amp = data['simConfig']['IClamp0']['amp']
lops = data['LOP_k']
gop = data['GOP']
t_phase = data['t_phase']
win = 201

for k, lop in lops.items():
    print(f'--> LOP k: {k}, window: {win}')
    mlp = metrics.mean_lop_window(lop, win)
    plotMeanLOPWin(mlp, t_phase, gop, win, k)
    del mlp

print('~~')

