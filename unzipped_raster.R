library(raster)
library(GSIF)
library(rgdal)

ifolder <- '/media/user/data/AWC-IN_022016/sdata'

setwd(ifolder)

slt <- raster("SLTPPT_sd1_M_1km_T386.tif")
plot(slt)

#please click the points representative of the xmin,ymin and xmax,ymax on the plot to set the extent
Ext <- drawExtent()

snd <- raster("SNDPPT_sd1_M_1km_T386.tif")
cec <- raster("CEC_sd1_M_1km_T386.tif")
bld <- raster('BLD_sd1_M_1km_T386.tif')
ph <- raster('PHIHOX_sd1_M_1km_T386.tif')
cly <- raster('CLYPPT_sd1_M_1km_T386.tif')
org <- raster('ORCDRC_sd1_M_1km_T386.tif')

variable_brick <- brick(snd, slt, cly, org, bld, cec, ph)

brick_crop <- crop(variable_brick, Ext)
df <- as.data.frame(brick_crop)

summary(df)
length(df[1,])
length(df[,1])
str(df[1])
str(df[1][[1]])
df[[1]][[14899]]

#test
# i <- 1567
# y <- AWCPTF(df[[1]][[i]], df[[2]][[i]], df[[3]][[i]], df[[4]][[i]], df[[5]][[i]], df[[6]][[i]], df[[7]][[i]])
# str(y)

#running for each pixel .. takes long
awc <- c()

#run AWCPTF for cropped area
t <- length(df[,1])
for (i in c(1:t)){
x <- AWCPTF(df[[1]][[i]], df[[2]][[i]], df[[3]][[i]], df[[4]][[i]], df[[5]][[i]], df[[6]][[i]], df[[7]][[i]])
awc <- rbind(awc, x)
}
str(awc)
awc$WWP
#create empty raster with resolution, extent of the brick
awc_raster <- raster(brick_crop)
summary(awc_raster)
#replaces values of the raster from NA to the WWP values
awc_raster <- replace(awc_raster, awc_raster, values = awc$WWP)

summary(awc_raster)
plot(awc_raster)
