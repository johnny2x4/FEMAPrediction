##Imports libraries
#import h5py
import os
import glob
import pandas as pd
import numpy as np
import netCDF4 as cdf
from netCDF4 import Dataset
import geopandas as gp
import sys
from shapely.geometry import Point
import logging.config
from array import array


sys.path.append("..")
_log = logging.getLogger(__name__)
def setup_logger():
    """ Sets up logger and main window for app.

    """
    # set up logger here then use throughout modules
    format_str = '%(asctime)s - %(levelname)s - %(name)s - %(filename)s: %(lineno)s - %(message)s'
    formatter = logging.Formatter(format_str)
    file_handler = logging.FileHandler(filename='logfile.log',mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    handlers = [file_handler,console_handler]
    logging.basicConfig(level = logging.DEBUG,
                                    handlers = handlers,
                                    format = format_str)
    
    _log.info('Logger Setup and Ready')



def string_cleanup(str_to_clean):
    bad_chars = ['.', '[', ']'] 
    cleaned = str(str_to_clean)
    for i in bad_chars : 
        cleaned = cleaned.replace(i, '')
    return cleaned


class convertedFile():
    __out_fname = str()
    __fpath = str()
    __save_loc = str()
    __gdf = None

    def __init__(self,fpath,save_loc):
        self.__fpath = fpath
        self.__save_loc = save_loc

        self.__process_file()


    @property
    def fpath(self):
        return self.__fpath
    
    @property
    def save_loc(self):
        return self.__save_loc
    
    @property
    def out_fpath(self):
        # should return cleaned name and full path
        return self.__save_loc + self.__out_fname + '.csv'

    @property
    def gdf(self):
        return self.__gdf


    def __process_file(self):
        """ Processes a single file at a time

            PARAMETER
            -----
            fpath : STRING
                File path to import data from for processing.

            RETURNS
            -----
            GEODATAFRAME
        """
        data = cdf.Dataset(self.__fpath,mode='r')
        #data = h5py.File(self.__fpath, mode='r')

        # reads in data needed from the NC4 files
        lons = data.variables['lon'][:]
        lats = data.variables['lat'][:]
        precipitationCal = data.variables['precipitationCal']
        time = data.variables['time'][:]

        self.__out_fname = string_cleanup(time)

        # Converts data into NP arrays
        np.array(lats)
        np.array(lons)
        np.array(precipitationCal)
        np.array(time)
        

        _log.debug(lats)

        # Reshape precipitation data from a 3D array to a 2D array
        pCal = np.reshape(precipitationCal, (3600, 1800))

        # Flattens precipitation data
        pCal2 = pCal.flatten()

        # Converts lats into an array that repeats: [Lats] X 3600
        # Converts lons into an array that repeats: Lon1, Lon2, Lon3... X 1800
        lats2 = pd.DataFrame(np.tile(lats, 3600))
        lons2 = pd.DataFrame(np.repeat(lons, 1800))
        time2 = pd.DataFrame(np.repeat(time, 6480000))
        pCal2 = pd.DataFrame(pCal2)

        # Pulls four data arrays into columns of a dataset
        result2 = pd.concat([time2, lats2, lons2, pCal2], axis=1)
        #slices dataframe to inlcude rows for Florida
        result2 = result2.iloc[1664400:1799370, ]


        # Gives column names
        result2.columns = ['Time', 'Lat', 'Lon', 'Precip']
        _log.debug('joining geo data \n {}'.format(result2))
        
        # build lat lon list
        geometry = [Point(x,y) for (x,y) in zip(result2.Lon, result2.Lat)]
        _log.debug('geo built \n{}'.format(geometry))

        # remove lat lon leaving time and precip
        result2 = result2.drop(['Lon', 'Lat'], axis=1)
        _log.debug('fields cleaned up \n{}'.format(result2))

        # create geodataframe with lat lon and time / precip
        gdf = gp.GeoDataFrame(result2, crs="EPSG:4269", geometry=geometry)
        _log.info('created gdf')

        self.__gdf = gdf



def shp_to_gdf(fpath):
    """ Takes in shape file location and creates a geopandas df

        PARAMETER
        -----
        fpath : STRING
            Path to shape file to ingest
        
        RETURNS
        -----
        GEODATAFRAME

    """

    gdf = gp.read_file(fpath)
    _log.debug('basegeo done')
    
    return gdf



def process_nc4_data(dpath,geo_target_path,save_loc=None):
    floridaGeo = shp_to_gdf(geo_target_path)

    for fpath in [os.path.join(dpath,fname) for fname in os.listdir(dpath) if fname.endswith(".nc4")]:
        cfile = convertedFile(fpath,save_loc)

        gdf_join = gp.sjoin(cfile.gdf, floridaGeo, how="inner", op='intersects')
        _log.debug('gdf join complete \n{}'.format(gdf_join))

        gdf_join.to_csv(cfile.out_fpath)
        _log.info('csv saved to : {}'.format(cfile.out_fpath))



if __name__=='__main__':
    setup_logger()
    directory = '//Users//brianlyoder//Desktop//NASA_Data_Rainfall//NC4Files//' #input("Input DIRECTORY PATH that contains files to process : ")
    geo_target_path = '//Users//brianlyoder//Desktop//NASA_Data_Rainfall//FloridaGIS.shp' #input("Input COUNTY SHP FILE PATH : ")
    save_loc = '//Users//brianlyoder//Desktop//out//' #input("Input SAVE LOCATION : ")



    process_nc4_data(directory,geo_target_path,save_loc)