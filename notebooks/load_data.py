import pickle
import json
import pandas as pd
import numpy as np

data_cv_mean = pd.DataFrame({})
data_cv_std = pd.DataFrame({})

for batch in range(1,2000):
    if batch in list(range(10)): batch = f'0{batch}'
    for current in range(4):
        file = f'../data3/v1_batch{batch}/v1_batch{batch}_0_{current}_data.json'

        with open(file, 'rb') as f:
            data = json.load(f)

        amp = data['simConfig']['IClamp0']['amp']
        gex = data['simConfig']['gex']

        try:
            isicv_file = f'../data3/v1_batch{batch}/v1_batch{batch}_0_{current}_spikeStats_isicv.pkl'
            
            with open(isicv_file, 'rb') as f:
                isicv_data = pickle.load(f)

            cv = np.mean(isicv_data['statData'][0])
            cv_std = np.std(isicv_data['statData'][0])

            data_cv_mean.loc[amp, gex] = cv
            data_cv_std.loc[amp, gex] = cv_std

        except:
            raise Exception(f'Error to open: {isicv_file}')

data_cv_mean.to_csv('../data3/data_cv_mean.csv', sep=',')
data_cv_std.to_csv('../data3/data_cv_std.csv', sep=',')