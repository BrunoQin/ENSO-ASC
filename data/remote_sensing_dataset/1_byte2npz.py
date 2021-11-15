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
    wspd_lf = []
    vapor = []
    cloud = []
    rain = []
    count = 0
    for record in averaged_records:
        if all(clue in record for clue in [str(year)+str(month).rjust(2, "0"), 'd3d']):
            print(record)
            sst.append(REMSSaveraged(record, missing=np.nan).variables['sst'])
            wspd_lf.append(REMSSaveraged(record, missing=np.nan).variables['windLF'])
            vapor.append(REMSSaveraged(record, missing=np.nan).variables['vapor'])
            cloud.append(REMSSaveraged(record, missing=np.nan).variables['cloud'])
            rain.append(REMSSaveraged(record, missing=np.nan).variables['rain'])
            count += 1
    sst = non_zero_mean(np.array(sst))
    wspd_lf = non_zero_mean(np.array(wspd_lf))
    vapor = non_zero_mean(np.array(vapor))
    cloud = non_zero_mean(np.array(cloud))
    rain = non_zero_mean(np.array(rain))
    print(f'year {year} month {month} done! {count} files are found and calculated!')
    return sst, wspd_lf, vapor, cloud, rain

if __name__ == '__main__':
    sst_data = []
    wspd_lf_data = []
    vapor_data = []
    cloud_data = []
    rain_data = []

    for i in tmi_year:
        if i == 1997:
            averaged_records = []
            for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m12/'):
                averaged_records.append(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m12/{record}')
            sst, wspd_lf, vapor, cloud, rain = cal_month_averaged(averaged_records, i, 12)
            sst_data.append(sst)
            wspd_lf_data.append(wspd_lf)
            vapor_data.append(vapor)
            cloud_data.append(cloud)
            rain_data.append(rain)
        elif i == 2012:
            for j in range(1, 7):
                averaged_records = []
                for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m{str(j).rjust(2, "0")}/'):
                    averaged_records.append(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m{str(j).rjust(2, "0")}/{record}')
                sst, wspd_lf, vapor, cloud, rain = cal_month_averaged(averaged_records, i, j)
                sst_data.append(sst)
                wspd_lf_data.append(wspd_lf)
                vapor_data.append(vapor)
                cloud_data.append(cloud)
                rain_data.append(rain)
        else:
            for j in range(1, 13):
                averaged_records = []
                for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m{str(j).rjust(2, "0")}/'):
                    averaged_records.append(f'./data/remote_sensing_dataset/meta-data/tmi/bmaps_v07.1/y{i}/m{str(j).rjust(2, "0")}/{record}')
                sst, wspd_lf, vapor, cloud, rain = cal_month_averaged(averaged_records, i, j)
                sst_data.append(sst)
                wspd_lf_data.append(wspd_lf)
                vapor_data.append(vapor)
                cloud_data.append(cloud)
                rain_data.append(rain)

    for i in amsr_year:
        if i == 2012:
            for j in range(7, 13):
                averaged_records = []
                for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/'):
                    averaged_records.append(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/{record}')
                sst, wspd_lf, vapor, cloud, rain = cal_month_averaged(averaged_records, i, j)
                sst_data.append(sst)
                wspd_lf_data.append(wspd_lf)
                vapor_data.append(vapor)
                cloud_data.append(cloud)
                rain_data.append(rain)
        elif i == 2021:
            for j in range(1, 3):
                averaged_records = []
                for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/'):
                    averaged_records.append(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/{record}')
                sst, wspd_lf, vapor, cloud, rain = cal_month_averaged(averaged_records, i, j)
                sst_data.append(sst)
                wspd_lf_data.append(wspd_lf)
                vapor_data.append(vapor)
                cloud_data.append(cloud)
                rain_data.append(rain)
        else:
            for j in range(1, 13):
                averaged_records = []
                for record in os.listdir(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/'):
                    averaged_records.append(f'./data/remote_sensing_dataset/meta-data/amsr/bmaps_v08/y{i}/m{str(j).rjust(2, "0")}/{record}')
                sst, wspd_lf, vapor, cloud, rain = cal_month_averaged(averaged_records, i, j)
                sst_data.append(sst)
                wspd_lf_data.append(wspd_lf)
                vapor_data.append(vapor)
                cloud_data.append(cloud)
                rain_data.append(rain)

    sst_data = np.array(sst_data)
    wspd_lf_data = np.array(wspd_lf_data)
    vapor_data = np.array(vapor_data)
    cloud_data = np.array(cloud_data)
    rain_data = np.array(rain_data)

    data = {'sst': sst_data}
    np.savez(f'./data/remote_sensing_dataset/final/sst-no-nan.npz', **data)
    data = {'wspd_lf': wspd_lf_data}
    np.savez(f'./data/remote_sensing_dataset/final/wspd_lf-no-nan.npz', **data)
    data = {'vapor': vapor_data}
    np.savez(f'./data/remote_sensing_dataset/final/vapor-no-nan.npz', **data)
    data = {'cloud': cloud_data}
    np.savez(f'./data/remote_sensing_dataset/final/cloud-no-nan.npz', **data)
    data = {'rain': rain_data}
    np.savez(f'./data/remote_sensing_dataset/final/rain-no-nan.npz', **data)
