import os
os.environ["LOGURU_INFO_COLOR"] = "<green>"
import platform
import time
import re
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import pandas as pd
from loguru import logger

from progress.spinner import MoonSpinner

from train.params import *
EXP = params.EXP
if EXP == 'REMOTE-SENSING':
    from train.remote_sensing_models.model_factory import *
    from train.remote_sensing_models.loss_model import *
    from train.remote_sensing_models.input import *
elif EXP == 'REANALYSIS':
    from train.reanalysis_models.model_factory import *
    from train.reanalysis_models.loss_model import *
    from train.reanalysis_models.input import *


if 'Win' in platform.system():
    cross_device_ops = tf.distribute.HierarchicalCopyAllReduce(num_packs=2)
    strategy = tf.distribute.MirroredStrategy(cross_device_ops=cross_device_ops)
else:
    strategy = tf.distribute.MirroredStrategy()

GLOBAL_BATCH_SIZE = params.batch_size * strategy.num_replicas_in_sync

with strategy.scope():
    if EXP == 'REMOTE-SENSING':
        adj = pd.read_csv(f'{params.remote_sensing_dataset_dir}/adjacency.csv', header=None, sep=',').values
    elif EXP == 'REANALYSIS':
        adj = pd.read_csv(f'{params.reanalysis_dataset_dir}/adjacency.csv', header=None, sep=',').values
    adj = tf.constant(adj, dtype = tf.float32)
    if EXP == 'REMOTE-SENSING':
        model = model_factory(adj, params.remote_sensing_variables)
    elif EXP == 'REANALYSIS':
        model = model_factory(adj, params.reanalysis_variables)
    model_loss = Loss(model)
    optimizer = tf.keras.optimizers.Adam(learning_rate=params.learning_rate)
    checkpoint_file = params.checkpoint_file
    if checkpoint_file == '':
        checkpoint_file = 'ckp_0.h5'
    else:
        model.load_weights(f'{params.multi_gpus_model_dir}/{checkpoint_file}')

with strategy.scope():
    def single_step(x_batch, y_batch, model, flag='train'):
        with tf.GradientTape() as tape:
            y_predict = model(x_batch)
            loss_ssim, loss_l2, loss_l1, loss = model_loss((y_batch, y_predict))
        if flag == 'test':
            return loss_ssim, loss_l2, loss_l1, loss
        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))
        return loss_ssim, loss_l2, loss_l1, loss

with strategy.scope():
    @tf.function
    def distributed_step(x_batch, y_batch, model, flag='train'):
        loss_ssim, loss_l2, loss_l1, loss = strategy.experimental_run_v2(single_step, args=(x_batch, y_batch, model, flag))
        loss_ssim = strategy.reduce(tf.distribute.ReduceOp.MEAN, loss_ssim, axis=None)
        loss_l2 = strategy.reduce(tf.distribute.ReduceOp.MEAN, loss_l2, axis=None)
        loss_l1 = strategy.reduce(tf.distribute.ReduceOp.MEAN, loss_l1, axis=None)
        loss = strategy.reduce(tf.distribute.ReduceOp.MEAN, loss, axis=None)
        return loss_ssim, loss_l2, loss_l1, loss

    logger.add(f"{params.logout_dir}/{params.sequence_length}_{params.lead_time}_train.log", enqueue=True)
    train_dataset, test_dataset = train_input_fn()
    train_dist_dataset = strategy.experimental_distribute_dataset(train_dataset)
    test_dist_dataset = strategy.experimental_distribute_dataset(test_dataset)

    for epoch in range(params.num_epochs):
        total_train = 0
        for step, (x_batch_train, y_batch_train) in enumerate(train_dist_dataset):
            total_train += 1
        for step, (x_batch_train, y_batch_train) in enumerate(train_dist_dataset):
            if step < total_train - 1:
                start = time.clock()
                loss_ssim, loss_l2, loss_l1, loss = distributed_step(x_batch_train, y_batch_train, model)
                elapsed = (time.clock() - start)
                template = ("step {} loss is {:1.5f}, "
                            "loss ssim is {:1.5f}, "
                            "loss l2 is {:1.5f}, "
                            "loss l1 is {:1.5f}."
                            "({:1.2f}s/step)")
                logger.info(template.format(step, loss.numpy(), loss_ssim.numpy(), loss_l2.numpy(), loss_l1.numpy(), elapsed))
        if epoch % params.num_epoch_record == 0:
            total_test = 0
            for step, (x_test, y_test) in enumerate(test_dist_dataset):
                total_test += 1
            loss_test = 0
            loss_ssim_test = 0
            loss_l2_test = 0
            loss_l1_test = 0
            count = 0
            spinner = MoonSpinner('Testing ')
            for step, (x_test, y_test) in enumerate(test_dist_dataset):
                if step < total_test - 1:
                    loss_ssim, loss_l2, loss_l1, loss = distributed_step(x_test, y_test, model, flag='test')
                    loss_ssim_test += loss_ssim.numpy()
                    loss_l2_test += loss_l2.numpy()
                    loss_l1_test += loss_l1.numpy()
                    loss_test += loss.numpy()
                    count += 1
                spinner.next()
            spinner.finish()
            logger.info("TEST COMPLETE!")
            template = ("TEST DATASET STATISTICS: "
                        "loss is {:1.5f}, "
                        "loss ssim is {:1.5f}, "
                        "loss l2 is {:1.5f}, "
                        "loss l1 is {:1.5f}.")
            logger.info(template.format(loss_test/count, loss_ssim_test/count, loss_l2_test/count, loss_l1_test/count))

            total_epoch = int(re.findall("\d+", checkpoint_file)[0])
            checkpoint_file = checkpoint_file.replace(f'_{total_epoch}.h5', f'_{total_epoch + 1}.h5')
            model.save_weights(f'{params.multi_gpus_model_dir}/{checkpoint_file}')
            logger.info("Saved checkpoint_file {}".format(checkpoint_file))
