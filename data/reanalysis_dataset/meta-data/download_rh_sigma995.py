#!/usr/bin/env python
#################################################################
# Python Script to retrieve 328 online Data files of 'ds131.2',
# total 9.64G. This script uses 'requests' to download data.
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
'pgrbanl/pgrbanl_mean_1851_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1852_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1853_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1854_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1855_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1856_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1857_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1858_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1859_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1860_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1861_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1862_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1863_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1864_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1865_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1866_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1867_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1868_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1869_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1870_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1871_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1872_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1873_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1874_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1875_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1876_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1877_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1878_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1879_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1880_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1881_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1882_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1883_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1884_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1885_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1886_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1887_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1888_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1889_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1890_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1891_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1892_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1893_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1894_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1895_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1896_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1897_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1898_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1899_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1900_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1901_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1902_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1903_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1904_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1905_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1906_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1907_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1908_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1909_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1910_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1911_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1912_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1913_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1914_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1915_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1916_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1917_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1918_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1919_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1920_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1921_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1922_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1923_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1924_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1925_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1926_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1927_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1928_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1929_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1930_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1931_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1932_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1933_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1934_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1935_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1936_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1937_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1938_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1939_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1940_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1941_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1942_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1943_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1944_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1945_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1946_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1947_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1948_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1949_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1950_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1951_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1952_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1953_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1954_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1955_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1956_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1957_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1958_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1959_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1960_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1961_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1962_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1963_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1964_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1965_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1966_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1967_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1968_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1969_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1970_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1971_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1972_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1973_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1974_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1975_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1976_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1977_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1978_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1979_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1980_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1981_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1982_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1983_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1984_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1985_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1986_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1987_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1988_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1989_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1990_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1991_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1992_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1993_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1994_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1995_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1996_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1997_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1998_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_1999_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2000_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2001_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2002_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2003_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2004_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2005_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2006_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2007_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2008_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2009_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2010_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2011_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2012_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2013_RH_sigma.grib',
'pgrbanl/pgrbanl_mean_2014_RH_sigma.grib']
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
