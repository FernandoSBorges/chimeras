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
<<<<<<< HEAD
gex = [0.0001, 0.0002, 0.0003, 0.0004]# 0.0005]

# external current
i_ext = [0.72, 0.82, 0.92, 1.02]#np.arange(0.61,1., 0.01)
=======
# gex = np.arange(1,11) * 1e-5

# # external current
# i_ext = np.arange(0.76,.91, 0.01)
# currents = np.array_split(i_ext, len(i_ext)/4)
# currents = [0.71, 0.9, 0.94]

gex = np.linspace(1,16,10) * 1e-5

# external current
i_ext = np.round(np.linspace(0.76,.9, 10),decimals=5)
>>>>>>> 880fcb7 (Update files)
currents = np.array_split(i_ext, len(i_ext)/2)

#desyncr_spikes_period = 7  # default 7 = 1 spike every 7.143ms
#desyncr_spikes_dur = 500 # defaut 500 = 50 ms
#numCellsDesync = 80  # numCells to produce desyncronization

batch = 1
for g in gex:
    for current in currents:
        os.system(f'python3 batch.py 6 {batch} {g:.5f} ' + f'{current}')
<<<<<<< HEAD
=======
        for c in range(len(current)+1):
            os.system(f'python3 plotRaster.py 6 {batch} {c}')
>>>>>>> 880fcb7 (Update files)
        batch+=1




