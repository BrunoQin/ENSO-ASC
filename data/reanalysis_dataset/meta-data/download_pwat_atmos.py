#!/usr/bin/env python
#################################################################
# Python Script to retrieve 328 online Data files of 'ds131.2',
# total 11.86G. This script uses 'requests' to download data.
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
'pgrbanl/pgrbanl_mean_1851_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1852_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1853_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1854_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1855_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1856_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1857_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1858_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1859_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1860_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1861_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1862_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1863_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1864_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1865_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1866_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1867_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1868_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1869_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1870_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1871_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1872_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1873_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1874_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1875_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1876_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1877_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1878_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1879_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1880_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1881_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1882_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1883_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1884_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1885_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1886_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1887_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1888_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1889_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1890_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1891_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1892_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1893_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1894_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1895_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1896_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1897_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1898_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1899_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1900_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1901_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1902_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1903_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1904_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1905_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1906_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1907_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1908_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1909_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1910_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1911_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1912_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1913_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1914_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1915_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1916_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1917_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1918_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1919_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1920_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1921_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1922_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1923_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1924_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1925_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1926_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1927_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1928_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1929_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1930_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1931_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1932_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1933_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1934_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1935_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1936_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1937_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1938_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1939_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1940_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1941_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1942_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1943_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1944_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1945_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1946_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1947_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1948_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1949_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1950_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1951_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1952_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1953_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1954_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1955_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1956_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1957_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1958_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1959_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1960_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1961_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1962_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1963_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1964_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1965_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1966_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1967_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1968_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1969_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1970_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1971_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1972_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1973_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1974_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1975_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1976_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1977_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1978_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1979_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1980_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1981_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1982_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1983_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1984_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1985_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1986_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1987_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1988_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1989_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1990_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1991_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1992_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1993_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1994_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1995_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1996_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1997_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1998_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_1999_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2000_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2001_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2002_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2003_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2004_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2005_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2006_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2007_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2008_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2009_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2010_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2011_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2012_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2013_PWAT_atmos-col.grib',
'pgrbanl/pgrbanl_mean_2014_PWAT_atmos-col.grib']
for file in filelist:
    filename=dspath+file
    file_base = '.\\data\\dataset\\pwat\\' + os.path.basename(file)
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
