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
#print df.min()
#print df.max()

#print len(df.CEC)
for columns in df:
    df[columns][df[columns] == 255 ] = None
    df[columns][df[columns] == -9999] = None

#print df.CEC[1]
#print df.BLD[1]
#print df.min()
#print df.max()
#print df['BLD'].argmax()
from rpy2.robjects.packages import importr

#x = np.array(df[varname_list[0]][[153208]])
#print x
#
#y= np.array(df[varname_list[1]][[153208]])
#z = np.array(df[varname_list[2]][[153208]])
#a = np.array(df[varname_list[3]][[153208]])
#b = np.array(df[varname_list[4]][[153208]])
#c = np.array(df[varname_list[5]][[153208]])
#d = np.array(df[varname_list[6]][[153208]])


GSIF = importr('GSIF')
#WWP_ls = []
#for i in range(0,len(df.CEC)):
#    _,_,_,WWP,_ = GSIF.AWCPTF(np.array(df[varname_list[0][[i]]),df[varname_list[0][[i]]),df[varname_list[0][[i]]),df[varname_list[0][[i]],df[varname_list[0][[i]],df[varname_list[0][[i]])
#    WWP_ls.append(WWP)
#    
#_,_,_,WWP,_ = GSIF.AWCPTF(x, y, z, a, b, c, d)

_,_,_,WWP,_ = GSIF.AWCPTF(30,25,48,23,1200,12,6.4)
print WWP
#WWP_ls.append(WWP)
#print WWP_ls
 