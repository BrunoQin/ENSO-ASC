#!/usr/bin/env python
#################################################################
# Python Script to retrieve 328 online Data files of 'ds131.2',
# total 11.62G. This script uses 'requests' to download data.
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
dspath = 'https://rda.ucar.edu/data/ds131.2/'
filelist = [
'pgrbanl/pgrbanl_mean_1851_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1852_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1853_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1854_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1855_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1856_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1857_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1858_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1859_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1860_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1861_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1862_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1863_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1864_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1865_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1866_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1867_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1868_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1869_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1870_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1871_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1872_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1873_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1874_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1875_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1876_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1877_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1878_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1879_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1880_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1881_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1882_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1883_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1884_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1885_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1886_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1887_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1888_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1889_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1890_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1891_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1892_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1893_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1894_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1895_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1896_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1897_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1898_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1899_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1900_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1901_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1902_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1903_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1904_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1905_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1906_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1907_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1908_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1909_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1910_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1911_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1912_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1913_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1914_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1915_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1916_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1917_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1918_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1919_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1920_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1921_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1922_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1923_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1924_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1925_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1926_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1927_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1928_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1929_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1930_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1931_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1932_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1933_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1934_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1935_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1936_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1937_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1938_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1939_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1940_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1941_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1942_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1943_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1944_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1945_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1946_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1947_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1948_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1949_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1950_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1951_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1952_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1953_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1954_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1955_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1956_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1957_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1958_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1959_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1960_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1961_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1962_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1963_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1964_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1965_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1966_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1967_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1968_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1969_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1970_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1971_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1972_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1973_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1974_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1975_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1976_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1977_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1978_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1979_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1980_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1981_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1982_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1983_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1984_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1985_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1986_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1987_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1988_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1989_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1990_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1991_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1992_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1993_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1994_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1995_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1996_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1997_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1998_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_1999_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2000_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2001_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2002_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2003_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2004_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2005_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2006_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2007_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2008_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2009_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2010_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2011_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2012_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2013_TMP_sigma.grib',
'pgrbanl/pgrbanl_mean_2014_TMP_sigma.grib']
for file in filelist:
    filename=dspath+file
    file_base = '.\\data\\dataset\\rh\\' + os.path.basename(file)
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
