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
gex = np.linspace(1,10,10) * 1e-5

# external current
i_ext = np.round(np.linspace(0.2,0.8,10), 3) #np.arange(0.61,1., 0.01)
currents = np.array_split(i_ext, len(i_ext)/2)

#desyncr_spikes_period = 7  # default 7 = 1 spike every 7.143ms
#desyncr_spikes_dur = 500 # defaut 500 = 50 ms
#numCellsDesync = 80  # numCells to produce desyncronization

batch = 1
for g in gex:
    for current in currents:
        os.system(f'python3 batch.py 6 {batch} {g:.5f} ' + f'{current}')
        for c in range(len(current)+1):
            os.system(f'python3 plotRaster.py 6 {batch} {c}')
        batch+=1




