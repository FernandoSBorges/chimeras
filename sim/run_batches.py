"""
run_batches.py

Script python to run n-th batches 

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import os
import numpy as np

# coupling of elements
gex = [0.0]
# external current
i_ext = i_ext = np.arange(0.1,1.1, 0.01)
currents = np.array_split(i_ext, 25)

batch = 1
for g in gex:
    for current in currents:
        os.system(f'python3 batch.py 1 {batch} {g:.5f} ' + f'{current}')
        batch+=1