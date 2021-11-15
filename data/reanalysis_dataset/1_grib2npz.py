# # NOTE: run on MacOS or Linux
import pygrib as pg
import numpy as np
import calendar
import os

from progress.bar import PixelBar

from train.params import *

dic = [f'{params.reanalysis_dataset_dir}/meta-data/cwat',
       f'{params.reanalysis_dataset_dir}/meta-data/cape',
       f'{params.reanalysis_dataset_dir}/meta-data/cin',
       f'{params.reanalysis_dataset_dir}/meta-data/pot',
       f'{params.reanalysis_dataset_dir}/meta-data/pres',
       f'{params.reanalysis_dataset_dir}/meta-data/pwat',
       f'{params.reanalysis_dataset_dir}/meta-data/rh',
       f'{params.reanalysis_dataset_dir}/meta-data/tmp',
       f'{params.reanalysis_dataset_dir}/meta-data/uwind',
       f'{params.reanalysis_dataset_dir}/meta-data/vwind']
final = params.reanalysis_npz_dir
smonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
bmonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def read_grib(path):

    print(f'Parsing parameter {str.split(path, "/")[-1]}')
    bar = PixelBar(r'Parsing', max=len(os.listdir(path)), suffix='%(percent)d%%')

    year_record = {}
    for i in os.listdir(path):
        month = smonth
        year = int(str.split(i, '_')[2])
        if calendar.isleap(year):
            month = bmonth

        records = []
        grbs = pg.open(f'{path}/{i}')
        for grb in grbs:
            records.append(grb.values)

        month_record = []
        count = 0
        for j in range(12):
            sum = None
            for k in range(count, count + (month[j] * 4)):
                if sum is None:
                    sum = records[k]
                else:
                    sum += records[k]
                count += 1
            month_record.append(np.array(sum / (month[j] * 4)))
        month_record = np.array(month_record)
        year_record[year] = month_record
        bar.next()
    bar.finish()

    reanalysis = []
    for i in range(1851, 2015):
        reanalysis.append(year_record[i])
    reanalysis = np.array(reanalysis)
    data = {f'{str.split(path, "/")[-1]}': reanalysis}
    np.savez(f'{final}/{str.split(path, "/")[-1]}.npz', **data)


def main():
    for i in dic:
        read_grib(i)

if __name__ == "__main__":
    main()
