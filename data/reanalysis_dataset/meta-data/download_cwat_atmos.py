#!/usr/bin/env python
#################################################################
# Python Script to retrieve 328 online Data files of 'ds131.2',
# total 8.94G. This script uses 'requests' to download data.
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
'pgrbanl/pgrbanl_mean_1851_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1852_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1853_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1854_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1855_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1856_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1857_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1858_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1859_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1860_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1861_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1862_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1863_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1864_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1865_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1866_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1867_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1868_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1869_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1870_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1871_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1872_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1873_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1874_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1875_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1876_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1877_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1878_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1879_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1880_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1881_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1882_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1883_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1884_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1885_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1886_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1887_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1888_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1889_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1890_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1891_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1892_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1893_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1894_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1895_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1896_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1897_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1898_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1899_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1900_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1901_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1902_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1903_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1904_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1905_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1906_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1907_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1908_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1909_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1910_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1911_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1912_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1913_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1914_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1915_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1916_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1917_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1918_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1919_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1920_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1921_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1922_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1923_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1924_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1925_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1926_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1927_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1928_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1929_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1930_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1931_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1932_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1933_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1934_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1935_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1936_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1937_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1938_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1939_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1940_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1941_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1942_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1943_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1944_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1945_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1946_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1947_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1948_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1949_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1950_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1951_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1952_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1953_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1954_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1955_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1956_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1957_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1958_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1959_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1960_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1961_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1962_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1963_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1964_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1965_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1966_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1967_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1968_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1969_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1970_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1971_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1972_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1973_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1974_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1975_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1976_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1977_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1978_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1979_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1980_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1981_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1982_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1983_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1984_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1985_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1986_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1987_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1988_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1989_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1990_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1991_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1992_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1993_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1994_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1995_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1996_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1997_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1998_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1999_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2000_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2001_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2002_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2003_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2004_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2005_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2006_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2007_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2008_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2009_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2010_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2011_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2012_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2013_CWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2014_CWAT_atmos-col.grib',]
for file in filelist:
    filename=dspath+file
    file_base = '.\\cwat\\' + os.path.basename(file)
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
