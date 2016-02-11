library(raster)
library(GSIF)
library(rgdal)

ifolder <- '/media/user/data/AWC-IN_022016/sdata'

setwd(ifolder)

slt <- raster("SLTPPT_sd1_M_1km_T386.tif")
snd <- raster("SNDPPT_sd1_M_1km_T386.tif")
cec <- raster("CEC_sd1_M_1km_T386.tif")
bld <- raster('BLD_sd1_M_1km_T386.tif')
ph <- raster('PHIHOX_sd1_M_1km_T386.tif')
cly <- raster('CLYPPT_sd1_M_1km_T386.tif')
org <- raster('ORCDRC_sd1_M_1km_T386.tif')

variable_brick <- brick(snd, slt, cly, org, bld, cec, ph)

df <- as.data.frame(variable_brick)

summary(df)
length(df[1,])
length(df[,1])
str(df[1])
str(df[1][[1]])
df[[1]][[14899]]

#test
i <- 1
y <- AWCPTF(df[[1]][[i]], df[[2]][[i]], df[[3]][[i]], df[[4]][[i]], df[[5]][[i]], df[[6]][[i]], df[[7]][[i]])
str(y)

#running for each pixel .. takes long
for (i in c(1:1440000)){
x <- AWCPTF(df[[1]][[i]], df[[2]][[i]], df[[3]][[i]], df[[4]][[i]], df[[5]][[i]], df[[6]][[i]], df[[7]][[i]])
awc <- rbind(awc, x)
}																																
str(awc)

awc_raster <- rasterize(slt, slt, field = awc$AWCh1, na.rm = T)