"""
init.py

Starting script to run NetPyNE-based model.

Usage:
    - First, in the "sim" folder, run "nrnivmodl mod" in the terminal.
    - then python init.py # Run simulation, optionally plot a raster

MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""
from netpyne import sim
import pickle, json
import numpy as np

# import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers
from matplotlib import pyplot as plt


# cfg, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
cfg, netParams = sim.readCmdLineArgs()

sim.initialize(
    simConfig = cfg, 	
    netParams = netParams)  				# create network object and set cfg and net params
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations

# print(sim.rank,sim.net.cells[0].gid,sim.net.cells[0].tags)

r = 50  # radius
center = (50, 50) # center in um
theta = np.linspace(2*np.pi/cfg.cellNumber, 2*np.pi, cfg.cellNumber)  # angle 
x = center[0] + r*np.cos(theta) # x-values in um
z = center[1] + r*np.sin(theta) # z-values in um

for i, metype in enumerate(sim.net.cells):
    if 'sPY' in metype.tags['pop']:
        # looping to change the spatial coordinates of neurons
        ii = metype.gid
        metype.tags['x'] = x[ii]     # x positions in um (netParams.sizeX)
        metype.tags['y'] = 50.0
        metype.tags['z'] = z[ii]    # z positions in um (netParams.sizeZ)
        metype.tags['xnorm'] = metype.tags['x']/100.0
        metype.tags['ynorm'] = metype.tags['y']/100.0
        metype.tags['znorm'] = metype.tags['z']/100.0

# print(sim.rank,sim.net.cells[0].gid,sim.net.cells[0].tags)

sim.net.connectCells()            			# create connections between cells based on params
sim.net.addStims() 							# add network stimulation
sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)
sim.runSim()                      			# run parallel Neuron simulation  

sim.gatherData()                  			# gather spiking data and cell info from each node
sim.saveData()                    			# save params, cell info and sim output to file (pickle,mat,txt,etc)#

# sim.saveDataInNodes()
# sim.gatherDataFromFiles()

sim.analysis.plotData()         			# plot spike raster etc


# code to run with batch.py
rate = sim.analysis.plotSpikeStats(include=cfg.allpops, saveData='../data/'+cfg.simLabel[0:12]+'/'+cfg.simLabel + '_rate.json', stats=['rate'], saveFig=False)
isicv = sim.analysis.plotSpikeStats(include=cfg.allpops, saveData='../data/'+cfg.simLabel[0:12]+'/'+cfg.simLabel + '_CV.json', stats=['isicv'], saveFig=False)
sync = sim.analysis.plotSpikeStats(include=cfg.allpops, saveData='../data/'+cfg.simLabel[0:12]+'/'+cfg.simLabel + '_sync.json', stats=['sync'], saveFig=False)

# code to test with init.py
# rate = sim.analysis.plotSpikeStats(include=cfg.allpops, saveData='../data/'+cfg.simLabel + '_rate.json', stats=['rate'], saveFig=False)
# isicv = sim.analysis.plotSpikeStats(include=cfg.allpops, saveData='../data/'+cfg.simLabel + '_CV.json', stats=['isicv'], saveFig=False)
# sync = sim.analysis.plotSpikeStats(include=cfg.allpops, saveData='../data/'+cfg.simLabel + '_sync.json', stats=['sync'], saveFig=False)

#print("\n \t %s \t FR = %.3f Hz \t CV = %.3f \t sync = %.3f "  % (cfg.simLabel,np.mean(rate[1]['statData']),np.mean(isicv[1]['statData']),np.mean(sync[1]['statData'])))
