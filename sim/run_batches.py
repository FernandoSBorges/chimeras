"""
run_batches.py

Script python to run n-th batches 

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import os
import numpy as np

gex = [0.0]
i_ext = np.arange(0.01,1.51, 0.02)
currents = np.array_split(i_ext, 25) # array split i_ext where each list have 5 elements

batch = 1
for g in gex:
    for current in currents:
        os.system(f'python3 batch.py 3 {batch} {g:.5f} ' + f'{current}')
        batch+=1
