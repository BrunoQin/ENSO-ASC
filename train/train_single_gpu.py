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


def main():
    if EXP == 'REMOTE-SENSING':
        adj = pd.read_csv(f'{params.remote_sensing_dataset_dir}/adjacency.csv', header=None, sep=',').values
    elif EXP == 'REANALYSIS':
        adj = pd.read_csv(f'{params.reanalysis_dataset_dir}/adjacency.csv', header=None, sep=',').values
    adj = tf.constant(adj, dtype = tf.float32)

    train_dataset, test_dataset = train_input_fn()
    optimizer = tf.keras.optimizers.Adam(learning_rate=params.learning_rate)
    if EXP == 'REMOTE-SENSING':
        model = model_factory(adj, params.remote_sensing_variables)
    elif EXP == 'REANALYSIS':
        model = model_factory(adj, params.reanalysis_variables)
    model_loss = Loss(model)

    checkpoint_file = params.checkpoint_file
    if checkpoint_file == '':
        checkpoint_file = 'ckp_0.h5'
    else:
        model.load_weights(f'{params.single_gpu_model_dir}/{checkpoint_file}')

    logger.add(f"{params.logout_dir}/{params.sequence_length}_{params.lead_time}_train.log", enqueue=True)

    for epoch in range(params.num_epochs):
        for step, (x_batch_train, y_batch_train) in enumerate(train_dataset):
            start = time.clock()
            with tf.GradientTape() as tape:
                y_predict = model(x_batch_train)
                loss_ssim, loss_l2, loss_l1, loss = model_loss((y_predict, y_batch_train))
            grads = tape.gradient(loss, model.trainable_weights)
            optimizer.apply_gradients(zip(grads, model.trainable_weights))
            elapsed = (time.clock() - start)
            template = ("step {} loss is {:1.5f}, "
                        "loss ssim is {:1.5f}, "
                        "loss l2 is {:1.5f}, "
                        "loss l1 is {:1.5f}."
                        "({:1.2f}s/step)")
            logger.info(template.format(step, loss.numpy(), loss_ssim.numpy(), loss_l2.numpy(), loss_l1.numpy(), elapsed))

        if epoch % params.num_epoch_record == 0:
            loss_test = 0
            loss_ssim_test = 0
            loss_l2_test = 0
            loss_l1_test = 0
            count = 0
            spinner = MoonSpinner('Testing ')
            for step, (x_batch_test, y_batch_test) in enumerate(test_dataset):
                y_predict = model(x_batch_test)
                loss_ssim, loss_l2, loss_l1, loss = model_loss((y_predict, y_batch_test))
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
            model.save_weights(f'{params.single_gpu_model_dir}/{checkpoint_file}')
            logger.info("Saved checkpoint_file {}".format(checkpoint_file))


if __name__ == '__main__':
    main()
