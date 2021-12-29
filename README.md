# ENSO-ASC 1.0.0

This is the code for this [paper](https://gmd.copernicus.org/preprints/gmd-2021-213) `https://doi.org/10.5194/gmd-2021-213`
This project can be built and trained on Ubuntu 18.04.3 LTS, with python3.6/3.7 and CUDA 10.0/cudnn 7.6.5.

### 0. Environment
```
conda create -n enso python=3.6
source activate enso

pip install tensorflow-gpu==2.0.0
pip install netCDF4==1.5.3
pip install pandas==0.25.3
pip install scikit-learn==0.21.3
pip install progress==1.5
pip install loguru==0.3.2
pip install absl-py
pip install cmaps
pip install geos
pip install pyproj
pip install h5py==2.10
conda install -c conda-forge basemap-data-hires=1.0.8.dev0
conda install -c conda-forge pygrib
```

### 1. Download climate dataset
Scripts in `./data/reanalysis_dataset/meta-data` and `./data/remote_sensing_dataset/meta-data` are prepared well for download data from [NOAA/CIRES Twentieth Century Global Reanalysis Version 2c](https://rda.ucar.edu/datasets/ds131.2/index.html/) and [Remote Sensing System](http://www.remss.com/). [Hadley Centre Global Sea Ice and Sea Surface Temperature (HadISST)](https://rda.ucar.edu/datasets/ds277.3/index.html) can be downloaded from website.
```
python ./data/download_*_*.py
```
The archieved dataset is also in [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5179867.svg)](https://doi.org/10.5281/zenodo.5179867) (not the latest!)

### 2. For the reanalysis dataset (only need to run once for the later transfer learning)
Firstly, use the following commands to parse and parpare training data.
```
python -m data.reanalysis_dataset.1_grib2npz
python -m data.reanalysis_dataset.2_interpolation
```
The output training data files are in `./data/reanalysis_dataset/final`

Then, train the model:
```
python -m data.preprocess_reanalysis_transfer
python -m train.train_multi_gpus [or] python -m train.train_single_gpu
```
### 3. For the remote sensing dataset (need to train for every month)
Firstly, use the following commands to parse and parpare training data.
```
python -m data.remote_sensing_dataset.1_byte2npz
python -m data.remote_sensing_dataset.2_nc2npz
python -m data.remote_sensing_dataset.3_crop_region_and_fill_land
```
The output training data files are in `./data/remote_sensing_dataset/final`

Then, train the model:
```
python -m data.preprocess_remote_sensing
python -m train.train_multi_gpus [or] python -m train.train_single_gpu
```

### 4. Monthly ENSO forecasting
Firstly, download the remote sensing data from the above wetsites and modify the `./data/remote_sensing_dataset/record.txt` to supplement the new data for data preprocessing, such as:
```
2022-1,2,3  # split months by ',' if more than one month
```
Secondly, prepare the new data:
```
python -m data.remote_sensing_dataset.1_byte2npz
python -m data.remote_sensing_dataset.2_nc2npz
python -m data.remote_sensing_dataset.3_crop_region_and_fill_land
```
Thirdly, fine-tune the trained model:
```
python workflow.py
```
Finally, make forecasts for the future 18 months:
```
python forecast.py
```
The forecast results will be recorded in `./result-{year}-{month}.csv`
