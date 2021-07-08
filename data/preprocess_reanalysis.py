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

    cape = np.load(f"{params.reanalysis_npz_dir}/{'cape'}.npz")['cape'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    cin = np.load(f"{params.reanalysis_npz_dir}/{'cin'}.npz")['cin'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    pot = np.load(f"{params.reanalysis_npz_dir}/{'pot'}.npz")['pot'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    pres = np.load(f"{params.reanalysis_npz_dir}/{'pres'}.npz")['pres'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    pwat = np.load(f"{params.reanalysis_npz_dir}/{'pwat'}.npz")['pwat'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    rh = np.load(f"{params.reanalysis_npz_dir}/{'rh'}.npz")['rh'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    tmp = np.load(f"{params.reanalysis_npz_dir}/{'tmp'}.npz")['tmp'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    uwind = np.load(f"{params.reanalysis_npz_dir}/{'uwind'}.npz")['uwind'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    vwind = np.load(f"{params.reanalysis_npz_dir}/{'vwind'}.npz")['vwind'].reshape((-1, 91, 180))[228:, 30:60, 80:110]
    sst_l = nc.Dataset(f"{params.reanalysis_dataset_dir}/meta-data/HadISST_sst.nc").variables['sst'][0:1740, 60:120, 340:360]
    sst_r = nc.Dataset(f"{params.reanalysis_dataset_dir}/meta-data/HadISST_sst.nc").variables['sst'][0:1740, 60:120, 0:40]
    sst = np.concatenate((sst_l, sst_r), axis=2).filled()
    sst[sst == -1.0e+30] = 0

    cape = np.flipud(cape)
    cin = np.flipud(cin)
    pot = np.flipud(pot)
    pres = np.flipud(pres)
    pwat = np.flipud(pwat)
    rh = np.flipud(rh)
    tmp = np.flipud(tmp)
    uwind = np.flipud(uwind)
    vwind = np.flipud(vwind)
    sst = np.flipud(sst)

    # cape -= np.mean(cape, axis=0)
    # cin -= np.mean(cin, axis=0)
    # pot -= np.mean(pot, axis=0)
    # pres -= np.mean(pres, axis=0)
    # pwat -= np.mean(pwat, axis=0)
    # rh -= np.mean(rh, axis=0)
    # tmp -= np.mean(tmp, axis=0)
    # uwind -= np.mean(uwind, axis=0)
    # vwind -= np.mean(vwind, axis=0)
    # sst -= np.mean(sst, axis=0)

    scaler = MinMaxScaler()
    # scaler = StandardScaler()
    # scaler = Normalizer()
    cape = np.reshape(scaler.fit_transform(np.reshape(cape, (-1, 30*30))), (-1, 30, 30))
    cin = np.reshape(scaler.fit_transform(np.reshape(cin, (-1, 30*30))), (-1, 30, 30))
    pot = np.reshape(scaler.fit_transform(np.reshape(pot, (-1, 30*30))), (-1, 30, 30))
    pres = np.reshape(scaler.fit_transform(np.reshape(pres, (-1, 30*30))), (-1, 30, 30))
    pwat = np.reshape(scaler.fit_transform(np.reshape(pwat, (-1, 30*30))), (-1, 30, 30))
    rh = np.reshape(scaler.fit_transform(np.reshape(rh, (-1, 30*30))), (-1, 30, 30))
    tmp = np.reshape(scaler.fit_transform(np.reshape(tmp, (-1, 30*30))), (-1, 30, 30))
    uwind = np.reshape(scaler.fit_transform(np.reshape(uwind, (-1, 30*30))), (-1, 30, 30))
    vwind = np.reshape(scaler.fit_transform(np.reshape(vwind, (-1, 30*30))), (-1, 30, 30))
    sst = np.reshape(scaler.fit_transform(np.reshape(sst, (-1, 60*60))), (-1, 60, 60))

    data = []
    target = []
    for i in range(cape.shape[0] - params.sequence_length + 1 - params.lead_time):
        data.append({'cape': cape[i:i+params.sequence_length].astype(np.float32),
                           'cin': cin[i:i+params.sequence_length].astype(np.float32),
                           'pot': pot[i:i+params.sequence_length].astype(np.float32),
                           'pres': pres[i:i+params.sequence_length].astype(np.float32),
                           'pwat': pwat[i:i+params.sequence_length].astype(np.float32),
                           'rh': rh[i:i+params.sequence_length].astype(np.float32),
                           'tmp': tmp[i:i+params.sequence_length].astype(np.float32),
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
            'cape': _bytes_feature(np.array(s['cape']).tobytes()),
            'cin': _bytes_feature(s['cin'].tobytes()),
            'pot': _bytes_feature(s['pot'].tobytes()),
            'pres': _bytes_feature(s['pres'].tobytes()),
            'pwat': _bytes_feature(s['pwat'].tobytes()),
            'rh': _bytes_feature(s['rh'].tobytes()),
            'tmp': _bytes_feature(s['tmp'].tobytes()),
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
