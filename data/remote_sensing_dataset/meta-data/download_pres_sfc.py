#!/usr/bin/env python
#################################################################
# Python Script to retrieve 328 online Data files of 'ds131.2',
# total 15.74G. This script uses 'requests' to download data.
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
'pgrbanl/pgrbanl_mean_1851_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1852_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1853_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1854_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1855_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1856_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1857_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1858_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1859_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1860_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1861_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1862_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1863_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1864_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1865_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1866_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1867_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1868_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1869_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1870_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1871_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1872_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1873_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1874_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1875_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1876_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1877_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1878_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1879_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1880_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1881_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1882_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1883_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1884_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1885_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1886_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1887_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1888_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1889_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1890_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1891_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1892_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1893_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1894_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1895_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1896_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1897_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1898_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1899_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1900_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1901_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1902_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1903_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1904_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1905_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1906_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1907_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1908_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1909_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1910_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1911_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1912_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1913_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1914_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1915_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1916_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1917_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1918_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1919_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1920_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1921_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1922_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1923_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1924_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1925_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1926_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1927_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1928_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1929_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1930_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1931_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1932_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1933_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1934_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1935_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1936_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1937_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1938_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1939_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1940_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1941_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1942_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1943_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1944_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1945_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1946_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1947_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1948_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1949_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1950_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1951_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1952_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1953_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1954_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1955_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1956_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1957_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1958_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1959_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1960_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1961_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1962_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1963_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1964_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1965_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1966_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1967_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1968_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1969_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1970_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1971_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1972_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1973_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1974_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1975_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1976_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1977_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1978_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1979_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1980_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1981_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1982_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1983_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1984_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1985_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1986_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1987_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1988_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1989_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1990_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1991_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1992_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1993_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1994_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1995_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1996_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1997_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1998_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_1999_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2000_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2001_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2002_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2003_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2004_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2005_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2006_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2007_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2008_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2009_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2010_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2011_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2012_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2013_PRES_sfc.grib',
'pgrbanl/pgrbanl_mean_2014_PRES_sfc.grib']
for file in filelist:
    filename=dspath+file
    file_base = '.\\data\\dataset\\pres\\' + os.path.basename(file)
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
