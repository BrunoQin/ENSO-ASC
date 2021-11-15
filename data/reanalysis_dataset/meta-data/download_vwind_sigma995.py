#!/usr/bin/env python
#################################################################
# Python Script to retrieve 328 online Data files of 'ds131.2',
# total 11.29G. This script uses 'requests' to download data.
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
'pgrbanl/pgrbanl_mean_1851_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1852_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1853_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1854_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1855_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1856_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1857_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1858_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1859_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1860_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1861_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1862_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1863_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1864_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1865_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1866_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1867_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1868_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1869_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1870_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1871_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1872_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1873_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1874_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1875_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1876_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1877_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1878_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1879_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1880_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1881_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1882_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1883_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1884_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1885_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1886_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1887_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1888_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1889_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1890_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1891_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1892_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1893_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1894_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1895_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1896_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1897_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1898_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1899_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1900_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1901_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1902_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1903_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1904_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1905_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1906_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1907_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1908_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1909_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1910_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1911_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1912_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1913_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1914_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1915_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1916_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1917_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1918_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1919_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1920_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1921_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1922_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1923_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1924_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1925_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1926_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1927_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1928_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1929_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1930_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1931_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1932_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1933_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1934_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1935_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1936_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1937_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1938_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1939_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1940_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1941_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1942_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1943_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1944_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1945_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1946_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1947_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1948_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1949_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1950_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1951_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1952_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1953_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1954_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1955_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1956_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1957_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1958_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1959_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1960_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1961_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1962_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1963_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1964_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1965_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1966_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1967_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1968_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1969_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1970_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1971_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1972_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1973_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1974_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1975_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1976_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1977_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1978_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1979_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1980_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1981_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1982_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1983_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1984_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1985_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1986_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1987_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1988_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1989_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1990_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1991_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1992_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1993_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1994_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1995_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1996_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1997_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1998_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_1999_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2000_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2001_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2002_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2003_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2004_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2005_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2006_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2007_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2008_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2009_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2010_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2011_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2012_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2013_VGRD_sigma.grib',
'pgrbanl/pgrbanl_mean_2014_VGRD_sigma.grib']
for file in filelist:
    filename=dspath+file
    file_base = '.\\data\\dataset\\vwind\\' + os.path.basename(file)
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
