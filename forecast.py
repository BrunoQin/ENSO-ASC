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

def run_cmd(command):
    exitcode, output = subprocess.getstatusoutput(command)
    if exitcode != 0:
        raise Exception(output)
    return output

def write2File(filename, lag_month):
    with open(filename, "r", encoding="utf-8") as f_read:
        content = f_read.readlines()
    with open(filename, "w", encoding="utf-8") as f_write:
        for i in range(len(content)):
            if 'lead_time' in content[i]:
                f_write.write(f'flags.DEFINE_integer("lead_time", {lag_month}, "Lead time for predicting.")\n')
            elif 'checkpoint_file' in content[i]:
                f_write.write('flags.DEFINE_string("checkpoint_file", "' + f'forecast_{lag_month}.h5' + '", "Path to save trained models.")\n')
            else:
                f_write.write(content[i])

def prepare_model_and_data(lag_month):
    if os.path.exists(f'./checkpoints_archive/forecast_{lag_month}.h5'):
        write2File('./train/params.py', lag_month)
    else:
        template = ("model-{:1.0f} forecasting error!")
        logger.info(template.format(lag_month))

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


def forecast(lag_month):

    pwat, cwat, rh, uwind, vwind, sst, sst_origin, cli_mean = preprocess_helper()

    sst_scaler = MinMaxScaler()
    sst_scaler.fit_transform(np.reshape(sst_origin, (-1, 320*440)))

    length = sst_origin.shape[0]

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
    app = Predict()
    for m in range(len(forecast_domain)):
        y_predict = np.reshape(np.squeeze(app.predict(x_in[m])), (1, 320*440))
        y_forecast.append(np.reshape(sst_scaler.inverse_transform(np.reshape(y_predict, (1, -1))), (320, 440)))

    nino3_4 = []
    for m in range(len(forecast_domain)):
        y_anomaly = y_forecast[m] - cli_mean[(forecast_domain[m] + params.sequence_length - 1 + params.lead_time) % 12]
        nino3_4.append(np.mean(y_anomaly[140:180, 120:320]))
    template = ("model-{:1.0f} forecasting success!")
    logger.info(template.format(lag_month))
    return nino3_4

def colloct_result(result):
    f = open(f'result-{datetime.datetime.today().year}-{datetime.datetime.today().month}.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(f)
    for i in range(len(result)):
        csv_writer.writerow(result[i])
    f.close()


if __name__ == '__main__':
    result = []
    for lag_month in range(1, 19):
        prepare_model_and_data(lag_month)
        result.append(forecast(lag_month))
    colloct_result(result)
