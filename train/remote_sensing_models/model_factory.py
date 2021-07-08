import numpy as np
import tensorflow as tf
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Lambda, Concatenate, Add, Average

from train.params import *
from train.remote_sensing_models.extra_model import *
from train.remote_sensing_models.sst_model import *


def model_factory(adj, variables, reuse=True):

    inputs_list = []
    for vrb in params.remote_sensing_variables:
        inputs_list.append(Input(shape=(params.sequence_length, 320, 440, 1), name=vrb))

    sst = Input(shape=(params.sequence_length, 320, 440, 1), name='sst')

    variables_encoder_list = []
    if reuse:
        general_feature_extractor = ExtraModel()
        for each_input in inputs_list:
            variables_encoder_list.append(general_feature_extractor(each_input))
    else:
        for each_input in inputs_list:
            variables_encoder_list.append(ExtraModel()(each_input))

    extra = Concatenate(axis=1)(variables_encoder_list)
    outputs = SSTModel(adj=adj)({'sst': sst, 'extra': extra})

    # sst_mean = Average()(Lambda(lambda x: tf.split(x, num_or_size_splits=params.sequence_length, axis=1))(sst))
    # sst_mean = tf.squeeze(sst_mean, axis=1)
    # sst_mean = tf.keras.layers.Cropping2D(cropping=((2, 2), (2, 2)))(sst_mean)
    # outputs = Add()([sst_mean, sst_res])

    inputs_dic = {}
    for i, vrb in enumerate(params.remote_sensing_variables):
        inputs_dic[vrb] = inputs_list[i]
    inputs_dic["sst"] = sst

    model = Model(inputs=inputs_dic, outputs=outputs)

    print(model.summary())

    return model
