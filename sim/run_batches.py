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
gex = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005]

# external current
i_ext = np.arange(0.61,1., 0.01)
currents = np.array_split(i_ext, len(i_ext)/3)
#currents = [0.71, 0.9, 0.94]

#desyncr_spikes_period = 7  # default 7 = 1 spike every 7.143ms
#desyncr_spikes_dur = 500 # defaut 500 = 50 ms
#numCellsDesync = 80  # numCells to produce desyncronization

batch = 1
for g in gex:
    for current in currents:
        os.system(f'python3 batch.py 5 {batch} {g:.5f} ' + f'{current}')
        batch+=1




