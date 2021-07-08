from data.remote_sensing_dataset.bytemaps import sys
from data.remote_sensing_dataset.bytemaps import Dataset
from data.remote_sensing_dataset.bytemaps import Verify


class REMSSaveraged(Dataset):
    """ Read averaged AMSR2 bytemaps. """
    """
    Public data:
        filename = name of data file
        missing = fill value used for missing data;
                  if None, then fill with byte codes (251-255)
        dimensions = dictionary of dimensions for each coordinate
        variables = dictionary of data for each variable
    """

    def __init__(self, filename, missing=None):
        """
        Required arguments:
            filename = name of data file to be read (string)

        Optional arguments:
            missing = fill value for missing data,
                      default is the value used in verify file
        """
        self.filename = filename
        self.missing = missing
        Dataset.__init__(self)

    # Dataset:

    def _attributes(self):
        return ['coordinates','long_name','units','valid_min','valid_max']

    def _coordinates(self):
        return ('variable','latitude','longitude')

    def _shape(self):
        return (6,720,1440)

    def _variables(self):
        return ['sst','windLF','windMF','vapor','cloud','rain',
                'longitude','latitude','land','ice','nodata']

    # _default_get():

    def _get_index(self,var):
        return {'sst' : 0,
                'windLF' : 1,
                'windMF' : 2,
                'vapor' : 3,
                'cloud' : 4,
                'rain' : 5,
                }[var]

    def _get_offset(self,var):
        return {'sst' : -3.0,
                'cloud' : -0.05,
                }[var]

    def _get_scale(self,var):
        return {'sst' : 0.15,
                'windLF' : 0.2,
                'windMF' : 0.2,
                'vapor' : 0.3,
                'cloud' : 0.01,
                'rain' : 0.1,
                }[var]

    # _get_ attributes:

    def _get_long_name(self,var):
        return {'sst' : 'Sea Surface Temperature',
                'windLF' : '10m Surface Wind Speed (low frequency)',
                'windMF' : '10m Surface Wind Speed (medium frequency)',
                'vapor' : 'Columnar Water Vapor',
                'cloud' : 'Cloud Liquid Water',
                'rain'  :'Surface Rain Rate',
                'longitude' : 'Grid Cell Center Longitude',
                'latitude' : 'Grid Cell Center Latitude',
                'land' : 'Is this land?',
                'ice' : 'Is this ice?',
                'nodata' : 'Is there no data?',
                }[var]

    def _get_units(self,var):
        return {'sst' : 'deg Celsius',
                'windLF' : 'm/s',
                'windMF' : 'm/s',
                'vapor' : 'mm',
                'cloud' : 'mm',
                'rain' : 'mm/hr',
                'longitude' : 'degrees east',
                'latitude' : 'degrees north',
                'land' : 'True or False',
                'ice' : 'True or False',
                'nodata' : 'True or False',
                }[var]

    def _get_valid_min(self,var):
        return {'sst' : -3.0,
                'windLF' : 0.0,
                'windMF' : 0.0,
                'vapor' : 0.0,
                'cloud' : -0.05,
                'rain' : 0.0,
                'longitude' : 0.0,
                'latitude' : -90.0,
                'land' : False,
                'ice' : False,
                'nodata' : False,
                }[var]

    def _get_valid_max(self,var):
        return {'sst' : 34.5,
                'windLF' : 50.0,
                'windMF' : 50.0,
                'vapor' : 75.0,
                'cloud' : 2.45,
                'rain' : 25.0,
                'longitude' : 360.0,
                'latitude' : 90.0,
                'land' : True,
                'ice' : True,
                'nodata' : True,
                }[var]


class ThreedayVerify(Verify):
    """ Contains info for verification. """

    def __init__(self,dataset, verify_file):
        self.filename = verify_file
        self.ilon1 = 170
        self.ilon2 = 175
        self.ilat1 = 274
        self.ilat2 = 278
        self.variables = ['sst','windLF','windMF','vapor','cloud','rain']
        self.startline = {'sst' : 117,
                          'windLF' : 124,
                          'windMF' : 131,
                          'vapor' : 138,
                          'cloud' : 145,
                          'rain' : 152 }
        Verify.__init__(self,dataset)


class WeeklyVerify(Verify):
    """ Contains info for verification. """

    def __init__(self,dataset, verify_file):
        self.filename = verify_file
        self.ilon1 = 170
        self.ilon2 = 175
        self.ilat1 = 274
        self.ilat2 = 278
        self.variables = ['sst','windLF','windMF','vapor','cloud','rain']
        self.startline = {'sst' : 163,
                          'windLF' : 170,
                          'windMF' : 177,
                          'vapor' : 184,
                          'cloud' : 191,
                          'rain' : 198 }
        Verify.__init__(self,dataset)


class MonthlyVerify(Verify):
    """ Contains info for verification. """

    def __init__(self, dataset, verify_file):
        self.filename = verify_file
        self.ilon1 = 170
        self.ilon2 = 175
        self.ilat1 = 274
        self.ilat2 = 278
        self.variables = ['sst','windLF','windMF','vapor','cloud','rain']
        self.startline = {'sst' : 209,
                          'windLF' : 216,
                          'windMF' : 223,
                          'vapor' : 230,
                          'cloud' : 237,
                          'rain' : 244}
        Verify.__init__(self,dataset)
