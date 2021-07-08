import tensorflow as tf
from tensorflow.keras.layers import Concatenate, Lambda
from tensorflow.keras.layers import Flatten, Dropout, Reshape, BatchNormalization
from tensorflow.keras.layers import ConvLSTM2D, Conv2D, Dense, MaxPool2D, MaxPool3D, UpSampling2D, Conv2DTranspose, Conv3D
from tensorflow.keras.layers import Cropping2D, Concatenate, Add

from train.params import *
from train.reanalysis_models.graph_convolution_layer import *


class ComparisonBlock1(tf.keras.Model):
    def __init__(self, **kwargs):
        super(ComparisonBlock1, self).__init__(**kwargs)

    def call(self, inputs):
        inputs = Lambda(lambda x: tf.split(x, num_or_size_splits=len(params.variables)+1, axis=-2))(inputs)
        outputs = Add()(inputs)
        return outputs


class ComparisonBlock2(tf.keras.Model):
    def __init__(self, **kwargs):
        super(ComparisonBlock2, self).__init__(**kwargs)
        self.conv3D = Conv3D(filters=64, kernel_size=(len(params.variables)+1, 3, 3), activation=tf.keras.layers.LeakyReLU())

    def call(self, inputs):
        inputs = Lambda(lambda x: tf.split(x, num_or_size_splits=len(params.variables)+1, axis=-2))(inputs)
        inputs = Lambda(lambda x: tf.stack(x, axis=1))(inputs)
        inputs = Reshape((len(params.variables)+1, 7, 7, 64))(inputs)
        paddings = [[0, 0], [0, 0], [1, 1], [1, 1], [0, 0]]
        inputs = Lambda(lambda x: tf.pad(x, paddings, mode='CONSTANT'))(inputs)
        outputs = self.conv3D(inputs)
        return outputs
