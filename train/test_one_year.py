import tensorflow as tf
import numpy as np
import pandas as pd
import netCDF4 as nc
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap
from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer
from mpl_toolkits.axes_grid1 import ImageGrid

from data.remote_sensing_dataset.remss_averaged import REMSSaveraged
from train.remote_sensing_models.model_factory import *
from train.params import *
from train.components.predict_helper import *
from train.components.correlation_helper import *


def preprocess_helper():

    pwat = np.load(f"{params.remote_sensing_npz_dir}/{'rain-no-nan'}.npz")['rain']
    cwat = np.load(f"{params.remote_sensing_npz_dir}/{'cloud-no-nan'}.npz")['cloud']
    rh = np.load(f"{params.remote_sensing_npz_dir}/{'vapor-no-nan'}.npz")['vapor']
    uwind = np.load(f"{params.remote_sensing_npz_dir}/{'uwind-no-nan'}.npz")['uwind']
    vwind = np.load(f"{params.remote_sensing_npz_dir}/{'vwind-no-nan'}.npz")['vwind']
    sst = np.load(f"{params.remote_sensing_npz_dir}/{'sst-no-nan'}.npz")['sst']

    sst[abs(sst) < 8e-17] = 0
    rh[abs(rh) < 5e-16] = 0
    sst_origin = sst

    # pwat = np.load(f"{params.reanalysis_npz_dir}/{'pwat-resolve'}.npz")['pwat']
    # cwat = np.load(f"{params.reanalysis_npz_dir}/{'cwat-resolve'}.npz")['cwat']
    # rh = np.load(f"{params.reanalysis_npz_dir}/{'rh-resolve'}.npz")['rh']
    # uwind = np.load(f"{params.reanalysis_npz_dir}/{'uwind-resolve'}.npz")['uwind']
    # vwind = np.load(f"{params.reanalysis_npz_dir}/{'vwind-resolve'}.npz")['vwind']
    # sst = np.load(f"{params.reanalysis_npz_dir}/{'sst-resolve'}.npz")['sst']
    #
    # sst = np.flipud(sst)
    # pwat = np.flipud(pwat)
    # cwat = np.flipud(cwat)
    # rh = np.flipud(rh)
    # uwind = np.flipud(uwind)
    # vwind = np.flipud(vwind)
    # sst[abs(sst) < 0] = 0
    # sst_origin = sst

    scaler = MinMaxScaler()
    # scaler = StandardScaler()
    # scaler = Normalizer()
    pwat = np.reshape(scaler.fit_transform(np.reshape(pwat, (-1, 320*440))), (1, -1, 320, 440, 1))
    cwat = np.reshape(scaler.fit_transform(np.reshape(cwat, (-1, 320*440))), (1, -1, 320, 440, 1))
    rh = np.reshape(scaler.fit_transform(np.reshape(rh, (-1, 320*440))), (1, -1, 320, 440, 1))
    uwind = np.reshape(scaler.fit_transform(np.reshape(uwind, (-1, 320*440))), (1, -1, 320, 440, 1))
    vwind = np.reshape(scaler.fit_transform(np.reshape(vwind, (-1, 320*440))), (1, -1, 320, 440, 1))
    sst = np.reshape(scaler.fit_transform(np.reshape(sst, (-1, 320*440))), (1, -1, 320, 440, 1))

    return pwat, cwat, rh, uwind, vwind, sst, sst_origin


def plot_helper(data, llcrnrlon=150, urcrnrlon=230, llcrnrlat=-40, urcrnrlat=40, xgrid=0, ygrid=0, year=0):
    m = Basemap(projection="cyl", llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon,
                llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat, resolution='i')
    m.shadedrelief()
    # m.etopo()
    # m.fillcontinents(color='grey')
    m.drawcoastlines(linewidth=0.2)
    m.drawcountries()

    # m.drawparallels(np.arange(llcrnrlat, urcrnrlat+1, 30), labels=[True, False, True, False], linewidth=0.2, color='k', fontsize=6)
    # m.drawmeridians(np.arange(llcrnrlon, urcrnrlon+1, 30), labels=[True, False, False, True], linewidth=0.2, color='k', fontsize=6)
    # m.shadedrelief()

    xx = np.linspace(llcrnrlon, urcrnrlon, xgrid)
    yy = np.linspace(llcrnrlat, urcrnrlat, ygrid)
    Lon, Lat = np.meshgrid(xx, yy)
    x, y = m(Lon, Lat)
    cs = m.contourf(x, y, data, cmap=cmaps.GMT_panoply)

    UWind = np.load(f"{params.remote_sensing_npz_dir}/{'uwind-no-nan'}.npz")['uwind']
    VWind = np.load(f"{params.remote_sensing_npz_dir}/{'vwind-no-nan'}.npz")['vwind']
    VWind = VWind[year] - np.mean(VWind, axis=0)
    UWind = UWind[year] - np.mean(UWind, axis=0)
    uproj, vproj, xx, yy = m.transform_vector(UWind, VWind, np.linspace(160, 270, 440), np.linspace(-40, 40, 320), 31, 31, returnxy=True, masked=True)
    m.quiver(xx, yy, uproj, vproj)

    # cbar = m.colorbar(cs)
    # cbar.outline.set_linewidth(1)
    return m

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


if __name__ == "__main__":

    pwat, cwat, rh, uwind, vwind, sst, sst_origin = preprocess_helper()

    sst_scaler = MinMaxScaler()
    sst_scaler.fit_transform(np.reshape(sst_origin, (-1, 320*440)))
    cli_mean = np.mean(sst_origin, axis=0)

    one_year = range(213, 216)
    y_origin = []
    y_real = []
    x_in = []
    for m in one_year:
        scope = range(m, m + params.sequence_length)
        data = {
            'rain': pwat[:, scope, :, :, :], 'cloud': cwat[:, scope, :, :, :],
            'vapor': rh[:, scope, :, :, :], 'uwind': uwind[:, scope, :, :, :],
            'vwind': vwind[:, scope, :, :, :], 'sst': sst[:, scope, :, :, :]
        }
        x_in.append(data)
        y_origin.append(sst_origin[m+params.sequence_length-1+params.lead_time, :, :])

    y_forecast = []
    app = Predict()
    for m in range(len(one_year)):
        y_predict = np.reshape(np.squeeze(app.predict(x_in[m])), (1, 320*440))
        y_forecast.append(np.reshape(sst_scaler.inverse_transform(np.reshape(y_predict, (1, -1))), (320, 440)))

    fig = plt.figure(figsize=(300, 100))
    grid = ImageGrid(fig, 111, nrows_ncols=(2, 3), axes_pad=0.8,
                     cbar_mode='single', cbar_location="right")
    is_land = REMSSaveraged('./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y1997/m12/f12_19971207v7.1_d3d.gz').variables['land']
    is_land = is_land[200:520, 640:1080]
    for i in range(6):
        print(i)
        if i % 2 == 0:
            index = int(i / 2)
            data = y_forecast[index] - cli_mean
            sub_title = f'{months[index]}_prediction'
        else:
            index = int((i - 1) / 2)
            data = y_origin[index] - cli_mean
            sub_title = f'{months[index]}_real'

        for m in range(is_land.shape[0]):
            for n in range(is_land.shape[1]):
                if is_land[m, n] == True:
                    data[m, n] = np.nan
        plt.sca(grid[i])
        m = plot_helper(data=data, llcrnrlon=160, urcrnrlon=270, llcrnrlat=-40, urcrnrlat=40, xgrid=data.shape[1], ygrid=data.shape[0], year=one_year[index])
        # plt.title(sub_title, fontsize=6, pad=10)

    # plt.tight_layout()
    # cbar = fig.colorbar(m, cax=grid[i].cax)
    plt.colorbar(cax=grid[0].cax)
    # plt.tight_layout()
    plt.savefig(f'{params.outputs_dir}/one_year.jpg')
    plt.close(0)

    # ras_np_res_corr, ras_np_res_pear = correlation_helper(y_forecast, y_origin)
    # ras_np_res_corr = np.flipud(ras_np_res_corr)
    # is_land = REMSSaveraged('./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y1997/m12/f12_19971207v7.1_d3d.gz').variables['land']
    # is_land = is_land[200:520, 640:1080]
    # for m in range(is_land.shape[0]):
    #     for n in range(is_land.shape[1]):
    #         if is_land[m, n] == True:
    #             ras_np_res_corr[m, n] = np.nan
    # plot_helper(data=ras_np_res_corr, llcrnrlon=160, urcrnrlon=270, llcrnrlat=-40, urcrnrlat=40, xgrid=ras_np_res_corr.shape[1], ygrid=ras_np_res_corr.shape[0])
    # plt.show()
