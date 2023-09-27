"""
cfg.py 

Simulation configuration for ...
This file has sim configs as well as specification for parameterized values in netParams.py 

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""


import os
from matplotlib import pyplot as plt
from netpyne import specs
import numpy as np

cfg = specs.SimConfig()     

#------------------------------------------------------------------------------
#
# SIMULATION CONFIGURATION
#
#------------------------------------------------------------------------------

cfg.simType = 'Pospischil2008_RS'

cfg.coreneuron = False

rootFolder = os.getcwd()

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------

cfg.duration = 12000.0 ## Duration of the sim, in ms  
cfg.dt = 0.01
# ~ cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 34, 'v_init': -65}  
cfg.verbose = False
cfg.createNEURONObj = True
cfg.createPyStruct = True
cfg.cvode_active = False
cfg.cvode_atol = 1e-6
cfg.cache_efficient = True
cfg.printRunTime = 0.5

cfg.includeParamsLabel = False
cfg.printPopAvgRates = True
cfg.checkErrors = False

# cfg.allpops = ['sPY', 'initialspikes']
# cfg.allcells = ['sPY']#, 'sIN']#, 'sPYbr', 'sPYb', 'sPYr', 'sPY']
cfg.allpops = ['sPY']
cfg.allcells = ['sPY']#, 'sIN']#, 'sPYbr', 'sPYb', 'r'sPY, 'sPY']

#------------------------------------------------------------------------------
# Net
#------------------------------------------------------------------------------
cfg.cellNumber = 200
cfg.gex = 0.00020 # default 0.0005
cfg.n_neighbors = 34 #int(0.3 * cfg.cellNumber) # all conetions 
cfg.amp = 0.75
cfg.synapse_delay = 0.025 #0.05 #1 #0.01
#------------------------------------------------------------------------------
# Current inputs 
#------------------------------------------------------------------------------
cfg.addIClamp = 1
# IClamp0 to produce spikes during 2000ms
cfg.IClamp0 =   {
    'pop': cfg.allpops[0],
    'cellList': list(range(cfg.cellNumber)),
    'sec': 'soma_0',
    'loc': 0.5,
    'start': 0,
    'dur': cfg.duration,
    'amp': cfg.amp #default 0.07
    }
# np.random.seed(23462825)
# cfg.cellListAmpExtra = list(set(np.random.randint(100, size=50)))
# cfg.IClamp1 =  {
#     'pop': cfg.allpops[0],
#     'cellList': list(range(50)),
#     'sec': 'soma_0',
#     'loc': 0.5,
#     'start': 0,
#     'dur': cfg.duration,
#     'amp': 0.0001 #default 0.07
#     }

# spikes during 50 ms to create desyncronization
# 50ms / 7 = 1 spike every 7.143ms
cfg.desyncr_spikes_period = 7  # default 7 = 1 spike every 7.143ms
cfg.desyncr_spikes_dur = 500 # defaut 500 = 50 ms
cfg.numCellsDesync = 70 #100 # numCells to produce desyncronization

#------------------------------------------------------------------------------
# Record Data 
#------------------------------------------------------------------------------
cfg.cellsrec = 0
if cfg.cellsrec == 0:  cfg.recordCells = cfg.allpops # record all cells (except cells to produce desync)
elif cfg.cellsrec == 1: cfg.recordCells = [(pop,0) for pop in cfg.allpops] # record one cell of each pop
elif cfg.cellsrec == 2: cfg.recordCells = [(pop,ii) for pop in cfg.allpops for ii in range(int(cfg.cellNumber/10))] # record 10 cells of each pop

#------------------------------------------------------------------------------
# Analysis and plotting 
#------------------------------------------------------------------------------
# cfg.analysis['plotTraces'] = {'include': cfg.allpops, 'saveFig': True, 'showFig': False, 'oneFigPer':'trace', 'overlay':True, 'figSize':(10, 4), 'fontSize':12}
# cfg.analysis['plotSpikeStats'] = {'include': cfg.allpops, 'stats':['rate', 'isicv', 'sync'],'saveData': True, 'saveFig': True, 'showFig': False, 'figSize': (12,12), 'fontSize':12}

# cfg.analysis['plot2Dnet']   = {
#     #cfg.allpops
#     'include': cfg.allpops , 'saveFig': True, 'showFig': False, 'showConns': True,
#     'figSize': (12,12), 'view': 'xz', 'fontSize':12,
#     }

# cfg.analysis['plotRaster'] = {  ## Plot a raster
#     'include': cfg.allpops, 'saveFig': True, 'showFig': False, 'popRates': False,
#     'orderInverse': True, 'timeRange': [600,cfg.duration],'figSize': (24,12),
#     'lw': 0.3, 'markerSize':10, 'marker': '.', 'dpi': 300, 'popColors':{'sPY':'black'}
#     }

# cfg.analysis['plotSpikeStats'] = {
#     'include': cfg.allpops, 'stats':['rate', 'isicv', 'sync'],
#     'saveData': True, 'saveFig': False, 'showFig': False,
#     'figSize': (12,12), 'fontSize':12
#     }

cfg.recordTraces = {'V_soma': {'sec':'soma_0', 'loc':0.5, 'var':'v'}}  ## Dict with traces to record
cfg.recordStim = True
cfg.recordTime = True
cfg.recordStep = 0.1            

cfg.simLabel = 'v1_batch0'  # default: v0_batch0
cfg.saveFolder = '../data/'+cfg.simLabel
# cfg.filename =                	## Set file output name
cfg.savePickle = True         	## Save pkl file
cfg.saveJson = False           	## Save json file
cfg.saveDataInclude = ['simConfig', 'netParams', 'simData'] ## 
cfg.backupCfgFile = None 		##  
cfg.gatherOnlySimData = False	##  
cfg.saveCellSecs = False			##  
cfg.saveCellConns = True		##
