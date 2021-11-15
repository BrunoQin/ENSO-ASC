#!/usr/bin/env python
#################################################################
# Python Script to retrieve 328 online Data files of 'ds131.2',
# total 11.65G. This script uses 'requests' to download data.
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
'pgrbanl/pgrbanl_mean_1851_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1852_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1853_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1854_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1855_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1856_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1857_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1858_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1859_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1860_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1861_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1862_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1863_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1864_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1865_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1866_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1867_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1868_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1869_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1870_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1871_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1872_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1873_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1874_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1875_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1876_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1877_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1878_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1879_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1880_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1881_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1882_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1883_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1884_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1885_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1886_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1887_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1888_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1889_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1890_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1891_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1892_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1893_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1894_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1895_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1896_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1897_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1898_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1899_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1900_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1901_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1902_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1903_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1904_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1905_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1906_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1907_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1908_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1909_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1910_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1911_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1912_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1913_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1914_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1915_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1916_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1917_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1918_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1919_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1920_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1921_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1922_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1923_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1924_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1925_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1926_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1927_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1928_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1929_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1930_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1931_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1932_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1933_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1934_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1935_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1936_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1937_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1938_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1939_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1940_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1941_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1942_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1943_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1944_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1945_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1946_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1947_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1948_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1949_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1950_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1951_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1952_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1953_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1954_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1955_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1956_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1957_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1958_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1959_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1960_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1961_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1962_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1963_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1964_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1965_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1966_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1967_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1968_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1969_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1970_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1971_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1972_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1973_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1974_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1975_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1976_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1977_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1978_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1979_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1980_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1981_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1982_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1983_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1984_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1985_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1986_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1987_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1988_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1989_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1990_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1991_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1992_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1993_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1994_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1995_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1996_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1997_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1998_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_1999_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2000_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2001_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2002_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2003_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2004_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2005_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2006_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2007_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2008_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2009_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2010_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2011_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2012_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2013_POT_sigma.grib',
'pgrbanl/pgrbanl_mean_2014_POT_sigma.grib']
for file in filelist:
    filename=dspath+file
    file_base = '.\\data\\dataset\\pot\\' + os.path.basename(file)
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
