import tensorflow as tf
import numpy as np

from train.params import *


def parse_fn(example):
    features = {
        'cape': tf.io.FixedLenFeature([], tf.string), 'cin': tf.io.FixedLenFeature([], tf.string),
        'pot': tf.io.FixedLenFeature([], tf.string), 'pres': tf.io.FixedLenFeature([], tf.string),
        'pwat': tf.io.FixedLenFeature([], tf.string), 'rh': tf.io.FixedLenFeature([], tf.string),
        'tmp': tf.io.FixedLenFeature([], tf.string), 'uwind': tf.io.FixedLenFeature([], tf.string),
        'vwind': tf.io.FixedLenFeature([], tf.string), 'sst': tf.io.FixedLenFeature([], tf.string),
        'output': tf.io.FixedLenFeature([], tf.string)}

    parsed = tf.io.parse_single_example(serialized=example, features=features)

    inputs_list = []
    for vrb in params.reanalysis_variables:
        inputs_list.append(tf.reshape(tf.io.decode_raw(parsed[vrb], tf.float32), [params.sequence_length, 30, 30, 1]))

    sst = tf.reshape(tf.io.decode_raw(parsed['sst'], tf.float32), [params.sequence_length, 60, 60, 1])
    output = tf.reshape(tf.io.decode_raw(parsed['output'], tf.float32), [60, 60, 1])[2:58, 2:58, :]

    input_features = {}
    for i, vrb in enumerate(params.reanalysis_variables):
        input_features[vrb] = inputs_list[i]
    input_features["sst"] = sst

    return input_features, output


def train_input_fn():

    train_filenames = [params.preprocess_out_dir + "/train.tfrecords"]
    train_dataset = tf.data.TFRecordDataset(train_filenames)
    train_dataset = train_dataset.map(parse_fn)
    train_dataset = train_dataset.shuffle(params.random_seed).batch(params.batch_size)

    test_filenames = [params.preprocess_out_dir + "/test.tfrecords"]
    test_dataset = tf.data.TFRecordDataset(test_filenames)
    test_dataset = test_dataset.map(parse_fn)
    test_dataset = test_dataset.batch(params.batch_size)

    return train_dataset, test_dataset
