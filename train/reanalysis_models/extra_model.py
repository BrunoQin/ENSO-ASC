import numpy as np
import tensorflow as tf
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import ConvLSTM2D, Conv2D, Dense, MaxPool2D, UpSampling2D
from tensorflow.keras.layers import Flatten, Dropout, Reshape, BatchNormalization

from train.params import *
from train.reanalysis_models.integration_blocks import *
from train.reanalysis_models.attention_layers import *


# Genral encoder network
def ExtraModel():
    extra = Input(shape=(params.sequence_length, 30, 30, 1), name='general')

    convLSTM_out = ConvLSTM2D(filters=8, kernel_size=(3, 3), activation=tf.keras.layers.LeakyReLU(), return_sequences=True,
                              padding='same', use_bias=True, dropout=0.3)(extra)    # (batch_size, sequence_length, 30, 30, 8)
    convLSTM_out = BatchNormalization()(convLSTM_out)

    convLSTM_out = ConvLSTMMaxPoolBlock(filters=16)(convLSTM_out)                   # (batch_size, sequence_length, 15, 15, 16)
    convLSTM_out = Reshape((params.sequence_length, 15*15*16))(convLSTM_out)
    alpha = ConvLSTMAttentionLayer(k=16, name='extra_attention')(convLSTM_out)
    convLSTM_out = WeightedSumBlock(reshape=True, l=params.sequence_length,
                                    w=15, h=15, c=16)((alpha, convLSTM_out))        # (batch_size, 15, 15, 16)

    conv_out = ConvMaxPoolBlock(filters=32)(convLSTM_out)                           # (batch_size, 7, 7, 32)
    conv_out = Conv2D(filters=64, kernel_size=3, padding='same',
                      activation=tf.keras.layers.LeakyReLU())(conv_out)                                  # (batch_size, 7, 7, 64)
    conv_out = BatchNormalization()(conv_out)

    outputs = Reshape((1, 7*7*64))(conv_out)
    model = Model(inputs=extra, outputs=outputs)
    return model
