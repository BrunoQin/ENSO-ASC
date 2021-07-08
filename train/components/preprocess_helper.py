import numpy as np
import netCDF4 as nc

from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer

from train.params import *


def preprocess_helper():
    cape = np.load(f"{params.npz_dir}/{'cape'}.npz")['cape'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    cin = np.load(f"{params.npz_dir}/{'cin'}.npz")['cin'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    pot = np.load(f"{params.npz_dir}/{'pot'}.npz")['pot'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    pres = np.load(f"{params.npz_dir}/{'pres'}.npz")['pres'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    pwat = np.load(f"{params.npz_dir}/{'pwat'}.npz")['pwat'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    rh = np.load(f"{params.npz_dir}/{'rh'}.npz")['rh'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    tmp = np.load(f"{params.npz_dir}/{'tmp'}.npz")['tmp'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    uwind = np.load(f"{params.npz_dir}/{'uwind'}.npz")['uwind'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    vwind = np.load(f"{params.npz_dir}/{'vwind'}.npz")['vwind'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    sst_l = nc.Dataset(f"{params.dataset_dir}/HadISST_sst.nc").variables['sst'][0:1740, 60:120, 340:360]
    sst_r = nc.Dataset(f"{params.dataset_dir}/HadISST_sst.nc").variables['sst'][0:1740, 60:120, 0:40]
    sst = np.concatenate((sst_l, sst_r), axis=2).filled()
    sst[sst == -1.0e+30] = 0

    sst_origin_l = nc.Dataset(f"{params.dataset_dir}/HadISST_sst.nc").variables['sst'][0:1752, 60:120, 340:360]
    sst_origin_r = nc.Dataset(f"{params.dataset_dir}/HadISST_sst.nc").variables['sst'][0:1752, 60:120, 0:40]
    sst_origin = np.concatenate((sst_origin_l, sst_origin_r), axis=2).filled()
    sst_origin[sst_origin == -1.0e+30] = 0

    scaler = MinMaxScaler()
    # scaler = StandardScaler()
    # scaler = Normalizer()
    cape = np.reshape(scaler.fit_transform(np.reshape(cape, (-1, 30*30))), (1, -1, 30, 30, 1))
    cin = np.reshape(scaler.fit_transform(np.reshape(cin, (-1, 30*30))), (1, -1, 30, 30, 1))
    pot = np.reshape(scaler.fit_transform(np.reshape(pot, (-1, 30*30))), (1, -1, 30, 30, 1))
    pres = np.reshape(scaler.fit_transform(np.reshape(pres, (-1, 30*30))), (1, -1, 30, 30, 1))
    pwat = np.reshape(scaler.fit_transform(np.reshape(pwat, (-1, 30*30))), (1, -1, 30, 30, 1))
    rh = np.reshape(scaler.fit_transform(np.reshape(rh, (-1, 30*30))), (1, -1, 30, 30, 1))
    tmp = np.reshape(scaler.fit_transform(np.reshape(tmp, (-1, 30*30))), (1, -1, 30, 30, 1))
    uwind = np.reshape(scaler.fit_transform(np.reshape(uwind, (-1, 30*30))), (1, -1, 30, 30, 1))
    vwind = np.reshape(scaler.fit_transform(np.reshape(vwind, (-1, 30*30))), (1, -1, 30, 30, 1))
    sst = np.reshape(scaler.fit_transform(np.reshape(sst, (-1, 60*60))), (1, -1, 60, 60, 1))

    return cape, cin, pot, pres, pwat, rh, tmp, uwind, vwind, sst, sst_origin
