import numpy as np
import tensorflow as tf
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Concatenate, Lambda
from tensorflow.keras.layers import Flatten, Dropout, Reshape, BatchNormalization
from tensorflow.keras.layers import ConvLSTM2D, Conv2D, Dense, MaxPool2D, UpSampling2D, Conv2DTranspose
from tensorflow.keras.layers import Cropping2D

from train.params import *
from train.reanalysis_models.integration_blocks import *
from train.reanalysis_models.comparison_blocks import *
from train.reanalysis_models.attention_layers import *
from train.reanalysis_models.graph_convolution_layer import *


def SSTModel(adj):

    sst = Input(shape=(params.sequence_length, 60, 60, 1), name='sst')
    extra = Input(shape=(len(params.reanalysis_variables), 7*7*64), name='extra')

    convLSTM_out = ConvLSTM2D(filters=8, kernel_size=(3, 3), activation=tf.keras.layers.LeakyReLU(), return_sequences=True,
                              padding='same', use_bias=True, dropout=0.3)(sst)      # (batch_size, sequence_length, 60, 60, 8)
    convLSTM_out = BatchNormalization()(convLSTM_out)

    convLSTM_out = ConvLSTMMaxPoolBlock(filters=16)(convLSTM_out)                   # (batch_size, sequence_length, 30, 30, 16)
    convLSTM_out = Reshape((params.sequence_length, 30*30*16))(convLSTM_out)
    alpha = ConvLSTMAttentionLayer(k=16, name='sst_attention_1')(convLSTM_out)
    conv_30_16 = WeightedSumBlock(reshape=True, l=params.sequence_length,
                                  w=30, h=30, c=16)((alpha, convLSTM_out))          # (batch_size, 30, 30, 16)
    convLSTM_out = Reshape((params.sequence_length, 30, 30, 16))(convLSTM_out)

    convLSTM_out = ConvLSTMMaxPoolBlock(filters=32)(convLSTM_out)                   # (batch_size, sequence_length, 15, 15, 32)
    convLSTM_out = Reshape((params.sequence_length, 15*15*32))(convLSTM_out)
    alpha = ConvLSTMAttentionLayer(k=16, name='sst_attention_2')(convLSTM_out)
    conv_15_32 = WeightedSumBlock(reshape=True, l=params.sequence_length,
                                  w=15, h=15, c=32)((alpha, convLSTM_out))          # (batch_size, 15, 15, 32)
    convLSTM_out = Reshape((params.sequence_length, 15, 15, 32))(convLSTM_out)

    convLSTM_out = ConvLSTMMaxPoolBlock(filters=64)(convLSTM_out)                   # (batch_size, sequence_length, 7, 7, 64)
    convLSTM_out = Reshape((params.sequence_length, 7*7*64))(convLSTM_out)
    alpha = ConvLSTMAttentionLayer(k=16, name='sst_attention_3')(convLSTM_out)
    conv_7_64 = WeightedSumBlock(reshape=True, l=params.sequence_length,
                                 w=7, h=7, c=64)((alpha, convLSTM_out))             # (batch_size, 7, 7, 64)

    sst_feature = Reshape((1, 7*7*64))(conv_7_64)
    graph_in = Concatenate(axis=1)([extra, sst_feature])
    graph_in = ParameterAttentionLayer(k=16)(graph_in)

    if params.experiment_style == 'original':
        chebys = ChebyshevPolynomials(adj, 3)
        graph_out = GraphConvolutionBlock(hidden_dim=7*7*64, supports=chebys)(graph_in) # (batch_size, 2, len(params.variables)*7*7*64)
        alpha = GraphConvolutionAttentionLayer(k=16)(graph_out)
        graph_attention_out = WeightedSumBlock(reshape=False, l=2)((alpha, graph_out))  # (batch_size, 1, len(params.variables)*7*7*64)
        graph_attention_out = Reshape(((1+len(params.reanalysis_variables)), 7*7*64))(graph_attention_out)
        sst_out = Lambda(lambda x: tf.split(x, num_or_size_splits=(1+len(params.reanalysis_variables)), axis=1))(graph_attention_out)[-1]
    elif params.experiment_style == 'comparison_1':
        sst_out = ComparisonBlock1()(graph_in)
    elif params.experiment_style == 'comparison_2':
        sst_out = ComparisonBlock2()(graph_in)

    sst_out = Reshape((7, 7, 64))(sst_out)                                          # (batch_size, 7, 7, 64)
    sst_out = BatchNormalization()(sst_out)

    sst_out = Concatenate()([conv_7_64, sst_out])                                   # (batch_size, 7, 7, 128)
    sst_out = ConvTransUpSamplingBlock(filters=32)(sst_out)                         # (batch_size, 14, 14, 32)
    sst_out = Concatenate()([Cropping2D(cropping=((1, 0), (1, 0)))(conv_15_32), sst_out])
    sst_out = ConvTransUpSamplingBlock(filters=16)(sst_out)                         # (batch_size, 28, 28, 16)
    sst_out = Concatenate()([Cropping2D(cropping=((1, 1), (1, 1)))(conv_30_16), sst_out])
    sst_out = ConvTransUpSamplingBlock(filters=8)(sst_out)                          # (batch_size, 56, 56, 8)

    outputs = Conv2DTranspose(filters=1, kernel_size=3, strides=(1,1),
                              activation='tanh', padding='same')(sst_out)           # (batch_size, 56, 56, 1)
    model = Model(inputs={'sst': sst, 'extra': extra}, outputs=outputs)
    return model
