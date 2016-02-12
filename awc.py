# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 11:56:19 2016

@author: user
"""
import gdal, osr
from gdalconst import *
import glob
import numpy as np
import pandas as pd

ifolder = '/media/user/data/AWC-IN_022016'

var_folder = os.path.join(ifolder,'sdata')
os.chdir(var_folder)

#listing files for easy handling
varfile_list = glob.glob("*.tif")

varname_list = []

for files in varfile_list:
    var = files[0:3]
    varname_list.append(var)
    
#print var_list

#testing with one variable
var_file1 = gdal.Open(varfile_list[2])
myarray1 = var_file1.GetRasterBand(1).ReadAsArray().astype(int)
a1 = np.ravel(myarray1)
#print a1

i = 0
array_all = np.zeros(shape = (7, 1440000), dtype = 'float')
# now applying operation to all
for files in varfile_list:
    var_file = gdal.Open(varfile_list[i])
    myarray = var_file.GetRasterBand(1).ReadAsArray().astype(float)
    array = np.ravel(myarray)
    array_all[i,:] = array
    i = i + 1

#store these in dataframe
df = pd.DataFrame(array_all.T, columns = varname_list)
#print dir(df)
#print df('CEC')
#print df['CEC']
from rpy2.robjects.packages import importr
#import rpy2.robjects.packages as rpy
import rpy2.robjects as ro
from rpy2.robjects import IntVector, Formula
#from rpy2.robjects import pandas2ri
#pandas2ri.activate()

GSIF = importr('GSIF')
_,_,_,WWP,_ = GSIF.AWCPTF(30,25,48,23,1200,12,6.4)
print WWP

 