"""
Simplified model of bursting cortical neuron
	============================================

    Single-compartment model of bursting pyramidal neurons.
	The model is based on the presence of three voltage-dependent currents: 
        - INa, IK: action potentials
        - IM: slow K+ current for spike-frequency adaptation
"""

import os
import numpy as np
from scipy import signal
import seaborn as sns
from matplotlib import pyplot as plt


import matplotlib.colors as mcolors
cores = list(mcolors.TABLEAU_COLORS.keys())
cores = [cor.split(':')[-1] for cor in cores]

os.chdir('../notebooks/PospischilEtAl2008')

import neuron as nrn # NEURON simulator
nrn.h.load_file("mosinit.hoc");
nrn.h.load_file("demo_PY_IBR.hoc");

os.chdir('../..')

def create_soma(verbose=False):
    soma = nrn.h.Section(name='soma')
    soma.nseg = 1 #
    soma.diam = 96 #
    soma.L = 96 #			// so that area is about 29000 um2
    soma.cm = 1 #
    soma.Ra = 100 #		// geometry 

    if verbose:
        print("- Soma object:", soma)
        print("- Number of segments in the soma:", soma.nseg)
        print(f'- Diam: {soma.diam} | L: {soma.L} | cm: {soma.cm} | Ra: {soma.Ra}')
    return soma

def insert_mechanisms(soma, hh2=True, pas=True, im : float = False, return_mechs = False):
    if pas:
        soma.insert('pas')
        soma.e_pas = -70 #-85
        soma.g_pas = 1e-4 #1e-5 #		// idem TC cell

    if hh2:
        soma.insert('hh2'); #		// Hodgin-Huxley INa and IK 
        soma.ek = -100 #		// potassium reversal potential 
        soma.ena = 50 #			// sodium reversal potential 
        soma.vtraub_hh2 = -56.2 #-55 #	// Resting Vm, BJ was -55
        soma.gnabar_hh2 = 0.05 #	// McCormick=15 muS, thal was 0.09
        soma.gkbar_hh2 = 0.005 #	// spike duration of pyr cells
        celsius = 36
        v_init = -84
    
    if im:
        soma.insert('im'); #		// M current 
        taumax_im = 1000
        soma.gkbar_im = im # sPY template_im = 7.5e-5 #3e-5 #		// specific to LTS pyr cell
    
    if return_mechs:
        return soma, hh2, pas, im
    else:
        return soma


def simConfig(soma, t, amp, dur, delay, return_channels=False, verbose=False):
    # Simulations Config
    ## Runs:
    nrn.h.tstop = t
    nrn.h.dt = 0.025

    iclamp = nrn.h.IClamp(.5, sec=soma)
    iclamp.amp = amp # nA
    iclamp.delay = delay # ms
    iclamp.dur = dur # ms

    #### Vectors
    time = nrn.h.Vector()
    voltage = nrn.h.Vector()
    stim_current = nrn.h.Vector()

    time.record(nrn.h._ref_t)
    voltage.record(soma(.5)._ref_v);
    stim_current.record(iclamp._ref_i)

    mechs_ionic = {}
    for mechs, param_mechs in soma.psection()['density_mechs'].items():
        for key_mechs in param_mechs.keys():
            if key_mechs in ['m','n','h']:
                # find the mechanisms and create a vector to record data.
                mechs_ionic[f'{key_mechs}_{mechs}'] = nrn.h.Vector()

    channels = {}
    for channel, mechs in mechs_ionic.items():
        # for every ionic mechanism, get the attribute and record it
        ref_record = getattr(soma(.5), f'_ref_{channel}')
        channels[channel] = mechs.record(ref_record);
        if verbose:
            print(f'--> mechanism {mechs_ionic} of soma is recorded...')

    if verbose:
        print("- Simulation stop time: %f ms" % nrn.h.tstop)
        print("- Integration time step: %f ms" % nrn.h.dt)
        print("- Amplitude external current: %f nA" % iclamp.amp)
        print("- Duration external current: %f ms" % iclamp.dur)
        print("- Delay external current: %f ms" % iclamp.delay)
        print('- Return Channels: ', return_channels)
    nrn.h.run()
    
    if return_channels:
        return time, voltage, stim_current, channels
    else:
        return time, voltage, stim_current

def create_cell(im):
    soma = create_soma()
    soma = insert_mechanisms(soma, hh2=True, pas=True, im=im)
    return soma

def frequency(time_array, voltage_array):
    tpeaks, _ = signal.find_peaks(voltage_array)
    spkt = time_array[tpeaks[1:-1]]
    if len(spkt) > 1:
        freq = len(spkt)/(time_array[-1] - time_array[0]) # n spikes / t ms  = [Hz/10e-3]
        return freq * 1e3 # 
    else:
        return 0 


current_injected = np.linspace(0.01, 1.0, 100)
g_m = np.linspace(0, 10, 100)*1e-5

n = len(current_injected)
data = np.zeros((n,n))

for i, current in enumerate(current_injected):
    for j, g_im in enumerate(g_m):
        soma = create_cell(g_im)
        time, voltage, stim = simConfig(soma, 3000, current, 2800, 100, return_channels=False)
        freq = frequency(np.array(time),np.array(voltage))
        data[i, j] = freq
        

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

fig, ax = plt.subplots()
tg, ig = np.meshgrid(current_injected, g_m)
hm = ax.pcolor(ig, tg, data, cmap='jet')#, shading='auto')
cbar = plt.colorbar(hm, ax=ax, label='Fr(Hz)')
ax.set_ylabel('Injected Current (nA)')
ax.set_xlabel('$g_m$ (S/cm²)')
plt.savefig('./figures/YamadaModel_Space_param_freq2.png',dpi=600,)