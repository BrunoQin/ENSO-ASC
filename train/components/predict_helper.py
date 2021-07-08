import tensorflow as tf
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer

from train.remote_sensing_models.model_factory import *
from train.params import *


class Predict(object):
    def __init__(self):
        adj = pd.read_csv(f'{params.remote_sensing_dataset_dir}/adjacency.csv', header=None, sep=',').values
        adj = tf.constant(adj, dtype = tf.float32)
        self.model_factory = model_factory(adj, params.remote_sensing_variables)

    def predict(self, data):
        self.model_factory.load_weights(f'{params.archive_model_dir}/{params.checkpoint_file}')
        y_pred = self.model_factory.predict({
            'rain': data['rain'], 'cloud': data['cloud'],
            'vapor': data['vapor'], 'uwind': data['uwind'],
            'vwind': data['vwind'], 'sst': data['sst']
        })
        return y_pred[0]
