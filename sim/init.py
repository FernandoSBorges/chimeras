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

import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers
import seaborn as sns
from matplotlib import pyplot as plt


# cfg, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
cfg, netParams = sim.readCmdLineArgs()

sim.initialize(
    simConfig = cfg, 	
    netParams = netParams)  				# create network object and set cfg and net params
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations

r = 50  # radius
center = (50, 50) # center in um
theta = np.linspace(0, 2*np.pi, len(sim.net.cells))  # angle 
x = center[0] + r*np.cos(theta) # x-values in um
z = center[1] + r*np.sin(theta) # z-values in um

# print(sim.rank,sim.net.cells[0].tags)
for i, metype in enumerate(sim.net.cells):
    # looping to change the spatial coordinates of neurons
    metype.tags['xnorm'] = 0.5
    metype.tags['ynorm'] = 0.5
    metype.tags['znorm'] = 0.5
    metype.tags['x'] = x[i]     # x positions in um
    metype.tags['y'] = 50.0
    metype.tags['z'] = z[i]     # z positions in um
# print(sim.rank,sim.net.cells[0].tags)

sim.net.connectCells()            			# create connections between cells based on params
sim.net.addStims() 							# add network stimulation
sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)
sim.runSim()                      			# run parallel Neuron simulation  
sim.gatherData()                  			# gather spiking data and cell info from each node
sim.saveData()                    			# save params, cell info and sim output to file (pickle,mat,txt,etc)#
sim.analysis.plotData()         			# plot spike raster etc