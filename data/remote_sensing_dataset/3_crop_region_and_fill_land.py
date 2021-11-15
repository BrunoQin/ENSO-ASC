import numpy as np

from data.remote_sensing_dataset.remss_averaged import REMSSaveraged


parameters = ['sst', 'wspd_lf', 'vapor', 'cloud', 'rain']

if __name__ == '__main__':
    is_land = REMSSaveraged('./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y1997/m12/f12_19971207v7.1_d3d.gz').variables['land']
    is_land = is_land[200:520, 640:1080]

    for para in parameters:
        data = np.load(f'./data/remote_sensing_dataset/final/{para}-no-nan.npz')[para]
        print(para, data.shape)
        data = data[:, 200:520, 640:1080]

        for i in range(is_land.shape[0]):
            for j in range(is_land.shape[1]):
                if is_land[i, j] == True:
                    data[:, i, j] = 0

        data[np.isnan(data)] = 0

        data = {f'{para}': data}
        np.savez(f'./data/remote_sensing_dataset/final/{para}-no-nan.npz', **data)
