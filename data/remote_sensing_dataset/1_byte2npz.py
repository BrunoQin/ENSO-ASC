import os
import numpy as np

from data.remote_sensing_dataset.remss_averaged import REMSSaveraged
from train.params import *

tmi_year = range(1997, 2013)
amsr_year = range(2012, 2022)

def non_zero_mean(np_arr):
    np_arr[np.isnan(np_arr)] = 0
    exist = (np_arr != 0)
    num = np_arr.sum(axis=0)
    den = exist.sum(axis=0)
    return num / den

def cal_month_averaged(averaged_records, year, month):
    sst = []
    vapor = []
    cloud = []
    rain = []
    count = 0
    for record in averaged_records:
        if all(clue in record for clue in [str(year)+str(month).rjust(2, "0"), 'd3d']):
            print(record)
            sst.append(REMSSaveraged(record, missing=np.nan).variables['sst'])
            vapor.append(REMSSaveraged(record, missing=np.nan).variables['vapor'])
            cloud.append(REMSSaveraged(record, missing=np.nan).variables['cloud'])
            rain.append(REMSSaveraged(record, missing=np.nan).variables['rain'])
            count += 1
    sst = non_zero_mean(np.array(sst))
    vapor = non_zero_mean(np.array(vapor))
    cloud = non_zero_mean(np.array(cloud))
    rain = non_zero_mean(np.array(rain))
    print(f'year {year} month {month} done! {count} files are found and calculated!')
    return sst, vapor, cloud, rain

if __name__ == '__main__':

    sst_data = []
    vapor_data = []
    cloud_data = []
    rain_data = []

    if not os.path.exists(f'{params.remote_sensing_dataset_dir}/record.txt'):

        for i in tmi_year:
            if i == 1997:
                averaged_records = []
                for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m12/'):
                    averaged_records.append(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m12/{record}')
                sst, vapor, cloud, rain = cal_month_averaged(averaged_records, i, 12)
                sst_data.append(sst)
                vapor_data.append(vapor)
                cloud_data.append(cloud)
                rain_data.append(rain)
            elif i == 2012:
                for j in range(1, 7):
                    averaged_records = []
                    for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m{str(j).rjust(2, "0")}/'):
                        averaged_records.append(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m{str(j).rjust(2, "0")}/{record}')
                    sst, vapor, cloud, rain = cal_month_averaged(averaged_records, i, j)
                    sst_data.append(sst)
                    vapor_data.append(vapor)
                    cloud_data.append(cloud)
                    rain_data.append(rain)
            else:
                for j in range(1, 13):
                    averaged_records = []
                    for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m{str(j).rjust(2, "0")}/'):
                        averaged_records.append(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m{str(j).rjust(2, "0")}/{record}')
                    sst, vapor, cloud, rain = cal_month_averaged(averaged_records, i, j)
                    sst_data.append(sst)
                    vapor_data.append(vapor)
                    cloud_data.append(cloud)
                    rain_data.append(rain)

        for i in amsr_year:
            if i == 2012:
                for j in range(7, 13):
                    averaged_records = []
                    for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/'):
                        averaged_records.append(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/{record}')
                    sst, vapor, cloud, rain = cal_month_averaged(averaged_records, i, j)
                    sst_data.append(sst)
                    vapor_data.append(vapor)
                    cloud_data.append(cloud)
                    rain_data.append(rain)
            elif i == 2021:
                for j in range(1, 3):
                    averaged_records = []
                    for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/'):
                        averaged_records.append(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/{record}')
                    sst, vapor, cloud, rain = cal_month_averaged(averaged_records, i, j)
                    sst_data.append(sst)
                    vapor_data.append(vapor)
                    cloud_data.append(cloud)
                    rain_data.append(rain)
            else:
                for j in range(1, 13):
                    averaged_records = []
                    for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/'):
                        averaged_records.append(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/{record}')
                    sst, vapor, cloud, rain = cal_month_averaged(averaged_records, i, j)
                    sst_data.append(sst)
                    vapor_data.append(vapor)
                    cloud_data.append(cloud)
                    rain_data.append(rain)

        sst_data = np.array(sst_data)
        vapor_data = np.array(vapor_data)
        cloud_data = np.array(cloud_data)
        rain_data = np.array(rain_data)

    else:
        restart = open(f'{params.remote_sensing_dataset_dir}/record.txt', encoding='utf-8').readline()
        [year, month] = str.split(restart, '-')
        month = str.split(month[:-1], ',')
        for j in month:
            averaged_records = []
            for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{year}/m{str(j).rjust(2, "0")}/'):
                averaged_records.append(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{year}/m{str(j).rjust(2, "0")}/{record}')
            sst, vapor, cloud, rain = cal_month_averaged(averaged_records, year, j)
            sst_data.append(sst)
            vapor_data.append(vapor)
            cloud_data.append(cloud)
            rain_data.append(rain)

        sst_data = np.array(sst_data)
        vapor_data = np.array(vapor_data)
        cloud_data = np.array(cloud_data)
        rain_data = np.array(rain_data)

        sst = np.load(f'./data/remote_sensing_dataset/final/sst.npz')['sst']
        vapor = np.load(f'./data/remote_sensing_dataset/final/vapor.npz')['vapor']
        cloud = np.load(f'./data/remote_sensing_dataset/final/cloud.npz')['cloud']
        rain = np.load(f'./data/remote_sensing_dataset/final/rain.npz')['rain']

        sst_data = np.concatenate([sst, sst_data], axis=0)
        vapor_data = np.concatenate([vapor, vapor_data], axis=0)
        cloud_data = np.concatenate([cloud, cloud_data], axis=0)
        rain_data = np.concatenate([rain, rain_data], axis=0)

    print(sst_data.shape)
    print(vapor_data.shape)
    print(cloud_data.shape)
    print(rain_data.shape)

    data = {'sst': sst_data}
    np.savez(f'./data/remote_sensing_dataset/final/sst.npz', **data)
    data = {'vapor': vapor_data}
    np.savez(f'./data/remote_sensing_dataset/final/vapor.npz', **data)
    data = {'cloud': cloud_data}
    np.savez(f'./data/remote_sensing_dataset/final/cloud.npz', **data)
    data = {'rain': rain_data}
    np.savez(f'./data/remote_sensing_dataset/final/rain.npz', **data)
