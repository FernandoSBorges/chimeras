"""
run_batches.py

Script python to run n-th batches 

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import os
import numpy as np

gex = np.round(np.linspace(0.0005, .015,50),5)
i_ext = np.arange(0.09,2.09, 0.01) # [0.05,0.06,...., 2.05]
currents = np.array_split(i_ext, 40) # array split i_ext where each list have 5 elements

# 80 batches are executed  (40 gex + 40 eletric currents)
batch = 1
for g in gex:
    for current in currents:
        os.system(f'python3 batch.py 1 {batch} {g:.5f} ' + f'{current}')
        batch+=1
