"""
run_batches.py

Script python to run n-th batches 

params: 
    - python3 batch.py version batch_number list_Gex list_I_ex

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import os
import numpy as np

# coupling of elements
gex = np.round(np.linspace(6,8,20) * 1e-4, 6)
# external current
# i_ext = np.round(np.linspace(0.72, 0.9, 10), 3)
# currents = np.array_split(i_ext, 2)

n_cons_network = np.arange(11,31,1)
ncons = np.array_split(n_cons_network,5)

batch = 1
v = 9
k_max = 10

for g in gex[:41]:
    for conn in ncons:
        # os.system(f'python3 batch.py {v} {batch} {g:.6f} ' + f'{conn}')
        for c in range(len(ncons)):
            os.system(f'python3 preprocessing.py {v} {batch} {c} {k_max}')
            os.system(f'python3 plotRaster.py {v} {batch} {c}')
            os.system(f'python3 plotPhase.py {v} {batch} {c}')
            os.system(f'python3 plotHistBoxPlot.py {v} {batch} {c}')
            os.system(f'python3 plotGOP.py {v} {batch} {c}')
            os.system(f'python3 plotLOP.py {v} {batch} {c}')
            os.system(f'python3 plotMeanLOPWindow.py {v} {batch} {c}')
        batch+=1




