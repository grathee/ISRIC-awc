library(GSIF)
library(rgdal)
library(raster)

ifolder = '/media/user/data/AWC-IN_022016'
setwd(ifolder)

var <- c('SNDPPT','SLTPPT','CLYPPT','ORCDRC','BLD','CEC','PHIHOX')

for (ind in var){
	fol = file.path(ifolder, 'unzipped_d', ind)
	print (fol)
	setwd(fol)
	m = list.files(pattern = glob2rx('*sd1_M'))
	sub_fol = file.path(fol, m)
	setwd(sub_fol)
	zip = list.files(pattern = glob2rx("*.tif.gz"))
	print (zip)
	unzip = unzip(zip, exdir = file.path(ifolder,'variables'))
	#raster saved in ifolder
	setwd = ifolder
}



GDALinfo(zip)
x <- AWCPTF(sndp, sltp, clyp, orc, bld, cec, phihox)

str(x)
attr(x, "coef")
data(afsp)
names(afsp$horizons)