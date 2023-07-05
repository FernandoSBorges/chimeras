import pickle
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import sys

def plotRaster2(t_spikes):
    fig, ax = plt.subplots(1,1, figsize=(8,4))
    fig.set_tight_layout(20)
    label_gex = f'{gex}'+'S/cm²'
    parameters = r'g_{ex}' + f'={label_gex}' + '\quad' + r'i_{ex}' + f'={amp}nA'+ '\quad'+ 'PopRate'+f'={popRates:.2f}Hz'

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title('Raster Plot \n$'+parameters+'$', pad=20)
    ax.set_ylabel('$n$-ésimo Neurônio')
    ax.set_xlabel('Tempo (ms)')

    ax.set_ylim(0, len(t_peaks))
    ax.set_xlim(t_sample[id_first_spk]-20, t_sample[id_last_spk]+20)

    ax.eventplot(t_peaks, color='black')
    plt.savefig(file+f'_PlotRaster_{gex}_{amp}.png', dpi=600, bbox_inches='tight')
    # plt.show()

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
popRates = data['simData']['popRates']['sPY']
trans_i = 30100
trans_f = 20100
ti = len(data['simData']['t'])- trans_i
tf = len(data['simData']['t'])- trans_f


t_data, v_data = metrics.get_numpy(data)
v_sample = v_data[:, ti:tf]
t_sample = t_data[ti:tf]

print(f'Samples: {v_sample.shape}')
peaksmat, t_peaks = [], []  # listas para encontrar id e tempo dos picos
for v in v_sample:
    peaks_id, t_peak, v_peak = metrics.find_peaks(t_sample, v)
    peaksmat.append(peaks_id)
    t_peaks.append(t_peak)
id_first_spk = min([min(peak) for peak in peaksmat]) # id primeiro spk
id_last_spk = min([max(peak) for peak in peaksmat]) # id do primeiro dos ultimos spk
plotRaster2(t_peaks)
