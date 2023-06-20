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
gex = [0.0001]

# external current
i_ext = np.arange(0.5,1.01, 0.01)
currents = np.array_split(i_ext, 13)

#desyncr_spikes_period = 7  # default 7 = 1 spike every 7.143ms
#desyncr_spikes_dur = 500 # defaut 500 = 50 ms
#numCellsDesync = 80  # numCells to produce desyncronization

batch = 1
for g in gex:
    for current in currents:
        os.system(f'python3 batch.py 3 {batch} {g:.5f} ' + f'{current}')
        batch+=1


