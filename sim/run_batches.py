"""
run_batches.py

Script python to run n-th batches 

params: 
    - python3 batch.py version batch_number list_Gex list_I_ex

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import os
import numpy as np

gex = np.round(np.linspace(6,20,5) * 1e-4, 6)

# external current
i_ext = np.round(np.linspace(0.72, 0.9, 6), 3) #np.arange(0.61,1., 0.01)
currents = np.array_split(i_ext, 2)

#desyncr_spikes_period = 7  # default 7 = 1 spike every 7.143ms
#desyncr_spikes_dur = 500 # defaut 500 = 50 ms
#numCellsDesync = 80  # numCells to produce desyncronization

batch = 1
v = 1
neighbors = 4

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




