import os
import glob
import netCDF4 as cdf
from netCDF4 import Dataset
import numpy as np
import pandas as pd

nc4files = []
for file in glob.glob("*.nc4*"):
    nc4files.append(file)
    print (file)

for file in nc4files:
    nc4data = cdf.Dataset(file)
    lons = nc4data.variables['lon'][:]
    lats = nc4data.variables['lat'][:]
    time = nc4data.variables['time'][:]
    percip = nc4data.variables['precipitationCal']

    print(time)

    np.array(lons)
    np.array(lats)
    np.array(time)
    np.array(percip)

    pCal = np.reshape(percip, (3600, 1800))

    pCal2 = pCal.flatten()

    lats2 = pd.DataFrame(np.tile(lats, 3600))
    lons2 = pd.DataFrame(np.repeat(lons, 1800))
    time2 = pd.DataFrame(np.repeat(time, 6480000))
    pCal2 = pd.DataFrame(pCal2)

    # Pulls four data arrays into columns of a dataset
    result2 = pd.concat([time2, lats2, lons2, pCal2], axis=1)
    #slices dataframe to inlcude rows for Florida
    result2 = result2.iloc[1664400:1799370, ]
    result2
    result2.columns = ['Time', 'Lat', 'Lon', 'Precip']
    result2.to_csv(str(file.strip())+ '.csv')

    #print(result2)