import sys
import pickle
import numpy as np
from metrics import *

# read variables of file
v = 'v'+str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)
neighbors = sys.argv[4]
file = f'../data/{v}_{batch_number}/{v}_{batch_number}_{subbatch_number}'


print('\n~~ Pre processing ')
with open(file+'_data.pkl', 'rb') as f:
    data = pickle.load(f)

size_in_mb = get_dict_size(data)

print(f"Tamanho do dicionário:{size_in_mb:.4f}MB")

t_data, v_data = get_numpy(data)
print('~ Computing phase')
t_phase, phases, peaksmat, t_peaks, id_first_spk, id_last_spk = phase_of_v(t_data, v_data, return_peaks=True)

data['t_phase'] = t_phase
data['phases'] = phases
data['peaksmat'] = peaksmat
data['t_peaks'] = t_peaks
data['id_first_spk'] = id_first_spk
data['id_last_spk'] = id_last_spk

print('~ Computing GOP')
gop = np.zeros(phases.shape[1])
for i, spatial_phase in enumerate(phases.T):
    gop[i] = kuramoto_param_global_order(spatial_phase)
data['GOP'] = gop

print('~ Computing LOP:')
lops = {}
for k in range(2, neighbors+1,2):
    print(f'--> K: {k}')
    lop = np.zeros_like(phases.T)
    for i, spatial_phase in enumerate(phases.T):
        lop[i] = kuramoto_param_local_order(spatial_phase, k=k)
    lops[k] = lop
data['LOP_k'] = lops

size_in_mb = get_dict_size(data)

print(f"Tamanho final do dicionário:{size_in_mb:.4f}MB")
print(f'~ Dump pickle file: {file}\n')
with open(file+'_data.pkl', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
