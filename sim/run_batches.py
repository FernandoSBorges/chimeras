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
gex = np.round(np.linspace(6,10,10) * 1e-4, 6)
# external current
i_ext = np.round(np.linspace(0.72, 0.9, 10), 3)
currents = np.array_split(i_ext, 2)

batch = 1
v = 8
neighbors = 10

for g in gex:
    for current in currents:
        os.system(f'python3 batch.py {v} {batch} {g:.6f} ' + f'{current}')
        for c in range(len(current)):
            os.system(f'python3 preprocessing.py {v} {batch} {c} {neighbors}')
            os.system(f'python3 plotRaster.py {v} {batch} {c}')
            os.system(f'python3 plotPhase.py {v} {batch} {c}')
            os.system(f'python3 plotGOP.py {v} {batch} {c}')
            os.system(f'python3 plotLOP.py {v} {batch} {c}')
        batch+=1




