import sys

from absl import flags

flags.DEFINE_string("EXP", "REMOTE-SENSING", "***")

# ---------- Pre-Processing ----------
flags.DEFINE_string("preprocess_out_dir", "./data/records", "Path to save the pre-process output.")
flags.DEFINE_string("outputs_dir", "./outputs", "Path to test images.")
flags.DEFINE_string("single_gpu_model_dir", "./checkpoints_single", "Path to save trained models.")
flags.DEFINE_string("multi_gpus_model_dir", "./checkpoints_multi", "Path to save trained models.")
flags.DEFINE_string("archive_model_dir", "./checkpoints_archive", "Path to save trained models.")
flags.DEFINE_string("checkpoint_file", "", "Path to save trained models.")

# reanalysis dataset experiment
flags.DEFINE_string("reanalysis_dataset_dir", "./data/reanalysis_dataset", "Path to save the origin data.")
flags.DEFINE_string("reanalysis_npz_dir", "./data/reanalysis_dataset/final", "Path to save the npz data.")

# remote sensing dataset experiment
flags.DEFINE_string("remote_sensing_dataset_dir", "./data/remote_sensing_dataset", "Path to save the origin data.")
flags.DEFINE_string("remote_sensing_npz_dir", "./data/remote_sensing_dataset/final", "Path to save trained models.")

# Eval/Train
flags.DEFINE_float("train_eval_split", 0.1, "Percentage amount of testing data to use for eval.")
flags.DEFINE_integer("random_seed", 10, "Seed to use for random number generation and shuffling.")

# ---------- Training ----------
# "original", "comparison_1" for no graph convolution, "comparison_2" for 3D convolution
flags.DEFINE_string("experiment_style", "original", "Path to save training logs.")
flags.DEFINE_string("logout_dir", "./results/materials", "Path to save training logs.")
flags.DEFINE_integer("num_gpus", 2, "The numbers of GPUs for training.")
flags.DEFINE_integer("sequence_length", 6, "Sequence lenghth for predicting.")
flags.DEFINE_integer("lead_time", 1, "Lead time for predicting.")
flags.DEFINE_integer("batch_size", 2, "The batch size for training.")
flags.DEFINE_float("learning_rate", 0.0001, "The learning rate for training.")
flags.DEFINE_integer("num_epochs", 521, "Number of epochs to train for.")
flags.DEFINE_integer("num_epoch_record", 1, "Number of step to record checkpoint.")

# ---------- Testing ----------
# test region [0, 1728] for [1871.12, 2015.12]
# flags.DEFINE_list("one_year", [193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204], "The whole year for predicting in test.")
flags.DEFINE_list("one_year", [205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216], "The whole year for predicting in test.")
# flags.DEFINE_list("one_year", [1717, 1718, 1719, 1720, 1721, 1722, 1723, 1724, 1725, 1726, 1727, 1728], "The whole year for predicting in test.")
flags.DEFINE_list("single_month", [270, 271, 272, 273, 274, 275, 276], "The single months for predicting in test.")

# ---------- Model ----------
# Complete variables list: ["cape", "cin", "pot", "pres", "pwat", "rh", "tmp", "uwind", "vwind"]
flags.DEFINE_list("reanalysis_variables", ["pres", "pwat", "rh", "tmp", "uwind", "vwind"], "The variables for building the model.")
flags.DEFINE_list("remote_sensing_variables", ["uwind", "vwind", "vapor", "cloud", "rain"], "The variables for building the model.")

params = flags.FLAGS
params(sys.argv)
