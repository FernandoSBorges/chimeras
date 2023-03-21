import os
import netParams
import cfg
from netpyne import sim


rootFolder = os.getcwd()

sim.createSimulateAnalyze(netParams, cfg)