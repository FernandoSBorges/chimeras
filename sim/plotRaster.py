import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager
import os
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

def plotRaster(t_phase_smp, t_peaks, ti, tf, n):
    fig, ax = plt.subplots(1,1, figsize=(8,4))
    fig.set_tight_layout(20)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title('$g_{ex}='+f'{gex}$ S/cm²' + ' | '+'$I='+f'{amp}$ nA'+ '\n' +f'PopRate $={popRates:.2f}$Hz'+ ' | '+f'$r$: {float(r)}', fontsize=14)
    ax.set_ylabel('$n$-ésimo Neurônio')
    ax.set_xlabel('Tempo (ms)')
    ax.set_ylim(0, len(t_peaks))
    ax.set_xlim(ti, tf)
    ax.eventplot(t_peaks, color='black')
    plt.savefig(file+f'_PlotRaster_{gex}_{amp}_({n}).png', dpi=600, bbox_inches='tight')
    # plt.show()

v = str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)

file = f'../data/v{v}_{batch_number}/v{v}_{batch_number}_{subbatch_number}'
# file = f'../data/v1_batch0/v1_batch0'

print('~~ Plot Raster')
print(f'Reading: "{file}"')

with open(file+'_data.pkl', 'rb') as f:
    data = pickle.load(f)
    
gex = data['simConfig']['gex']
amp = data['simConfig']['IClamp0']['amp']
n_neighbors = data['simConfig']['n_neighbors']
cellNumber = data['simConfig']['cellNumber']
r = n_neighbors / cellNumber
popRates = data['simData']['popRates']['sPY']
t_phase = data['t_phase']
t_peaks = data['t_peaks']

ti1=t_phase[int(0.1*len(t_phase))]
tf1=t_phase[int(len(t_phase)-1)]

ti2=t_phase[int(0.1*len(t_phase))]
tf2=t_phase[int(0.5*len(t_phase))]

plotRaster(t_phase, t_peaks, ti=ti1, tf=tf1, n = 1)
plotRaster(t_phase, t_peaks, ti=ti2, tf=tf2, n = 2)

print('\n~~')
