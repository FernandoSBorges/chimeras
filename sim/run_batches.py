"""
run_batches.py

Script python to run n-th batches 

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import os
import numpy as np

# coupling of elements
gex = np.arange(0.0001, 0.00044, 0.00002)
# external current
i_ext = np.arange(0.14, 0.31, 0.01)
currents = np.array_split(i_ext, 4)

batch = 1
for g in gex:
    for current in currents:
        os.system(f'python3 batch.py 3 {batch} {g:.5f} ' + f'{current}')
        batch+=1