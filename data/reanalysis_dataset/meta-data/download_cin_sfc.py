#!/usr/bin/env python
#################################################################
# Python Script to retrieve 328 online Data files of 'ds131.2',
# total 12.34G. This script uses 'requests' to download data.
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
'pgrbanl/pgrbanl_mean_1851_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1852_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1853_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1854_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1855_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1856_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1857_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1858_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1859_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1860_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1861_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1862_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1863_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1864_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1865_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1866_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1867_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1868_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1869_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1870_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1871_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1872_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1873_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1874_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1875_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1876_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1877_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1878_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1879_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1880_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1881_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1882_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1883_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1884_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1885_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1886_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1887_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1888_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1889_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1890_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1891_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1892_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1893_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1894_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1895_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1896_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1897_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1898_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1899_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1900_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1901_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1902_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1903_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1904_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1905_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1906_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1907_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1908_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1909_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1910_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1911_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1912_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1913_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1914_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1915_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1916_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1917_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1918_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1919_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1920_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1921_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1922_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1923_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1924_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1925_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1926_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1927_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1928_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1929_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1930_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1931_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1932_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1933_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1934_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1935_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1936_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1937_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1938_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1939_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1940_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1941_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1942_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1943_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1944_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1945_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1946_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1947_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1948_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1949_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1950_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1951_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1952_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1953_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1954_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1955_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1956_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1957_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1958_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1959_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1960_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1961_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1962_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1963_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1964_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1965_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1966_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1967_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1968_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1969_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1970_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1971_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1972_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1973_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1974_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1975_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1976_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1977_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1978_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1979_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1980_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1981_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1982_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1983_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1984_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1985_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1986_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1987_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1988_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1989_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1990_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1991_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1992_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1993_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1994_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1995_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1996_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1997_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1998_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_1999_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2000_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2001_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2002_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2003_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2004_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2005_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2006_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2007_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2008_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2009_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2010_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2011_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2012_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2013_CIN_sfc.grib',
'pgrbanl/pgrbanl_mean_2014_CIN_sfc.grib']
for file in filelist:
    filename=dspath+file
    file_base = '.\\data\\dataset\\cin\\' + os.path.basename(file)
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
