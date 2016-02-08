library(GSIF)
library(rgdal)
library(raster)

ifolder = '/media/user/data'
setwd(ifolder)

source("/media/user/data/AWC-IN_022016/fun_AWCPTF/unzip.R")

var <- c('SNDPPT','SLTP','CLYPPT','ORCDRC','BLD','CEC','PHIHOX')

for (ind in var){
	fol = file.path(ifolder, ind)
	setwd(fol)
	m = list.files(pattern = glob2rx('*sd1_M'))
	sub_fol = file.path(fol, m)
	setwd(sub_fol)
	zip = list.files(pattern = glob2rx("*.tif.gz"))
	print (zip)
	fi = strsplit(file.path(sub_fol,zip), split = ".gz")
	#raster saved in ifolder
	setwd = ifolder
}
fi = strsplit(zip, split = ".gz")	
unzip(zip)
zz <- gzfile(zip, "r+")
GDALinfo(zip)
zz
library(rtiff)
GDALinfo(zip)
x <- AWCPTF(sndp, sltp, clyp, orc, bld, cec, phihox)

str(x)
attr(x, "coef")
data(afsp)
names(afsp$horizons)