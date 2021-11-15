import os
import numpy as np
import netCDF4 as nc

from train.params import *

base_path = f"{params.remote_sensing_dataset_dir}/meta-data/ccmp"

uwind = []
vwind = []
for f in os.listdir(base_path):
    if os.path.isfile(f'{base_path}/{f}'):
        uwind.append(nc.Dataset(f'{base_path}/{f}').variables['uwnd'][0])
        vwind.append(nc.Dataset(f'{base_path}/{f}').variables['vwnd'][0])

for m in os.listdir(f'{base_path}/Y2019'):
    temp_u = []
    temp_v = []
    print(m)
    for f in os.listdir(f'{base_path}/Y2019/{m}'):
        temp_u.append(np.mean(nc.Dataset(f'{base_path}/Y2019/{m}/{f}').variables['uwnd'], axis=0))
        temp_v.append(np.mean(nc.Dataset(f'{base_path}/Y2019/{m}/{f}').variables['vwnd'], axis=0))
    temp_u = np.array(temp_u)
    temp_v = np.array(temp_v)
    uwind.append(np.mean(temp_u, axis=0))
    vwind.append(np.mean(temp_v, axis=0))

for m in os.listdir(f'{base_path}/Y2020'):
    temp_u = []
    temp_v = []
    print(m)
    for f in os.listdir(f'{base_path}/Y2020/{m}'):
        temp_u.append(np.mean(nc.Dataset(f'{base_path}/Y2020/{m}/{f}').variables['uwnd'], axis=0))
        temp_v.append(np.mean(nc.Dataset(f'{base_path}/Y2020/{m}/{f}').variables['vwnd'], axis=0))
    temp_u = np.array(temp_u)
    temp_v = np.array(temp_v)
    uwind.append(np.mean(temp_u, axis=0))
    vwind.append(np.mean(temp_v, axis=0))

for m in os.listdir(f'{base_path}/Y2021'):
    temp_u = []
    temp_v = []
    print(m)
    for f in os.listdir(f'{base_path}/Y2020/{m}'):
        temp_u.append(np.mean(nc.Dataset(f'{base_path}/Y2020/{m}/{f}').variables['uwnd'], axis=0))
        temp_v.append(np.mean(nc.Dataset(f'{base_path}/Y2020/{m}/{f}').variables['vwnd'], axis=0))
    temp_u = np.array(temp_u)
    temp_v = np.array(temp_v)
    uwind.append(np.mean(temp_u, axis=0))
    vwind.append(np.mean(temp_v, axis=0))

uwind = np.array(uwind)
vwind = np.array(vwind)

uwind = uwind[:, 156:476, 640:1080]
vwind = vwind[:, 156:476, 640:1080]

print(uwind.shape)
print(vwind.shape)

data = {'uwind': uwind}
np.savez(f'{params.remote_sensing_npz_dir}/uwind-no-nan.npz', **data)

data = {'vwind': vwind}
np.savez(f'{params.remote_sensing_npz_dir}/vwind-no-nan.npz', **data)
