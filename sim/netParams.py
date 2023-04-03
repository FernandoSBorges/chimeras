
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
   

#------------------------------------------------------------------------------
# Cell parameters
#------------------------------------------------------------------------------
for cellName in cfg.allcells:
    cellRule = netParams.importCellParams(label=cellName + '_rule', somaAtOrigin=False,
        conds={'cellType': cellName, 'cellModel': 'HH_full'},
        fileName='cellwrapper_Pospischil2008.py',
        cellName='loadCell',
        cellArgs={'template': cellName},
        cellInstance = True)

    # observation:
    # - when import template cells the label of 'soma' is 'soma_0'.
    print(netParams.cellParams[cellName + '_rule']['secs']['soma_0'])

#------------------------------------------------------------------------------
# Population parameters
#------------------------------------------------------------------------------

# for ith-pop create pop with ith-cell of allcells 

for pop in cfg.allpops:
    netParams.popParams[pop] = {
        'cellType': cfg.allcells[0],
        'cellModel': 'HH_full',
        'numCells': 50
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