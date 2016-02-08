library(raster)
library(GSIF)
library(rgdal)

ifolder <- '/media/user/data/AWC-IN022016/sdata'

setwd(ifolder)
setwd('/media/user/data/AWC-IN_022016/sdata')
slt <- raster("SLTPPT_sd1_M_1km_T386.tif")
snd <- raster("SNDPPT_sd1_M_1km_T386.tif")
cec <- raster("CEC_sd1_M_1km_T386.tif")
bld <- raster('BLD_sd1_M_1km_T386.tif')
ph <- raster('PHIHOX_sd1_M_1km_T386.tif')
cly <- raster('CLYPPT_sd1_M_1km_T386.tif')
org <- raster('ORCDRC_sd1_M_1km_T386.tif')


