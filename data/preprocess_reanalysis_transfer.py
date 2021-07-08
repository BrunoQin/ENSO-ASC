import os
import json
import random
import numpy as np
import tensorflow as tf
import netCDF4 as nc
from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer
from sklearn.model_selection import train_test_split
from progress.bar import PixelBar

from train.params import *


# ---------- Helpers ----------
def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy()
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


# ---------- Prepare Data ----------
def parse_npz_and_nc_data():

    pwat = np.load(f"{params.reanalysis_npz_dir}/{'pwat-resolve'}.npz")['pwat']
    cwat = np.load(f"{params.reanalysis_npz_dir}/{'cwat-resolve'}.npz")['cwat']
    rh = np.load(f"{params.reanalysis_npz_dir}/{'rh-resolve'}.npz")['rh']
    uwind = np.load(f"{params.reanalysis_npz_dir}/{'uwind-resolve'}.npz")['uwind']
    vwind = np.load(f"{params.reanalysis_npz_dir}/{'vwind-resolve'}.npz")['vwind']
    sst = np.load(f"{params.reanalysis_npz_dir}/{'sst-resolve'}.npz")['sst']

    sst = np.flipud(sst)
    pwat = np.flipud(pwat)
    cwat = np.flipud(cwat)
    rh = np.flipud(rh)
    uwind = np.flipud(uwind)
    vwind = np.flipud(vwind)
    sst[abs(sst) < 0] = 0

    scaler = MinMaxScaler()
    # scaler = StandardScaler()
    # scaler = Normalizer()
    pwat = np.reshape(scaler.fit_transform(np.reshape(pwat, (-1, 320*440))), (-1, 320, 440))
    cwat = np.reshape(scaler.fit_transform(np.reshape(cwat, (-1, 320*440))), (-1, 320, 440))
    rh = np.reshape(scaler.fit_transform(np.reshape(rh, (-1, 320*440))), (-1, 320, 440))
    uwind = np.reshape(scaler.fit_transform(np.reshape(uwind, (-1, 320*440))), (-1, 320, 440))
    vwind = np.reshape(scaler.fit_transform(np.reshape(vwind, (-1, 320*440))), (-1, 320, 440))
    sst = np.reshape(scaler.fit_transform(np.reshape(sst, (-1, 320*440))), (-1, 320, 440))

    data = []
    target = []
    for i in range(sst.shape[0] - params.sequence_length + 1 - params.lead_time):
        data.append({'pwat': pwat[i:i+params.sequence_length].astype(np.float32),
                     'cwat': cwat[i:i+params.sequence_length].astype(np.float32),
                     'rh': rh[i:i+params.sequence_length].astype(np.float32),
                     'uwind': uwind[i:i+params.sequence_length].astype(np.float32),
                     'vwind': vwind[i:i+params.sequence_length].astype(np.float32),
                     'sst': sst[i:i+params.sequence_length].astype(np.float32)})
        target.append({'output': sst[i+params.sequence_length-1+params.lead_time].astype(np.float32)})

    train_data, test_data, train_target, test_target = train_test_split(data, target, test_size=params.train_eval_split, random_state=params.random_seed)
    print(len(train_data), len(test_data), len(train_target), len(test_target))
    return train_data, test_data, train_target, test_target

# ---------- IO ----------
def write_records(data, filename):
    series = data[0]
    target = data[1]
    writer = tf.io.TFRecordWriter(f'{params.preprocess_out_dir}/{filename}')

    bar = PixelBar(r'Generating', max=len(data), suffix='%(percent)d%%')
    for s, t in zip(series, target):
        example = tf.train.Example(features=tf.train.Features(feature={
            'rain': _bytes_feature(s['pwat'].tobytes()),
            'cloud': _bytes_feature(s['cwat'].tobytes()),
            'vapor': _bytes_feature(s['rh'].tobytes()),
            'uwind': _bytes_feature(s['uwind'].tobytes()),
            'vwind': _bytes_feature(s['vwind'].tobytes()),
            'sst': _bytes_feature(np.array(s['sst']).tobytes()),
            'output': _bytes_feature(np.array(t['output']).tobytes())}))
        writer.write(example.SerializeToString())
        bar.next()
    writer.close()
    bar.finish()


# ---------- Go! ----------
if __name__ == "__main__":
    if not os.path.exists(params.preprocess_out_dir):
        print("Creating output directory {}...".format(params.preprocess_out_dir))
        os.makedirs(params.preprocess_out_dir)

    print("Parsing raw data...")
    train_data, test_data, train_target, test_target = parse_npz_and_nc_data()
    print("Writing TF Records to file...")
    write_records((train_data, train_target), "train.tfrecords")
    write_records((test_data, test_target), "test.tfrecords")

    print("Done!")
