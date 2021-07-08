#!/usr/bin/env python
#################################################################
# Python Script to retrieve 328 online Data files of 'ds131.2',
# total 13.64G. This script uses 'requests' to download data.
#
# Highlight this script by Select All, Copy and Paste it into a file;
# make the file executable and run it on command line.
#
# You need pass in your password as a parameter to execute
# this script; or you can set an environment variable RDAPSWD
# if your Operating System supports it.
#
# Contact rpconroy@ucar.edu (Riley Conroy) for further assistance.
#################################################################


import sys, os
import requests

def check_file_status(filepath, filesize):
    sys.stdout.write('\r')
    sys.stdout.flush()
    size = int(os.stat(filepath).st_size)
    percent_complete = (size/filesize)*100
    sys.stdout.write('%.3f %s' % (percent_complete, '% Completed'))
    sys.stdout.flush()

# Try to get password
if len(sys.argv) < 2 and not 'RDAPSWD' in os.environ:
    try:
        import getpass
        input = getpass.getpass
    except:
        try:
            input = raw_input
        except:
            pass
    pswd = input('Password: ')
else:
    try:
        pswd = sys.argv[1]
    except:
        pswd = os.environ['RDAPSWD']

url = 'https://rda.ucar.edu/cgi-bin/login'
values = {'email' : 'brunoqin@163.com', 'passwd' : pswd, 'action' : 'login'}
# Authenticate
ret = requests.post(url,data=values)
if ret.status_code != 200:
    print('Bad Authentication')
    print(ret.text)
    exit(1)
dspath = 'http://rda.ucar.edu/data/ds131.2/'
filelist = [
'pgrbanl/pgrbanl_mean_1851_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1852_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1853_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1854_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1855_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1856_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1857_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1858_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1859_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1860_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1861_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1862_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1863_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1864_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1865_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1866_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1867_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1868_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1869_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1870_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1871_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1872_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1873_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1874_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1875_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1876_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1877_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1878_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1879_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1880_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1881_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1882_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1883_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1884_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1885_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1886_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1887_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1888_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1889_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1890_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1891_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1892_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1893_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1894_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1895_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1896_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1897_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1898_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1899_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1900_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1901_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1902_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1903_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1904_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1905_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1906_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1907_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1908_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1909_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1910_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1911_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1912_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1913_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1914_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1915_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1916_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1917_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1918_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1919_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1920_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1921_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1922_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1923_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1924_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1925_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1926_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1927_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1928_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1929_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1930_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1931_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1932_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1933_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1934_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1935_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1936_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1937_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1938_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1939_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1940_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1941_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1942_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1943_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1944_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1945_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1946_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1947_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1948_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1949_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1950_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1951_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1952_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1953_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1954_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1955_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1956_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1957_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1958_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1959_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1960_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1961_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1962_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1963_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1964_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1965_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1966_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1967_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1968_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1969_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1970_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1971_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1972_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1973_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1974_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1975_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1976_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1977_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1978_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1979_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1980_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1981_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1982_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1983_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1984_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1985_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1986_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1987_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1988_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1989_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1990_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1991_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1992_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1993_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1994_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1995_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1996_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1997_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1998_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_1999_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2000_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2001_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2002_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2003_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2004_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2005_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2006_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2007_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2008_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2009_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2010_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2011_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2012_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2013_CAPE_sfc.grib',
'pgrbanl/pgrbanl_mean_2014_CAPE_sfc.grib']
for file in filelist:
    filename=dspath+file
    file_base = '.\\data\\dataset\\cape\\' + os.path.basename(file)
    print('Downloading',file_base)
    req = requests.get(filename, cookies = ret.cookies, allow_redirects=True, stream=True)
    filesize = int(req.headers['Content-length'])
    with open(file_base, 'wb') as outfile:
        chunk_size=1048576
        for chunk in req.iter_content(chunk_size=chunk_size):
            outfile.write(chunk)
            if chunk_size < filesize:
                check_file_status(file_base, filesize)
    check_file_status(file_base, filesize)
    print()
