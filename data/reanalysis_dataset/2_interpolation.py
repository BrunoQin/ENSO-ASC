import os
import numpy as np
import netCDF4 as nc

from PIL import Image

from train.params import *


pwat = np.load(f"{params.reanalysis_npz_dir}/{'pwat'}.npz")['pwat'].reshape((-1, 91, 180))[228:, 25:65, 80:135]
cwat = np.load(f"{params.reanalysis_npz_dir}/{'cwat'}.npz")['cwat'].reshape((-1, 91, 180))[228:, 25:65, 80:135]
rh = np.load(f"{params.reanalysis_npz_dir}/{'rh'}.npz")['rh'].reshape((-1, 91, 180))[228:, 25:65, 80:135]
uwind = np.load(f"{params.reanalysis_npz_dir}/{'uwind'}.npz")['uwind'].reshape((-1, 91, 180))[228:, 25:65, 80:135]
vwind = np.load(f"{params.reanalysis_npz_dir}/{'vwind'}.npz")['vwind'].reshape((-1, 91, 180))[228:, 25:65, 80:135]
sst_l = nc.Dataset(f"{params.reanalysis_dataset_dir}/meta-data/HadISST_sst.nc").variables['sst'][0:1740, 50:130, 340:360]
sst_r = nc.Dataset(f"{params.reanalysis_dataset_dir}/meta-data/HadISST_sst.nc").variables['sst'][0:1740, 50:130, 0:90]
sst = np.concatenate((sst_l, sst_r), axis=2).filled()
sst[sst == -1.0e+30] = 0

print(pwat.shape, cwat.shape, rh.shape, uwind.shape, vwind.shape, sst.shape)

pwat_resolve = []
for i in range(pwat.shape[0]):
    data = pwat[i]
    size = tuple((data.shape[1] * 8, data.shape[0] * 8))
    data = np.array(Image.fromarray(data).resize(size, Image.BICUBIC))
    pwat_resolve.append(data)

cwat_resolve = []
for i in range(cwat.shape[0]):
    data = cwat[i]
    size = tuple((data.shape[1] * 8, data.shape[0] * 8))
    data = np.array(Image.fromarray(data).resize(size, Image.BICUBIC))
    cwat_resolve.append(data)

rh_resolve = []
for i in range(rh.shape[0]):
    data = rh[i]
    size = tuple((data.shape[1] * 8, data.shape[0] * 8))
    data = np.array(Image.fromarray(data).resize(size, Image.BICUBIC))
    rh_resolve.append(data)

uwind_resolve = []
for i in range(uwind.shape[0]):
    data = uwind[i]
    size = tuple((data.shape[1] * 8, data.shape[0] * 8))
    data = np.array(Image.fromarray(data).resize(size, Image.BICUBIC))
    uwind_resolve.append(data)

vwind_resolve = []
for i in range(vwind.shape[0]):
    data = vwind[i]
    size = tuple((data.shape[1] * 8, data.shape[0] * 8))
    data = np.array(Image.fromarray(data).resize(size, Image.BICUBIC))
    vwind_resolve.append(data)

sst_resolve = []
for i in range(sst.shape[0]):
    data = sst[i]
    size = tuple((data.shape[1] * 4, data.shape[0] * 4))
    data = np.array(Image.fromarray(data).resize(size, Image.BICUBIC))
    sst_resolve.append(data)

data = {'pwat': np.array(pwat_resolve)}
np.savez(f'{params.reanalysis_npz_dir}/pwat-resolve.npz', **data)
data = {'cwat': np.array(cwat_resolve)}
np.savez(f'{params.reanalysis_npz_dir}/cwat-resolve.npz', **data)
data = {'rh': np.array(rh_resolve)}
np.savez(f'{params.reanalysis_npz_dir}/rh-resolve.npz', **data)
data = {'uwind': np.array(uwind_resolve)}
np.savez(f'{params.reanalysis_npz_dir}/uwind-resolve.npz', **data)
data = {'vwind': np.array(vwind_resolve)}
np.savez(f'{params.reanalysis_npz_dir}/vwind-resolve.npz', **data)
data = {'sst': np.array(sst_resolve)}
np.savez(f'{params.reanalysis_npz_dir}/sst-resolve.npz', **data)
