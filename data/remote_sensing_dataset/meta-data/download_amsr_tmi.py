import urllib.request
import requests
import re, os

from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from bs4 import BeautifulSoup

def get_url(base_url):
    '''
    :param base_url:给定一个网址
    :return: 获取给定网址中的所有链接
    '''
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    req_obj = requests.Session()
    req_obj.mount('http://', adapter)

    str_home = req_obj.get(base_url)
    soup_home = BeautifulSoup(str_home.text, 'lxml')
    all_a = soup_home.find_all(name='a')
    urls = []
    for a in all_a:
        urls.append(base_url + str.split(a.get('href'), '/')[-1])
    return urls

if __name__ == '__main__':
    # http://data.remss.com/tmi/bmaps_v07.1/
    # http://data.remss.com/amsr2/bmaps_v08/
    # http://data.remss.com/ccmp/v02.1.NRT/
    # urls = get_url('http://data.remss.com/amsr2/bmaps_v08/Y2022/M02/')
    urls = get_url('http://data.remss.com/ccmp/v02.1.NRT/Y2022/M02/')
    for url in urls:
        print(url)
