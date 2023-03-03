import os
import csv
import datetime
import subprocess
import numpy as np

from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer
from loguru import logger

from train.components.predict_helper import *
from train.params import *


logger.add("./forecast.log", enqueue=True)


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

    scaler = MinMaxScaler()
    pwat = np.reshape(scaler.fit_transform(np.reshape(pwat, (-1, 320*440))), (1, -1, 320, 440, 1))
    cwat = np.reshape(scaler.fit_transform(np.reshape(cwat, (-1, 320*440))), (1, -1, 320, 440, 1))
    rh = np.reshape(scaler.fit_transform(np.reshape(rh, (-1, 320*440))), (1, -1, 320, 440, 1))
    uwind = np.reshape(scaler.fit_transform(np.reshape(uwind, (-1, 320*440))), (1, -1, 320, 440, 1))
    vwind = np.reshape(scaler.fit_transform(np.reshape(vwind, (-1, 320*440))), (1, -1, 320, 440, 1))
    sst = np.reshape(scaler.fit_transform(np.reshape(sst, (-1, 320*440))), (1, -1, 320, 440, 1))

    cli_mean = []
    for i in range(12):
        tem = sst_origin[i::12, ...]
        cli_mean.append(np.mean(tem, axis=0))
    cli_mean = np.array(cli_mean)

    return pwat, cwat, rh, uwind, vwind, sst, sst_origin, cli_mean


def colloct_result(result):
    f = open(f'result-{datetime.datetime.today().year}-{datetime.datetime.today().month}.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(f)
    for i in range(len(result)):
        csv_writer.writerow(result[i])
    f.close()


if __name__ == '__main__':

    pwat, cwat, rh, uwind, vwind, sst, sst_origin, cli_mean = preprocess_helper()
    sst_scaler = MinMaxScaler()
    sst_scaler.fit_transform(np.reshape(sst_origin, (-1, 320*440)))
    length = sst_origin.shape[0]

    result = []
    for lag_month in range(1, 20):
        forecast_domain = range(length - params.sequence_length + 1 - lag_month, length - params.sequence_length + 1)
        x_in = []
        for m in forecast_domain:
            scope = range(m, m + params.sequence_length)
            data = {
                'rain': pwat[:, scope, :, :, :], 'cloud': cwat[:, scope, :, :, :],
                'vapor': rh[:, scope, :, :, :], 'uwind': uwind[:, scope, :, :, :],
                'vwind': vwind[:, scope, :, :, :], 'sst': sst[:, scope, :, :, :]
            }
            x_in.append(data)

        y_forecast = []
        app = Predict(lag_month=lag_month)
        for m in range(len(forecast_domain)):
            y_predict = np.reshape(np.squeeze(app.predict(x_in[m])), (1, 320*440))
            y_forecast.append(np.reshape(sst_scaler.inverse_transform(np.reshape(y_predict, (1, -1))), (320, 440)))

        nino3_4 = []
        output = []
        for m in range(len(forecast_domain)):
            y_anomaly = y_forecast[m] - cli_mean[(forecast_domain[m] + params.sequence_length - 1 + params.lead_time) % 12]
            output.append(y_anomaly)
            nino3_4.append(np.mean(y_anomaly[140:180, 120:320]))
        np.savez(f'output-{lag_month}.npz', data=output)

        template = ("model-{:1.0f} forecasting success!")
        logger.info(template.format(lag_month))
        result.append(nino3_4)
    colloct_result(result)
