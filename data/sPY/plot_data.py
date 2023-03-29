"""
plot_data.py 

File to plot json data of simulations RS pyramidal excitatory and inhibitory neurons

Contributors: conradinho@gmail.com, fernandodasilvaborges@gmail.com
"""

import json
import seaborn as sns
import numpy as np

from matplotlib import pyplot as plt
sns.set_context('paper')

#------------------------------------------------------------------------------
# Read data
#------------------------------------------------------------------------------
f = open(f'Pospischil2008_RS_sPY_inh_data.json')
Pospischil2008_RS_sPY_data = json.load(f)

#------------------------------------------------------------------------------
# Set arrays
#------------------------------------------------------------------------------
amp = Pospischil2008_RS_sPY_data['simConfig']['IClamp0']['amp']
dur = Pospischil2008_RS_sPY_data['simConfig']['IClamp0']['dur']
start = Pospischil2008_RS_sPY_data['simConfig']['IClamp0']['start']
recordStep = Pospischil2008_RS_sPY_data['simConfig']['recordStep']

voltage = np.array(list(Pospischil2008_RS_sPY_data['simData']['V_soma'].values())[0])
time = np.array(Pospischil2008_RS_sPY_data['simData']['t'])
stim_current = np.array([0 if x < start/recordStep or x > (dur+start)/recordStep else amp for x in range(0, len(time))])


#------------------------------------------------------------------------------
# Plot figure
#------------------------------------------------------------------------------
f, (ax0, ax1) = plt.subplots(2,1, figsize=(10,3), gridspec_kw = {'height_ratios':[3, 1]})
sns.lineplot(x = time, y =voltage, color='black', ax=ax0)
ax1.plot(time,stim_current, 'gray')

ax0.set_ylabel('Voltage (mV)')
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.spines['bottom'].set_visible(False)
ax0.get_xaxis().set_visible(False)


ax1.plot([0,0],[0,0.15],'k')
ax1.text(20,0.125,f'{stim_current.max()}nA',va='center')
ax1.set_ylabel('I (nA)')
ax1.set_xlabel('t (ms)')

ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.get_yaxis().set_visible(False)
plt.tight_layout()

#------------------------------------------------------------------------------
# Save figure
#------------------------------------------------------------------------------
plt.savefig('RS_sPY_inh_spikes.png')