import tensorflow as tf
from tensorflow.keras.layers import Concatenate, Lambda
from tensorflow.keras.layers import Flatten, Dropout, Reshape, BatchNormalization
from tensorflow.keras.layers import ConvLSTM2D, Conv2D, Dense, MaxPool2D, MaxPool3D, UpSampling2D, Conv2DTranspose
from tensorflow.keras.layers import Cropping2D, Concatenate, Add

from train.params import *
from train.remote_sensing_models.graph_convolution_layer import *


class ConvLSTMMaxPoolBlock(tf.keras.Model):
    def __init__(self, filters, kernel_size=3, pool_size=2, strides=2, return_sequences=True, **kwargs):
        super(ConvLSTMMaxPoolBlock, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.return_sequences = return_sequences
        self.conv_lstm = ConvLSTM2D(filters=filters, kernel_size=kernel_size, return_sequences=return_sequences,
                               padding='same', activation=tf.keras.layers.LeakyReLU())
        self.max_pool = MaxPool3D(pool_size=(1, pool_size, pool_size), strides=(1, strides, strides))
        self.bn = BatchNormalization()

    def call(self, inputs):
        conv_lstm_out = self.conv_lstm(inputs)
        pool_out = self.max_pool(conv_lstm_out)
        bn_out = self.bn(pool_out)
        return bn_out


class ConvMaxPoolBlock(tf.keras.Model):
    def __init__(self, filters, kernel_size=3, pool_size=2, strides=2, **kwargs):
        super(ConvMaxPoolBlock, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.conv = Conv2D(filters=filters, kernel_size=kernel_size, padding='same', activation=tf.keras.layers.LeakyReLU())
        self.max_pool = MaxPool2D(pool_size=pool_size, strides=strides)
        self.bn = BatchNormalization()

    def call(self, inputs):
        conv_out = self.conv(inputs)
        pool_out = self.max_pool(conv_out)
        bn_out = self.bn(pool_out)
        return bn_out


class ConvTransUpSamplingBlock(tf.keras.Model):
    def __init__(self, filters, kernel_size=3, strides=2, **kwargs):
        super(ConvTransUpSamplingBlock, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.conv_trans = Conv2DTranspose(filters=filters, kernel_size=kernel_size, padding='same', activation=tf.keras.layers.LeakyReLU())
        self.up_sampling = UpSampling2D(size=strides)
        self.bn = BatchNormalization()

    def call(self, inputs):
        conv_trans_out = self.conv_trans(inputs)
        up_sampling_out = self.up_sampling(conv_trans_out)
        bn_out = self.bn(up_sampling_out)
        return bn_out


class GraphConvolutionBlock(tf.keras.Model):
    def __init__(self, hidden_dim, supports, dropout_rate=0.5, **kwargs):
        super(GraphConvolutionBlock, self).__init__(**kwargs)
        self.hidden_dim = hidden_dim
        self.supports = supports
        self.dropout_rate = dropout_rate
        self.gc_layer1 = GraphConvolution(filters=hidden_dim, supports=supports, dropout_rate=dropout_rate, activation=tf.keras.layers.LeakyReLU())
        self.gc_layer2 = GraphConvolution(filters=hidden_dim, supports=supports, dropout_rate=dropout_rate, activation=tf.keras.layers.LeakyReLU())
        self.gc_layer3 = GraphConvolution(filters=hidden_dim, supports=supports, dropout_rate=dropout_rate, activation=tf.keras.layers.LeakyReLU())
        self.reshape = Reshape((1, (1+len(params.remote_sensing_variables))*hidden_dim))
        self.concatenate = Concatenate(axis=1)

    def call(self, inputs):
        gc_layer1_out = self.gc_layer1(inputs)
        gc_layer2_in = Add()([gc_layer1_out, inputs])
        gc_layer2_out = self.gc_layer2(gc_layer2_in)

        gc_layer1_out = self.reshape(gc_layer1_out)
        gc_layer2_out = self.reshape(gc_layer2_out)
        outputs = self.concatenate([gc_layer1_out, gc_layer2_out])
        return outputs


class WeightedSumBlock(tf.keras.Model):
    def __init__(self, reshape=None, l=None, w=None, h=None, c=None, **kwargs):
        super(WeightedSumBlock, self).__init__(**kwargs)
        self.l = l
        self.add = Add()
        self.reshape = reshape
        if self.reshape:
            self.w = w
            self.h = h
            self.c = c
            self.reshape1 = Reshape((l, w*h*c))
            self.reshape2 = Reshape((w, h, c))

    def call(self, inputs):
        info = inputs[1]
        if self.reshape:
            info = self.reshape1(info)
        info = tf.multiply(inputs[0], info)
        info = Lambda(lambda x: tf.split(x, num_or_size_splits=self.l, axis=-2))(info)
        outputs = self.add(info)
        if self.reshape:
            outputs = self.reshape2(outputs)
        return outputs
