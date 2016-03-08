# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:03:12 2016

@author: user
"""
import pandas as pd
import numpy as np
import math
SNDPPT = 30 
SLTPPT = 25 
CLYPPT = 48 
ORCDRC = 23 
BLD = 1200 
CEC = 12 
PHIHOX = 6.4
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
    CLYPPT = int(CLYPPT*100) / int(add)
    SLTPPT = int(SLTPPT*100) / int(add)
    SNDPPT = int(SNDPPT*100) / int(add)
    if BLD < 100:
        BLD = 100
        
    if BLD > 2650:
        BLD = 2650
            
    clm = [SNDPPT, SLTPPT, CLYPPT, ORCDRC/10, BLD*0.001, CEC, PHIHOX, math.pow(SLTPPT,2), math.pow(CLYPPT,2), SNDPPT*SLTPPT, SNDPPT*CLYPPT]

    x = [(PTF_coef[i][variables[0]]*clm[i-1]) for i in [1,2,3,4,5,6,7,8,9,10,11]]
    alfa = math.exp((PTF_coef[0][variables[0]]+ sum(x))/100)
    y = [(PTF_coef[i][variables[1]]*clm[i-1]) for i in [1,2,3,4,5,6,7,8,9,10,11]]
    N = math.exp((PTF_coef[0][variables[1]]+ sum(y))/100)
    z = [(PTF_coef[i][variables[2]]*clm[i-1]) for i in [1,2,3,4,5,6,7,8,9,10,11]]
    tetaS = (PTF_coef[0][variables[2]]+ sum(z))/100
    k = [(PTF_coef[i][variables[3]]*clm[i-1]) for i in [1,2,3,4,5,6,7,8,9,10,11]]
    tetaR = (PTF_coef[0][variables[3]]+ sum(k))/100

    tetaS1 = [(PTF_coef[0][variables[2]] + PTF_coef[i][variables[2]]*clm[i-1]) for i in [1,2,3,4,5,6,7,8,9,10,11]]
#    print alfa, N, tetaS, tetaR
    m = 1-1/N

    tetah1 = tetaR + (tetaS-tetaR)/math.pow((1+math.pow((alfa*-1*h1),N)),m)
    tetah2 = tetaR + (tetaS-tetaR)/math.pow((1+math.pow((alfa*-1*h2),N)),m)
    tetah3 = tetaR + (tetaS-tetaR)/math.pow((1+math.pow((alfa*-1*h3),N)),m)
    WWP = tetaR + (tetaS-tetaR)/math.pow((1+math.pow((alfa*-1*pwp),N)),m)
    AWCh1 = tetah1 - WWP
    AWCh2 = tetah2 - WWP
    AWCh3 = tetah3 - WWP
    
    return (AWCh1, AWCh2, AWCh3, WWP)


(AWCh1, AWCh2, AWCh3, WWP) = AWCPTF(30,25,48,23,1200,12,6.4)

print WWP