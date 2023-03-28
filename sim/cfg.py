"""
cfg.py 

Simulation configuration for ...
This file has sim configs as well as specification for parameterized values in netParams.py 

Contributors: conradinho@gmail.com, fernandodasilvaborges@gmail.com
"""


import os
from matplotlib import pyplot as plt
from netpyne import specs

cfg = specs.SimConfig()     

#------------------------------------------------------------------------------
#
# SIMULATION CONFIGURATION
#
#------------------------------------------------------------------------------

cfg.coreneuron = False

rootFolder = os.getcwd()

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------

cfg.duration = 3000.0 ## Duration of the sim, in ms  
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

cfg.allpops = []
cfg.allcells = ['sPYr'] #'sIN', 'sPYbr', 'sPYb', 'sPYr']
for i in range(0,40):
    if i<10:
        cfg.allpops.append(f'{cfg.allcells[0]}_stim0{i}')
    else:
        cfg.allpops.append(f'{cfg.allcells[0]}_stim{i}')

#------------------------------------------------------------------------------
# Analysis and plotting 
#------------------------------------------------------------------------------
#cfg.analysis['plotTraces'] = {'include': cfg.allpops[-5:], 'saveFig': True, 'showFig': False, 'oneFigPer':'trace', 'overlay':False, 'figSize':(20, 9), 'fontSize':12}
#cfg.analysis['plot2Dnet']   = {'include': cfg.allcells, 'saveFig': True, 'showConns': False, 'figSize': (12,12), 'view': 'xz', 'fontSize':12} 

#------------------------------------------------------------------------------
# Current inputs 
#------------------------------------------------------------------------------
cfg.addIClamp = 1

delaystim = 500
durationstim = 2000
step1_current = 0.0

cfg.IClamp0 =   {'pop': f'{cfg.allcells[0]}_stim00', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.050}    
cfg.IClamp1 =   {'pop': f'{cfg.allcells[0]}_stim01', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.100}
cfg.IClamp2 =   {'pop': f'{cfg.allcells[0]}_stim02', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.150}
cfg.IClamp3 =   {'pop': f'{cfg.allcells[0]}_stim03', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.200}
cfg.IClamp4 =   {'pop': f'{cfg.allcells[0]}_stim04', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.250}
cfg.IClamp5 =   {'pop': f'{cfg.allcells[0]}_stim05', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.300}
cfg.IClamp6 =   {'pop': f'{cfg.allcells[0]}_stim06', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.350}
cfg.IClamp7 =   {'pop': f'{cfg.allcells[0]}_stim07', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.400}
cfg.IClamp8 =   {'pop': f'{cfg.allcells[0]}_stim08', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.450}
cfg.IClamp9 =   {'pop': f'{cfg.allcells[0]}_stim09', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.500}
cfg.IClamp10 =  {'pop': f'{cfg.allcells[0]}_stim10', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.550}
cfg.IClamp11 =  {'pop': f'{cfg.allcells[0]}_stim11', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.600}
cfg.IClamp12 =  {'pop': f'{cfg.allcells[0]}_stim12', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.650}
cfg.IClamp13 =  {'pop': f'{cfg.allcells[0]}_stim13', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.700}
cfg.IClamp14 =  {'pop': f'{cfg.allcells[0]}_stim14', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.750}
cfg.IClamp15 =  {'pop': f'{cfg.allcells[0]}_stim15', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.800}
cfg.IClamp16 =  {'pop': f'{cfg.allcells[0]}_stim16', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.850}
cfg.IClamp17 =  {'pop': f'{cfg.allcells[0]}_stim17', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.900}
cfg.IClamp18 =  {'pop': f'{cfg.allcells[0]}_stim18', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 0.950}
cfg.IClamp19 =  {'pop': f'{cfg.allcells[0]}_stim19', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.000}
cfg.IClamp20 =  {'pop': f'{cfg.allcells[0]}_stim20', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.050}
cfg.IClamp21 =  {'pop': f'{cfg.allcells[0]}_stim21', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.100}
cfg.IClamp22 =  {'pop': f'{cfg.allcells[0]}_stim22', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.150}
cfg.IClamp23 =  {'pop': f'{cfg.allcells[0]}_stim23', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.200}
cfg.IClamp24 =  {'pop': f'{cfg.allcells[0]}_stim24', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.250}
cfg.IClamp25 =  {'pop': f'{cfg.allcells[0]}_stim25', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.300}
cfg.IClamp26 =  {'pop': f'{cfg.allcells[0]}_stim26', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.350}
cfg.IClamp27 =  {'pop': f'{cfg.allcells[0]}_stim27', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.400}
cfg.IClamp28 =  {'pop': f'{cfg.allcells[0]}_stim28', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.450}
cfg.IClamp29 =  {'pop': f'{cfg.allcells[0]}_stim29', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.500}
cfg.IClamp30 =  {'pop': f'{cfg.allcells[0]}_stim30', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.550}
cfg.IClamp31 =  {'pop': f'{cfg.allcells[0]}_stim31', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.600}
cfg.IClamp32 =  {'pop': f'{cfg.allcells[0]}_stim32', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.650}
cfg.IClamp33 =  {'pop': f'{cfg.allcells[0]}_stim33', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.700}
cfg.IClamp34 =  {'pop': f'{cfg.allcells[0]}_stim34', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.750}
cfg.IClamp35 =  {'pop': f'{cfg.allcells[0]}_stim35', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.800}
cfg.IClamp36 =  {'pop': f'{cfg.allcells[0]}_stim36', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.850}
cfg.IClamp37 =  {'pop': f'{cfg.allcells[0]}_stim37', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.900}
cfg.IClamp38 =  {'pop': f'{cfg.allcells[0]}_stim38', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 1.950}
cfg.IClamp39 =  {'pop': f'{cfg.allcells[0]}_stim39', 'sec': 'soma', 'loc': 0.5, 'start': delaystim, 'dur': durationstim, 'amp': 2.000}




#------------------------------------------------------------------------------
# Record Data 
#------------------------------------------------------------------------------

cfg.recordCells = cfg.allpops  # which cells to record from
cfg.recordTraces = {'V_soma': {'sec':'soma_0', 'loc':0.5, 'var':'v'}}  ## Dict with traces to record
cfg.recordStim = True
cfg.recordTime = True
cfg.recordStep = 0.1            

cfg.simLabel = f'Pospischil2008_{cfg.allcells[0]}'
cfg.saveFolder = '../data/'
# cfg.filename =                	## Set file output name
cfg.savePickle = False         	## Save pkl file
cfg.saveJson = True           	## Save json file
cfg.saveDataInclude = ['simConfig', 'netParams', 'simData'] ## 
cfg.backupCfgFile = None 		##  
cfg.gatherOnlySimData = False	##  
cfg.saveCellSecs = False			##  
cfg.saveCellConns = False		##  


