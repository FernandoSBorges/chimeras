"""
run_batches.py

Script python to run n-th batches 

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import os
import numpy as np

# coupling of elements
gex = [0.0001]

steps = 5
center = 0.2 # where to find chimera states
q = 0.01

min_current = center - steps*q
max_current = center + steps*q

i_ext = np.arange(min_current, max_current, q)
currents = np.array_split(i_ext, 4)

batch = 1
for g in gex:
    for current in currents:
        os.system(f'python3 batch.py 2 {batch} {g:.5f} ' + f'{current}')
        batch+=1
