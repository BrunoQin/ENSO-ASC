import os
import numpy as np

# from remss_daily import REMSSdaily
from data.remote_sensing_dataset.remss_averaged import REMSSaveraged


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
    count = 0
    for record in averaged_records:
        if all(clue in record for clue in [str(year)+str(month).rjust(2, "0"), 'd3d']):
            print(record)
            sst.append(REMSSaveraged(record, missing=np.nan).variables['sst'])
            count += 1
    sst = non_zero_mean(np.array(sst))
    print(f'year {year} month {month} done! {count} files are found and calculated!')
    return sst

if __name__ == '__main__':
    sst_data = []

    # for i in tmi_year:
    #     if i == 1997:
    #         averaged_records = []
    #         for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m12/'):
    #             averaged_records.append(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m12/{record}')
    #         sst = cal_month_averaged(averaged_records, i, 12)
    #         sst_data.append(sst)
    #     elif i == 2012:
    #         for j in range(1, 7):
    #             averaged_records = []
    #             for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m{str(j).rjust(2, "0")}/'):
    #                 averaged_records.append(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m{str(j).rjust(2, "0")}/{record}')
    #             sst = cal_month_averaged(averaged_records, i, j)
    #             sst_data.append(sst)
    #     else:
    #         for j in range(1, 13):
    #             averaged_records = []
    #             for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m{str(j).rjust(2, "0")}/'):
    #                 averaged_records.append(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m{str(j).rjust(2, "0")}/{record}')
    #             sst = cal_month_averaged(averaged_records, i, j)
    #             sst_data.append(sst)
    #
    # for i in amsr_year:
    #     if i == 2012:
    #         for j in range(7, 13):
    #             averaged_records = []
    #             for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/'):
    #                 averaged_records.append(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/{record}')
    #             sst = cal_month_averaged(averaged_records, i, j)
    #             sst_data.append(sst)
    #     elif i == 2021:
    #         for j in range(1, 3):
    #             averaged_records = []
    #             for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/'):
    #                 averaged_records.append(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/{record}')
    #             sst = cal_month_averaged(averaged_records, i, j)
    #             sst_data.append(sst)
    #     else:
    #         for j in range(1, 13):
    #             averaged_records = []
    #             for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/'):
    #                 averaged_records.append(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/{record}')
    #             sst = cal_month_averaged(averaged_records, i, j)
    #             sst_data.append(sst)
    # sst_data = np.array(sst_data)

    # year = 2021
    #
    # for i in range(3, 6):
    #     averaged_records = []
    #     for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{year}/m{str(i).rjust(2, "0")}/'):
    #         averaged_records.append(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{year}/m{str(i).rjust(2, "0")}/{record}')
    #     sst = cal_month_averaged(averaged_records, year, i)
    #     sst_data.append(sst)
    #
    # sst_data = np.array(sst_data)
    # sst = np.load('./data/remote_sensing_dataset/final/sst-exp.npz')['sst']
    # print('sst_data: ', sst_data.shape)
    # print('sst: ', sst.shape)
    # sst_data = np.concatenate((sst, sst_data), axis=0)
    # print(sst_data.shape)
    #
    # data = {'sst': sst_data}
    # np.savez(f'./data/remote_sensing_dataset/final/sst-exp.npz', **data)

    lon = REMSSaveraged('./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y1997/m12/f12_19971207v7.1_d3d.gz', missing=np.nan).variables['longitude']
    lat = REMSSaveraged('./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y1997/m12/f12_19971207v7.1_d3d.gz', missing=np.nan).variables['latitude']
    print(lon)
    print(lat)
    data = {'lon': lon, 'lat': lat}
    np.savez(f'./data/remote_sensing_dataset/final/lat-lon.npz', **data)
