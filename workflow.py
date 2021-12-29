import os
import subprocess

from loguru import logger

from train.params import *

logger.add("./workflow.log", enqueue=True)

def run_cmd(command):
    exitcode, output = subprocess.getstatusoutput(command)
    if exitcode != 0:
        raise Exception(output)
    return output

def write2File(filename, lag_month):
    with open(filename, "r", encoding="utf-8") as f_read:
        content = f_read.readlines()
    with open(filename, "w", encoding="utf-8") as f_write:
        for i in range(len(content)):
            if 'lead_time' in content[i]:
                f_write.write(f'flags.DEFINE_integer("lead_time", {lag_month}, "Lead time for predicting.")\n')
            elif 'checkpoint_file' in content[i]:
                f_write.write('flags.DEFINE_string("checkpoint_file", "ckp_1.h5", "Path to save trained models.")\n')
            else:
                f_write.write(content[i])

def train(lag_month):
    if os.path.exists(f'./checkpoints_archive/forecast_{lag_month}.h5'):
        run_cmd(f'cp ./checkpoints_archive/forecast_{lag_month}.h5 ./checkpoints_multi/ckp_1.h5')
    else:
        run_cmd('cp ./checkpoints_archive/base_model.h5 ./checkpoints_multi/ckp_1.h5')
    write2File('./train/params.py', lag_month)
    run_cmd('python -m data.preprocess_remote_sensing')
    run_cmd('python -m train.train_multi_gpus')

def update_model(lag_month):
    if os.path.exists(f'./checkpoints_multi/ckp_{params.num_epochs + 1}.h5'):
        run_cmd(f'mv ./checkpoints_multi/ckp_{params.num_epochs + 1}.h5 ./checkpoints_archive/forecast_{lag_month}.h5')
    else:
        template = ("model-{:1.0f} training error!")
        logger.info(template.format(lag_month))

def clean(lag_month):
    for i in range(1, params.num_epochs + 1):
        run_cmd(f'rm -rf ./checkpoints_multi/ckp_{i}.h5')
    template = ("model-{:1.0f} training success!")
    logger.info(template.format(lag_month))


if __name__ == '__main__':
    for lag_month in range(1, 19):
        train(lag_month)
        update_model(lag_month)
        clean(lag_month)
