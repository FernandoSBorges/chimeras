import pickle
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib import cm 
from matplotlib.colors import ListedColormap,LinearSegmentedColormap

import matplotlib.colors as mcolors
cores = list(mcolors.TABLEAU_COLORS.keys())
cores = [cor.split(':')[-1] for cor in cores]

sns.set_context('paper')
hsv_modified = cm.get_cmap('hsv', 256)# create new hsv colormaps in range of 0.3 (green) to 0.7 (blue)
newcmp = ListedColormap(hsv_modified(np.linspace(-0.05,1.1, 256)))# show figure

def plot_params():
    plt.rc('text', usetex=True)
    plt.rc('font', size=13)
    plt.rc('xtick', labelsize=15)
    plt.rc('ytick', labelsize=15)
    plt.rc('axes', labelsize=18)
    plt.rc('legend', fontsize=14)
    plt.rc('lines', linewidth=1.0)
    plt.rcParams["axes.formatter.limits"] = (-3, 4)
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})

def load_batch(batch_number, current):
    if batch_number in list(range(1,17)) and current in list(range(4)):
        batch_number = str(batch_number).zfill(4)
        file = f'../data/v6_batch{batch_number}/v6_batch{batch_number}_0_{current}'
        with open(file + f'_data.pkl', 'rb') as f:
            data = pickle.load(f)

        with open(file + f'_CV.pkl', 'rb') as f:
            data['CV'] = pickle.load(f)

        with open(file + f'_rate.pkl', 'rb') as f:
            data['rate'] = pickle.load(f)   

        return data
    else:
        raise Exception('Batch not found')
    
def plotRaster(data, fname, ti=550, tf=None):
    sns.set_context('notebook')
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
    ax.scatter(y = spkid, x = spkt, s=2,color='black')
    ax.set_xlim(ti, tf)
    ax.set_ylim(0,100)
    plt.show()
    plt.savefig(f'../new_figures/{infos}_RasterPlot.png', dpi=600, bbox_inches='tight')
    del gex
    del amp 
    del popRates
    del spkid
    del spkt

def phase(spkt, spkid, len_network, step_t = 1, trans=0):
    """
    Calculates the phase values for spike data.

    Args:
        spkt (numpy.ndarray): Array of spike times.
        spkid (numpy.ndarray): Array of neuron IDs corresponding to spike times.
        len_network (int): Number of neurons in the network.
        step_t (int, optional): Time step for phase calculation. Defaults to 1.

    Returns:
        numpy.ndarray: Array of phase values for each neuron.
    """
    # Create a neuron matrix with m-th spikes 
    spkmat = [[spkt for spkind, spkt in zip(spkid, spkt) if spkind == neuron] for neuron in set(range(len_network))]

    # Lambda function to calculate phase
    phase_t = lambda t, t0, t1 : 2*np.pi*(t-t0)/(t1 - t0)

    # List comprehension to calculate phase values for each neuron
    phimat = [[phase_t(t,t1,t0) for (t0, t1) in zip(spk_k, spk_k[1:]) for t in np.arange(min(spk_k), max(spk_k), step_t) if t0 < t < t1] for spk_k in spkmat if len(spk_k) > 10]

    min_samples = np.min([len(phi) for phi in phimat])
    spatial_phi = np.array([phi[-min_samples:] for phi in phimat])[:,-trans:]

    del spkmat
    del phase_t
    del min_samples

    return spatial_phi

def kuramoto_param_global_order(spatial_phase):
    """
    Calculates the global order parameter of Kuramoto for a set of spatial phases.

    Args:
        spatial_phase (list): List of spatial phases.

    Returns:
        float: Value of the global order parameter of Kuramoto.

    """
    n = len(spatial_phase)
    somatorio = 0
    for j in range(0, n + 1):
        # if j == n or j == 0:
        j = j % n
        somatorio += np.exp(complex(0, spatial_phase[j]))
    z = np.abs(somatorio / n)
    del spatial_phase
    return z


def param_global_order(spkt, spkid, len_network=100, step_t = 1, trans=0):
    """
    Calculates the Kuramoto global parameter order of spatial phase.

    Args:
        spkt (numpy.ndarray): Array of spike times.
        spkid (numpy.ndarray): Array of neuron IDs corresponding to spike times.
        len_network (int): Number of neurons in the network.
        n_neighbours (int): Number of neighboring neurons to consider for Kuramoto parameter order.
        step_t (int, optional): Time step for phase calculation. Defaults to 1.

    Returns:
        tuple: A tuple containing the spatial phase array and Kuramoto parameter order array.
    """
    phimat = phase(spkt, spkid, len_network=len_network, step_t = step_t, trans=trans)

    # param global order
    min_samples = np.min([len(phi) for phi in phimat])
    spatial_phi = np.array([phi[-min_samples:] for phi in phimat]).T
    z = np.array([kuramoto_param_global_order(phi) for phi in spatial_phi]).T

    del min_samples
    del phimat

    return spatial_phi, z

def plot_phase_gop(spatial_phi, gop,fname):
    t = np.arange(spatial_phi.shape[0])
    i = np.arange(spatial_phi.shape[1])

    plot_params()

    fig, ax = plt.subplots(ncols=1, nrows=2, figsize=(10,5.5))
    tg, ig = np.meshgrid(t, i)
    cb_format = FuncFormatter(lambda val,pos: '{:.0g}$\pi$'.format(val/np.pi) if val !=0 else '0')
    hm = ax[0].pcolor(tg, ig, spatial_phi.T, cmap=newcmp)#, shading='auto')
    cbar = plt.colorbar(hm, ax=ax[0], format = cb_format)
    #cbar.set_label(label='$\phi_k(t)$', rotation=0, fontsize=14, )
    ax[0].text(3500, 50, '$\Phi_k(t)$', fontsize=18)
    ax[0].set_ylabel('$n^{th}$-neuron')
    ax[0].set_title('Phase map with a GOP; transient: 7000 ms'+network_infos)

    sns.lineplot(gop, ax=ax[1], color='darkred', label='Global Order Parameter')
    #ax[1].legend(loc='lower right')
    ax[1].set_xlim(0,3700)
    ax[1].spines['right'].set_visible(False)
    ax[1].spines['top'].set_visible(False)
    ax[1].set_ylim(-0.05,1.05)
    ax[1].set_xlabel('Time (ms)')
    fig.set_tight_layout(2)
    plt.savefig(f'../new_figures/{infos}_Gop.png', dpi=600, )

def kuramoto_param_local_order(spatial_phase, k):
    """
    Calculates the Kuramoto parameter order for a given spatial phase distribution.

    Args:
        spatial_phase (numpy.ndarray): Array representing the spatial phase distribution of neurons.
        k (int): Number of neighboring neurons to consider.

    Returns:
        numpy.ndarray: Array of Kuramoto parameter order values for each neuron.
    """
    n = len(spatial_phase)
    p = int(k/2)  # neurons in one direction
    z = np.zeros_like(spatial_phase)

    for i in range(n):
        somatorio = 0
        for vizinhos in range(i - p, i + p + 1):
            if vizinhos == 0 or vizinhos == n:
                j = n
            else:
                j = vizinhos % n
            if j >= n:
                j = j % n
            somatorio += np.exp(complex(0, spatial_phase[j]))
        z[i] = np.abs(somatorio / (int(2*p)+1))
    return z


def param_local_order(spkt, spkid, k, len_network=100, step_t = 1, trans=0):
    """
    Calculates the spatial phase and Kuramoto parameter order for a given spike data.

    Args:
        spkt (numpy.ndarray): Array of spike times.
        spkid (numpy.ndarray): Array of neuron IDs corresponding to spike times.
        len_network (int): Number of neurons in the network.
        k (int): Number of neighboring neurons to consider for Kuramoto parameter order.
        step_t (int, optional): Time step for phase calculation. Defaults to 1.

    Returns:
        tuple: A tuple containing the spatial phase array and Kuramoto parameter order array.
    """
     
    phimat = phase(spkt, spkid, len_network=len_network, step_t = step_t, trans=trans)

    # param order
    min_samples = np.min([len(phi) for phi in phimat])
    spatial_phi = np.array([phi[-min_samples:] for phi in phimat]).T
    z = np.array([kuramoto_param_local_order(phi, k=k) for phi in spatial_phi])

    return spatial_phi, z

def plot_phase_lop(spatial_phi, lop, fname, k):
    t = np.arange(spatial_phi.shape[0])
    i = np.arange(spatial_phi.shape[1])


    fig, ax = plt.subplots(ncols=1, nrows=2, figsize=(10,5))
    tg, ig = np.meshgrid(t, i)
    cb_format = FuncFormatter(lambda val,pos: '{:.0g}$\pi$'.format(val/np.pi) if val !=0 else '0')
    hm = ax[0].pcolor(tg, ig, spatial_phi.T, cmap=newcmp)#, shading='auto')
    cbar = plt.colorbar(hm, ax=ax[0], format = cb_format)
    ax[0].text(3500, 50, '$\Phi_k(t)$', fontsize=18)
    ax[0].set_ylabel('$n^{th}$-neuron')
    ax[0].set_title(f'Phase map and LOP with $k={k}$; transient: 7000 ms'+network_infos)

    hm = ax[1].pcolor(tg, ig, lop.T, cmap='gnuplot', vmin=0, vmax=1)#, shading='auto')
    cbar = plt.colorbar(hm, ax=ax[1])
    #cbar.set_label(label='$\phi_k(t)$', rotation=0, fontsize=14, )
    ax[1].set_ylabel('$n^{th}$-neuron')
    ax[1].text(3500, 50, '$LOP(t)$', fontsize=18)
    ax[1].set_xlabel('Time (ms)')
    fig.set_tight_layout(2)
    plt.savefig(f'../new_figures/{infos}_Lop_k{k}.png', dpi=600)

def run_lop(k):
    spatial_phi, lop = param_local_order(spkt, spkid,k=k, trans=3000)
    del spatial_phi
    return lop
    


gex = [0.0001, 0.0002, 0.0003, 0.0004]

# external current
i_ext = np.arange(0.76,.91, 0.01)
currents = np.array_split(i_ext, len(i_ext)/4)
batch = 1

batchs_currents = {}
for g in gex:
    for current in currents:
        #print(f'python3 batch.py 6 {batch} {g:.5f} ' + f'{current}')
        for i, c in enumerate(current):
            batchs_currents[f'{g}_{c:.3f}'] = (batch, i)
        batch+=1
        
for key in batchs_currents:
    print(key)

batch_load = str(input('Digite o batch a ser lido: '))

b, c = batchs_currents[batch_load]
netdata = load_batch(b, c)

gex = netdata['simConfig']['gex']
amp = netdata['simConfig']['IClamp0']['amp']

infos = f'{gex:.4f}_{amp:.2f}'
network_infos = '\n$g_{ex}'+f'={gex:.4f}'+ '\qquad I_{ext}' f'={amp:.2f}'+'$'

plotRaster(netdata, ti=1000, fname=infos)

spkt=netdata['simData']['spkt']
spkid=netdata['simData']['spkid']

spatial_phi, gop = param_global_order(spkt, spkid, trans=3000)

plot_phase_gop(spatial_phi, gop, infos)

for vizinhos in [2,4,6,10,16,20]:
    lop = run_lop(vizinhos)
    plot_phase_lop(spatial_phi,lop, infos+f'k={vizinhos}', vizinhos)
