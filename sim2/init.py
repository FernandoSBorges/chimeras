import os
import cfg
import netParams
from netpyne import sim
rootFolder = os.getcwd()

os.system('nrnivmodl mod')

sim.createSimulateAnalyze(netParams, cfg)

print(sim.simData)