import pickle
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import sys

v = 'v'+str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)

file = f'../data/{v}_{batch_number}/{v}_{batch_number}_{subbatch_number}'
print(50*'-=')
print(f'Reading: "{file}"')
print(50*'-=')
with open(file + '_data.pkl', 'rb') as f:
    data = pickle.load(f)
with open(file + '_CV.pkl', 'rb') as f:
    data['CV'] = pickle.load(f)
with open(file + '_rate.pkl', 'rb') as f:
    data['rate'] = pickle.load(f)
with open(file + '_sync.pkl', 'rb') as f:
    data['sync'] = pickle.load(f)


def plotRaster(data):
    ti = data['simData']['t'][-1] - 2000
    tf = data['simData']['t'][-1] - 1000
    len_net = len(data['simData']['V_soma'].keys())
    gex = data['simConfig']['gex']
    amp = data['simConfig']['IClamp0']['amp']
    popRates = data['simData']['popRates']['sPY']
    #sync = data['sync']['statData'][0][0]
    #cv_bar = np.mean(data['CV']['statData'])

    spkid = np.array(data['simData']['spkid'])
    spkt = np.array(data['simData']['spkt'])

    if tf == None:
        tf = spkt[-1]

    fig, ax = plt.subplots(1,1, figsize=(10,2))

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylabel('$n$-th neuron')
    ax.set_xlabel('t (ms)')

    label_gex = f'{gex}'+'S/cm²'
    parameters = r'g_{ex}' + f'={label_gex}' + '\quad' + r'i_{ex}' + f'={amp}nA'+ '\quad'+ 'PopRate'+f'={popRates:.2f}Hz'

    ax.set_title('Raster Plot \n$'+parameters+'$', pad=20)
    sns.scatterplot(y = spkid, x = spkt, s=2, color='black', ax=ax)
    plt.xlim(ti, tf)
    plt.ylim(0,len_net)
    plt.savefig(file+f'RasterPlot_{gex}_{amp}.png', dpi=600, bbox_inches='tight')
    print(f'Ploting raster plot gex: {gex} | amp: {amp}')
    print(20*'-=')
    
plotRaster(data)