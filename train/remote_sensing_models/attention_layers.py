import tensorflow as tf

from tensorflow.keras.layers import Concatenate, Lambda
from tensorflow.keras.layers import Flatten, Dropout, Reshape, BatchNormalization
from tensorflow.keras.layers import ConvLSTM2D, Conv2D, Dense, MaxPool2D, UpSampling2D, Conv2DTranspose
from tensorflow.keras.layers import Cropping2D, Concatenate, Add

from train.params import *


class ConvLSTMAttentionLayer(tf.keras.Model):
    def __init__(self, k, name):
        super(ConvLSTMAttentionLayer, self).__init__(name=name)
        self.layer1 = Dense(units=k, activation='tanh')
        self.layer2 = Dense(units=1)

    def call(self, inputs):
        outputs = self.layer2(self.layer1(inputs))
        outputs = tf.nn.softmax(outputs, axis=-2)
        # tf.print(outputs, output_stream=sys.stderr, summarize=-1)
        return outputs


class GraphConvolutionAttentionLayer(tf.keras.Model):
    def __init__(self, k, **kwargs):
        super(GraphConvolutionAttentionLayer, self).__init__(**kwargs)
        self.layer1 = Dense(units=k, activation=tf.keras.layers.LeakyReLU())
        self.layer2 = Dense(units=1)

    def call(self, inputs):
        outputs = self.layer2(self.layer1(inputs))
        outputs = tf.nn.softmax(outputs, axis=-2)
        return outputs


class ParameterAttentionLayer(tf.keras.Model):
    def __init__(self, k, **kwargs):
        super(ParameterAttentionLayer, self).__init__(**kwargs)
        self.layer1 = Dense(units=k, activation=tf.keras.layers.LeakyReLU())
        self.layer2 = Dense(units=1)

    def call(self, inputs):
        alpha = self.layer2(self.layer1(inputs))
        alpha = tf.nn.softmax(alpha, axis=-2)
        # tf.print(alpha, output_stream=sys.stderr, summarize=-1)
        outputs = tf.multiply(inputs, alpha)
        return outputs
