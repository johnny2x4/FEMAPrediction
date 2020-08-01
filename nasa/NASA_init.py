from requests.auth import HTTPDigestAuth
url = '"https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDF.06/2018/10/3B-DAY.MS.MRG.3IMERG.20181017-S000000-E235959.V06.nc4"'
requests.get(url, auth='urs.earthdata.nasa.gov'('brianyoder', 'ZyLAQ7hRy83fj9z'))