import numpy as np
import tensorflow as tf
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import ConvLSTM2D, Conv2D, Dense, MaxPool2D, UpSampling2D
from tensorflow.keras.layers import Flatten, Dropout, Reshape, BatchNormalization

from train.params import *
from train.remote_sensing_models.integration_blocks import *
from train.remote_sensing_models.attention_layers import *


# Genral encoder network
def ExtraModel():
    extra = Input(shape=(params.sequence_length, 320, 440, 1), name='general')

    convLSTM_out = ConvLSTM2D(filters=2, kernel_size=(3, 3), activation=tf.keras.layers.LeakyReLU(), return_sequences=True,
                              padding='same', use_bias=True, dropout=0.3)(extra)      # (batch_size, sequence_length, 240, 320, 8)
    convLSTM_out = BatchNormalization()(convLSTM_out)

    convLSTM_out = ConvLSTMMaxPoolBlock(filters=4)(convLSTM_out)                   # (batch_size, sequence_length, 160, 220, 16)
    convLSTM_out = Reshape((params.sequence_length, 160*220*4))(convLSTM_out)
    alpha = ConvLSTMAttentionLayer(k=16, name='extra_attention_1')(convLSTM_out)
    conv_30_16 = WeightedSumBlock(reshape=True, l=params.sequence_length,
                                  w=160, h=220, c=4)((alpha, convLSTM_out))          # (batch_size, 120, 160, 16)
    convLSTM_out = Reshape((params.sequence_length, 160, 220, 4))(convLSTM_out)

    convLSTM_out = ConvLSTMMaxPoolBlock(filters=8)(convLSTM_out)                   # (batch_size, sequence_length, 80, 110, 32)
    convLSTM_out = Reshape((params.sequence_length, 80*110*8))(convLSTM_out)
    alpha = ConvLSTMAttentionLayer(k=16, name='extra_attention_2')(convLSTM_out)
    conv_15_32 = WeightedSumBlock(reshape=True, l=params.sequence_length,
                                  w=80, h=110, c=8)((alpha, convLSTM_out))          # (batch_size, 80, 110, 32)
    convLSTM_out = Reshape((params.sequence_length, 80, 110, 8))(convLSTM_out)

    convLSTM_out = ConvLSTMMaxPoolBlock(filters=16)(convLSTM_out)                   # (batch_size, sequence_length, 40, 55, 64)
    convLSTM_out = Reshape((params.sequence_length, 40*55*16))(convLSTM_out)
    alpha = ConvLSTMAttentionLayer(k=16, name='extra_attention_3')(convLSTM_out)
    conv_out = WeightedSumBlock(reshape=True, l=params.sequence_length,
                                w=40, h=55, c=16)((alpha, convLSTM_out))             # (batch_size, 40, 55, 64)

    conv_out = Conv2D(filters=32, kernel_size=5, strides=5, activation=tf.keras.layers.LeakyReLU())(conv_out)      # (batch_size, 6, 8, 64)
    outputs = Reshape((1, 8*11*32))(conv_out)
    model = Model(inputs=extra, outputs=outputs)
    return model
