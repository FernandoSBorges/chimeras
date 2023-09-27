import sys
import pickle
import numpy as np
from metrics import *
import datetime

# read variables of file
v = str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)
delta = int(sys.argv[4])
file = f'../data/v{v}_{batch_number}/v{v}_{batch_number}_{subbatch_number}'

# file = f'../data/v1_batch0/v1_batch0'
delta = 5

now = datetime.datetime.now()
print(f'\n~~ Start pre processing {now}')
print(f'~ Read file: {file}')
with open(file+'_data.pkl', 'rb') as f:
    data = pickle.load(f)

step = data['simConfig']['recordStep']
n_neighbors = data['simConfig']['n_neighbors']
cellNumber = data['simConfig']['cellNumber']
r = n_neighbors / cellNumber
data['r'] = r
print(f'Cell number: {cellNumber} \t n_neighbors: {n_neighbors} \t r: {r}')
print(f"time simulation: {data['simData']['t'][-1]:.2f}\n")
t_data, v_data = get_numpy(data)

#ti_sample = int((data['simConfig']['desyncr_spikes_dur'] + 100) / 0.1)
ti_sample = int(6000 / step)
# ti_sample = 15000
# tf_sample = 51001
print(f"time sample: {data['simData']['t'][-1] - data['simData']['t'][ti_sample]:.2f}\n")


# data['ti_sample'] = ti_sample
# data['tf_sample'] = tf_sample

v_sample = v_data[:, ti_sample:] 
t_sample = t_data[ti_sample:]


print('~ Computing phase')
result_phase = phase_of_v(t_sample, v_sample, return_peaks=True)
t_phase, phases, peaksmat, t_peaks, id_first_spk, id_last_spk = result_phase
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
data['tempo_para_coerencia'] = time_to_coherence(gop, t_phase, gop_threshold = 0.90, percent_threshold=0.8)

std_thresholds = [0.05, 0.1, 0.2]
data['std_thresholds'] = std_thresholds
data['tau_gop'] = t_convergencia_gop(gop = gop, t_sample = t_phase, std_thresholds=std_thresholds)

print('~ Computing LOP:')
lops = {}
deltas = np.arange(delta, delta+1, 1)
print(f' -- deltas: {deltas}')
for d in deltas:
    print(f'--> d: {d}')
    lop = np.zeros_like(phases.T)
    for i, spatial_phase in enumerate(phases.T):
        lop[i] = kuramoto_param_local_order(spatial_phase, delta=d)
    lops[d] = lop
data['LOP_delta'] = lops

print('~ Computing Tau Convergence:')
tau_lops = {}
for d in deltas:
    print(f'--> d: {d}')
    tau_lops[d] = t_convergencia_lop(lop = data['LOP_delta'][d], t_sample=t_phase, std_thresholds=std_thresholds)
data['tau_lops_delta'] = tau_lops

get_size(file+'_data.pkl')
print(f'~ Dump pickle file: {file}\n')
with open(file+'_data.pkl', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
get_size(file+'_data.pkl')

now = datetime.datetime.now()
print(f'Finish preprocessing: {now}')

