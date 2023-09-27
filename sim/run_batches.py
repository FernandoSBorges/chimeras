"""
run_batches.py

Script python to run n-th batches 

params: 
    - python3 batch.py version batch_number list_Gex list_n_cons_network

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import os
import numpy as np

# coupling of elements
# gex = np.round(np.arange(2.,3.1,0.2) * 1e-4, 6)
# external current
# i_ext = np.round(np.linspace(0.7, 0.9, 12), 3)
# currents = np.array_split(i_ext, 4)

# n_cons_network = np.arange(36,48,2)
# ncons = np.array_split(n_cons_network, 2)


# coupling of elements
gex = np.round(np.arange(1.9,2.2,0.1) * 1e-4, 6)
# external current
# i_ext = np.round(np.linspace(0.7, 0.9, 12), 3)
# currents = np.array_split(i_ext, 4)

n_cons_network = [30, 34, 38, 42]
ncons = np.array_split(n_cons_network, 1)


batch = 1
v = 7
delta_max = 5

for g in gex:
    for conn in ncons:
        # os.system(f'python3 batch.py {v} {batch} {g:.7f} ' + f'{conn}')
        for c in range(len(conn)):
            os.system(f'python3 preprocessing.py {v} {batch} {c} {delta_max}')
            os.system(f'python3 plotRaster.py {v} {batch} {c}')
            os.system(f'python3 plotGOP.py {v} {batch} {c}')
            os.system(f'python3 plotMeanLOP.py {v} {batch} {c}')
            os.system(f'python3 plotLOP.py {v} {batch} {c}')

            # os.system(f'python3 plotPhase.py {v} {batch} {c}')
            # os.system(f'python3 plotHistBoxPlot.py {v} {batch} {c}')
            # os.system(f'python3 plotHistBoxPlotLOP.py {v} {batch} {c}')
            # os.system(f'python3 plotMeanLOPWindow.py {v} {batch} {c}')
        batch+=1




