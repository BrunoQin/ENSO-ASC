import numpy as np
# from fancyimpute import KNN, NuclearNormMinimization, SoftImpute, BiScaler

from data.remote_sensing_dataset.remss_averaged import REMSSaveraged


parameters = ['sst', 'wspd_lf', 'vapor', 'cloud', 'rain']

if __name__ == '__main__':
    is_land = REMSSaveraged('./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y1997/m12/f12_19971207v7.1_d3d.gz').variables['land']
    is_land = is_land[200:520, 640:1080]

    for para in parameters:
        data = np.load(f'./data/remote_sensing_dataset/final/{para}.npz')[para]
        print(para, data.shape)
        data = data[:, 200:520, 640:1080]

        for i in range(is_land.shape[0]):
            for j in range(is_land.shape[1]):
                if is_land[i, j] == True:
                    data[:, i, j] = 0

        # X = np.reshape(data, (data.shape[0], -1))

        # for j in range(X.shape[1]):
        #     if all(np.isnan(X[:, j])):
        #         X[:, j] = 0
        data[np.isnan(data)] = 0
        print(data)
        # biscaler = BiScaler()
        # softImpute = SoftImpute()
        # X_incomplete_normalized = biscaler.fit_transform(X)
        # X_filled_softimpute = softImpute.fit_transform(X_incomplete_normalized)
        # X_filled_softimpute = biscaler.inverse_transform(X_filled_softimpute)
        #
        # X = np.reshape(X_filled_softimpute, (data.shape[0], data.shape[1], data.shape[2]))

        data = {f'{para}': data}
        np.savez(f'./data/remote_sensing_dataset/final/{para}-no-nan.npz', **data)
