import numpy as np
import tensorflow as tf
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Concatenate, Lambda
from tensorflow.keras.layers import Flatten, Dropout, Reshape, BatchNormalization
from tensorflow.keras.layers import ConvLSTM2D, Conv2D, Dense, MaxPool2D, UpSampling2D, Conv2DTranspose
from tensorflow.keras.layers import Cropping2D

from train.params import *
from train.remote_sensing_models.integration_blocks import *
from train.remote_sensing_models.comparison_blocks import *
from train.remote_sensing_models.attention_layers import *
from train.remote_sensing_models.graph_convolution_layer import *


def SSTModel(adj):

    sst = Input(shape=(params.sequence_length, 320, 440, 1), name='sst')
    extra = Input(shape=(len(params.remote_sensing_variables), 8*11*32), name='extra')

    convLSTM_out = ConvLSTM2D(filters=2, kernel_size=(3, 3), activation=tf.keras.layers.LeakyReLU(), return_sequences=True,
                              padding='same', use_bias=True, dropout=0.3)(sst)      # (batch_size, sequence_length, 320, 440, 2)
    convLSTM_out = BatchNormalization()(convLSTM_out)

    convLSTM_out = ConvLSTMMaxPoolBlock(filters=4)(convLSTM_out)                   # (batch_size, sequence_length, 160, 220, 4)
    convLSTM_out = Reshape((params.sequence_length, 160*220*4))(convLSTM_out)
    alpha = ConvLSTMAttentionLayer(k=16, name='sst_attention_1')(convLSTM_out)
    conv_30_16 = WeightedSumBlock(reshape=True, l=params.sequence_length,
                                  w=160, h=220, c=4)((alpha, convLSTM_out))          # (batch_size, 160, 220, 4)
    convLSTM_out = Reshape((params.sequence_length, 160, 220, 4))(convLSTM_out)

    convLSTM_out = ConvLSTMMaxPoolBlock(filters=8)(convLSTM_out)                   # (batch_size, sequence_length, 80, 110, 8)
    convLSTM_out = Reshape((params.sequence_length, 80*110*8))(convLSTM_out)
    alpha = ConvLSTMAttentionLayer(k=16, name='sst_attention_2')(convLSTM_out)
    conv_15_32 = WeightedSumBlock(reshape=True, l=params.sequence_length,
                                  w=80, h=110, c=8)((alpha, convLSTM_out))          # (batch_size, 80, 110, 8)
    convLSTM_out = Reshape((params.sequence_length, 80, 110, 8))(convLSTM_out)

    convLSTM_out = ConvLSTMMaxPoolBlock(filters=16)(convLSTM_out)                   # (batch_size, sequence_length, 40, 55, 16)
    convLSTM_out = Reshape((params.sequence_length, 40*55*16))(convLSTM_out)
    alpha = ConvLSTMAttentionLayer(k=16, name='sst_attention_3')(convLSTM_out)
    conv_7_64 = WeightedSumBlock(reshape=True, l=params.sequence_length,
                                 w=40, h=55, c=16)((alpha, convLSTM_out))             # (batch_size, 40, 55, 16)

    conv_out = Conv2D(filters=32, kernel_size=5, strides=5, activation=tf.keras.layers.LeakyReLU())(conv_7_64)
    sst_feature = Reshape((1, 8*11*32))(conv_out)
    graph_in = Concatenate(axis=1)([extra, sst_feature])
    graph_in = ParameterAttentionLayer(k=16)(graph_in)

    if params.experiment_style == 'original':
        chebys = ChebyshevPolynomials(adj, 3)
        graph_out = GraphConvolutionBlock(hidden_dim=8*11*32, supports=chebys)(graph_in) # (batch_size, 2, len(params.variables)*30*55*64)
        alpha = GraphConvolutionAttentionLayer(k=16)(graph_out)
        graph_attention_out = WeightedSumBlock(reshape=False, l=2)((alpha, graph_out))  # (batch_size, 1, len(params.variables)*30*55*64)
        graph_attention_out = Reshape(((1+len(params.remote_sensing_variables)), 8*11*32))(graph_attention_out)
        sst_out = Lambda(lambda x: tf.split(x, num_or_size_splits=(1+len(params.remote_sensing_variables)), axis=1))(graph_attention_out)[-1]
    elif params.experiment_style == 'comparison_1':
        sst_out = ComparisonBlock1()(graph_in)
    elif params.experiment_style == 'comparison_2':
        sst_out = ComparisonBlock2()(graph_in)

    sst_out = Reshape((8, 11, 32))(sst_out)                                          # (batch_size, 8, 11, 32)
    sst_out = Conv2DTranspose(filters=16, kernel_size=5, strides=5, activation=tf.keras.layers.LeakyReLU())(sst_out)
    sst_out = BatchNormalization()(sst_out)

    sst_out = Concatenate()([conv_7_64, sst_out])                                   # (batch_size, 40, 55, 32)
    sst_out = ConvTransUpSamplingBlock(filters=8)(sst_out)                          # (batch_size, 80, 110, 8)
    sst_out = Concatenate()([conv_15_32, sst_out])                                  # (batch_size, 80, 110, 16)
    sst_out = ConvTransUpSamplingBlock(filters=4)(sst_out)                          # (batch_size, 160, 220, 4)
    sst_out = Concatenate()([conv_30_16, sst_out])                                  # (batch_size, 160, 220, 8)
    sst_out = ConvTransUpSamplingBlock(filters=2)(sst_out)                          # (batch_size, 320, 440, 2)

    outputs = Conv2DTranspose(filters=1, kernel_size=3, strides=(1,1),
                              activation='tanh', padding='same')(sst_out)           # (batch_size, 320, 440, 1)
    model = Model(inputs={'sst': sst, 'extra': extra}, outputs=outputs)
    return model
