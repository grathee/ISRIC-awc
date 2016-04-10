# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 16:01:08 2016

@author: user
"""

rf = gdal.Open("/media/user/data/AWC-IN_022016/sdata/BLD_sd1_M_1km_T386.tif")
cols = rf.RasterXSize
rows = rf.RasterYSize
geotransform = rf.GetGeoTransform()
originX= geotransform[0]
originY= geotransform[3]
pixelWidth= geotransform[1]
pixelHeight= geotransform[5]
driver = rf.GetDriver()

