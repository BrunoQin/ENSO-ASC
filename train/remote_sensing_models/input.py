import tensorflow as tf
import numpy as np

from train.params import *


def parse_fn(example):
    features = {
        'sst': tf.io.FixedLenFeature([], tf.string), 'uwind': tf.io.FixedLenFeature([], tf.string),
        'vwind': tf.io.FixedLenFeature([], tf.string), 'vapor': tf.io.FixedLenFeature([], tf.string),
        'cloud': tf.io.FixedLenFeature([], tf.string), 'rain': tf.io.FixedLenFeature([], tf.string),
        'output': tf.io.FixedLenFeature([], tf.string)}

    parsed = tf.io.parse_single_example(serialized=example, features=features)

    inputs_list = []
    for vrb in params.remote_sensing_variables:
        inputs_list.append(tf.reshape(tf.io.decode_raw(parsed[vrb], tf.float32), [params.sequence_length, 320, 440, 1])[:, :, :, :])

    sst = tf.reshape(tf.io.decode_raw(parsed['sst'], tf.float32), [params.sequence_length, 320, 440, 1])[:, :, :, :]
    output = tf.reshape(tf.io.decode_raw(parsed['output'], tf.float32), [320, 440, 1])[:, :, :]

    input_features = {}
    for i, vrb in enumerate(params.remote_sensing_variables):
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
