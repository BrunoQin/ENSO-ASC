#!/usr/bin/env python
#################################################################
# Python Script to retrieve 327 online Data files of 'ds131.2',
# total 11.28G. This script uses 'requests' to download data.
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
'pgrbanl/pgrbanl_mean_1851_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1852_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1853_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1854_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1855_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1856_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1857_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1858_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1859_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1860_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1861_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1862_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1863_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1864_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1865_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1866_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1867_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1868_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1869_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1870_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1871_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1872_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1873_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1874_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1875_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1876_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1877_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1878_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1879_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1880_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1881_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1882_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1883_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1884_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1885_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1886_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1887_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1888_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1889_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1890_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1891_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1892_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1893_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1894_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1895_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1896_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1897_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1898_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1899_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1900_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1901_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1902_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1903_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1904_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1905_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1906_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1907_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1908_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1909_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1910_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1911_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1912_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1913_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1914_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1915_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1916_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1917_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1918_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1919_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1920_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1921_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1922_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1923_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1924_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1925_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1926_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1927_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1928_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1929_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1930_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1931_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1932_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1933_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1934_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1935_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1936_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1937_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1938_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1939_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1940_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1941_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1942_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1943_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1944_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1945_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1946_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1947_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1948_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1949_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1950_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1951_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1952_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1953_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1954_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1955_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1956_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1957_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1958_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1959_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1960_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1961_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1962_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1963_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1964_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1965_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1966_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1967_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1968_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1969_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1970_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1971_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1972_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1973_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1974_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1975_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1976_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1977_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1978_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1979_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1980_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1981_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1982_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1983_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1984_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1985_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1986_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1987_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1988_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1989_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1990_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1991_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1992_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1993_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1994_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1995_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1996_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1997_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1998_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1999_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2000_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2001_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2002_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2003_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2004_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2005_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2006_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2007_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2008_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2009_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2010_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2011_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2012_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2013_UGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2014_UGRD_sigma.grib]
for file in filelist:
    filename=dspath+file
    file_base = '.\\data\\dataset\\uwind\\' + os.path.basename(file)
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
