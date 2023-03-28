"""
init.py

Starting script to run NetPyNE-based model.

Usage:
    - First, in the "sim" folder, run "nrnivmodl mod" in the terminal.
    - then python init.py # Run simulation, optionally plot a raster

MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py

Contributors: @gmail.com, fernandodasilvaborges@gmail.com
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

print(sim.rank,sim.net.cells[0].tags)
ii = 0
for i,metype in enumerate(sim.net.cells):

    ii = ii * 1      
    metype.tags['xnorm'] = 0.5
    metype.tags['ynorm'] = 0.5
    metype.tags['znorm'] = 0.5
    metype.tags['x'] = 50.0
    metype.tags['y'] = 50.0
    metype.tags['z'] = 50.0

print(sim.rank,sim.net.cells[0].tags)

sim.net.connectCells()            			# create connections between cells based on params
sim.net.addStims() 							# add network stimulation
sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)
sim.runSim()                      			# run parallel Neuron simulation  
sim.gatherData()                  			# gather spiking data and cell info from each node
sim.saveData()                    			# save params, cell info and sim output to file (pickle,mat,txt,etc)#
sim.analysis.plotData()         			# plot spike raster etc