# ENSO-ASC 1.0.0

This project is built and trained on Windows 10, with python3.6/3.7 and CUDA 10.0/11.0/11.2.

### 0. Environment
Preprocess:

| dependency | version | dependency | version |
| :-----: | :-----: | :-----: | :-----: |
| pygrib | 2.0.4 | netCDF4 | 1.5.3 |

Train:

| dependency | version | dependency | version |
| :-----: | :-----: | :-----: | :-----: |
| tensorflow-gpu | 2.0.0 | numpy | 1.17.3 |
| pandas | 0.25.3 | scikit-learn | 0.21.3 |
| progress | 1.5 | loguru | 0.3.2 |

Test:

| dependency | version |
| :-----: | :-----: |
| basemap([windows](https://download.lfd.uci.edu/pythonlibs/t7epjj8p/basemap-1.2.1-cp36-cp36m-win_amd64.whl), [linux](https://github.com/matplotlib/basemap/releases/tag/v1.2.1rel)) | 1.2.1 |
| cmaps | 1.0.0 |

### 1. Download climate dataset
Scripts in `./data` are prepared well for download data from [NOAA/CIRES Twentieth Century Global Reanalysis Version 2c](https://rda.ucar.edu/datasets/ds131.2/index.html/), [Hadley Centre Global Sea Ice and Sea Surface Temperature (HadISST)](https://rda.ucar.edu/datasets/ds277.3/index.html), and [Remote Sensing System](http://www.remss.com/)
```
python ./data/download_*_*.py
```

### 2. Parse `.grib` to `.npz`
The download files are in `grib` formats, because Windows doesn't support `pygrib`, I parse data on MacOS, use following commands to install `pygrib` and parse data on MacOS. Linux will be ok as well.
```
conda install -c conda-forge pygrib
python data/grib2npz.py
```
The output files are in `./data/dataset/final`

### 3. Download the data for model
```
python -m data.prepare_*
```

### 4. Train the model
```
python -m train.train_single_gpu
```
or
```
python -m train.train_multi_gpus
```

### 5. Test the model
The output images depend on `matplotlib.basemap`.

Windows:
```
pip install basemap-1.2.1-cp36-cp36m-win_amd64.whl
```
Linux:
```
pip install --upgrade --user matplotlib numpy pyproj pyshp OWSLib Pillow
sudo apt install libgeos-dev
pip install --user --upgrade basemap-1.2.1rel.tar.gz
```
Color bars on basemap depend on `cmaps`
```
pip install cmaps
```
Then run the test script:
```
python -m train.test_one_year
```
