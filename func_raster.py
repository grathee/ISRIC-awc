# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 12:33:01 2016

@author: Geetika
"""

import gdal, osr
from gdalconst import *
import glob
import numpy as np
import pandas as pd
import math
import time

#set input directory
ifolder = '/media/user/data/AWC-IN_022016'

#find data folder in the directory
var_folder = os.path.join(ifolder,'sdata')

#make data folder the working directory
os.chdir(var_folder)

#listing files and extract names for easy handling
varfile_list = glob.glob("*.tif")
varname_list = []
for files in varfile_list:
    var = files[0:3]
    varname_list.append(var)
    
#print var_list

# now applying operation to all
i = 0
array_all = np.zeros(shape = (7, 1440000), dtype = 'float')
for files in varfile_list:
    var_file = gdal.Open(varfile_list[i])
    myarray = var_file.GetRasterBand(1).ReadAsArray().astype(float)
    array = np.ravel(myarray)
    array_all[i,:] = array
    i = i + 1

#store these in dataframe
df = pd.DataFrame(array_all.T, columns = varname_list)

for columns in df:
    df[columns][df[columns] == 255 ] = None
    df[columns][df[columns] == -9999] = None

# ==== function starts ==== #
def AWCPTF(SNDPPT, SLTPPT, CLYPPT, ORCDRC, BLD, CEC, PHIHOX):
    h1=-10
    h2=-20
    h3=-31.6
    pwp=-1585
    variables = ['lnAlfa', 'lnN', 'tetaS', 'tetaR']
    d = np.array([[-2.294, 0, -3.526, 0, 2.44, 0, -0.076, -11.331, 0.019, 0, 0, 0], 
                    [62.986, 0, 0, -0.833, -0.529, 0, 0, 0.593, 0, 0.007, -0.014, 0],
                    [81.799, 0, 0, 0.099, 0, -31.42, 0.018, 0.451, 0, 0, 0, -5e-04],
                    [22.733, -0.164, 0, 0, 0, 0, 0.235, -0.831, 0, 0.0018, 0, 0.0026]])

    #print d[0][0]
    PTF_coef = pd.DataFrame(data=d, index=variables)
    #print PTF_coef[0][variables[2]]

    add = CLYPPT+SLTPPT+SNDPPT
    #print add
    CLYPPT = float(CLYPPT*100) / float(add)
    SLTPPT = float(SLTPPT*100) / float(add)
    SNDPPT = float(SNDPPT*100) / float(add)
    if BLD < 100:
        BLD = 100
        
    if BLD > 2650:
        BLD = 2650
            
    clm = [SNDPPT, SLTPPT, CLYPPT, ORCDRC/10, BLD*0.001, CEC, PHIHOX, math.pow(SLTPPT,2), math.pow(CLYPPT,2), SNDPPT*SLTPPT, SNDPPT*CLYPPT]

    x = [(PTF_coef[i][variables[0]]*clm[i-1]) for i in xrange(1,12)]
    alfa = math.exp((PTF_coef[0][variables[0]]+ sum(x))/100)
    y = [(PTF_coef[i][variables[1]]*clm[i-1]) for i in xrange(1,12)]
    N = math.exp((PTF_coef[0][variables[1]]+ sum(y))/100)
    z = [(PTF_coef[i][variables[2]]*clm[i-1]) for i in xrange(1,12)]
    tetaS = (PTF_coef[0][variables[2]]+ sum(z))/100
    k = [(PTF_coef[i][variables[3]]*clm[i-1]) for i in xrange(1,12)]
    tetaR = (PTF_coef[0][variables[3]]+ sum(k))/100
    
    if tetaR < 0:
        tetaR = 0
    if tetaS < 0:
        tetaS = 0
#    tetaS1 = [(PTF_coef[0][variables[2]] + PTF_coef[i][variables[2]]*clm[i-1]) for i in [1,2,3,4,5,6,7,8,9,10,11]]
#    print alfa, N, tetaS, tetaR
    m = 1-1/N

    tetah1 = tetaR + (tetaS-tetaR)/math.pow((1+math.pow((alfa*-1*h1),N)),m)
    tetah2 = tetaR + (tetaS-tetaR)/math.pow((1+math.pow((alfa*-1*h2),N)),m)
    tetah3 = tetaR + (tetaS-tetaR)/math.pow((1+math.pow((alfa*-1*h3),N)),m)
    WWP = tetaR + (tetaS-tetaR)/math.pow((1+math.pow((alfa*-1*pwp),N)),m)
    AWCh1 = format(tetah1 - WWP , '.5f')
    AWCh2 = format(tetah2 - WWP, '.5f')
    AWCh3 = format(tetah3 - WWP, '.5f')
    WWP = format(WWP, '.3f')
    tetaS = format(tetaS, '.5f')
    return (AWCh1, AWCh2, AWCh3, WWP, tetaS)

#j=599
#(pAWCh1, pAWCh2, pAWCh3, pWWP) = AWCPTF(df['SND'][j],df['SLT'][j],df['CLY'][j],df['ORC'][j],df['BLD'][j],df['CEC'][j],df['PHI'][j])
#(rAWCh1, rAWCh2, rAWCh3, rWWP,_) = GSIF.AWCPTF(df['SND'][j],df['SLT'][j],df['CLY'][j],df['ORC'][j],df['BLD'][j],df['CEC'][j],df['PHI'][j])
#print pWWP
#print rWWP

start = time.time()
j = 0
k = 1440000
awc_all = np.zeros(shape = (5, k+1), dtype = 'float')
awc_vars = ['AWCh1', 'AWCh2', 'AWCh3', 'WWP', 'tetaS']

for j in range(k):
    (AWCh1, AWCh2, AWCh3, WWP, tetaS) = AWCPTF(df['SND'][j],df['SLT'][j],df['CLY'][j],df['ORC'][j],df['BLD'][j],df['CEC'][j],df['PHI'][j])
    awc = np.zeros(shape = (5,1), dtype = 'float')
    awc = [AWCh1, AWCh2, AWCh3, WWP, tetaS]
    awc_all[:,j] = awc
    j = j+1

awc_values = pd.DataFrame(awc_all.T, columns = awc_vars)
end =time.time()
print awc_values['WWP'][579]
print end - start

st =time.time()
from rpy2.robjects.packages import importr
GSIF = importr('GSIF')
#note r awc values are object data type 
rawc_all = np.zeros(shape = (5, k+1), dtype = object)

for j in range(k):
    (AWCh1, AWCh2, AWCh3, WWP, tetaS) = GSIF.AWCPTF(df['SND'][j],df['SLT'][j],df['CLY'][j],df['ORC'][j],df['BLD'][j],df['CEC'][j],df['PHI'][j])
    rawc = np.zeros(shape = (5,1), dtype = object)
    rawc = [AWCh1, AWCh2, AWCh3, WWP, tetaS]
    rawc_all[:,j] = rawc
    j = j+1

rawc_values = pd.DataFrame(rawc_all.T, columns = awc_vars)
ed =time.time()
print rawc_values['WWP'][579]
print ed-st