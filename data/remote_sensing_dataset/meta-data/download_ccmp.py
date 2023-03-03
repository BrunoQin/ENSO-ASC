# year = range(1997, 2020)
#
# if __name__ == '__main__':
#     base_url = 'http://data.remss.com/ccmp/v02.0'
#     for y in year:
#         if y == 1997:
#             print(f'{base_url}/Y{y}/m{12}/CCMP_Wind_Analysis_{y}12_V02.0_L3.5_RSS.nc')
#         elif y == 2019:
#             for m in range(1, 5):
#                 print(f'{base_url}/Y{y}/m{str(m).rjust(2, "0")}/CCMP_Wind_Analysis_{y}{str(m).rjust(2, "0")}_V02.0_L3.5_RSS.nc')
#         else:
#             for m in range(1, 13):
#                 print(f'{base_url}/Y{y}/m{str(m).rjust(2, "0")}/CCMP_Wind_Analysis_{y}{str(m).rjust(2, "0")}_V02.0_L3.5_RSS.nc')


if __name__ == '__main__':
    year = 2022
    month = 10
    base_url = f'http://data.remss.com/ccmp/v02.1.NRT/Y{year}'
    for d in range(1, 32):
        print(f'{base_url}/M{str(month).rjust(2, "0")}/CCMP_RT_Wind_Analysis_{year}{str(month).rjust(2, "0")}{str(d).rjust(2, "0")}_V02.0_L3.0_RSS.nc')
