
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
   
netParams.propVelocity = 100.0    # propagation velocity (um/ms)
netParams.probLengthConst = 10.0 # length constant for conn probability (um)


#------------------------------------------------------------------------------
# Cell parameters
#------------------------------------------------------------------------------
for cellName in cfg.allcells:
    cellRule = netParams.importCellParams(label=cellName + '_rule', somaAtOrigin=False,
        conds={'cellType': cellName, 'cellModel': 'HH_full'},
        fileName='cellwrapper_Pospischil2008.py',
        cellName='loadCell',
        cellArgs={'template': cellName},
        cellInstance = True,
        importSynMechs=True
        )

    # observation:
    # - when import template cells the label of 'soma' is 'soma_0'.
    print(netParams.cellParams[cellName + '_rule']['secs']['soma_0'])

#------------------------------------------------------------------------------
# Population parameters
#------------------------------------------------------------------------------

# for ith-pop create pop with ith-cell of allcells 
numCells = 50
for i, pop in enumerate(cfg.allpops):
    netParams.popParams[pop] = {
        'cellType': cfg.allcells[i],
        'cellModel': 'HH_full',
        'numCells': numCells
    }

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
            'sec': f'{sec}_0', # target 'soma_0'
            'loc': loc}


#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------
#  Conrado: This synaptic mechanism is being used because of the NetPyNE Package Reference.
# http://www.netpyne.org/reference.html#synaptic-mechanisms-parameters
#   synaptic mechanism parameters for a simple excitatory synaptic mechanism labeled NMDA,
#   implemented using the Exp2Syn model, with rise time (tau1) of 0.1 ms, decay time (tau2)
#   of 5 ms, and equilibrium potential (e) of 0 mV
netParams.synMechParams['NMDA'] = {
    'mod': 'Exp2Syn',
    'tau1': 0.1,
    'tau2': 5.0,
    'e': 0
    }
# netParams.synMechParams['NMDA'] = {'mod': 'Exp2Syn', 'tau1': 15.0, 'tau2': 150.0, 'e': 0.0}
#netParams.synMechParams['AMPA'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 5.0, 'e': 0.0}
#ESynMech    = ['AMPA', 'NMDA']

#------------------------------------------------------------------------------
# Connectivity rules
#------------------------------------------------------------------------------

## Spatial disposition of neurons
r = 50  # radius of circle
center = (50, 50) # center in um
theta = np.linspace(0, 2*np.pi, numCells)  # angle 
x = center[0] + r*np.cos(theta) # x-values in um
z = center[1] + r*np.sin(theta) # z-values in um
dist_between_neurons = np.sqrt((x[1] - x[0])**2 + (z[1] - z[0])**2)

a0 = 1.0 # weight of probability
x0 = 1.
n_neighbors = 2

# number of neighbors * neuronal distance * (circlecorrection)
radius_conns = n_neighbors * dist_between_neurons

#'%s*exp(-%s*(dist_2D))*(dist_2D<%s)' % (a0, x0, radius_conns)
prob = '%s * (dist_2D<%s)' % (a0, radius_conns)

netParams.connParams['EE'] = { 
    'preConds': {'pop': cfg.allpops},
    'postConds': {'pop': cfg.allpops},
    'synMech': 'NMDA', #'AMPA', # ESynMech,
    'probability': prob, 
    'weight': 0.001 #gex, # 'delay': 'defaultDelay+dist_3D/propVelocity', 'synsPerConn': int(synperconnNumber[pre][post]+0.5)
    }

# netParams.connParams['all'] = {
#         'preConds': {'pop': cfg.allpops},
#         'postConds': {'pop': cfg.allpops},
#         'synMech': ['NMDA'],
#         'weight':0.05, 
#         'probability': 1#0.02 #'0.1*exp(-1/probLengthConst)',
# }