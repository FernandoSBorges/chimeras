"""
run_batches.py

Script python to run n-th batches 

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import os
import numpy as np

# coupling of elements
gex = [0.0001]

i_ext = np.arange(0.08, 0.31, 0.01)
currents = np.array_split(i_ext, 6)

batch = 1
for g in gex:
    for current in currents:
        os.system(f'python3 batch.py 2 {batch} {g:.5f} ' + f'{current}')
        batch+=1
