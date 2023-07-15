
"""
netParams.py

... model using NetPyNE

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

from netpyne import specs
import os
import numpy as np

netParams = specs.NetParams()   # object of class NetParams to store the network parameters

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg

#------------------------------------------------------------------------------
#
# NETWORK PARAMETERS
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# General network parameters
#------------------------------------------------------------------------------
netParams.scale = 1.0 # Scale factor for number of cells
netParams.sizeX = 100.0 # x-dimension (horizontal length) size in um
netParams.sizeY = 100.0 # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = 100.0 # z-dimension (horizontal depth) size in um
netParams.shape = 'cylinder' # cylindrical (column-like) volume
   
netParams.propVelocity = 300.0    # propagation velocity (um/ms)
netParams.probLengthConst = 10.0 # length constant for conn probability (um)


#------------------------------------------------------------------------------
# Cell parameters
#------------------------------------------------------------------------------
for cellName in cfg.allcells:
    cellRule = netParams.importCellParams(label=cellName + '_rule', somaAtOrigin=False,
        conds={'cellType': cellName, 'cellModel': 'HH_simple'},
        fileName='cells/PospischilEtAl2008/cellwrapper_Pospischil2008.py',
        cellName='loadCell',
        cellArgs={'template': cellName},
        cellInstance = True,
        importSynMechs=True
        )

    # observation:
    # - when import template cells the label of 'soma' is 'soma_0'.
    # print(netParams.cellParams[cellName + '_rule']['secs']['soma_0'])

#------------------------------------------------------------------------------
# Population parameters
#------------------------------------------------------------------------------

# for ith-pop create pop with ith-cell of allcells 

for pop in cfg.allpops:
    netParams.popParams[pop] = {
        'cellType': pop,
        'cellModel': 'HH_simple',
        'numCells': cfg.cellNumber
    }

#------------------------------------------------------------------------------
# VecStim with spike times
#------------------------------------------------------------------------------
spkTimes = [ti for ti in range(1, cfg.desyncr_spikes_dur + 1, cfg.desyncr_spikes_period)] # spikes during 50 ms to create desyncronization
netParams.popParams['initialspikes'] = {'cellModel': 'VecStim', 'numCells': cfg.numCellsDesync, 'spkTimes': spkTimes}  

#------------------------------------------------------------------------------
# Current inputs (IClamp)
#------------------------------------------------------------------------------
if cfg.addIClamp:
     for key in [k for k in dir(cfg) if k.startswith('IClamp')]:
        params = getattr(cfg, key, None)
        [pop,sec,loc,start,dur,amp] = [params[s] for s in ['pop','sec','loc','start','dur','amp']]
        #cfg.analysis['plotTraces']['include'].append((pop,0))  # record that pop
        # add stim source
        netParams.stimSourceParams[key] = {'type': 'IClamp', 'delay': start, 'dur': dur, 'amp': amp}
        # connect stim source to target
        netParams.stimTargetParams[key+'_'+pop] =  {
            'source': key, 
            'conds': {'pop': pop},
            'sec': sec, 
            'loc': loc}

#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------

netParams.synMechParams['NMDA'] = {'mod': 'Exp2Syn', 'tau1': 15.0, 'tau2': 150.0, 'e': 0.0}
netParams.synMechParams['AMPA'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 5.0, 'e': 0.0}
ESynMech    = ['AMPA', 'NMDA']

#------------------------------------------------------------------------------
# Connectivity rules
#------------------------------------------------------------------------------

## Spatial disposition of neurons
r = netParams.sizeX/2.0  # radius of circle
dist_between_neurons = 2.0*r*np.sin(np.pi/cfg.cellNumber)
radius_conns = cfg.n_neighbors * dist_between_neurons + 0.001

prob = '(dist_2D<%s)' % (radius_conns)

# print(dist_between_neurons,radius_conns,prob)
netParams.connParams['EE'] = { 
    'preConds': {'pop': cfg.allpops},
    'postConds': {'pop': cfg.allpops},
    'synMech': 'AMPA', 
    'probability': prob, 
    'weight': cfg.gex, # 'delay': 'defaultDelay+dist_3D/propVelocity', 'synsPerConn': int(synperconnNumber[pre][post]+0.5)
    }

# connect initial spikes
netParams.connParams['initialrandom'] = { 
    'preConds': {'pop': 'initialspikes'},
    'postConds': {'pop': cfg.allpops},
    'synMech': 'AMPA', # target synaptic mechanism
    'probability': 0.50, 
    'weight': 0.0001, 
    'delay': 0.05
    }  

#------------------------------------------------------------------------------
# Description
#------------------------------------------------------------------------------
netParams.description = f""" 
- Code based: 
- v0    -   test
- v1    -   Reproduce a spike the one neuron in figures/Fig1_Pospischil_Minimal-Hodgkin–Huxley.png
- v2    -   A PRY neuron with various applied currents.
        -   Analyze the trigger frequency.
        -   i_ext = np.arange(0.1,1.1, 0.01)
        
- v3    -   building a non-local network with fix gex=0.0001 and i_ext = np.arange(0.5,1.01, 0.01)

- v4 - d1 Network without extra neurons to produce a noise.
     - d2 Network with 50 extra neurons to produce a noise.
     - d3 Network with 100 extra neurons to produce a noise.
     - d4 Network with 150 extra neurons to produce a noise.

- v5 - Run a network with gex [0.0001, 0.0002, 0.0003, 0.0004] and 
     - externar currents np.arange(0.76,.91, 0.01)

- v6    - Run network time simulation 3 ms
        - gex = np.round(np.linspace(6,40,10) * 1e-4, 6)
        - i_ext = np.round(np.linspace(0.72, 0.9, 10), 3)
        - lenght network = 100 neurons

- v7    - Run network time simulation 3 ms
        - gex = np.round(np.linspace(6,40,10) * 1e-4, 6)
        - i_ext = np.round(np.linspace(0.72, 0.9, 10), 3)
        - lenght network = 200 neurons

- v8    - Run network time simulation 6 ms
        - gex = np.round(np.linspace(6,10,10) * 1e-4, 6)
        - i_ext = np.round(np.linspace(0.72, 0.9, 10), 3)
        - lenght network = 100 neurons

- v8    - Run network time simulation 6 ms
        - gex = np.round(np.linspace(6,10,10) * 1e-4, 6)
        - i_ext = np.round(np.linspace(0.72, 0.9, 10), 3)
        - lenght network = 200 neurons
"""